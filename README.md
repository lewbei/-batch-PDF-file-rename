# Batch PDF File Renamer

A Python utility that automatically renames PDF files based on their embedded metadata titles. This tool helps you organize large collections of PDF documents by giving them meaningful filenames extracted from their internal metadata.

## Features

### Core Functionality
- **Automatic Renaming**: Extracts PDF title metadata and uses it as the filename
- **Recursive Processing**: Scans directories and subdirectories for PDF files
- **Smart Validation**:
  - Filters invalid filename characters across all operating systems
  - Automatic duplicate handling with numbered suffixes
  - Skips files without metadata titles
- **Dry Run Mode**: Preview changes before actually renaming files (enabled by default)
- **Audit Logging**: Creates timestamped logs of all rename operations

### Security Features
- **Path Traversal Prevention**: Validates all paths to prevent accessing files outside the target directory
- **Symlink Protection**: Detects and skips symbolic links that could point to sensitive locations
- **Filename Sanitization**: Removes control characters and enforces filesystem limits (255 chars)
- **Metadata Validation**: Limits title length (1000 chars) to prevent metadata corruption exploits
- **Permission Checks**: Verifies read/write access before processing

### Reliability
- **Error Handling**: Robust error handling for corrupted or non-standard PDFs
- **Resource Management**: Properly closes file handles to prevent memory leaks
- **User Feedback**: Detailed console output showing processing status and summary statistics
- **Interactive Mode**: Prompts for directory path and options

## Requirements

- Python 3.6+
- PyMuPDF (fitz)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/lewbei/-batch-PDF-file-rename.git
cd -batch-PDF-file-rename
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install PyMuPDF
```

## Usage

### Running in Jupyter Notebook or Google Colab

1. Open `PDF_file_rename_based_on_PDF_titles.ipynb` in Jupyter Notebook or upload to Google Colab
2. Run the first cell to import required libraries
3. Run the second cell and follow the interactive prompts:
   - Enter the directory path (or press Enter for current directory)
   - Choose whether to run in dry-run mode (recommended first time)
   - Choose whether to automatically number duplicate filenames
4. Review the output and check the generated log file

### Example Output

```
================================================================================
PDF BATCH RENAMER - Based on PDF Metadata Titles
================================================================================

Enter the directory path containing PDF files (or press Enter for current directory): /path/to/pdfs
Perform dry run first? (y/n, default: y): y

🔍 DRY RUN MODE - No files will be renamed

Automatically number duplicate filenames? (y/n, default: y): y

Scanning directory: /path/to/pdfs
--------------------------------------------------------------------------------

Processing: /path/to/pdfs/document1.pdf
  ✓ Would rename to: Introduction to Machine Learning.pdf

Processing: /path/to/pdfs/file2.pdf
  ⚠ Skipped: No title in metadata

Processing: /path/to/pdfs/paper.pdf
  ✓ Would rename to: Deep Learning Applications in Computer Vision.pdf

Processing: /path/to/pdfs/another.pdf
  ✓ Would rename to: Introduction to Machine Learning (1).pdf

================================================================================
SUMMARY
================================================================================
Total PDF files found: 4
Would rename: 3
Skipped: 1
Errors: 0
================================================================================

💡 Tip: Run again with dry_run='n' to perform actual renaming
```

## How It Works

1. **Scan**: Recursively walks through the specified directory
2. **Filter**: Only processes files with `.pdf` extension
3. **Extract**: Opens each PDF and reads the title from metadata
4. **Sanitize**: Removes invalid filename characters (`< > : " / \ | ? *`)
5. **Validate**: Checks if the title exists and if target filename is available
6. **Rename**: Updates the filename while preserving the directory structure

## Safety & Security Features

### Data Safety
- **Non-destructive**: Only renames files, doesn't modify PDF content
- **Dry Run Mode**: Preview all changes before committing (default: enabled)
- **Duplicate Handling**: Automatically numbers duplicates or skips to prevent overwrites
- **Audit Logging**: Creates detailed logs with timestamps for accountability
- **Error Recovery**: Continues processing even if individual files fail

### Security Protections
- **Path Traversal Prevention**: Validates all file paths stay within target directory
- **Symlink Detection**: Refuses to process symbolic links that could escape directory boundaries
- **Input Validation**: Sanitizes and validates all user inputs
- **Permission Verification**: Checks directory permissions before starting
- **Filename Length Limits**: Enforces 255-character limit to prevent filesystem issues
- **Control Character Filtering**: Removes ASCII control characters from filenames
- **Metadata Size Limits**: Rejects suspiciously long metadata (>1000 chars)

### Resource Management
- **Proper Cleanup**: All file handles closed using try/finally blocks
- **Memory Efficient**: Processes files one at a time
- **Graceful Degradation**: Individual errors don't crash the entire operation

See [SECURITY.md](SECURITY.md) for detailed security information.

## Common Use Cases

- Organizing academic papers and research documents
- Managing downloaded PDFs with generic filenames
- Cleaning up document libraries
- Batch processing scanned documents with metadata

## Limitations

- Only processes files with embedded title metadata
- Skips PDFs without title information
- Cannot handle extremely long titles (OS filename length limits apply)
- Requires read/write permissions in the target directory

## Troubleshooting

**Problem**: PDF not renamed
**Solution**: Check if the PDF has title metadata. Some PDFs, especially scanned documents, may not have this information.

**Problem**: "File already exists" error
**Solution**: Enable automatic numbering of duplicates when prompted, or manually resolve the conflict.

**Problem**: Permission denied
**Solution**: Ensure you have read/write permissions for the directory and files.

**Problem**: Symbolic link warning
**Solution**: This is a security feature. The tool skips symlinks to prevent accessing files outside the target directory.

**Problem**: "Title too long" message
**Solution**: The PDF metadata may be corrupted. This is a security measure to prevent malformed metadata from causing issues.

## Security

This tool implements multiple security measures to protect your system:

- Path traversal prevention
- Symbolic link detection
- Input validation and sanitization
- Metadata validation
- Resource management

For detailed security information, see [SECURITY.md](SECURITY.md).

**Best Practices:**
- Always run with dry-run mode first
- Backup important files before batch operations
- Only process PDFs from trusted sources
- Review logs after operations
- Keep PyMuPDF updated for security patches

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [PyMuPDF](https://github.com/pymupdf/PyMuPDF) for PDF processing
- Designed for use in Jupyter Notebooks and Google Colab

## Contact

If you have any questions or suggestions, please open an issue on GitHub.

---

**Note**: Always backup your files before running batch rename operations.
