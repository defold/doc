# Documentation Consistency Checker

A Python script designed to check consistency between English and Chinese documentation files in the Defold project. This tool compares file structures and Markdown syntax trees to ensure translations maintain the same structure and formatting.

## Features

- **File Structure Comparison**: Compares the directory structure between English and Chinese documentation
- **Markdown Syntax Tree Analysis**: Analyzes and compares Markdown syntax elements including:
  - Headers (h1, h2, h3, etc.)
  - Code blocks
  - Inline code
  - Bold text
  - Italic text
  - Links
  - Lists
- **Excel Report Generation**: Creates a comprehensive Excel report with comparison results
- **Specific File Checking**: Allows checking individual files or specific file pairs

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - openpyxl

## Installation

1. Clone or download the repository
2. Install the required package:
   ```
   pip install openpyxl
   ```

## Usage

### Basic Usage

To run a full comparison between English and Chinese documentation:

```bash
python scripts/docs_consistency_checker.py
```

This will:
- Use default paths: `docs/en` for English documentation and `docs/zh` for Chinese documentation
- Generate an output file named `docs_structure_comparison.xlsx`

### Advanced Usage

#### Specify Custom Directories

```bash
python scripts/docs_consistency_checker.py --en-dir /path/to/english/docs --zh-dir /path/to/chinese/docs
```

#### Check a Specific File

```bash
python scripts/docs_consistency_checker.py --file manuals/game-project/game-project.md
```

#### Check Specific File Pairs

```bash
python scripts/docs_consistency_checker.py --en-file /path/to/english/file.md --zh-file /path/to/chinese/file.md
```

#### Specify Output File

```bash
python scripts/docs_consistency_checker.py --output custom_comparison.xlsx
```

### Command Line Arguments

| Argument | Description |
|----------|-------------|
| `--file` | Specify a particular file to check (relative to docs directory) |
| `--en-dir` | Path to English documentation directory |
| `--zh-dir` | Path to Chinese documentation directory |
| `--output` | Path for the output Excel file |
| `--en-file` | Path to a specific English file |
| `--zh-file` | Path to a specific Chinese file |

## Output

The script generates an Excel file with the following columns:

1. **File Path**: Relative path of the file
2. **File Extension**: File extension type
3. **Top Directory**: Top-level directory containing the file
4. **English Version Exists**: Whether the file exists in English documentation
5. **Chinese Version Exists**: Whether the file exists in Chinese documentation
6. **Status**: 
   - "Consistent" - File exists in both versions
   - "English Only" - File exists only in English version
   - "Chinese Only" - File exists only in Chinese version
   - "Does Not Exist" - File doesn't exist in either version
7. **English File Size (KB)**: Size of the English file
8. **Chinese File Size (KB)**: Size of the Chinese file
9. **Markdown Syntax Consistency**: Results of Markdown syntax comparison
10. **Formula**: Recommended actions for ensuring translation consistency

## How It Works

1. **File Collection**: The script recursively collects all files from both English and Chinese documentation directories.
2. **File Comparison**: It compares the file structures between the two directories.
3. **Markdown Analysis**: For Markdown files that exist in both versions, the script:
   - Parses the Markdown content to build syntax trees
   - Compares the syntax trees to identify inconsistencies
   - Reports differences in structure, formatting, and elements
4. **Report Generation**: All comparison results are compiled into an Excel spreadsheet with color-coded status indicators.

## Error Handling

The script includes comprehensive error handling for:
- File access issues
- Encoding problems (especially for Chinese characters)
- Markdown parsing errors
- Excel file generation issues

## Module Structure

The script is organized into several modules:

- `docs_consistency_checker.py`: Main entry point and command-line interface
- `modules/main.py`: Core comparison logic
- `modules/file_handler.py`: File operations and utilities
- `modules/markdown_handler.py`: Markdown parsing and comparison
- `modules/excel_handler.py`: Excel report generation
