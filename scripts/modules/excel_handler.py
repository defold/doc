import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill


def create_workbook():
    """
    创建Excel工作簿并设置基本格式
    
    返回:
        tuple: (工作簿对象, 工作表对象)
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Docs Structure Comparison"
    
    # 设置表头
    headers = ["文件路径", "文件后缀", "最顶级目录", "英文版存在", "中文版存在", 
               "状态", "英文版文件大小(KB)", "中文版文件大小(KB)", 
               "Markdown语法标记一致性", "公式"]
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal="center")
    
    return wb, ws


def get_status_fills():
    """
    获取不同状态对应的填充颜色
    
    返回:
        dict: 包含不同状态填充颜色的字典
    """
    return {
        'consistent': PatternFill(start_color='FFC6EFCE', end_color='FFC6EFCE', fill_type='solid'),  # 绿色
        'en_only': PatternFill(start_color='FFFFC7CE', end_color='FFFFC7CE', fill_type='solid'),    # 红色
        'zh_only': PatternFill(start_color='FFFFFF00', end_color='FFFFFF00', fill_type='solid')     # 黄色
    }


def write_file_info(ws, row_num, file_path, file_info, en_exists, zh_exists, status_fills):
    """
    将文件信息写入工作表
    
    参数:
        ws: 工作表对象
        row_num: 行号
        file_path: 文件路径
        file_info: 文件信息字典
        en_exists: 英文版是否存在
        zh_exists: 中文版是否存在
        status_fills: 状态填充颜色字典
        
    返回:
        str: 文件状态
    """
    # 确定状态
    if en_exists and zh_exists:
        status = "一致"
        status_fill = status_fills['consistent']
    elif en_exists and not zh_exists:
        status = "仅英文版存在"
        status_fill = status_fills['en_only']
    elif not en_exists and zh_exists:
        status = "仅中文版存在"
        status_fill = status_fills['zh_only']
    else:
        status = "不存在"
        status_fill = None
    
    # 写入基本信息
    ws.cell(row=row_num, column=1, value=file_path)
    ws.cell(row=row_num, column=2, value=file_info['extension'])
    ws.cell(row=row_num, column=3, value=file_info['top_dir'])
    ws.cell(row=row_num, column=4, value="是" if en_exists else "否")
    ws.cell(row=row_num, column=5, value="是" if zh_exists else "否")
    
    # 设置状态单元格
    status_cell = ws.cell(row=row_num, column=6, value=status)
    if status_fill:
        status_cell.fill = status_fill
    
    return status


def write_file_sizes(ws, row_num, en_file_info, zh_file_info):
    """
    写入文件大小信息
    
    参数:
        ws: 工作表对象
        row_num: 行号
        en_file_info: 英文版文件信息
        zh_file_info: 中文版文件信息
    """
    ws.cell(row=row_num, column=7, value=en_file_info.get('size', ''))
    ws.cell(row=row_num, column=8, value=zh_file_info.get('size', ''))


def write_markdown_consistency(ws, row_num, consistency_result):
    """
    写入Markdown语法标记一致性结果
    
    参数:
        ws: 工作表对象
        row_num: 行号
        consistency_result: 一致性检查结果
    """
    ws.cell(row=row_num, column=9, value=consistency_result)


def write_formula_text(ws, row_num, file_path):
    """
    写入公式列
    
    参数:
        ws: 工作表对象
        row_num: 行号
        file_path: 文件路径
    """
    # 根据文件路径生成公式文本
    # formula_text = f"先执行 python scripts2\\docs_consistency_checker.py --en-file docs\\en\\{file_path} --zh-file docs\\zh\\{file_path}，确保文件内容一致。\n"
    formula_text = f"以每个标题为段落，逐段落比对 docs\\en\\{file_path} 和 docs\\zh\\{file_path} ，确保中文版是英文版的完整准确翻译。"
    ws.cell(row=row_num, column=10, value=formula_text)


def adjust_column_widths(ws):
    """
    调整工作表列宽
    
    参数:
        ws: 工作表对象
    """
    ws.column_dimensions['A'].width = 50  # 文件路径
    ws.column_dimensions['B'].width = 10  # 文件后缀
    ws.column_dimensions['C'].width = 15  # 最顶级目录
    ws.column_dimensions['D'].width = 15  # 英文版存在
    ws.column_dimensions['E'].width = 15  # 中文版存在
    ws.column_dimensions['F'].width = 20  # 状态
    ws.column_dimensions['G'].width = 20  # 英文版文件大小
    ws.column_dimensions['H'].width = 20  # 中文版文件大小
    ws.column_dimensions['I'].width = 50  # Markdown语法标记一致性
    ws.column_dimensions['J'].width = 100 # 公式


def save_workbook(wb, output_file):
    """
    保存工作簿到文件
    
    参数:
        wb: 工作簿对象
        output_file: 输出文件路径
        
    返回:
        bool: 保存是否成功
    """
    try:
        print(f"准备保存Excel文件到: {output_file}")
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"创建输出目录: {output_dir}")
        
        # 保存Excel文件
        wb.save(output_file)
        print(f"\n完成！文件结构对比结果已保存到: {output_file}")
        
        # 验证文件是否成功创建
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"Excel文件已成功创建，文件大小: {file_size} 字节")
            return True
        else:
            print("错误：Excel文件未成功创建")
            return False
            
    except Exception as e:
        print(f"保存Excel文件时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def print_statistics(ws, row_num):
    """
    打印统计结果
    
    参数:
        ws: 工作表对象
        row_num: 总行数
    """
    print(f"共对比了 {row_num - 2} 个文件")
    
    # 统计结果
    consistent_count = sum(1 for i in range(2, row_num) if ws.cell(row=i, column=6).value == "一致")
    en_only_count = sum(1 for i in range(2, row_num) if ws.cell(row=i, column=6).value == "仅英文版存在")
    zh_only_count = sum(1 for i in range(2, row_num) if ws.cell(row=i, column=6).value == "仅中文版存在")
    
    print(f"统计结果:")
    print(f"- 两个版本都存在的文件: {consistent_count} 个")
    print(f"- 仅英文版存在的文件: {en_only_count} 个")
    print(f"- 仅中文版存在的文件: {zh_only_count} 个")