#!/usr/bin/env python3
"""
Setup script for OSGit
Author: rhyru9
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="osgit",
    version="0.0.1",
    author="rhyru9",
    description="GitHub OSINT Tool for subdomain discovery and path extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "tldextract>=3.0.0",
        "colored>=1.4.0"
    ],
    entry_points={
        "console_scripts": [
            "osgit=osgit.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_data={
        "osgit": ["**/*.py"],
    },
    include_package_data=True,
)