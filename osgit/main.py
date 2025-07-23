#!/usr/bin/env python3
"""
OSGit - GitHub OSINT Tool
Author: rhyru9
Version: v0.0.1

A comprehensive tool for GitHub reconnaissance including subdomain discovery and repository path extraction.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Color support
try:
    from colored import fg, attr
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    def fg(color): return ""
    def attr(code): return ""

# ASCII Banner
BANNER = """
╔══════════════════════════════════════════════════════════════╗

            ██████╗   ███████╗  ██████╗  ██╗ ████████╗
            ██╔═══██╗ ██╔════╝ ██╔════╝  ██║ ╚══██╔══╝
            ██║   ██║ ███████╗ ██║  ███╗ ██║    ██║
            ██║   ██║ ╚════██║ ██║   ██║ ██║    ██║
            ╚██████╔╝ ███████║ ╚██████╔╝ ██║    ██║
            ╚═════╝  ╚══════╝  ╚═════╝  ╚═╝    ╚═╝
            GitHub OSINT Tool by https://github.com/rhyru9
                                                Version v0.0.1
╚══════════════════════════════════════════════════════════════╝
"""

class OSGitCore:
    """Core functionality for OSGit tool"""

    def __init__(self):
        self.config_dir = Path(__file__).parent / 'config'
        self.config_file = self.config_dir / 'conf.json'
        self.ensure_config_directory()

    def ensure_config_directory(self):
        """Ensure config directory exists"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.create_default_config()

    def create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "github_tokens": [],
            "version": "v0.0.1",
            "author": "rhyru9"
        }
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        return default_config

    def load_config(self):
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.create_default_config()

    def save_config(self, config):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)

    def add_token(self, token):
        """Add GitHub token to configuration"""
        config = self.load_config()
        if token not in config['github_tokens']:
            config['github_tokens'].append(token)
            self.save_config(config)
            print(f"{fg('green')}[+] Token added successfully!{attr(0)}")
        else:
            print(f"{fg('yellow')}[!] Token already exists in configuration{attr(0)}")

    def remove_token(self, token):
        """Remove GitHub token from configuration"""
        config = self.load_config()
        if token in config['github_tokens']:
            config['github_tokens'].remove(token)
            self.save_config(config)
            print(f"{fg('green')}[+] Token removed successfully!{attr(0)}")
        else:
            print(f"{fg('yellow')}[!] Token not found in configuration{attr(0)}")

    def list_tokens(self):
        """List configured GitHub tokens (masked)"""
        config = self.load_config()
        tokens = config.get('github_tokens', [])
        if tokens:
            print(f"{fg('green')}[+] Configured tokens:{attr(0)}")
            for i, token in enumerate(tokens, 1):
                if len(token) > 12:
                    masked = token[:8] + '*' * (len(token) - 12) + token[-4:]
                else:
                    masked = token[:4] + '*' * 4 + token[-2:]
                print(f"  {fg('cyan')}{i}. {masked}{attr(0)}")
        else:
            print(f"{fg('yellow')}[!] No tokens configured{attr(0)}")
            print(f"{fg('cyan')}[*] Use: ./osgit token add -t YOUR_TOKEN{attr(0)}")

def show_banner():
    """Display the tool banner"""
    print(BANNER)

class ColoredHelpFormatter(argparse.RawDescriptionHelpFormatter):
    """Custom formatter that preserves colors and formatting"""
    
    def _format_usage(self, usage, actions, groups, prefix):
        if prefix is None:
            prefix = f'{fg("cyan")}usage:{attr(0)} ' if COLORS_AVAILABLE else 'usage: '
        return super()._format_usage(usage, actions, groups, prefix)
    
    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return f'{fg("green")}{metavar}{attr(0)}' if COLORS_AVAILABLE else metavar
        else:
            parts = []
            if action.nargs == 0:
                if COLORS_AVAILABLE:
                    parts.extend([f'{fg("yellow")}{opt}{attr(0)}' for opt in action.option_strings])
                else:
                    parts.extend(action.option_strings)
            else:
                default = action.dest.upper()
                args_string = self._format_args(action, default)
                for option_string in action.option_strings:
                    if COLORS_AVAILABLE:
                        parts.append(f'{fg("yellow")}{option_string}{attr(0)} {fg("green")}{args_string}{attr(0)}')
                    else:
                        parts.append(f'{option_string} {args_string}')
            return ', '.join(parts)

def setup_token_commands(subparsers):
    """Setup token management commands"""
    token_parser = subparsers.add_parser(
        'token',
        help='Manage GitHub tokens',
        description='Manage GitHub Personal Access Tokens for API authentication',
        formatter_class=ColoredHelpFormatter,
        epilog=f"""{fg('cyan') if COLORS_AVAILABLE else ''}Examples:{attr(0) if COLORS_AVAILABLE else ''}
  {fg('green') if COLORS_AVAILABLE else ''}./osgit token add -t ghp_your_token_here{attr(0) if COLORS_AVAILABLE else ''}
  {fg('green') if COLORS_AVAILABLE else ''}./osgit token list{attr(0) if COLORS_AVAILABLE else ''}
  {fg('green') if COLORS_AVAILABLE else ''}./osgit token remove -t ghp_token_to_remove{attr(0) if COLORS_AVAILABLE else ''}"""
    )
    token_subparsers = token_parser.add_subparsers(
        dest='token_action',
        help='Token management actions'
    )

    # Add token
    add_parser = token_subparsers.add_parser(
        'add',
        help='Add a new GitHub token',
        formatter_class=ColoredHelpFormatter
    )
    add_parser.add_argument('-t', '--token', required=True,
        help='GitHub Personal Access Token')
    
    # Remove token
    remove_parser = token_subparsers.add_parser(
        'remove',
        help='Remove a GitHub token',
        formatter_class=ColoredHelpFormatter
    )
    remove_parser.add_argument('-t', '--token', required=True,
        help='GitHub token to remove')
    
    # List tokens
    token_subparsers.add_parser(
        'list',
        help='List configured tokens',
        formatter_class=ColoredHelpFormatter
    )

def handle_token_commands(args, core):
    """Handle token management commands"""
    if args.token_action == 'add':
        # Validate token format
        token = args.token.strip()
        if not token:
            print(f"{fg('red')}[-] Token cannot be empty{attr(0)}")
            return

        if not (token.startswith('ghp_') or token.startswith('github_pat_') or len(token) == 40):
            print(f"{fg('yellow')}[!] Warning: Token format doesn't match GitHub PAT patterns{attr(0)}")
            print(f"{fg('yellow')}[!] Expected: ghp_xxx, github_pat_xxx, or 40-char classic token{attr(0)}")

        core.add_token(token)

    elif args.token_action == 'remove':
        core.remove_token(args.token)

    elif args.token_action == 'list':
        core.list_tokens()

    else:
        print(f"{fg('red')}[-] Invalid token action: {args.token_action}{attr(0)}")
        print(f"{fg('yellow')}[!] Use: add, remove, or list{attr(0)}")

def main():
    # Only show banner for main help or no command
    show_main_banner = len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ['-h', '--help'])
    
    if show_main_banner:
        show_banner()
    
    core = OSGitCore()

    parser = argparse.ArgumentParser(
        prog='osgit',
        description='GitHub OSINT Tool for subdomain discovery and repository analysis',
        formatter_class=ColoredHelpFormatter,
        add_help=False  # We'll handle help manually
    )
    
    # Add custom help
    parser.add_argument('-h', '--help', action='store_true', help='Show this help message and exit')

    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands'
    )

    # Setup subcommands
    setup_token_commands(subparsers)

    # Subdomain finder
    sub_parser = subparsers.add_parser(
        'sub',
        help='Find subdomains using GitHub search',
        description='Discover subdomains by searching through GitHub repositories',
        formatter_class=ColoredHelpFormatter,
        epilog=f"""{fg('cyan') if COLORS_AVAILABLE else ''}Examples:{attr(0) if COLORS_AVAILABLE else ''}
  {fg('green') if COLORS_AVAILABLE else ''}./osgit sub -d example.com -o results.txt{attr(0) if COLORS_AVAILABLE else ''}
  {fg('green') if COLORS_AVAILABLE else ''}./osgit sub -d example.com -e -s -v{attr(0) if COLORS_AVAILABLE else ''}"""
    )
    sub_parser.add_argument('-d', '--domain', required=True,
                            help='Target domain to search for')
    sub_parser.add_argument('-e', '--extend', action='store_true',
                            help='Extended search for *.parent-domain patterns')
    sub_parser.add_argument('-s', '--source', action='store_true',
                            help='Show source URLs where subdomains are found')
    sub_parser.add_argument('-v', '--verbose', action='store_true',
                            help='Enable verbose output')
    sub_parser.add_argument('-o', '--output',
                            help='Output file to save results')
    sub_parser.add_argument('-t', '--token',
                            help='GitHub token to use (overrides config)')

    # Path extractor
    path_parser = subparsers.add_parser(
        'path',
        help='Extract paths from GitHub repository',
        description='Extract file paths and directory structures from public GitHub repositories',
        formatter_class=ColoredHelpFormatter,
        epilog=f"""{fg('cyan') if COLORS_AVAILABLE else ''}Examples:{attr(0) if COLORS_AVAILABLE else ''}
  {fg('green') if COLORS_AVAILABLE else ''}./osgit path -orb 'owner,repo,main' -o paths.txt{attr(0) if COLORS_AVAILABLE else ''}
  {fg('green') if COLORS_AVAILABLE else ''}./osgit path -orb 'user,project,branch' -o output.txt -s{attr(0) if COLORS_AVAILABLE else ''}"""
    )
    path_parser.add_argument('-orb', required=True, metavar='OWNER,REPO,BRANCH',
                            help='Repository info as comma-separated values')
    path_parser.add_argument('-o', '--output', required=True,
                            help='Output filename to save results')
    path_parser.add_argument('-s', '--segments', action='store_true',
                            help='Extract full file paths instead of individual segments')

    # Parse arguments
    args, unknown = parser.parse_known_args()

    # Handle help manually
    if args.help or (not args.command and not unknown):
        if show_main_banner:
            print(f"\n{fg('cyan')}Usage:{attr(0)}")
            print(f"  ./osgit <command> [options]")
            print(f"\n{fg('cyan')}Commands:{attr(0)}")
            print(f"  {fg('green')}token{attr(0)}    Manage GitHub tokens")
            print(f"  {fg('green')}sub{attr(0)}      Find subdomains using GitHub search")
            print(f"  {fg('green')}path{attr(0)}     Extract paths from GitHub repository")
            print(f"\n{fg('cyan')}Quick Start:{attr(0)}")
            print(f"  1. Add token:     {fg('green')}./osgit token add -t ghp_your_token{attr(0)}")
            print(f"  2. Find domains:  {fg('green')}./osgit sub -d example.com -o results.txt{attr(0)}")
            print(f"  3. Extract paths: {fg('green')}./osgit path -orb 'user,repo,main' -o paths.txt{attr(0)}")
            print(f"\n{fg('cyan')}For command help: {fg('green')}./osgit <command> --help{attr(0)}")
        return

    if not args.command:
        print(f"{fg('yellow')}[!] No command specified. Use --help for usage information.{attr(0)}")
        return

    try:
        if args.command == 'token':
            handle_token_commands(args, core)
        elif args.command == 'sub':
            from sub.subdomain_finder import SubdomainFinder
            finder = SubdomainFinder(core)
            finder.run(args)
        elif args.command == 'path':
            from paths.path_extractor import PathExtractor
            extractor = PathExtractor()
            extractor.run(args)
        else:
            print(f"{fg('red')}[-] Unknown command: {args.command}{attr(0)}")
            print(f"{fg('cyan')}[*] Use --help to see available commands{attr(0)}")
    except KeyboardInterrupt:
        print(f"\n{fg('yellow')}[!] Operation cancelled by user{attr(0)}")
    except Exception as e:
        print(f"\n{fg('red')}[-] Unexpected error: {e}{attr(0)}")
        if args.command == 'sub' and hasattr(args, 'verbose') and args.verbose:
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()