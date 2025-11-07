#!/usr/bin/env python3
"""
PDF Backup Utility
Creates a backup of PDF files before running batch rename operations.

Usage:
    python backup_pdfs.py [options]

Options:
    --source PATH       Source directory containing PDF files (default: current directory)
    --backup PATH       Backup directory (default: ./pdf_backup_TIMESTAMP)
    --help             Show this help message
"""

import os
import sys
import shutil
import argparse
from datetime import datetime
from pathlib import Path

def create_backup(source_dir, backup_dir=None):
    """
    Create a backup of all PDF files from source directory.

    Args:
        source_dir: Source directory containing PDFs
        backup_dir: Destination backup directory (created if doesn't exist)

    Returns:
        tuple: (success: bool, backup_path: str, file_count: int)
    """
    # Validate source directory
    source_dir = os.path.abspath(source_dir)
    if not os.path.exists(source_dir):
        print(f"❌ Error: Source directory does not exist: {source_dir}")
        return False, None, 0

    if not os.path.isdir(source_dir):
        print(f"❌ Error: Source path is not a directory: {source_dir}")
        return False, None, 0

    # Create backup directory with timestamp
    if backup_dir is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(
            os.path.dirname(source_dir),
            f"pdf_backup_{timestamp}"
        )

    backup_dir = os.path.abspath(backup_dir)

    # Check if backup directory already exists
    if os.path.exists(backup_dir):
        print(f"⚠️  Warning: Backup directory already exists: {backup_dir}")
        response = input("Overwrite? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Backup cancelled.")
            return False, None, 0

    print("=" * 80)
    print("PDF BACKUP UTILITY")
    print("=" * 80)
    print(f"\nSource:      {source_dir}")
    print(f"Destination: {backup_dir}\n")
    print("-" * 80)

    # Create backup directory
    try:
        os.makedirs(backup_dir, exist_ok=True)
    except Exception as e:
        print(f"❌ Error creating backup directory: {e}")
        return False, None, 0

    # Count and copy PDF files
    file_count = 0
    error_count = 0
    total_size = 0

    for root_dir, dirs, files in os.walk(source_dir):
        # Calculate relative path for maintaining directory structure
        rel_path = os.path.relpath(root_dir, source_dir)
        dest_dir = os.path.join(backup_dir, rel_path) if rel_path != '.' else backup_dir

        # Create subdirectory in backup
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir, exist_ok=True)
            except Exception as e:
                print(f"⚠️  Error creating directory {dest_dir}: {e}")
                continue

        # Copy PDF files
        for filename in files:
            if not filename.lower().endswith('.pdf'):
                continue

            source_file = os.path.join(root_dir, filename)
            dest_file = os.path.join(dest_dir, filename)

            try:
                # Skip symbolic links for security
                if os.path.islink(source_file):
                    print(f"⚠️  Skipping symbolic link: {source_file}")
                    continue

                # Copy file
                shutil.copy2(source_file, dest_file)
                file_size = os.path.getsize(source_file)
                total_size += file_size
                file_count += 1

                print(f"✓ Backed up: {os.path.relpath(source_file, source_dir)}")

            except Exception as e:
                print(f"✗ Error backing up {source_file}: {e}")
                error_count += 1

    # Summary
    print("\n" + "=" * 80)
    print("BACKUP SUMMARY")
    print("=" * 80)
    print(f"Files backed up:  {file_count}")
    print(f"Errors:          {error_count}")
    print(f"Total size:      {total_size / (1024*1024):.2f} MB")
    print(f"Backup location: {backup_dir}")
    print("=" * 80)

    if file_count > 0:
        print("\n✅ Backup completed successfully!")
        print(f"\n💡 To restore, copy files from:")
        print(f"   {backup_dir}")
        print(f"   back to:")
        print(f"   {source_dir}")
    else:
        print("\n⚠️  No PDF files found to backup.")

    return file_count > 0, backup_dir, file_count

def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Create a backup of PDF files before batch renaming.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backup_pdfs.py                                    # Backup current directory
  python backup_pdfs.py --source /path/to/pdfs            # Backup specific directory
  python backup_pdfs.py --source /path/to/pdfs --backup /path/to/backup  # Custom backup location

Recommendations:
  - Always create a backup before running batch rename operations
  - Store backups on a different drive for maximum safety
  - Verify backup completed successfully before proceeding
        """
    )

    parser.add_argument(
        '--source',
        '-s',
        default='.',
        help='Source directory containing PDF files (default: current directory)'
    )

    parser.add_argument(
        '--backup',
        '-b',
        help='Backup directory (default: ./pdf_backup_TIMESTAMP)'
    )

    args = parser.parse_args()

    # Confirm operation
    source = os.path.abspath(args.source)
    print(f"\nYou are about to backup PDF files from:")
    print(f"  {source}")

    if args.backup:
        print(f"To:")
        print(f"  {os.path.abspath(args.backup)}")

    response = input("\nContinue? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("Backup cancelled.")
        sys.exit(0)

    print()

    # Create backup
    success, backup_path, file_count = create_backup(args.source, args.backup)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
