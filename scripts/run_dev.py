#!/usr/bin/env python3
"""
Development script for PyCppSQLJS.
This script helps with running tests, examples, and development tasks.
"""

import os
import sys
import argparse
from pathlib import Path

def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PyCppSQLJS Development Tools")
    parser.add_argument("--test", action="store_true", help="Run all tests")
    parser.add_argument("--example", type=str, help="Run a specific example file")
    parser.add_argument("--interactive", action="store_true", help="Start interactive mode")
    parser.add_argument("--lint", action="store_true", help="Run linters")
    parser.add_argument("--format", action="store_true", help="Format code using black")
    return parser

def run_tests() -> None:
    """Run all tests using pytest."""
    import pytest
    pytest.main(["-v", "tests/"])

def run_example(example_file: str) -> None:
    """Run a specific example file."""
    example_path = Path("examples") / example_file
    if not example_path.exists():
        print(f"Error: Example file '{example_file}' not found.")
        sys.exit(1)
    
    from src.interpreter import run_file
    run_file(str(example_path))

def run_interactive() -> None:
    """Start the interactive interpreter."""
    from src.interpreter import run_prompt
    run_prompt()

def run_linters() -> None:
    """Run code linters."""
    import subprocess
    
    # Run flake8
    print("Running flake8...")
    subprocess.run(["flake8", "src/", "tests/", "examples/"], check=True)
    
    # Run mypy
    print("\nRunning mypy...")
    subprocess.run(["mypy", "src/", "tests/", "examples/"], check=True)

def format_code() -> None:
    """Format code using black."""
    import subprocess
    print("Formatting code with black...")
    subprocess.run(["black", "src/", "tests/", "examples/"], check=True)

def main() -> None:
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Add src directory to Python path
    src_path = Path(__file__).parent.parent / "src"
    sys.path.insert(0, str(src_path))
    
    if args.test:
        run_tests()
    elif args.example:
        run_example(args.example)
    elif args.interactive:
        run_interactive()
    elif args.lint:
        run_linters()
    elif args.format:
        format_code()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 