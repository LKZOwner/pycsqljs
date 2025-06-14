import sys
from pathlib import Path
from typing import List

from lexer.scanner import Scanner, Token

def run_file(path: str) -> None:
    try:
        with open(path, 'r') as file:
            source = file.read()
        
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        
        # For now, just print the tokens
        for token in tokens:
            print(token)
            
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        sys.exit(74)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(65)

def run_prompt() -> None:
    print("PyCppSQLJS Interactive Mode")
    print("Type 'exit' to quit")
    
    while True:
        try:
            line = input("> ")
            if line.lower() == 'exit':
                break
                
            scanner = Scanner(line)
            tokens = scanner.scan_tokens()
            
            for token in tokens:
                print(token)
                
        except RuntimeError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: python interpreter.py [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()

if __name__ == "__main__":
    main() 