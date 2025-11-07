# Security Policy

## Security Features

This tool implements several security measures to ensure safe operation:

### 1. Path Traversal Prevention
- **Input Validation**: All directory paths are validated and resolved to absolute paths
- **Path Containment**: Verifies all processed files remain within the specified directory
- **Basename Extraction**: Removes path components from filenames to prevent directory traversal

### 2. Symbolic Link Protection
- **Link Detection**: Automatically detects and skips symbolic links
- **Warning Messages**: Alerts users when symbolic links are encountered
- **No Follow**: Never follows symlinks that could point outside the working directory

### 3. Filename Sanitization
- **Invalid Character Removal**: Removes characters invalid on Windows, Linux, and macOS: `< > : " / \ | ? *`
- **Control Character Filtering**: Strips ASCII control characters (0-31)
- **Length Limits**: Enforces maximum filename length (255 characters) to prevent filesystem issues
- **Special Sequence Removal**: Eliminates `..` sequences that could enable path traversal

### 4. Metadata Validation
- **Length Limits**: Rejects PDF titles longer than 1000 characters (potential metadata corruption)
- **Empty Check**: Validates that metadata exists and contains valid title information
- **Type Validation**: Ensures files are actually PDFs before processing

### 5. Resource Management
- **Proper Cleanup**: All file handles are closed using try/finally blocks
- **Error Isolation**: Individual file errors don't crash the entire process
- **Memory Efficiency**: Files are processed one at a time, not loaded into memory

### 6. Permission Checks
- **Read/Write Validation**: Verifies necessary permissions before starting
- **Directory Validation**: Confirms target is a valid, accessible directory
- **Graceful Failures**: Clear error messages for permission issues

### 7. Safe Defaults
- **Dry Run Mode**: Enabled by default to preview changes before execution
- **Duplicate Handling**: Automatically numbers duplicates to prevent overwrites
- **Audit Logging**: Creates timestamped logs of all rename operations

## Reporting a Vulnerability

If you discover a security vulnerability in this tool, please report it by:

1. **DO NOT** open a public issue
2. Email the repository owner or create a private security advisory
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if applicable)

## Security Best Practices for Users

When using this tool:

1. **Always run a dry run first** to preview changes
2. **Backup your files** before batch operations
3. **Use on trusted PDFs only** - don't process PDFs from untrusted sources
4. **Review the logs** after renaming to verify expected behavior
5. **Run with minimal privileges** - don't use root/admin unless necessary
6. **Keep PyMuPDF updated** to ensure PDF parsing security patches

## Known Limitations

- **Metadata Trust**: The tool trusts PDF metadata content. Maliciously crafted PDFs with manipulated metadata won't execute code but could create unusual filenames
- **Unicode Characters**: Some filesystem/OS combinations may not support all Unicode characters in filenames
- **Large Directories**: Processing thousands of files may take time; progress isn't shown for individual subdirectories

## Dependency Security

This tool relies on:
- **PyMuPDF (fitz)**: Actively maintained PDF library
  - Keep updated to receive security patches
  - Check for updates: `pip install --upgrade PyMuPDF`

## Version Support

Security updates will be provided for:
- The latest release
- Critical security issues may be backported to previous versions on request
