import re
import sys
from collections import defaultdict

from .file_handler import setup_console_encoding


def compare_markdown_syntax_trees(source_content, target_content, file_path):
    """
    Build Markdown syntax trees and compare the syntax structure of two documents,
    identifying inconsistent positions.
    
    Args:
        source_content (str): Source version Markdown content
        target_content (str): Target version Markdown content
        file_path (str): File path for error messages
        
    Returns:
        str: Consistency check result, "Consistent" if consistent, otherwise error message
    """
    # Build syntax tree for source version
    source_tree = build_markdown_syntax_tree(source_content)
    
    # Build syntax tree for target version
    target_tree = build_markdown_syntax_tree(target_content)
    
    # Compare syntax trees
    differences = compare_syntax_trees(source_tree, target_tree, file_path)
    
    if differences:
        return f"Inconsistent: {differences}"
    else:
        return "Consistent"


def build_markdown_syntax_tree(content):
    """
    Build a syntax tree for a Markdown document, with each token as a node.
    
    Args:
        content (str): Markdown document content
        
    Returns:
        list: Syntax tree represented as a list of nodes
    """
    if not content:
        return []
    
    # Split document into lines
    lines = content.split('\n')
    
    # Initialize syntax tree
    tree = []
    
    # Process each line
    for line_num, line in enumerate(lines, 1):
        # Skip empty lines
        if not line.strip():
            continue
            
        # Check if it's a header
        header_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if header_match:
            level = len(header_match.group(1))
            text = header_match.group(2)
            tree.append({
                'type': 'header',
                'level': level,
                'text': text,
                'line': line_num
            })
            continue
            
        # Check if it's a list item
        list_match = re.match(r'^(\s*)([*+-]|\d+\.)\s+(.*)', line)
        if list_match:
            indent = len(list_match.group(1))
            marker = list_match.group(2)
            text = list_match.group(3)
            tree.append({
                'type': 'list',
                'indent': indent,
                'marker': marker,
                'text': text,
                'line': line_num
            })
            continue
            
        # Check if it's a code block
        if line.strip().startswith('```'):
            tree.append({
                'type': 'code_block',
                'text': line.strip(),
                'line': line_num
            })
            continue
            
        # Check if it's a blockquote
        if line.strip().startswith('>'):
            tree.append({
                'type': 'blockquote',
                'text': line.strip(),
                'line': line_num
            })
            continue
            
        # Check if it's a horizontal rule
        if line.strip() in ['---', '***', '___']:
            tree.append({
                'type': 'hr',
                'line': line_num
            })
            continue
            
        # Check for inline elements
        # Bold text
        bold_matches = re.finditer(r'\*\*(.*?)\*\*', line)
        for match in bold_matches:
            tree.append({
                'type': 'bold',
                'text': match.group(1),
                'line': line_num
            })
            
        # Italic text
        italic_matches = re.finditer(r'\*(.*?)\*', line)
        for match in italic_matches:
            tree.append({
                'type': 'italic',
                'text': match.group(1),
                'line': line_num
            })
            
        # Inline code
        code_matches = re.finditer(r'`(.*?)`', line)
        for match in code_matches:
            tree.append({
                'type': 'inline_code',
                'text': match.group(1),
                'line': line_num
            })
            
        # Links
        link_matches = re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', line)
        for match in link_matches:
            tree.append({
                'type': 'link',
                'text': match.group(1),
                'url': match.group(2),
                'line': line_num
            })
            
        # Images
        img_matches = re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)', line)
        for match in img_matches:
            tree.append({
                'type': 'image',
                'alt': match.group(1),
                'url': match.group(2),
                'line': line_num
            })
    
    return tree


def compare_syntax_trees(source_tree, target_tree, file_path):
    """
    Compare two Markdown syntax trees, locate inconsistent positions by checking tree structure.
    
    Args:
        source_tree (list): Source version syntax tree
        target_tree (list): Target version syntax tree
        file_path (str): File path for error messages
        
    Returns:
        str: Error message describing differences, empty string if consistent
    """
    # Set console encoding to resolve character display issues
    setup_console_encoding()
    
    # Check if tree lengths are consistent
    if len(source_tree) != len(target_tree):
        return f"Number of elements inconsistent (Source: {len(source_tree)}, Target: {len(target_tree)})"
    
    # Check each element
    for i, (source_node, target_node) in enumerate(zip(source_tree, target_tree)):
        # Check if node types are consistent
        if source_node['type'] != target_node['type']:
            return f"Element type inconsistent at position {i+1} (Source: {source_node['type']}, Target: {target_node['type']})"
        
        # Check specific attributes based on node type
        if source_node['type'] == 'header':
            if source_node['level'] != target_node['level']:
                return f"Header level inconsistent at line {source_node['line']} (Source: {source_node['level']}, Target: {target_node['level']})"
                
        elif source_node['type'] == 'list':
            if source_node['indent'] != target_node['indent']:
                return f"List indent inconsistent at line {source_node['line']} (Source: {source_node['indent']}, Target: {target_node['indent']})"
            if source_node['marker'] != target_node['marker']:
                return f"List marker inconsistent at line {source_node['line']} (Source: {source_node['marker']}, Target: {target_node['marker']})"
                
        elif source_node['type'] == 'code_block':
            # For code blocks, we only check if both are code blocks, not content
            pass
            
        elif source_node['type'] == 'blockquote':
            # For blockquotes, we only check if both are blockquotes, not content
            pass
            
        elif source_node['type'] == 'hr':
            # For horizontal rules, we only check if both are horizontal rules
            pass
            
        elif source_node['type'] in ['bold', 'italic', 'inline_code']:
            # For inline elements, we only check if both are the same type
            pass
            
        elif source_node['type'] == 'link':
            # For links, check if URLs are consistent
            if source_node['url'] != target_node['url']:
                return f"Link URL inconsistent at line {source_node['line']} (Source: {source_node['url']}, Target: {target_node['url']})"
                
        elif source_node['type'] == 'image':
            # For images, check if URLs are consistent
            if source_node['url'] != target_node['url']:
                return f"Image URL inconsistent at line {source_node['line']} (Source: {source_node['url']}, Target: {target_node['url']})"
    
    # If no differences found, return empty string
    return ""


def split_document_by_headers(content):
    """
    Split document into multiple parts based on headers.
    
    Args:
        content (str): Markdown document content
        
    Returns:
        dict: Dictionary with headers as keys and content as values
    """
    if not content:
        return {}
    
    # Split document into lines
    lines = content.split('\n')
    
    # Initialize result dictionary
    sections = defaultdict(list)
    
    # Current section header
    current_header = "Introduction"
    
    # Process each line
    for line in lines:
        # Check if it's a header
        header_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if header_match:
            # Update current section header
            current_header = header_match.group(2)
        
        # Add line to current section
        sections[current_header].append(line)
    
    # Convert lists to strings
    for header, lines in sections.items():
        sections[header] = '\n'.join(lines)
    
    return sections


def compare_section_content(source_sections, target_sections):
    """
    Compare content under two header nodes.
    
    Args:
        source_sections (dict): Source version document sections
        target_sections (dict): Target version document sections
        
    Returns:
        dict: Dictionary with comparison results for each section
    """
    results = {}
    
    # Get all unique section headers
    all_headers = set(source_sections.keys()).union(set(target_sections.keys()))
    
    # Compare each section
    for header in all_headers:
        source_exists = header in source_sections
        target_exists = header in target_sections
        
        if source_exists and target_exists:
            # Both sections exist, check content structure
            source_tree = build_markdown_syntax_tree(source_sections[header])
            target_tree = build_markdown_syntax_tree(target_sections[header])
            
            differences = compare_syntax_trees(source_tree, target_tree, header)
            
            if differences:
                results[header] = f"Inconsistent: {differences}"
            else:
                results[header] = "Consistent"
                
        elif source_exists:
            # Only source version exists
            results[header] = "Source Only"
            
        elif target_exists:
            # Only target version exists
            results[header] = "Target Only"
    
    return results