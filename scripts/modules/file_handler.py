import os
import sys


def collect_files(directory):
    """
    Collect all file paths under the specified directory
    
    Parameters:
        directory: Directory path to traverse
        
    Returns:
        set: Set containing all file relative paths
    """
    files = set()
    print(f"Collecting files in {directory}...")
    
    for root, dirs, files_in_dir in os.walk(directory):
        for file in files_in_dir:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, directory)
            files.add(rel_path)
    
    return files


def get_file_info(file_path, base_dir):
    """
    Get file information
    
    Parameters:
        file_path: File relative path
        base_dir: File base directory
        
    Returns:
        dict: Dictionary containing file information
    """
    # Get file extension
    file_ext = os.path.splitext(file_path)[1].lower()
    if not file_ext:
        file_ext = "[No Extension]"
    
    # Get top level directory
    path_parts = file_path.split(os.sep)
    if len(path_parts) > 1:
        top_dir = path_parts[0]
    else:
        top_dir = "[Root Directory]"
    
    # Get file size
    file_size = ""
    full_path = os.path.join(base_dir, file_path)
    if os.path.exists(full_path):
        file_size = round(os.path.getsize(full_path) / 1024, 2)
    
    return {
        'extension': file_ext,
        'top_dir': top_dir,
        'size': file_size
    }


def read_file_content(file_path):
    """
    Read file content
    
    Parameters:
        file_path: File path
        
    Returns:
        str: File content, returns None if reading fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return None


def setup_console_encoding():
    """
    Set console encoding to resolve Chinese character display issues
    """
    if sys.platform == "win32":
        # Set console encoding to UTF-8 on Windows systems
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        
    # Force flush output buffer to ensure Chinese characters are displayed immediately
    sys.stdout.flush()