# OSGit - GitHub OSINT Tool

A comprehensive GitHub OSINT (Open Source Intelligence) tool designed for reconnaissance activities including subdomain discovery and repository path extraction for creating custom wordlists/seclists for fuzzing operations.

## Features

-  **Subdomain Discovery**: Find subdomains by searching through GitHub repositories
-  **Path Extraction**: Extract file paths and directory structures from GitHub repositories
-  **Token Management**: Secure GitHub token storage and rotation
-  **Multi-threading**: Fast parallel processing for efficient data collection
-  **Flexible Output**: Save results in various formats with detailed statistics
-  **Rate Limiting**: Built-in rate limiting and error handling for GitHub API

## Installation

### Prerequisites
- Python 3.7 or higher
- GitHub Personal Access Token (for API access)

### Install from Source
```bash
git clone https://github.com/rhyru9/osgit.git
cd osgit
pip install -e .
```

### Install Dependencies Only
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Configure GitHub Token
```bash
# Add your GitHub token
osgit token add -t ghp_your_github_token_here

# Verify token is added
osgit token list
```

### 2. Subdomain Discovery
```bash
# Basic subdomain search
osgit sub -d example.com -o subdomains.txt

# Verbose mode with source URLs
osgit sub -d example.com -s -o subdomains.txt -v

# Extended search (includes parent domain variations)
osgit sub -d example.com -e -o subdomains.txt
```

### 3. Repository Path Extraction
```bash
# Extract full file paths
osgit path -orb 'microsoft,vscode,main' -o paths.txt -s

# Extract path segments only
osgit path -orb 'owner,repository,branch' -o segments.txt
```

## Usage

### Token Management

The tool requires GitHub Personal Access Tokens for API access. You can manage tokens using:

```bash
# Add a new token
osgit token add -t ghp_your_token_here

# List configured tokens (masked for security)
osgit token list

# Remove a token
osgit token remove -t ghp_token_to_remove
```

**Note**: Tokens are stored in `config/conf.json` and are automatically rotated to handle rate limits.

### Subdomain Discovery

Find subdomains by searching through GitHub repositories:

```bash
# Basic usage
osgit sub -d target-domain.com -o results.txt

# With verbose output and source URLs
osgit sub -d target-domain.com -s -o results.txt -v

# Extended search (finds *.target-domain.com patterns)
osgit sub -d target-domain.com -e -o results.txt

# Use specific token (overrides config)
osgit sub -d target-domain.com -t ghp_specific_token -o results.txt
```

**Parameters:**
- `-d, --domain`: Target domain to search for (required)
- `-e, --extend`: Also search for parent domain variations
- `-s, --source`: Display source URLs where subdomains are found
- `-v, --verbose`: Enable verbose output for debugging
- `-o, --output`: Output file to save results
- `-t, --token`: Use specific GitHub token (overrides config)

### Repository Path Extraction

Extract file paths and directory structures from public GitHub repositories:

```bash
# Extract full paths
osgit path -orb 'owner,repository,branch' -o paths.txt -s

# Extract path segments only
osgit path -orb 'owner,repository,branch' -o segments.txt

# Example with real repository
osgit path -orb 'microsoft,vscode,main' -o vscode_paths.txt -s
```

**Parameters:**
- `-orb`: Owner,Repository,Branch in comma-separated format (required)
- `-o, --output`: Output filename (required)
- `-s, --segments`: Output full paths instead of individual segments

## Configuration

### Configuration File
The tool automatically creates a configuration file at `config/conf.json`:

```json
{
  "github_tokens": [
    "ghp_your_token_here"
  ],
  "version": "v0.0.1",
  "author": "rhyru9"
}
```

### GitHub Token Setup
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with appropriate scopes:
   - `public_repo` (for public repository access)
   - `read:org` (optional, for organization repositories)
3. Add the token using `osgit token add -t your_token`

## Examples

### Subdomain Discovery Examples

```bash
# Find subdomains for a single domain
osgit sub -d example.com -o example_subs.txt

# Comprehensive search with sources and verbose output
osgit sub -d target.com -e -s -v -o comprehensive_results.txt

# Quick search with specific token
osgit sub -d domain.com -t ghp_quick_token -o quick_results.txt
```

### Path Extraction Examples

```bash
# Extract all paths from a popular repository
osgit path -orb 'facebook,react,main' -o react_paths.txt -s

# Get path segments for analysis
osgit path -orb 'microsoft,TypeScript,main' -o typescript_segments.txt

# Extract from specific branch
osgit path -orb 'nodejs,node,v18.x' -o nodejs_v18_paths.txt -s
```

## Output Formats

### Subdomain Discovery Output
```
subdomain1.target.com
api.target.com
admin.target.com
test.subdomain.target.com
```

With source URLs (`-s` flag):
```
>>> https://github.com/user/repo/blob/main/config.js

api.target.com
admin.target.com

>>> https://github.com/another/repo/blob/master/endpoints.py

test.target.com
```

### Path Extraction Output
Full paths (`-s` flag):
```
src/main.py
config/settings.json
docs/README.md
tests/unit/test_main.py
```

Path segments (default):
```
src
main.py
config
settings.json
docs
README.md
tests
unit
test_main.py
```

## Advanced Usage

### Rate Limiting and Token Rotation
The tool automatically handles GitHub API rate limits by:
- Rotating between multiple configured tokens
- Implementing exponential backoff on rate limit errors
- Providing detailed error messages and suggestions

### Multi-threading
Both subdomain discovery and path extraction use multi-threading for improved performance:
- Subdomain discovery: 20 concurrent threads
- API requests: Built-in connection pooling

### Error Handling
Comprehensive error handling for:
- Invalid GitHub tokens
- Repository access permissions
- Network connectivity issues
- Malformed API responses

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is designed for legitimate security research and bug bounty activities. Users are responsible for ensuring they have proper authorization before scanning any domains or repositories. The authors are not responsible for any misuse of this tool.

## Author

**rhyru9** - *Initial work and development*

## References

github-subdomains - ([gwen001](https://github.com/gwen001/github-search))

## Acknowledgments

- GitHub API for providing comprehensive code search capabilities
- The cybersecurity community for inspiration and feedback
- All contributors who help improve this tool

---

 If you find this tool useful, please consider giving it a star on GitHub!

 Found a bug or have a feature request? Please open an issue.

 Questions? Feel free to reach out or start a discussion.