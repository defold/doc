import os
import sys


def collect_files(directory):
    """
    收集指定目录下的所有文件路径
    
    参数:
        directory: 要遍历的目录路径
        
    返回:
        set: 包含所有文件相对路径的集合
    """
    files = set()
    print(f"正在收集 {directory} 中的文件...")
    
    for root, dirs, files_in_dir in os.walk(directory):
        for file in files_in_dir:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, directory)
            files.add(rel_path)
    
    return files


def get_file_info(file_path, base_dir):
    """
    获取文件信息
    
    参数:
        file_path: 文件相对路径
        base_dir: 文件基础目录
        
    返回:
        dict: 包含文件信息的字典
    """
    # 获取文件后缀
    file_ext = os.path.splitext(file_path)[1].lower()
    if not file_ext:
        file_ext = "[无后缀]"
    
    # 获取最顶级目录
    path_parts = file_path.split(os.sep)
    if len(path_parts) > 1:
        top_dir = path_parts[0]
    else:
        top_dir = "[根目录]"
    
    # 获取文件大小
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
    读取文件内容
    
    参数:
        file_path: 文件路径
        
    返回:
        str: 文件内容，如果读取失败则返回None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {str(e)}")
        return None


def setup_console_encoding():
    """
    设置控制台编码，解决中文乱码问题
    """
    if sys.platform == "win32":
        # Windows系统下设置控制台编码为UTF-8
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        
    # 强制刷新输出缓冲区，确保中文立即显示
    sys.stdout.flush()