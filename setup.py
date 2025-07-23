#!/usr/bin/env python3
"""
Setup script for OSGit
Author: rhyru9
"""
from setuptools import setup, find_packages

setup(
    name="osgit",
    version="0.0.1",
    author="rhyru9",
    description="GitHub OSINT Tool for subdomain discovery and path extraction",
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
)