#!/usr/bin/env python3
"""
Setup script for OSGit
Author: rhyru9
Version: v0.0.1
"""

from setuptools import setup, find_packages
import os

def read_readme():
    """Read README file if it exists"""
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    return "OSGit - GitHub OSINT Tool by rhyru9"

def read_requirements():
    """Read requirements from requirements.txt if it exists"""
    requirements = [
        "requests>=2.25.0",
        "tldextract>=3.0.0",
        "colored>=1.4.0"
    ]

    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    return requirements

setup(
    name="osgit",
    version="0.0.1",
    author="rhyru9",
    description="GitHub OSINT Tool for subdomain discovery and repository path extraction",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Internet",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "osgit=osgit.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "osgit": ["config/*.json"],
    },
    zip_safe=False,
)

# Post-installation message
print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   OSGit Installation Complete!                           ║
║                                                           ║
║   Usage Examples:                                         ║
║   ─────────────────                                       ║
║                                                           ║
║   Token Management:                                       ║
║   python -m osgit.main token add -t your_github_token    ║
║   python -m osgit.main token list                        ║
║                                                           ║
║   Subdomain Discovery:                                    ║
║   python -m osgit.main sub -d example.com -o results.txt ║
║   python -m osgit.main sub -d example.com -s -v          ║
║                                                           ║
║   Path Extraction:                                        ║
║   python -m osgit.main path -orb 'user,repo,main' -o p.txt -s ║
║                                                           ║
║   Or if installed globally:                              ║
║   osgit token add -t your_token                          ║
║   osgit sub -d domain.com -o results.txt                 ║
║   osgit path -orb 'user,repo,main' -o paths.txt -s       ║
║                                                           ║
║                     Happy Hunting! 🕵️                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")