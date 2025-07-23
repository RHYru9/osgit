#!/usr/bin/env python3
"""
Subdomain Finder Module for OSGit
Author: rhyru9
Version: v0.0.1

GitHub-based subdomain discovery tool with enhanced token management and rate limiting.
"""

import os
import re
import time
import requests
import random
from functools import partial
from multiprocessing.dummy import Pool
import tldextract

try:
    from colored import fg, attr
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    def fg(color): return ""
    def attr(code): return ""

class SubdomainFinder:
    """GitHub-based subdomain discovery tool"""

    def __init__(self, core):
        self.core = core
        self.history = []
        self.history_urls = []
        self.output_file = None
        self.output_fp = None

    def get_github_tokens(self, token_override=None):
        """Get GitHub tokens from config or override"""
        if token_override:
            return [token_override]

        config = self.core.load_config()
        tokens = config.get('github_tokens', [])

        if not tokens:
            print(f"{fg('red')}[-] No GitHub tokens configured. Use 'python osgit.py token add -t YOUR_TOKEN'{attr(0)}")
            return []

        return tokens

    def github_api_search_code(self, token, search, page, sort, order, verbose):
        """Search GitHub code using API"""
        headers = {"Authorization": f"token {token}"}
        url = f'https://api.github.com/search/code?per_page=100&s={sort}&type=Code&o={order}&q={search}&page={page}'

        if verbose:
            print(f"{fg('cyan')}>>> {url}{attr(0)}")

        try:
            response = requests.get(url, headers=headers, timeout=10)

            # Handle rate limiting
            if response.status_code == 403:
                reset_time = response.headers.get('X-RateLimit-Reset', 0)
                if reset_time:
                    wait_time = int(reset_time) - int(time.time())
                    if wait_time > 0 and wait_time < 3600:  # Don't wait more than 1 hour
                        print(f"{fg('yellow')}[!] Rate limited. Waiting {wait_time}s...{attr(0)}")
                        time.sleep(wait_time + 1)
                        return self.github_api_search_code(token, search, page, sort, order, verbose)

            return response.json()

        except Exception as e:
            print(f"{fg('red')}[-] Error occurred: {e}{attr(0)}")
            return None

    def get_raw_url(self, result):
        """Convert GitHub blob URL to raw URL"""
        return result['html_url'].replace(
            'https://github.com/',
            'https://raw.githubusercontent.com/'
        ).replace('/blob/', '/')

    def fetch_code(self, url):
        """Fetch code content from raw URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"{fg('red')}[-] Error fetching {url}: {e}{attr(0)}")
            return None

    def extract_subdomains_from_code(self, domain_regexp, source, result):
        """Extract subdomains from code content"""
        time.sleep(random.uniform(0.3, 0.8))  # Rate limiting

        url = self.get_raw_url(result)
        if url in self.history_urls:
            return

        self.history_urls.append(url)
        code = self.fetch_code(url)

        if not code:
            return

        local_history = []
        output = ''

        matches = re.findall(domain_regexp, code, re.IGNORECASE)
        if matches:
            for match in matches:
                subdomain = match[0].lower().strip() if isinstance(match, tuple) else match.lower().strip()

                if subdomain and subdomain not in local_history:
                    local_history.append(subdomain)

                    if source:
                        if not output:
                            output += f"{fg('yellow')}>>> {result['html_url']}{attr(0)}\n\n"
                        self.history.append(subdomain)
                        output += f"{fg('green')}{subdomain}{attr(0)}\n"
                    elif subdomain not in self.history:
                        self.history.append(subdomain)
                        output += f"{fg('green')}{subdomain}{attr(0)}\n"

        if output.strip():
            print(output.strip())
            if self.output_fp:
                # Remove color codes for file output
                clean_output = re.sub(r'\033\[[0-9;]*m', '', output.strip())
                self.output_fp.write(clean_output + "\n")

    def setup_search_parameters(self, domain, extend):
        """Setup search query and regex pattern"""
        host_parse = tldextract.extract(domain)

        if extend:
            search_query = f'"{host_parse.domain}"'
            domain_regexp = rf'((?:[a-zA-Z0-9_-]+\.)*{re.escape(host_parse.domain)}\.{re.escape(host_parse.suffix)})'
        else:
            search_query = f'"{host_parse.domain}.{host_parse.suffix}"'
            domain_regexp = rf'((?:[a-zA-Z0-9_-]+\.)*{re.escape(domain)})'

        search_query = search_query.replace('-', '%2D')
        return search_query, domain_regexp

    def run(self, args):
        """Main execution function"""
        print(f"{fg('cyan')}[*] Starting subdomain discovery for: {args.domain}{attr(0)}")

        # Get tokens
        tokens = self.get_github_tokens(args.token)
        if not tokens:
            return

        # Setup output file
        if args.output:
            try:
                self.output_fp = open(args.output, "w")
                print(f"{fg('green')}[+] Output will be saved to: {args.output}{attr(0)}")
            except Exception as e:
                print(f"{fg('red')}[-] Cannot create output file: {e}{attr(0)}")
                return

        # Setup search parameters
        search_query, domain_regexp = self.setup_search_parameters(args.domain, args.extend)

        if args.verbose:
            print(f"{fg('cyan')}[*] Search Query: {search_query}{attr(0)}")
            print(f"{fg('cyan')}[*] Domain Regexp: {domain_regexp}{attr(0)}")
            print(f"{fg('cyan')}[*] Tokens available: {len(tokens)}{attr(0)}")

        # Search order combinations
        sort_orders = [
            {'sort': 'indexed', 'order': 'desc'},
            {'sort': 'indexed', 'order': 'asc'},
            {'sort': '', 'order': 'desc'}
        ]

        # Main search loop
        for sort_order in sort_orders:
            page = 1
            available_tokens = tokens.copy()

            if args.verbose:
                print(f"\n{fg('yellow')}[*] Search mode: {sort_order['sort']} {sort_order['order']}{attr(0)}")

            while available_tokens:
                if args.verbose:
                    print(f"{fg('cyan')}[*] Processing page {page}{attr(0)}")

                token = random.choice(available_tokens)
                result_json = self.github_api_search_code(
                    token, search_query, page,
                    sort_order['sort'], sort_order['order'],
                    args.verbose
                )

                if not result_json:
                    available_tokens.remove(token)
                    continue

                # Handle API errors
                if 'documentation_url' in result_json or 'message' in result_json:
                    if args.verbose:
                        print(f"{fg('red')}[-] API Error: {result_json.get('message', 'Unknown error')}{attr(0)}")
                    available_tokens.remove(token)
                    continue

                # Process results
                if 'items' in result_json and result_json['items']:
                    with Pool(20) as pool:  # Reduced thread count for better stability
                        pool.map(
                            partial(self.extract_subdomains_from_code, domain_regexp, args.source),
                            result_json['items']
                        )
                    page += 1
                else:
                    break

        # Cleanup and summary
        if self.output_fp:
            self.output_fp.close()

        unique_subdomains = len(set(self.history))
        print(f"\n{fg('green')}[+] Discovery completed!{attr(0)}")
        print(f"{fg('green')}[+] Total unique subdomains found: {unique_subdomains}{attr(0)}")

        if args.output:
            print(f"{fg('green')}[+] Results saved to: {args.output}{attr(0)}")