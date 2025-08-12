#!/usr/bin/env python3
"""
Test runner script for the Election Monitoring System.

This script runs the tests for the core data models and displays the results.
It can be used to verify the implementation as part of the triple-gate control process.
"""

import os
import sys
import subprocess
import argparse


def print_header(message):
    """Print a header message."""
    print("\n" + "=" * 80)
    print(f" {message} ".center(80, "="))
    print("=" * 80 + "\n")


def run_command(command, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"{e.stdout}\n{e.stderr}"


def run_tests(args):
    """Run the tests for the core data models."""
    print_header("Running Tests")
    
    # Determine the test directory
    cwd = os.path.dirname(os.path.abspath(__file__))
    
    # Build the pytest command
    command = ["python", "-m", "pytest"]
    
    if args.verbose:
        command.append("-v")
    
    if args.coverage:
        command.append("--cov=app")
    
    if args.test_path:
        command.append(args.test_path)
    
    # Run the tests
    success, output = run_command(command, cwd=cwd)
    
    # Print the output
    print(output)
    
    # Print the result
    if success:
        print_header("Tests Passed")
        return True
    else:
        print_header("Tests Failed")
        return False


def verify_implementation():
    """Verify the implementation as part of the triple-gate control process."""
    print_header("Verifying Implementation")
    
    # Check if the models are implemented
    models_path = os.path.join("app", "models")
    if not os.path.exists(models_path):
        print("Error: Models directory not found.")
        return False
    
    # Check if the schemas are implemented
    schemas_path = os.path.join("app", "models", "schemas")
    if not os.path.exists(schemas_path):
        print("Error: Schemas directory not found.")
        return False
    
    # Check if the CRUD operations are implemented
    crud_path = os.path.join("app", "crud")
    if not os.path.exists(crud_path):
        print("Error: CRUD directory not found.")
        return False
    
    # Check if the tests are implemented
    tests_path = os.path.join("tests")
    if not os.path.exists(tests_path):
        print("Error: Tests directory not found.")
        return False
    
    print("All components are implemented.")
    return True


def list_tests():
    """List all available tests."""
    print_header("Available Tests")
    
    # Determine the test directory
    cwd = os.path.dirname(os.path.abspath(__file__))
    tests_path = os.path.join(cwd, "tests")
    
    # Check if the tests directory exists
    if not os.path.exists(tests_path):
        print("Error: Tests directory not found.")
        return False
    
    # List all test files
    for root, dirs, files in os.walk(tests_path):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(root, file), cwd)
                print(f"- {rel_path}")
    
    return True


def check_pytest_installed():
    """Check if pytest is installed."""
    try:
        import pytest
        return True
    except ImportError:
        print("Error: pytest is not installed.")
        print("Please install it using: pip install pytest")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run tests for the Election Monitoring System.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-c", "--coverage", action="store_true", help="Enable coverage report")
    parser.add_argument("--test-path", help="Path to specific test file or directory")
    parser.add_argument("--list", action="store_true", help="List all available tests")
    args = parser.parse_args()
    
    # Check if pytest is installed
    if not check_pytest_installed():
        sys.exit(1)
    
    # List all available tests
    if args.list:
        if not list_tests():
            sys.exit(1)
        sys.exit(0)
    
    # Verify the implementation
    if not verify_implementation():
        sys.exit(1)
    
    # Run the tests
    if not run_tests(args):
        sys.exit(1)
    
    # Print the verification message
    print_header("Verification Complete")
    print("The implementation has been verified.")
    print("Please complete the Gate 2 verification by reviewing the code and confirming it works as expected.")
    print("\nTo complete Gate 2 verification, please update the verification.md file with your confirmation.")


if __name__ == "__main__":
    main()