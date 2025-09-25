import os
import sys

from .file_handler import collect_files, get_file_info, read_file_content, setup_console_encoding
from .excel_handler import create_workbook, get_status_fills, write_file_info, write_file_sizes, write_markdown_consistency, write_formula_text, adjust_column_widths, save_workbook, print_statistics
from .markdown_handler import compare_markdown_syntax_trees


def main(source_dir_path=None, target_dir_path=None, output_file_path=None):
    """
    Main function for document consistency checking
    
    Parameters:
        source_dir_path: Source document directory path (required)
        target_dir_path: Target document directory path (required)
        output_file_path: Output Excel file path (optional, defaults to docs_structure_comparison.xlsx)
    """
    # Check if required parameters are provided
    if source_dir_path is None or target_dir_path is None:
        print("Error: Both source_dir_path and target_dir_path parameters are required.")
        print("Usage: main(source_dir_path='path/to/source', target_dir_path='path/to/target')")
        return
    
    # Check if directories exist
    if not os.path.exists(source_dir_path):
        print(f"Error: Source directory does not exist: {source_dir_path}")
        return
    
    if not os.path.exists(target_dir_path):
        print(f"Error: Target directory does not exist: {target_dir_path}")
        return
    
    # Set default output file path if not provided
    if output_file_path is None:
        output_file_path = "docs_structure_comparison.xlsx"
        
    # Set console encoding to resolve character display issues
    setup_console_encoding()

    # Create Excel workbook
    wb, ws = create_workbook()
    
    # Get status fill colors
    status_fills = get_status_fills()

    # Row counter
    row_num = 2
    
    # Collect all file paths
    source_files = collect_files(source_dir_path)
    target_files = collect_files(target_dir_path)
    
    # Get all unique file paths
    all_files = source_files.union(target_files)
    
    # Compare file structure
    print("Comparing file structure...")
    for file_path in sorted(all_files):
        source_exists = file_path in source_files
        target_exists = file_path in target_files
        
        # Get file information
        source_file_info = get_file_info(file_path, source_dir_path) if source_exists else {}
        target_file_info = get_file_info(file_path, target_dir_path) if target_exists else {}
        
        # If file doesn't exist, use default information
        if not source_exists:
            source_file_info = get_file_info(file_path, "")
        if not target_exists:
            target_file_info = get_file_info(file_path, "")
        
        # Write file basic information
        status = write_file_info(ws, row_num, file_path, source_file_info, source_exists, target_exists, status_fills)
        
        # Write file sizes
        write_file_sizes(ws, row_num, source_file_info, target_file_info)
        
        # Check Markdown syntax consistency
        markdown_consistency = ""
        if source_exists and target_exists and source_file_info.get('extension') == ".md":
            try:
                source_full_path = os.path.join(source_dir_path, file_path)
                target_full_path = os.path.join(target_dir_path, file_path)
                
                source_content = read_file_content(source_full_path)
                target_content = read_file_content(target_full_path)
                
                if source_content is not None and target_content is not None:
                    # Build Markdown syntax tree and compare
                    markdown_consistency = compare_markdown_syntax_trees(source_content, target_content, file_path)
                else:
                    markdown_consistency = "File read failed"
            except Exception as e:
                markdown_consistency = f"Check error: {str(e)}"
        elif source_exists and target_exists and source_file_info.get('extension') != ".md":
            markdown_consistency = "Non-Markdown file"
        
        # Write Markdown consistency check results
        write_markdown_consistency(ws, row_num, markdown_consistency)
        
        # Write formula column
        write_formula_text(ws, row_num, file_path, 
                          source_dir=os.path.basename(source_dir_path), 
                          target_dir=os.path.basename(target_dir_path))
        
        row_num += 1
        print(f"Processed: {file_path} - {status}")
        # Force flush output buffer to ensure characters are displayed immediately
        sys.stdout.flush()

    # Adjust column widths
    adjust_column_widths(ws)
    
    # Save Excel file
    save_success = save_workbook(wb, output_file_path)
    
    if save_success:
        # Print statistics results
        print_statistics(ws, row_num)
    
    # Force flush output buffer to ensure characters are displayed immediately
    sys.stdout.flush()


if __name__ == "__main__":
    # When run directly, provide usage information
    print("This module is designed to be imported and used by docs_consistency_checker.py")
    print("Usage: from main import main")
    print("       main(source_dir_path='path/to/source', target_dir_path='path/to/target')")