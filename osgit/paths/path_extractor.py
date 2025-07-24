#!/usr/bin/env python3
"""
Author: rhyru9
Version: v0.0.1

GitHub repository path and structure extraction tool.
"""

import requests
import json

try:
    from colored import fg, attr
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    def fg(color): return ""
    def attr(code): return ""

class PathExtractor:
    """GitHub repository path extraction tool"""
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "OSGit-PathExtractor/v0.0.1",
            "Accept": "application/vnd.github.v3+json",
        })

    def get_github_tree(self, owner, repo, branch="main"):
        """Fetch repository tree structure from GitHub API"""
        url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

        print(f"{fg('cyan')}[*] Fetching tree from {owner}/{repo} (branch: {branch}){attr(0)}")

        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 404:
                print(f"{fg('red')}[-] Repository or branch not found: {owner}/{repo}:{branch}{attr(0)}")
                return None
            elif response.status_code == 403:
                print(f"{fg('red')}[-] Access forbidden. Repository might be private or rate limited{attr(0)}")
                return None
            elif response.status_code != 200:
                print(f"{fg('red')}[-] HTTP {response.status_code}: {response.reason}{attr(0)}")
                return None

            data = response.json()

            if 'message' in data:
                print(f"{fg('red')}[-] GitHub API Error: {data['message']}{attr(0)}")
                return None

            print(f"{fg('green')}[+] Successfully fetched repository tree{attr(0)}")
            return data

        except requests.exceptions.Timeout:
            print(f"{fg('red')}[-] Request timeout while fetching repository tree{attr(0)}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"{fg('red')}[-] Network error: {e}{attr(0)}")
            return None
        except json.JSONDecodeError:
            print(f"{fg('red')}[-] Invalid JSON response received{attr(0)}")
            return None

    def extract_paths_and_segments(self, tree_json, full_paths=True):
        if not tree_json or 'tree' not in tree_json:
            return []

        seen = set()
        results = []

        print(f"{fg('cyan')}[*] Processing {'full paths' if full_paths else 'path segments'}...{attr(0)}")

        for item in tree_json.get("tree", []):
            path = item.get("path")
            if not path:
                continue

            if full_paths:
                if path not in seen:
                    seen.add(path)
                    results.append(path)
            else:
                segments = path.split('/')
                for segment in segments:
                    if segment and segment not in seen:
                        seen.add(segment)
                        results.append(segment)

        results.sort()
        print(f"{fg('green')}[+] Extracted {len(results)} unique {'paths' if full_paths else 'segments'}{attr(0)}")

        return results

    def save_results_to_file(self, results, filename):
        """Save extracted results to file"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                for item in results:
                    f.write(item + "\n")

            print(f"{fg('green')}[+] Successfully saved {len(results)} lines to {filename}{attr(0)}")
            return True

        except IOError as e:
            print(f"{fg('red')}[-] Error saving to file {filename}: {e}{attr(0)}")
            return False

    def display_statistics(self, results, owner, repo, branch):
        print(f"\n{fg('yellow')}=== Extraction Statistics ==={attr(0)}")
        print(f"{fg('cyan')}Repository: {owner}/{repo}:{branch}{attr(0)}")
        print(f"{fg('cyan')}Total items extracted: {len(results)}{attr(0)}")

        if results:
            print(f"{fg('cyan')}Sample results (first 10):{attr(0)}")
            for i, item in enumerate(results[:10], 1):
                print(f"  {i:2d}. {item}")

            if len(results) > 10:
                print(f"  ... and {len(results) - 10} more")

    def validate_orb_format(self, orb_string):
        """Validate and parse ORB (Owner,Repo,Branch) string"""
        try:
            parts = [part.strip() for part in orb_string.split(",")]

            if len(parts) != 3:
                raise ValueError("ORB must contain exactly 3 parts: owner,repo,branch")

            owner, repo, branch = parts

            if not owner or not repo or not branch:
                raise ValueError("Owner, repo, and branch cannot be empty")

            if not all(c.isalnum() or c in '-_.' for c in owner):
                raise ValueError("Invalid characters in owner name")

            if not all(c.isalnum() or c in '-_.' for c in repo):
                raise ValueError("Invalid characters in repository name")

            return owner, repo, branch

        except ValueError as e:
            print(f"{fg('red')}[-] ORB format error: {e}{attr(0)}")
            print(f"{fg('yellow')}[!] Expected format: 'owner,repo,branch' (e.g., 'microsoft,vscode,main'){attr(0)}")
            return None, None, None

    def run(self, args):
        """Main execution function"""
        print(f"{fg('cyan')}[*] Starting path extraction...{attr(0)}")
        owner, repo, branch = self.validate_orb_format(args.orb)
        if not owner:
            return
        tree_data = self.get_github_tree(owner, repo, branch)
        if not tree_data:
            return

        results = self.extract_paths_and_segments(tree_data, full_paths=args.segments)

        if not results:
            print(f"{fg('yellow')}[!] No paths found in repository{attr(0)}")
            return

        if self.save_results_to_file(results, args.output):
            self.display_statistics(results, owner, repo, branch)
        print(f"{fg('green')}[+] Path extraction completed successfully!{attr(0)}")