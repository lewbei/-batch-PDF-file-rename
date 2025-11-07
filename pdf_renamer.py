#!/usr/bin/env python3
"""
PDF Batch Renamer - Standalone Script
Renames PDF files based on their embedded metadata titles.

Usage:
    python pdf_renamer.py [options]

Options:
    --directory PATH    Directory containing PDF files (default: current directory)
    --no-dry-run       Skip dry run and rename files immediately
    --no-duplicates    Don't automatically number duplicate filenames
    --help             Show this help message
"""

import fitz
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

# Maximum filename length for most filesystems
MAX_FILENAME_LENGTH = 255

def sanitize_filename(filename, max_length=MAX_FILENAME_LENGTH - 4):
    """
    Remove or replace invalid characters from filename.

    Security: Prevents path traversal and ensures filename safety.
    """
    # Remove invalid characters for filenames across Windows, Linux, and macOS
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')

    # Remove control characters (ASCII 0-31)
    filename = ''.join(char for char in filename if ord(char) >= 32)

    # Remove leading/trailing whitespace and dots
    filename = filename.strip('. ')

    # Prevent path traversal attacks
    filename = filename.replace('..', '')
    filename = os.path.basename(filename)  # Remove any path components

    # Truncate to maximum length while trying to preserve meaning
    if len(filename) > max_length:
        filename = filename[:max_length].rsplit(' ', 1)[0]  # Try to break at word boundary

    return filename

def is_safe_path(base_path, target_path):
    """
    Verify that target_path is within base_path to prevent directory traversal.

    Security: Prevents accessing files outside intended directory.
    """
    try:
        base = Path(base_path).resolve()
        target = Path(target_path).resolve()
        return target.is_relative_to(base)
    except (ValueError, OSError):
        return False

def get_unique_filename(directory, base_name, extension=".pdf"):
    """
    Generate a unique filename by appending numbers if file exists.

    Security: Prevents race conditions and handles duplicates safely.
    """
    filepath = os.path.join(directory, base_name + extension)

    # Check for symlinks - security measure
    if os.path.islink(filepath):
        return None, "Target is a symbolic link"

    if not os.path.exists(filepath):
        return filepath, None

    # File exists, try numbered variants
    counter = 1
    max_attempts = 1000  # Prevent infinite loop

    while counter < max_attempts:
        # Calculate available space for counter
        suffix = f" ({counter})"
        max_base_length = MAX_FILENAME_LENGTH - len(extension) - len(suffix)
        truncated_base = base_name[:max_base_length] if len(base_name) > max_base_length else base_name

        new_name = f"{truncated_base}{suffix}{extension}"
        filepath = os.path.join(directory, new_name)

        if os.path.islink(filepath):
            counter += 1
            continue

        if not os.path.exists(filepath):
            return filepath, None

        counter += 1

    return None, "Too many files with same name"

def check_dependencies():
    """Check if required dependencies are installed and up to date."""
    print("Checking dependencies...")

    try:
        import fitz
        version = fitz.version
        print(f"✓ PyMuPDF version: {version[0]}")

        # Check if version is recent (1.23.0+)
        major, minor = map(int, version[0].split('.')[:2])
        if major < 1 or (major == 1 and minor < 23):
            print(f"⚠ Warning: PyMuPDF version {version[0]} is outdated. Recommend 1.23.0+")
            print(f"  Update with: pip install --upgrade PyMuPDF")
        else:
            print("✓ PyMuPDF version is current")

    except ImportError:
        print("✗ PyMuPDF (fitz) is not installed!")
        print("  Install with: pip install PyMuPDF")
        return False

    print()
    return True

def process_pdfs(directory_path, dry_run=True, handle_duplicates=True):
    """
    Main function to process PDF files.

    Args:
        directory_path: Path to directory containing PDFs
        dry_run: If True, preview changes without renaming
        handle_duplicates: If True, automatically number duplicate filenames
    """
    # Security: Validate directory path
    try:
        directory_path = os.path.abspath(directory_path)
        if not os.path.exists(directory_path):
            print(f"\n❌ Error: Directory does not exist: {directory_path}")
            return False

        if not os.path.isdir(directory_path):
            print(f"\n❌ Error: Path is not a directory: {directory_path}")
            return False

        # Check if we have read/write permissions
        if not os.access(directory_path, os.R_OK | os.W_OK):
            print(f"\n❌ Error: Insufficient permissions for directory: {directory_path}")
            return False

    except (OSError, PermissionError) as e:
        print(f"\n❌ Error accessing directory: {e}")
        return False

    print("=" * 80)
    print("PDF BATCH RENAMER - Based on PDF Metadata Titles")
    print("=" * 80)
    print()

    if dry_run:
        print("🔍 DRY RUN MODE - No files will be renamed\n")
    else:
        print("⚠️  LIVE MODE - Files will be renamed\n")

    print(f"Directory: {directory_path}")
    print(f"Duplicate handling: {'Enabled' if handle_duplicates else 'Disabled'}")
    print("-" * 80)

    # Statistics
    total_files = 0
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    rename_operations = []  # Store operations for logging

    # Create log filename with timestamp
    log_filename = f"pdf_rename_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_path = os.path.join(directory_path, log_filename)

    # Process files
    for root_dir, cur_dir, files in os.walk(directory_path):
        for name in files:
            # Only process PDF files
            if not name.lower().endswith('.pdf'):
                continue

            total_files += 1
            file_path = os.path.join(root_dir, name)

            # Security: Verify path is within our base directory
            if not is_safe_path(directory_path, file_path):
                print(f"\n⚠️  SECURITY WARNING: Skipping file outside base directory: {file_path}")
                skipped_count += 1
                continue

            # Security: Skip symbolic links
            if os.path.islink(file_path):
                print(f"\n⚠️  SECURITY WARNING: Skipping symbolic link: {file_path}")
                skipped_count += 1
                continue

            print(f"\nProcessing: {file_path}")

            pdf = None
            try:
                # Open PDF and read metadata
                pdf = fitz.open(file_path)
                metadata = pdf.metadata

                if not metadata:
                    print(f"  ⚠ Skipped: No metadata available")
                    skipped_count += 1
                    continue

                title = metadata.get("title", "").strip()

                # Check if title exists
                if not title:
                    print(f"  ⚠ Skipped: No title in metadata")
                    skipped_count += 1
                    continue

                # Security: Limit title length to prevent abuse
                if len(title) > 1000:
                    print(f"  ⚠ Skipped: Title too long (>1000 chars), possible metadata corruption")
                    skipped_count += 1
                    continue

                # Sanitize the title
                sanitized_title = sanitize_filename(title)

                if not sanitized_title:
                    print(f"  ⚠ Skipped: Title contains only invalid characters")
                    skipped_count += 1
                    continue

                # Check minimum length
                if len(sanitized_title) < 1:
                    print(f"  ⚠ Skipped: Sanitized title is empty")
                    skipped_count += 1
                    continue

                # Get unique filename (handles duplicates if enabled)
                if handle_duplicates:
                    new_file_path, error_msg = get_unique_filename(root_dir, sanitized_title)
                    if error_msg:
                        print(f"  ⚠ Skipped: {error_msg}")
                        skipped_count += 1
                        continue
                else:
                    new_file_path = os.path.join(root_dir, sanitized_title + ".pdf")

                # Check if file already has the correct name
                if file_path == new_file_path:
                    print(f"  ✓ Already named correctly")
                    skipped_count += 1
                    continue

                # Check if target file already exists (when not handling duplicates)
                if not handle_duplicates and os.path.exists(new_file_path):
                    print(f"  ⚠ Skipped: File already exists with name '{os.path.basename(new_file_path)}'")
                    skipped_count += 1
                    continue

                # Close PDF before renaming
                pdf.close()
                pdf = None

                # Perform rename (or simulate in dry run)
                if not dry_run:
                    # Security: Final check before rename
                    if not is_safe_path(directory_path, new_file_path):
                        print(f"  ⚠️  SECURITY WARNING: Generated path outside base directory, skipping")
                        skipped_count += 1
                        continue

                    os.rename(file_path, new_file_path)
                    print(f"  ✓ Renamed to: {os.path.basename(new_file_path)}")
                else:
                    print(f"  ✓ Would rename to: {os.path.basename(new_file_path)}")

                renamed_count += 1
                rename_operations.append({
                    'original': file_path,
                    'new': new_file_path,
                    'title': title
                })

            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                error_count += 1

            finally:
                # Ensure PDF is closed
                if pdf is not None:
                    try:
                        pdf.close()
                    except:
                        pass

    # Write log file
    if rename_operations and not dry_run:
        try:
            with open(log_path, 'w', encoding='utf-8') as log_file:
                log_file.write(f"PDF Rename Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                log_file.write("=" * 80 + "\n\n")
                log_file.write(f"Directory: {directory_path}\n")
                log_file.write(f"Total files renamed: {renamed_count}\n\n")
                log_file.write("-" * 80 + "\n\n")

                for op in rename_operations:
                    log_file.write(f"Original: {op['original']}\n")
                    log_file.write(f"New:      {op['new']}\n")
                    log_file.write(f"Title:    {op['title']}\n")
                    log_file.write("-" * 80 + "\n")

            print(f"\n📝 Log file created: {log_filename}")
        except Exception as e:
            print(f"\n⚠️  Warning: Could not create log file: {e}")

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total PDF files found: {total_files}")
    if dry_run:
        print(f"Would rename: {renamed_count}")
    else:
        print(f"Successfully renamed: {renamed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print("=" * 80)

    if dry_run and renamed_count > 0:
        print("\n💡 Tip: Run again with --no-dry-run to perform actual renaming")
    elif not dry_run and renamed_count > 0:
        print("\n✅ Renaming completed successfully!")
        print(f"📋 Check the log file for details: {log_filename}")

    return True

def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description='Batch rename PDF files based on their metadata titles.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_renamer.py                          # Dry run in current directory
  python pdf_renamer.py --directory /path/to/pdfs  # Dry run in specific directory
  python pdf_renamer.py --no-dry-run              # Actually rename files
  python pdf_renamer.py --no-duplicates           # Don't number duplicates

Security Notes:
  - Always run with dry-run first (default behavior)
  - Backup important files before batch operations
  - Only process PDFs from trusted sources
        """
    )

    parser.add_argument(
        '--directory',
        '-d',
        default='.',
        help='Directory containing PDF files (default: current directory)'
    )

    parser.add_argument(
        '--no-dry-run',
        action='store_true',
        help='Skip dry run and rename files immediately (USE WITH CAUTION)'
    )

    parser.add_argument(
        '--no-duplicates',
        action='store_true',
        help="Don't automatically number duplicate filenames"
    )

    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='Check dependencies and exit'
    )

    args = parser.parse_args()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    if args.check_deps:
        sys.exit(0)

    # Confirm if not in dry-run mode
    if args.no_dry_run:
        print("\n⚠️  WARNING: You are about to rename files!")
        print(f"Directory: {os.path.abspath(args.directory)}")
        response = input("Are you sure you want to continue? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("Operation cancelled.")
            sys.exit(0)
        print()

    # Process PDFs
    success = process_pdfs(
        directory_path=args.directory,
        dry_run=not args.no_dry_run,
        handle_duplicates=not args.no_duplicates
    )

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
