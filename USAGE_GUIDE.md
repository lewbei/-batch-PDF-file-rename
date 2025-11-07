# PDF Batch Renamer - Usage Guide

This guide provides step-by-step instructions for safely using the PDF Batch Renamer tool.

## Quick Start

### Option 1: Jupyter Notebook (Recommended for beginners)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Open Jupyter Notebook
jupyter notebook PDF_file_rename_based_on_PDF_titles.ipynb

# 3. Run the cells and follow the prompts
```

### Option 2: Command-Line Script (Recommended for automation)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Check dependencies
python pdf_renamer.py --check-deps

# 3. Dry run (safe preview)
python pdf_renamer.py --directory /path/to/pdfs

# 4. Actually rename files
python pdf_renamer.py --directory /path/to/pdfs --no-dry-run
```

## Safety Checklist

Before renaming files, follow this checklist:

- [ ] **Create a backup** of your PDF files
- [ ] **Run in dry-run mode** first to preview changes
- [ ] **Review the preview** to ensure expected behavior
- [ ] **Check for warnings** (symlinks, security alerts, etc.)
- [ ] **Verify permissions** on the target directory
- [ ] **Close any open PDFs** that might be in use

## Step-by-Step Workflow

### Step 1: Create a Backup

**ALWAYS** create a backup before renaming files:

```bash
# Create timestamped backup
python backup_pdfs.py --source /path/to/pdfs

# Or specify custom backup location
python backup_pdfs.py --source /path/to/pdfs --backup /path/to/backup
```

**Verify the backup:**
```bash
# Check backup directory exists and contains files
ls -R /path/to/backup
```

### Step 2: Check Dependencies

Ensure all requirements are met:

```bash
python pdf_renamer.py --check-deps
```

Expected output:
```
Checking dependencies...
✓ PyMuPDF version: 1.23.x
✓ PyMuPDF version is current
```

If outdated:
```bash
pip install --upgrade PyMuPDF
```

### Step 3: Dry Run (Preview Changes)

**ALWAYS** run in dry-run mode first:

```bash
# Preview what would be renamed
python pdf_renamer.py --directory /path/to/pdfs
```

Review the output carefully:
- ✓ = Will be renamed
- ⚠ = Skipped (with reason)
- ✗ = Error occurred

**Check the summary:**
- How many files will be renamed?
- Are there unexpected skips?
- Any errors that need attention?

### Step 4: Review Preview Results

Look for these common scenarios:

**Good signs:**
- Files being renamed to descriptive titles
- Duplicates handled with numbers: `Title (1).pdf`
- Security warnings for symlinks (expected)

**Warning signs:**
- Many "No title in metadata" messages (PDFs may be scanned without OCR)
- "Title too long" messages (possible metadata corruption)
- Unexpected file paths

### Step 5: Execute Rename (If Safe)

Only proceed if preview looks good:

```bash
# Actually rename files
python pdf_renamer.py --directory /path/to/pdfs --no-dry-run
```

You'll be prompted to confirm:
```
⚠️  WARNING: You are about to rename files!
Directory: /path/to/pdfs
Are you sure you want to continue? (yes/no):
```

Type `yes` to proceed.

### Step 6: Verify Results

After renaming:

1. **Check the summary** for errors
2. **Review the log file**: `pdf_rename_log_YYYYMMDD_HHMMSS.txt`
3. **Spot check** some renamed files to ensure correctness
4. **Test opening** a few PDFs to ensure they weren't corrupted

## Common Scenarios

### Scenario 1: Academic Papers

```bash
# Typical use case: downloaded papers with generic names
# Before: paper1.pdf, document.pdf, download.pdf
# After:  Deep Learning in Computer Vision.pdf, etc.

python pdf_renamer.py --directory ~/Downloads/Papers
```

### Scenario 2: Handling Duplicates

If you have PDFs with identical titles:

```bash
# Automatically number duplicates (default)
python pdf_renamer.py --directory /path/to/pdfs

# Result: Title.pdf, Title (1).pdf, Title (2).pdf
```

Or skip duplicates:

```bash
# Skip files if target name exists
python pdf_renamer.py --directory /path/to/pdfs --no-duplicates
```

### Scenario 3: Nested Directories

The tool automatically processes subdirectories:

```bash
# Process entire directory tree
python pdf_renamer.py --directory /path/to/research

# Example structure:
# /path/to/research/
#   ├── 2023/
#   │   ├── paper1.pdf → Title1.pdf
#   │   └── paper2.pdf → Title2.pdf
#   └── 2024/
#       └── doc.pdf → Title3.pdf
```

### Scenario 4: Current Directory

```bash
# Rename PDFs in current directory
cd /path/to/pdfs
python pdf_renamer.py

# Or explicitly:
python pdf_renamer.py --directory .
```

## Troubleshooting

### Issue: "No title in metadata"

**Cause:** PDF doesn't have title metadata (common with scanned documents)

**Solutions:**
1. Use OCR software to add metadata
2. Rename these files manually
3. Accept that these files will be skipped

### Issue: "Title too long"

**Cause:** PDF metadata may be corrupted or contain entire abstract

**Solutions:**
1. Open PDF and check metadata
2. Manually set a reasonable title
3. Use PDF editing software to fix metadata

### Issue: "File already exists"

**Cause:** Multiple PDFs with same title

**Solutions:**
1. Use automatic numbering (default): `--no-duplicates` flag not used
2. Review why duplicates exist
3. Manually rename one of the duplicates first

### Issue: "Permission denied"

**Cause:** Insufficient permissions on directory or files

**Solutions:**
```bash
# Check permissions
ls -la /path/to/pdfs

# Fix permissions (Unix/Linux/Mac)
chmod -R u+rw /path/to/pdfs

# On Windows, right-click → Properties → Security
```

### Issue: Symbolic link warnings

**Cause:** Directory contains symbolic links (security feature)

**Solutions:**
1. This is expected behavior (security protection)
2. If you trust the symlinks, copy the actual files instead
3. Symlinks are automatically skipped

## Advanced Usage

### Automation with Cron/Task Scheduler

Create a script to automate backups and renaming:

```bash
#!/bin/bash
# rename_papers.sh

SOURCE="/path/to/papers"
BACKUP="/backups/papers_$(date +%Y%m%d)"

# Create backup
python backup_pdfs.py --source "$SOURCE" --backup "$BACKUP"

# Rename if backup successful
if [ $? -eq 0 ]; then
    python pdf_renamer.py --directory "$SOURCE" --no-dry-run
fi
```

Make executable and schedule:
```bash
chmod +x rename_papers.sh

# Add to cron (example: weekly on Sunday at 2 AM)
# crontab -e
# 0 2 * * 0 /path/to/rename_papers.sh
```

### Batch Processing Multiple Directories

```bash
#!/bin/bash
# Process multiple directories

for dir in /path/to/projects/*; do
    if [ -d "$dir" ]; then
        echo "Processing: $dir"
        python pdf_renamer.py --directory "$dir" --no-dry-run
    fi
done
```

### Integration with Git

Track changes in version-controlled paper repositories:

```bash
# Before renaming
git status

# Create backup
python backup_pdfs.py --source .

# Rename PDFs
python pdf_renamer.py --no-dry-run

# Review changes
git status
git diff --name-status

# Commit if satisfied
git add -A
git commit -m "Rename PDFs based on metadata titles"
```

## Best Practices

### 1. Always Backup
Create backups before ANY batch operation:
```bash
python backup_pdfs.py --source /path/to/important/pdfs
```

### 2. Test on Small Sample First
Before processing thousands of files:
```bash
# Create test directory
mkdir test_pdfs
cp /path/to/pdfs/*.pdf test_pdfs/ # Copy a few files

# Test on sample
python pdf_renamer.py --directory test_pdfs --no-dry-run

# If successful, proceed with full directory
```

### 3. Keep Logs
Archive log files for auditing:
```bash
mkdir logs
mv pdf_rename_log_*.txt logs/
```

### 4. Verify Metadata First
Check a few PDFs manually before batch processing:

**Linux/Mac:**
```bash
exiftool sample.pdf | grep Title
```

**Python:**
```python
import fitz
pdf = fitz.open("sample.pdf")
print(pdf.metadata["title"])
pdf.close()
```

### 5. Handle Special Cases Separately
Some files may need manual attention:
- Files without metadata
- Files with very long titles
- Duplicate titles
- Files with special characters in titles

### 6. Keep Original Names Reference
Save a list of original names before renaming:
```bash
# Before renaming
find /path/to/pdfs -name "*.pdf" > original_filenames.txt

# After renaming, you can compare with log file
```

## Security Reminders

1. **Only process trusted PDFs** - Don't run on files from unknown sources
2. **Review symlink warnings** - They're skipped for your protection
3. **Check path traversal warnings** - If you see these, investigate
4. **Keep PyMuPDF updated** - Run `pip install --upgrade PyMuPDF` regularly
5. **Review logs** - Check for any suspicious activity

## Getting Help

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Review [README.md](README.md) for feature descriptions
3. See [SECURITY.md](SECURITY.md) for security details
4. Open an issue on GitHub with:
   - What you tried to do
   - What happened (include error messages)
   - Your Python version: `python --version`
   - Your PyMuPDF version: `python -c "import fitz; print(fitz.version)"`

## Quick Reference

```bash
# Check dependencies
python pdf_renamer.py --check-deps

# Create backup
python backup_pdfs.py --source /path/to/pdfs

# Dry run (preview)
python pdf_renamer.py --directory /path/to/pdfs

# Actually rename
python pdf_renamer.py --directory /path/to/pdfs --no-dry-run

# Skip duplicate numbering
python pdf_renamer.py --directory /path/to/pdfs --no-duplicates

# Current directory
python pdf_renamer.py

# Get help
python pdf_renamer.py --help
python backup_pdfs.py --help
```
