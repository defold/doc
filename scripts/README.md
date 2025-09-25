# Documentation Consistency Checker

A Python script designed to check consistency between documentation files in different languages for the Defold project. This tool compares file structures and Markdown syntax trees to ensure translations maintain the same structure and formatting.

## Features

- **File Structure Comparison**: Compares the directory structure between source and target documentation directories
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

To run a full comparison between source and target documentation directories:

```bash
python docs_consistency_checker.py --source-dir ./docs/en --target-dir ./docs/zh
```

### Advanced Usage

#### Specify Custom Directories

```bash
python docs_consistency_checker.py --source-dir /path/to/source/docs --target-dir /path/to/target/docs
```

#### Check a Specific File

```bash
python docs_consistency_checker.py --source-dir ./docs/en --target-dir ./docs/zh --file manuals/game-project/game-project.md
```

#### Check Specific File Pairs

```bash
python docs_consistency_checker.py --source-file /path/to/source/file.md --target-file /path/to/target/file.md
```

#### Specify Output File

```bash
python docs_consistency_checker.py --source-dir ./docs/en --target-dir ./docs/zh --output custom_comparison.xlsx
```

### Command Line Arguments

| Argument | Description |
|----------|-------------|
| `--file` | Specify a particular file to check (relative to docs directory) |
| `--source-dir` | Path to source documentation directory |
| `--target-dir` | Path to target documentation directory |
| `--output` | Path for the output Excel file |
| `--source-file` | Path to a specific source file |
| `--target-file` | Path to a specific target file |
| `--help` | Show help message and exit |

## Output

The script generates an Excel file with the following columns:

1. **File Path**: Relative path of the file
2. **File Extension**: File extension type
3. **Top Directory**: Top-level directory containing the file
4. **Source Version Exists**: Whether the file exists in source documentation
5. **Target Version Exists**: Whether the file exists in target documentation
6. **Status**: 
   - "Consistent" - File exists in both versions
   - "Source Only" - File exists only in source version
   - "Target Only" - File exists only in target version
   - "Does Not Exist" - File doesn't exist in either version
7. **Source File Size (KB)**: Size of the source file
8. **Target File Size (KB)**: Size of the target file
9. **Markdown Syntax Consistency**: Results of Markdown syntax comparison
10. **Formula**: Recommended actions for ensuring translation consistency

## How It Works

1. **File Collection**: The script recursively collects all files from both source and target documentation directories.
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

### Compare entire documentation directories
```bash
python docs_consistency_checker.py --source-dir ../docs/en --target-dir ../docs/zh
```

### Compare specific file
```bash
python docs_consistency_checker.py --source-dir ../docs/en --target-dir ../docs/zh --file manuals/introduction.md
```

### Compare direct file paths
```bash
python docs_consistency_checker.py --source-file ../docs/en/manuals/introduction.md --target-file ../docs/zh/manuals/introduction.md
```

### Get help
```bash
python docs_consistency_checker.py --help
```
