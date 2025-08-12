#!/usr/bin/env python3
"""
Migration runner script for the Election Monitoring System.

This script runs the Alembic migrations for the database and displays the results.
It can be used to verify the implementation as part of the triple-gate control process.
"""

import os
import sys
import subprocess
import argparse
import sqlite3


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
        return False, e.stderr


def check_alembic_config():
    """Check if the Alembic configuration exists."""
    if not os.path.exists("alembic.ini"):
        print("Error: alembic.ini not found.")
        print("Please make sure you're running this script from the backend directory.")
        return False
    
    if not os.path.exists(os.path.join("alembic", "env.py")):
        print("Error: alembic/env.py not found.")
        print("Please make sure Alembic is properly configured.")
        return False
    
    return True


def run_migrations(args):
    """Run the Alembic migrations."""
    print_header("Running Migrations")
    
    # Determine the current directory
    cwd = os.path.dirname(os.path.abspath(__file__))
    
    # Check if the Alembic configuration exists
    if not check_alembic_config():
        return False
    
    # Build the Alembic command
    command = ["alembic"]
    
    if args.command == "upgrade":
        # Handle the case of multiple heads by using 'heads' instead of 'head'
        if args.revision == "head":
            command.extend(["upgrade", "heads"])
        else:
            command.extend(["upgrade", args.revision or "heads"])
    elif args.command == "downgrade":
        command.extend(["downgrade", args.revision or "-1"])
    elif args.command == "revision":
        command.extend(["revision", "--autogenerate", "-m", args.message or "Migration"])
    elif args.command == "history":
        command.append("history")
    elif args.command == "current":
        command.append("current")
    elif args.command == "heads":
        command.append("heads")
    elif args.command == "merge":
        command.extend(["merge", "heads", "-m", "merge_heads"])
    elif args.command == "reset":
        return reset_database(args)
    else:
        print(f"Error: Unknown command '{args.command}'.")
        return False
    
    # Run the command
    success, output = run_command(command, cwd=cwd)
    
    # Print the output
    print(output)
    
    # Print the result
    if success:
        print_header(f"Migration {args.command} Successful")
        return True
    else:
        print_header(f"Migration {args.command} Failed")
        return False


def reset_database(args):
    """Reset the database by deleting it and recreating it."""
    print_header("Resetting Database")
    
    # Get the database URL from the Alembic configuration
    with open("alembic.ini", "r") as f:
        config = f.read()
    
    import re
    match = re.search(r"sqlalchemy.url = (.*)", config)
    if not match:
        print("Error: Could not find database URL in alembic.ini.")
        return False
    
    db_url = match.group(1).strip()
    
    # Handle SQLite database
    if db_url.startswith("sqlite:///"):
        db_path = db_url[10:]
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"Deleted database file: {db_path}")
            except Exception as e:
                print(f"Error deleting database file: {e}")
                return False
        
        # Create a new empty database
        try:
            conn = sqlite3.connect(db_path)
            conn.close()
            print(f"Created new empty database file: {db_path}")
        except Exception as e:
            print(f"Error creating new database file: {e}")
            return False
        
        # Run the migrations
        print("Running migrations on the new database...")
        args.command = "upgrade"
        args.revision = "heads"
        return run_migrations(args)
    
    # Handle other database types
    else:
        print(f"Resetting database for {db_url} is not supported yet.")
        print("Please reset the database manually and run the migrations again.")
        return False


def setup_database_connection(args):
    """Set up the database connection in the Alembic configuration."""
    if not args.database_url:
        return True
    
    print_header("Setting Up Database Connection")
    
    # Read the Alembic configuration
    with open("alembic.ini", "r") as f:
        config = f.read()
    
    # Update the database URL
    import re
    config = re.sub(
        r"sqlalchemy.url = .*",
        f"sqlalchemy.url = {args.database_url}",
        config
    )
    
    # Write the updated configuration
    with open("alembic.ini", "w") as f:
        f.write(config)
    
    print(f"Database URL updated to: {args.database_url}")
    return True


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run Alembic migrations for the Election Monitoring System.")
    parser.add_argument("command", choices=["upgrade", "downgrade", "revision", "history", "current", "heads", "merge", "reset"],
                        help="Migration command to run")
    parser.add_argument("--revision", help="Revision to upgrade/downgrade to (default: heads for upgrade, -1 for downgrade)")
    parser.add_argument("--message", help="Message for the revision (default: 'Migration')")
    parser.add_argument("--database-url", help="Database URL to use (e.g., postgresql://username:password@localhost/electmoni)")
    args = parser.parse_args()
    
    # Set up the database connection
    if not setup_database_connection(args):
        sys.exit(1)
    
    # Run the migrations
    if not run_migrations(args):
        sys.exit(1)
    
    # Print the verification message
    print_header("Migration Complete")
    print("The database schema has been updated.")
    print("Please verify that the schema matches the expected structure.")
    print("\nTo complete Gate 2 verification, please update the verification.md file with your confirmation.")


if __name__ == "__main__":
    main()