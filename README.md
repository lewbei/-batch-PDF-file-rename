# Batch PDF File Renamer

A Python utility that automatically renames PDF files based on their embedded metadata titles. This tool helps you organize large collections of PDF documents by giving them meaningful filenames extracted from their internal metadata.

## Features

- **Automatic Renaming**: Extracts PDF title metadata and uses it as the filename
- **Recursive Processing**: Scans directories and subdirectories for PDF files
- **Smart Validation**:
  - Filters invalid filename characters
  - Prevents duplicate filenames
  - Skips files without metadata titles
- **Error Handling**: Robust error handling for corrupted or non-standard PDFs
- **Resource Management**: Properly closes file handles to prevent memory leaks
- **User Feedback**: Detailed console output showing processing status and summary statistics
- **Interactive**: Prompts for directory path, making it easy to use

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
pip install PyMuPDF
```

## Usage

### Running in Jupyter Notebook or Google Colab

1. Open `PDF_file_rename_based_on_PDF_titles.ipynb` in Jupyter Notebook or upload to Google Colab
2. Run the first cell to import required libraries
3. Run the second cell and enter the directory path when prompted
4. Review the summary of renamed files

### Example Output

```
Enter the directory path containing PDF files (or press Enter for current directory): /path/to/pdfs

Scanning directory: /path/to/pdfs

--------------------------------------------------------------------------------

Processing: /path/to/pdfs/document1.pdf
  ✓ Renamed to: Introduction to Machine Learning.pdf

Processing: /path/to/pdfs/file2.pdf
  ⚠ Skipped: No title in metadata

Processing: /path/to/pdfs/paper.pdf
  ✓ Renamed to: Deep Learning Applications in Computer Vision.pdf

================================================================================
SUMMARY
================================================================================
Total PDF files found: 3
Successfully renamed: 2
Skipped: 1
Errors: 0
================================================================================
```

## How It Works

1. **Scan**: Recursively walks through the specified directory
2. **Filter**: Only processes files with `.pdf` extension
3. **Extract**: Opens each PDF and reads the title from metadata
4. **Sanitize**: Removes invalid filename characters (`< > : " / \ | ? *`)
5. **Validate**: Checks if the title exists and if target filename is available
6. **Rename**: Updates the filename while preserving the directory structure

## Safety Features

- **Non-destructive**: Only renames files, doesn't modify PDF content
- **Duplicate Prevention**: Won't overwrite existing files
- **Error Recovery**: Continues processing even if individual files fail
- **Resource Cleanup**: Ensures all file handles are properly closed

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
**Solution**: Another file already has the same title. Manual intervention required to resolve the conflict.

**Problem**: Permission denied
**Solution**: Ensure you have read/write permissions for the directory and files.

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
