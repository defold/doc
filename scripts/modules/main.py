import os
import sys

from .file_handler import collect_files, get_file_info, read_file_content, setup_console_encoding
from .excel_handler import create_workbook, get_status_fills, write_file_info, write_file_sizes, write_markdown_consistency, write_formula_text, adjust_column_widths, save_workbook, print_statistics
from .markdown_handler import compare_markdown_syntax_trees


# 默认目录和输出文件路径
en_dir = "g:\\temp\\defold_doc\\docs\\en"
zh_dir = "g:\\temp\\defold_doc\\docs\\zh"
output_file = "docs_structure_comparison_updated.xlsx"


def main(en_dir=None, zh_dir=None, output_file=None):
    # 使用传入的参数或默认值
    if en_dir is None:
        en_dir = globals().get('en_dir', "g:\\temp\\defold_doc\\docs\\en")
    if zh_dir is None:
        zh_dir = globals().get('zh_dir', "g:\\temp\\defold_doc\\docs\\zh")
    if output_file is None:
        output_file = globals().get('output_file', "docs_structure_comparison_updated.xlsx")
        
    # 设置控制台编码，解决中文乱码问题
    setup_console_encoding()

    # 创建Excel工作簿
    wb, ws = create_workbook()
    
    # 获取状态填充颜色
    status_fills = get_status_fills()

    # 行计数器
    row_num = 2
    
    # 收集所有文件路径
    en_files = collect_files(en_dir)
    zh_files = collect_files(zh_dir)
    
    # 获取所有唯一的文件路径
    all_files = en_files.union(zh_files)
    
    # 对比文件结构
    print("正在对比文件结构...")
    for file_path in sorted(all_files):
        en_exists = file_path in en_files
        zh_exists = file_path in zh_files
        
        # 获取文件信息
        en_file_info = get_file_info(file_path, en_dir) if en_exists else {}
        zh_file_info = get_file_info(file_path, zh_dir) if zh_exists else {}
        
        # 如果文件不存在，使用默认信息
        if not en_exists:
            en_file_info = get_file_info(file_path, "")
        if not zh_exists:
            zh_file_info = get_file_info(file_path, "")
        
        # 写入文件基本信息
        status = write_file_info(ws, row_num, file_path, en_file_info, en_exists, zh_exists, status_fills)
        
        # 写入文件大小
        write_file_sizes(ws, row_num, en_file_info, zh_file_info)
        
        # 检查Markdown语法标记一致性
        markdown_consistency = ""
        if en_exists and zh_exists and en_file_info.get('extension') == ".md":
            try:
                en_full_path = os.path.join(en_dir, file_path)
                zh_full_path = os.path.join(zh_dir, file_path)
                
                en_content = read_file_content(en_full_path)
                zh_content = read_file_content(zh_full_path)
                
                if en_content is not None and zh_content is not None:
                    # 构建Markdown语法树并比较
                    markdown_consistency = compare_markdown_syntax_trees(en_content, zh_content, file_path)
                else:
                    markdown_consistency = "文件读取失败"
            except Exception as e:
                markdown_consistency = f"检查出错: {str(e)}"
        elif en_exists and zh_exists and en_file_info.get('extension') != ".md":
            markdown_consistency = "非Markdown文件"
        
        # 写入Markdown一致性检查结果
        write_markdown_consistency(ws, row_num, markdown_consistency)
        
        # 写入公式列
        write_formula_text(ws, row_num, file_path)
        
        row_num += 1
        print(f"已处理: {file_path} - {status}")
        # 强制刷新输出缓冲区，确保中文立即显示
        sys.stdout.flush()

    # 调整列宽
    adjust_column_widths(ws)
    
    # 保存Excel文件
    save_success = save_workbook(wb, output_file)
    
    if save_success:
        # 打印统计结果
        print_statistics(ws, row_num)
    
    # 强制刷新输出缓冲区，确保中文立即显示
    sys.stdout.flush()


if __name__ == "__main__":
    main()