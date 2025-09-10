#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档一致性检查器
使用 scripts2/modules 目录下的模块实现文档一致性检查功能
"""

import os
import sys
import argparse

# 导入模块
from modules.main import main
from modules.file_handler import setup_console_encoding
from modules.markdown_handler import compare_markdown_syntax_trees
from modules.file_handler import read_file_content


def run_docs_consistency_check(en_dir=None, zh_dir=None, output_file=None, specific_file=None, en_file=None, zh_file=None):
    """
    运行文档一致性检查
    
    参数:
        en_dir: 英文文档目录路径
        zh_dir: 中文文档目录路径
        output_file: 输出Excel文件路径
        specific_file: 特定要检查的文件路径（相对于docs目录）
        en_file: 指定英文版文件路径
        zh_file: 指定中文版文件路径
    """
    # 设置控制台编码，解决中文乱码问题
    setup_console_encoding()
    
    # 设置默认目录
    if en_dir is None:
        en_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "en")
    
    if zh_dir is None:
        zh_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "zh")
    
    if output_file is None:
        output_file = "docs_structure_comparison.xlsx"
    
    # 如果指定了具体的英文和中文文件路径，使用这些路径
    if en_file and zh_file:
        print(f"正在检查文件: 英文版 {en_file}, 中文版 {zh_file}")
        
        # 检查文件是否存在
        if not os.path.exists(en_file):
            print(f"错误: 英文文件不存在: {en_file}")
            return
        
        if not os.path.exists(zh_file):
            print(f"错误: 中文文件不存在: {zh_file}")
            return
        
        # 读取文件内容
        en_content = read_file_content(en_file)
        zh_content = read_file_content(zh_file)
        
        if en_content is None:
            print(f"错误: 无法读取英文文件: {en_file}")
            return
        
        if zh_content is None:
            print(f"错误: 无法读取中文文件: {zh_file}")
            return
        
        # 检查是否为Markdown文件
        if not (en_file.endswith('.md') and zh_file.endswith('.md')):
            print(f"警告: 文件不是Markdown文件，跳过语法树比较")
            return
        
        # 比较Markdown语法树
        print(f"正在比较文件的Markdown语法树...")
        inconsistencies = compare_markdown_syntax_trees(en_content, zh_content, os.path.basename(en_file))
        
        # 输出结果
        if inconsistencies and inconsistencies != "一致":
            # 检查是否是语法树比较出错的返回值
            if inconsistencies.startswith("语法树比较出错:"):
                print(inconsistencies)
            else:
                # 将分号分隔的不一致信息分割成列表，但保留特殊分隔符 |ERROR_SEPARATOR|
                # 首先检查是否有 [ERROR_COUNT:1] 标记
                if "[ERROR_COUNT:1]" in inconsistencies:
                    # 如果有标记，将整个错误作为一个元素添加到列表中
                    issues = [inconsistencies]
                else:
                    # 如果没有标记，正常分割，同时支持分号和换行符作为分隔符
                    # 将所有换行符替换为分号+空格，然后统一分割
                    temp_inconsistencies = inconsistencies.replace("\n", "; ")
                    issues = temp_inconsistencies.split("; ")
                
                # 计算实际错误数量，考虑特殊标记 [ERROR_COUNT:1]
                error_count = 0
                formatted_issues = []
                
                for issue in issues:
                    # 检查是否有错误计数标记
                    if "[ERROR_COUNT:1]" in issue:
                        error_count += 1
                        # 移除标记并将换行符替换为分号，然后添加到格式化问题列表
                        formatted_issue = issue.replace("[ERROR_COUNT:1]", "").replace("\n", "; ")
                        formatted_issues.append(formatted_issue)
                    else:
                        # 如果没有标记，检查是否是标题节点的子错误（已经被计数的错误）
                        # 检查前一个格式化的问题是否包含"标题节点"和"下的错误:"
                        is_sub_error = False
                        for prev_issue in formatted_issues:
                            if "标题节点" in prev_issue and "下的错误:" in prev_issue:
                                is_sub_error = True
                                break
                        
                        if not is_sub_error:
                            error_count += 1
                            # 确保所有问题中的换行符都被替换为分号
                            formatted_issue = issue.replace("\n", "; ")
                            formatted_issues.append(formatted_issue)
                        else:
                            # 确保所有问题中的换行符都被替换为分号
                            formatted_issue = issue.replace("\n", "; ")
                            formatted_issues.append(formatted_issue)
                
                print(f"发现 {error_count} 个不一致问题:")
                for i, issue in enumerate(formatted_issues, 1):
                    print(f"{i}. {issue}")
        else:
            print("未发现不一致问题，文档结构一致")
    # 如果指定了特定文件，只检查该文件
    elif specific_file:
        print(f"正在检查特定文件: {specific_file}")
        
        # 构建完整文件路径
        en_file_path = os.path.join(en_dir, specific_file)
        zh_file_path = os.path.join(zh_dir, specific_file)
        
        # 检查文件是否存在
        if not os.path.exists(en_file_path):
            print(f"错误: 英文文件不存在: {en_file_path}")
            return
        
        if not os.path.exists(zh_file_path):
            print(f"错误: 中文文件不存在: {zh_file_path}")
            return
        
        # 读取文件内容
        en_content = read_file_content(en_file_path)
        zh_content = read_file_content(zh_file_path)
        
        if en_content is None:
            print(f"错误: 无法读取英文文件: {en_file_path}")
            return
        
        if zh_content is None:
            print(f"错误: 无法读取中文文件: {zh_file_path}")
            return
        
        # 检查是否为Markdown文件
        if not specific_file.endswith('.md'):
            print(f"警告: 文件 {specific_file} 不是Markdown文件，跳过语法树比较")
            return
        
        # 比较Markdown语法树
        print(f"正在比较 {specific_file} 的Markdown语法树...")
        inconsistencies = compare_markdown_syntax_trees(en_content, zh_content, specific_file)
        
        # 输出结果
        if inconsistencies and inconsistencies != "一致":
            # 检查是否是语法树比较出错的返回值
            if inconsistencies.startswith("语法树比较出错:"):
                print(inconsistencies)
            else:
                # 将分号分隔的不一致信息分割成列表，但保留特殊分隔符 |ERROR_SEPARATOR|
                # 首先检查是否有 [ERROR_COUNT:1] 标记
                if "[ERROR_COUNT:1]" in inconsistencies:
                    # 如果有标记，将整个错误作为一个元素添加到列表中
                    issues = [inconsistencies]
                else:
                    # 如果没有标记，正常分割，同时支持分号和换行符作为分隔符
                    # 将所有换行符替换为分号+空格，然后统一分割
                    temp_inconsistencies = inconsistencies.replace("\n", "; ")
                    issues = temp_inconsistencies.split("; ")
                
                # 计算实际错误数量，考虑特殊标记 [ERROR_COUNT:1]
                error_count = 0
                formatted_issues = []
                
                for issue in issues:
                    # 检查是否有错误计数标记
                    if "[ERROR_COUNT:1]" in issue:
                        error_count += 1
                        # 移除标记并将换行符替换为分号，然后添加到格式化问题列表
                        formatted_issue = issue.replace("[ERROR_COUNT:1]", "").replace("\n", "; ")
                        formatted_issues.append(formatted_issue)
                    else:
                        # 如果没有标记，检查是否是标题节点的子错误（已经被计数的错误）
                        # 检查前一个格式化的问题是否包含"标题节点"和"下的错误:"
                        is_sub_error = False
                        for prev_issue in formatted_issues:
                            if "标题节点" in prev_issue and "下的错误:" in prev_issue:
                                is_sub_error = True
                                break
                        
                        if not is_sub_error:
                            error_count += 1
                            # 确保所有问题中的换行符都被替换为分号
                            formatted_issue = issue.replace("\n", "; ")
                            formatted_issues.append(formatted_issue)
                        else:
                            # 确保所有问题中的换行符都被替换为分号
                            formatted_issue = issue.replace("\n", "; ")
                            formatted_issues.append(formatted_issue)
                
                print(f"发现 {error_count} 个不一致问题:")
                for i, issue in enumerate(formatted_issues, 1):
                    print(f"{i}. {issue}")
        else:
            print("未发现不一致问题，文档结构一致")
    else:
        # 运行主函数，传递参数
        main(en_dir=en_dir, zh_dir=zh_dir, output_file=output_file)


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="文档一致性检查器")
    parser.add_argument("--file", help="指定要检查的特定文件路径（相对于docs目录）")
    parser.add_argument("--en-dir", help="英文文档目录路径")
    parser.add_argument("--zh-dir", help="中文文档目录路径")
    parser.add_argument("--output", help="输出Excel文件路径")
    parser.add_argument("--en-file", help="指定英文版文件路径")
    parser.add_argument("--zh-file", help="指定中文版文件路径")
    
    args = parser.parse_args()
    
    print("开始运行文档一致性检查...")
    run_docs_consistency_check(
        en_dir=args.en_dir,
        zh_dir=args.zh_dir,
        output_file=args.output,
        specific_file=args.file,
        en_file=args.en_file,
        zh_file=args.zh_file
    )
    print("文档一致性检查完成！")