#!/usr/bin/env python3
"""
Jewelry Design Generator
========================

A tool for generating 3D jewelry designs using AI.

This script serves as the entry point for the application.
"""

import sys
from src.python_jewelry_design_gen.cli import cli


if __name__ == "__main__":
    sys.exit(cli())
