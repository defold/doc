#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Document Consistency Checker
Uses modules in the scripts/modules directory to implement document consistency checking functionality
"""

import os
import sys
import argparse

# Import modules
from modules.main import main
from modules.file_handler import setup_console_encoding
from modules.markdown_handler import compare_markdown_syntax_trees
from modules.file_handler import read_file_content


def run_docs_consistency_check(source_dir=None, target_dir=None, output_file=None, specific_file=None, source_file=None, target_file=None):
    """
    Run document consistency check between two language directories
    
    Parameters:
        source_dir: Source document directory path
        target_dir: Target document directory path
        output_file: Output Excel file path
        specific_file: Specific file path to check (relative to docs directory)
        source_file: Specified source version file path
        target_file: Specified target version file path
    """
    # Set console encoding to resolve character display issues
    setup_console_encoding()
    
    # Set default directories
    if source_dir is None:
        source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "source")
    
    if target_dir is None:
        target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "target")
    
    if output_file is None:
        output_file = "docs_structure_comparison.xlsx"
    
    # If specific source and target file paths are specified, use these paths
    if source_file and target_file:
        print(f"Checking files: Source version {source_file}, Target version {target_file}")
        
        # Check if files exist
        if not os.path.exists(source_file):
            print(f"Error: Source file does not exist: {source_file}")
            return
        
        if not os.path.exists(target_file):
            print(f"Error: Target file does not exist: {target_file}")
            return
        
        # Read file contents
        source_content = read_file_content(source_file)
        target_content = read_file_content(target_file)
        
        if source_content is None:
            print(f"Error: Unable to read source file: {source_file}")
            return
        
        if target_content is None:
            print(f"Error: Unable to read target file: {target_file}")
            return
        
        # Check if they are Markdown files
        if not (source_file.endswith('.md') and target_file.endswith('.md')):
            print(f"Warning: Files are not Markdown files, skipping syntax tree comparison")
            return
        
        # Compare Markdown syntax trees
        print(f"Comparing Markdown syntax trees of files...")
        inconsistencies = compare_markdown_syntax_trees(source_content, target_content, os.path.basename(source_file))
        
        # Output results
        if inconsistencies and inconsistencies != "Consistent":
            # Check if it's a return value from syntax tree comparison error
            if inconsistencies.startswith("Syntax tree comparison error:"):
                print(inconsistencies)
            else:
                # Split the inconsistency information separated by semicolons into a list, but preserve special separator |ERROR_SEPARATOR|
                # First check if there is [ERROR_COUNT:1] tag
                if "[ERROR_COUNT:1]" in inconsistencies:
                    # If there is a tag, add the entire error as an element to the list
                    issues = [inconsistencies]
                else:
                    # If no tag, split normally, supporting both semicolon and newline as separators
                    # Replace all newlines with semicolon+space, then split uniformly
                    temp_inconsistencies = inconsistencies.replace("\n", "; ")
                    issues = temp_inconsistencies.split("; ")
                
                # Calculate actual error count, considering special tag [ERROR_COUNT:1]
                error_count = 0
                formatted_issues = []
                
                for issue in issues:
                    # Check if there is an error count tag
                    if "[ERROR_COUNT:1]" in issue:
                        error_count += 1
                        # Remove tag and replace newlines with semicolons, then add to formatted issues list
                        formatted_issue = issue.replace("[ERROR_COUNT:1]", "").replace("\n", "; ")
                        formatted_issues.append(formatted_issue)
                    else:
                        # If no tag, check if it's a sub-error of a heading node (already counted error)
                        # Check if the previous formatted issue contains "heading node" and "errors under:"
                        is_sub_error = False
                        for prev_issue in formatted_issues:
                            if "heading node" in prev_issue and "errors under:" in prev_issue:
                                is_sub_error = True
                                break
                        
                        if not is_sub_error:
                            error_count += 1
                            # Ensure all newlines in issues are replaced with semicolons
                            formatted_issue = issue.replace("\n", "; ")
                            formatted_issues.append(formatted_issue)
                        else:
                            # Ensure all newlines in issues are replaced with semicolons
                            formatted_issue = issue.replace("\n", "; ")
                            formatted_issues.append(formatted_issue)
                
                print(f"Found {error_count} inconsistency issues:")
                for i, issue in enumerate(formatted_issues, 1):
                    print(f"{i}. {issue}")
        else:
            print("No inconsistency issues found, document structure is consistent")
    # If a specific file is specified, only check that file
    elif specific_file:
        print(f"Checking specific file: {specific_file}")
        
        # Build complete file paths
        source_file_path = os.path.join(source_dir, specific_file)
        target_file_path = os.path.join(target_dir, specific_file)
        
        # Check if files exist
        if not os.path.exists(source_file_path):
            print(f"Error: Source file does not exist: {source_file_path}")
            return
        
        if not os.path.exists(target_file_path):
            print(f"Error: Target file does not exist: {target_file_path}")
            return
        
        # Read file contents
        source_content = read_file_content(source_file_path)
        target_content = read_file_content(target_file_path)
        
        if source_content is None:
            print(f"Error: Unable to read source file: {source_file_path}")
            return
        
        if target_content is None:
            print(f"Error: Unable to read target file: {target_file_path}")
            return
        
        # Check if it's a Markdown file
        if not specific_file.endswith('.md'):
            print(f"Warning: File {specific_file} is not a Markdown file, skipping syntax tree comparison")
            return
        
        # Compare Markdown syntax trees
        print(f"Comparing Markdown syntax trees of {specific_file}...")
        inconsistencies = compare_markdown_syntax_trees(source_content, target_content, specific_file)
        
        # Output results
        if inconsistencies and inconsistencies != "Consistent":
            # Check if it's a return value from syntax tree comparison error
            if inconsistencies.startswith("Syntax tree comparison error:"):
                print(inconsistencies)
            else:
                # Split the inconsistency information separated by semicolons into a list, but preserve special separator |ERROR_SEPARATOR|
                # First check if there is [ERROR_COUNT:1] tag
                if "[ERROR_COUNT:1]" in inconsistencies:
                    # If there is a tag, add the entire error as an element to the list
                    issues = [inconsistencies]
                else:
                    # If no tag, split normally, supporting both semicolon and newline as separators
                    # Replace all newlines with semicolon+space, then split uniformly
                    temp_inconsistencies = inconsistencies.replace("\n", "; ")
                    issues = temp_inconsistencies.split("; ")
                
                # Calculate actual error count, considering special tag [ERROR_COUNT:1]
                error_count = 0
                formatted_issues = []
                
                for issue in issues:
                    # Check if there is an error count tag
                    if "[ERROR_COUNT:1]" in issue:
                        error_count += 1
                        # Remove tag and replace newlines with semicolons, then add to formatted issues list
                        formatted_issue = issue.replace("[ERROR_COUNT:1]", "").replace("\n", "; ")
                        formatted_issues.append(formatted_issue)
                    else:
                        # If no tag, check if it's a sub-error of a heading node (already counted error)
                        # Check if the previous formatted issue contains "heading node" and "errors under:"
                        is_sub_error = False
                        for prev_issue in formatted_issues:
                            if "heading node" in prev_issue and "errors under:" in prev_issue:
                                is_sub_error = True
                                break
                        
                        if not is_sub_error:
                            error_count += 1
                            # Ensure all newlines in issues are replaced with semicolons
                            formatted_issue = issue.replace("\n", "; ")
                            formatted_issues.append(formatted_issue)
                        else:
                            # Ensure all newlines in issues are replaced with semicolons
                            formatted_issue = issue.replace("\n", "; ")
                            formatted_issues.append(formatted_issue)
                
                print(f"Found {error_count} inconsistency issues:")
                for i, issue in enumerate(formatted_issues, 1):
                    print(f"{i}. {issue}")
        else:
            print("No inconsistency issues found, document structure is consistent")
    else:
        # Run main function, passing parameters
        main(source_dir_path=source_dir, target_dir_path=target_dir, output_file_path=output_file)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Document Consistency Checker")
    parser.add_argument("--file", help="Specify the specific file path to check (relative to docs directory)")
    parser.add_argument("--source-dir", help="Source document directory path")
    parser.add_argument("--target-dir", help="Target document directory path")
    parser.add_argument("--output", help="Output Excel file path")
    parser.add_argument("--source-file", help="Specify source version file path")
    parser.add_argument("--target-file", help="Specify target version file path")
    
    args = parser.parse_args()
    
    print("Starting document consistency check...")
    run_docs_consistency_check(
        source_dir=args.source_dir,
        target_dir=args.target_dir,
        output_file=args.output,
        specific_file=args.file,
        source_file=args.source_file,
        target_file=args.target_file
    )
    print("Document consistency check completed!")