#!/usr/bin/env python3
"""
Script to help set up the GitHub repository for PyCppSQLJS.
This script will:
1. Initialize git repository if not already done
2. Create .gitignore if not exists
3. Add all files
4. Create initial commit
5. Help with GitHub remote setup
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd: list[str], check: bool = True) -> None:
    """Run a shell command and print its output."""
    try:
        result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}:")
        print(e.stderr)
        if check:
            sys.exit(1)

def init_git() -> None:
    """Initialize git repository if not already done."""
    if not Path(".git").exists():
        print("Initializing git repository...")
        run_command(["git", "init"])
    else:
        print("Git repository already initialized.")

def setup_gitignore() -> None:
    """Create .gitignore if it doesn't exist."""
    if not Path(".gitignore").exists():
        print("Creating .gitignore...")
        with open(".gitignore", "w") as f:
            f.write("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/
.env

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Project specific
*.pcsj
!examples/*.pcsj
!tests/*.pcsj
*.log
.coverage
htmlcov/
.pytest_cache/
""")
    else:
        print(".gitignore already exists.")

def add_files() -> None:
    """Add all files to git."""
    print("Adding files to git...")
    run_command(["git", "add", "."])

def create_initial_commit() -> None:
    """Create initial commit if no commits exist."""
    try:
        run_command(["git", "rev-parse", "HEAD"], check=False)
        print("Repository already has commits.")
    except subprocess.CalledProcessError:
        print("Creating initial commit...")
        run_command(["git", "commit", "-m", "Initial commit: Basic lexer implementation"])

def setup_remote() -> None:
    """Help set up GitHub remote."""
    print("\nTo set up GitHub remote:")
    print("1. Create a new repository on GitHub")
    print("2. Run these commands (replace with your repository URL):")
    print("   git remote add origin https://github.com/yourusername/pycsqljs.git")
    print("   git branch -M main")
    print("   git push -u origin main")

def main() -> None:
    """Main function to set up the repository."""
    print("Setting up PyCppSQLJS repository...")
    
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    init_git()
    setup_gitignore()
    add_files()
    create_initial_commit()
    setup_remote()
    
    print("\nRepository setup complete!")
    print("Next steps:")
    print("1. Create a GitHub repository")
    print("2. Follow the remote setup instructions above")
    print("3. Push your code to GitHub")

if __name__ == "__main__":
    main() 