import re


def compare_markdown_syntax_trees(en_content, zh_content, file_path):
    """
    构建Markdown语法树并比较两个文档的语法结构，识别不一致的位置
    
    参数:
        en_content: 英文文档内容
        zh_content: 中文文档内容
        file_path: 文件路径，用于错误报告
        
    返回:
        str: 描述不一致位置的字符串，如果没有不一致则返回"一致"
    """
    try:
        # 构建英文文档的语法树
        en_syntax_tree = build_markdown_syntax_tree(en_content)
        # 构建中文文档的语法树
        zh_syntax_tree = build_markdown_syntax_tree(zh_content)
        
        # 比较两个语法树
        inconsistencies = compare_syntax_trees(en_syntax_tree, zh_syntax_tree)
        
        if inconsistencies:
            return "; ".join(inconsistencies)
        else:
            return "一致"
    except Exception as e:
        return f"语法树比较出错: {str(e)}"


def build_markdown_syntax_tree(content):
    """
    构建Markdown文档的语法树，每个标记作为一个节点
    
    参数:
        content: Markdown文档内容
        
    返回:
        dict: 包含各种Markdown标记的语法树，每个标记包含完整的位置和内容信息
    """
    syntax_tree = {
        'headers': [],      # 标题
        'code_blocks': [],  # 代码块
        'inline_codes': [], # 行内代码
        'bolds': [],        # 粗体
        'italics': [],      # 斜体
        'links': [],        # 链接
        'lists': []         # 列表
    }
    
    lines = content.split('\n')
    
    # 提取标题标记 (# ## ### 等)
    for i, line in enumerate(lines):
        header_match = re.match(r'^(#+)\s+(.*)', line)
        if header_match:
            level = len(header_match.group(1))
            text = header_match.group(2).strip()
            syntax_tree['headers'].append({
                'line': i,
                'level': level,
                'text': text,
                'full_match': header_match.group(),
                'start_pos': header_match.start(),
                'end_pos': header_match.end()
            })
    
    # 提取代码块标记 (```)
    # 改进的代码块解析逻辑：区分开始和结束标记
    in_code_block = False
    code_block_start = 0
    code_block_start_pos = 0
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if '```' in stripped_line:
            backtick_pos = line.find('```')
            # 检查```后面是否有内容（语言标识符）
            after_backticks = stripped_line[stripped_line.find('```') + 3:].strip()
            
            if not in_code_block:
                # 当前不在代码块中，这是开始标记
                code_block_start = i
                code_block_start_pos = backtick_pos
                in_code_block = True
            elif after_backticks:  # 有语言标识符，一定是新代码块的开始
                # 先结束当前代码块（假设在前一个```行结束）
                # 找到前一个```行
                prev_end_line = i - 1
                while prev_end_line >= code_block_start and '```' not in lines[prev_end_line].strip():
                    prev_end_line -= 1
                
                if prev_end_line >= code_block_start and '```' in lines[prev_end_line].strip():
                    syntax_tree['code_blocks'].append({
                        'start_line': code_block_start,
                        'end_line': prev_end_line,
                        'start_pos': code_block_start_pos,
                        'end_pos': lines[prev_end_line].find('```'),
                        'start_text': lines[code_block_start].strip(),
                        'end_text': lines[prev_end_line].strip()
                    })
                
                # 开始新的代码块
                code_block_start = i
                code_block_start_pos = backtick_pos
                in_code_block = True
            else:
                # 没有语言标识符，这是结束标记
                syntax_tree['code_blocks'].append({
                    'start_line': code_block_start,
                    'end_line': i,
                    'start_pos': code_block_start_pos,
                    'end_pos': backtick_pos,
                    'start_text': lines[code_block_start].strip(),
                    'end_text': line.strip()
                })
                in_code_block = False
    
    # 提取行内代码标记 (`)
    for i, line in enumerate(lines):
        for match in re.finditer(r'`([^`]+)`', line):
            syntax_tree['inline_codes'].append({
                'line': i,
                'text': match.group(1),  # 只获取内容，不包括反引号
                'full_match': match.group(),
                'start_pos': match.start(),
                'end_pos': match.end()
            })
    
    # 提取粗体标记 (**)
    for i, line in enumerate(lines):
        for match in re.finditer(r'\*\*([^*]+)\*\*', line):
            syntax_tree['bolds'].append({
                'line': i,
                'text': match.group(1),  # 只获取内容，不包括星号
                'full_match': match.group(),
                'start_pos': match.start(),
                'end_pos': match.end()
            })
    
    # 提取斜体标记 (*)
    for i, line in enumerate(lines):
        for match in re.finditer(r'\*([^*]+)\*', line):
            syntax_tree['italics'].append({
                'line': i,
                'text': match.group(1),  # 只获取内容，不包括星号
                'full_match': match.group(),
                'start_pos': match.start(),
                'end_pos': match.end()
            })
    
    # 提取链接标记 [text](url)
    for i, line in enumerate(lines):
        for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', line):
            syntax_tree['links'].append({
                'line': i,
                'text': match.group(1),  # 链接文本
                'url': match.group(2),    # 链接URL
                'full_match': match.group(),
                'start_pos': match.start(),
                'end_pos': match.end()
            })
    
    # 提取列表标记 (-, *, 1.)
    for i, line in enumerate(lines):
        list_match = re.match(r'^\s*([-*]|\d+\.)\s+(.*)', line)
        if list_match:
            syntax_tree['lists'].append({
                'line': i,
                'type': list_match.group(1),
                'text': list_match.group(2).strip(),
                'full_match': list_match.group(),
                'start_pos': list_match.start(),
                'end_pos': list_match.end()
            })
    
    return syntax_tree


def compare_syntax_trees(en_tree, zh_tree):
    """
    比较两个Markdown语法树，通过核对树形结构来定位不一致的位置
    以标题为节点，先检测标题的一致性，如果标题不一致就仅提示标题不一致的错误，
    如果标题节点结构一致时，有多个标题节点内部有错误时，就仅提示第一个标题节点下的所有错误
    
    参数:
        en_tree: 英文文档的语法树
        zh_tree: 中文文档的语法树
        
    返回:
        list: 描述不一致位置的字符串列表，包含详细的差异信息
    """
    inconsistencies = []
    
    # 比较标题
    if len(en_tree['headers']) != len(zh_tree['headers']):
        # 打印所有英文标题
        en_all_headers = [f"行{h['line']}级别{h['level']}:{h['text']}" for h in en_tree['headers']]
        
        # 打印所有中文标题
        zh_all_headers = [f"行{h['line']}级别{h['level']}:{h['text']}" for h in zh_tree['headers']]
        
        # 将标题数量不一致和所有标题信息合并为一个错误，使用特殊标记确保计为1个错误
        header_error = f"[ERROR_COUNT:1]标题数量不一致(英文:{len(en_tree['headers'])}, 中文:{len(zh_tree['headers'])})。所有英文标题: {'; '.join(en_all_headers)}。所有中文标题: {'; '.join(zh_all_headers)}"
        inconsistencies.append(header_error)
        
        # 如果标题不一致，直接返回，不再检查其他元素
        return inconsistencies
    
    # 如果标题数量一致，检查每个标题级别是否一致
    header_mismatch = False
    for i in range(len(en_tree['headers'])):
        if en_tree['headers'][i]['level'] != zh_tree['headers'][i]['level']:
            header_mismatch = True
            break
    
    # 如果标题级别不一致，打印所有标题并返回
    if header_mismatch:
        # 打印所有英文标题
        en_all_headers = [f"行{h['line']}级别{h['level']}:{h['text']}" for h in en_tree['headers']]
        
        # 打印所有中文标题
        zh_all_headers = [f"行{h['line']}级别{h['level']}:{h['text']}" for h in zh_tree['headers']]
        
        # 将标题级别不一致和所有标题信息合并为一个错误，使用特殊标记确保计为1个错误
        header_error = f"[ERROR_COUNT:1]标题级别不一致。所有英文标题: {'; '.join(en_all_headers)}。所有中文标题: {'; '.join(zh_all_headers)}"
        inconsistencies.append(header_error)
        
        return inconsistencies
    
    # 标题结构一致，现在检查每个标题节点下的内容
    # 我们将文档按标题分割成多个部分，然后分别比较每个部分
    en_sections = split_document_by_headers(en_tree)
    zh_sections = split_document_by_headers(zh_tree)
    
    # 找出第一个有错误的标题节点
    first_error_section = None
    for i in range(len(en_sections)):
        section_errors = compare_section_content(en_sections[i], zh_sections[i])
        if section_errors:
            first_error_section = i
            break
    
    # 如果找到有错误的标题节点，只返回该节点的所有错误
    if first_error_section is not None:
        section_errors = compare_section_content(en_sections[first_error_section], zh_sections[first_error_section])
        # 使用特殊标记确保整个标题节点的错误计为1个错误
        # 将所有错误合并为一个错误信息，不使用分隔符
        header_info = f"[ERROR_COUNT:1]标题节点 '{en_tree['headers'][first_error_section]['text']}' (级别{en_tree['headers'][first_error_section]['level']}) 下的错误: "
        # 只取第一个错误作为代表，确保只显示一个错误
        if section_errors:
            combined_error = header_info + section_errors[0]
        else:
            combined_error = header_info + "未知错误"
        inconsistencies.append(combined_error)
        return inconsistencies
    
    # 如果没有错误，返回空列表
    return inconsistencies


def split_document_by_headers(syntax_tree):
    """
    根据标题将文档分割成多个部分
    
    参数:
        syntax_tree: Markdown文档的语法树
        
    返回:
        list: 包含每个标题节点下内容的列表
    """
    sections = []
    
    # 如果没有标题，整个文档作为一个部分
    if not syntax_tree['headers']:
        sections.append({
            'header': None,
            'code_blocks': syntax_tree['code_blocks'],
            'inline_codes': syntax_tree['inline_codes'],
            'bolds': syntax_tree['bolds'],
            'italics': syntax_tree['italics'],
            'links': syntax_tree['links'],
            'lists': syntax_tree['lists']
        })
        return sections
    
    # 按标题分割文档
    for i, header in enumerate(syntax_tree['headers']):
        # 确定当前标题的范围
        start_line = header['line']
        
        # 如果是最后一个标题，则到文档末尾
        if i == len(syntax_tree['headers']) - 1:
            end_line = float('inf')
        else:
            end_line = syntax_tree['headers'][i + 1]['line']
        
        # 提取当前标题范围内的所有元素
        # 修复：只包含完全在当前标题部分内的代码块（不跨越边界）
        section = {
            'header': header,
            'code_blocks': [cb for cb in syntax_tree['code_blocks'] 
                           if cb['start_line'] > start_line and 
                           cb['start_line'] < end_line and 
                           cb['end_line'] < end_line],
            'inline_codes': [ic for ic in syntax_tree['inline_codes'] if ic['line'] > start_line and ic['line'] < end_line],
            'bolds': [b for b in syntax_tree['bolds'] if b['line'] > start_line and b['line'] < end_line],
            'italics': [i for i in syntax_tree['italics'] if i['line'] > start_line and i['line'] < end_line],
            'links': [l for l in syntax_tree['links'] if l['line'] > start_line and l['line'] < end_line],
            'lists': [l for l in syntax_tree['lists'] if l['line'] > start_line and l['line'] < end_line]
        }
        
        sections.append(section)
    
    return sections


def compare_section_content(en_section, zh_section):
    """
    比较两个标题节点下的内容
    
    参数:
        en_section: 英文文档的标题节点
        zh_section: 中文文档的标题节点
        
    返回:
        list: 描述不一致位置的字符串列表
    """
    section_errors = []
    
    # 比较代码块
    if len(en_section['code_blocks']) != len(zh_section['code_blocks']):
        section_errors.append(f"代码块数量不一致(英文:{len(en_section['code_blocks'])}, 中文:{len(zh_section['code_blocks'])})")
        
        # 添加具体位置信息
        en_code_positions = [f"行{cb['start_line']}-{cb['end_line']}:{cb['start_text']}" for cb in en_section['code_blocks'][:3]]
        zh_code_positions = [f"行{cb['start_line']}-{cb['end_line']}:{cb['start_text']}" for cb in zh_section['code_blocks'][:3]]
        if en_code_positions:
            section_errors.append(f"英文代码块位置: {'; '.join(en_code_positions)}{'...' if len(en_section['code_blocks']) > 3 else ''}")
        if zh_code_positions:
            section_errors.append(f"中文代码块位置: {'; '.join(zh_code_positions)}{'...' if len(zh_section['code_blocks']) > 3 else ''}")
    
    # 比较行内代码
    if len(en_section['inline_codes']) != len(zh_section['inline_codes']):
        section_errors.append(f"行内代码数量不一致(英文:{len(en_section['inline_codes'])}, 中文:{len(zh_section['inline_codes'])})")
        
        # 添加具体位置信息
        en_inline_positions = [f"行{ic['line']}:`{ic['text']}`" for ic in en_section['inline_codes'][:5]]
        zh_inline_positions = [f"行{ic['line']}:`{ic['text']}`" for ic in zh_section['inline_codes'][:5]]
        if en_inline_positions:
            section_errors.append(f"英文行内代码位置: {'; '.join(en_inline_positions)}{'...' if len(en_section['inline_codes']) > 5 else ''}")
        if zh_inline_positions:
            section_errors.append(f"中文行内代码位置: {'; '.join(zh_inline_positions)}{'...' if len(zh_section['inline_codes']) > 5 else ''}")
    
    # 比较粗体
    if len(en_section['bolds']) != len(zh_section['bolds']):
        section_errors.append(f"粗体标记数量不一致(英文:{len(en_section['bolds'])}, 中文:{len(zh_section['bolds'])})")
        
        # 添加具体位置信息
        en_bold_positions = [f"行{b['line']}:**{b['text']}**" for b in en_section['bolds'][:5]]
        zh_bold_positions = [f"行{b['line']}:**{b['text']}**" for b in zh_section['bolds'][:5]]
        if en_bold_positions:
            section_errors.append(f"英文粗体标记位置: {'; '.join(en_bold_positions)}{'...' if len(en_section['bolds']) > 5 else ''}")
        if zh_bold_positions:
            section_errors.append(f"中文粗体标记位置: {'; '.join(zh_bold_positions)}{'...' if len(zh_section['bolds']) > 5 else ''}")
    
    # 比较斜体
    if len(en_section['italics']) != len(zh_section['italics']):
        section_errors.append(f"斜体标记数量不一致(英文:{len(en_section['italics'])}, 中文:{len(zh_section['italics'])})")
        
        # 添加具体位置信息
        en_italic_positions = [f"行{i['line']}:*{i['text']}*" for i in en_section['italics'][:5]]
        zh_italic_positions = [f"行{i['line']}:*{i['text']}*" for i in zh_section['italics'][:5]]
        if en_italic_positions:
            section_errors.append(f"英文斜体标记位置: {'; '.join(en_italic_positions)}{'...' if len(en_section['italics']) > 5 else ''}")
        if zh_italic_positions:
            section_errors.append(f"中文斜体标记位置: {'; '.join(zh_italic_positions)}{'...' if len(zh_section['italics']) > 5 else ''}")
    
    # 比较链接
    if len(en_section['links']) != len(zh_section['links']):
        section_errors.append(f"链接数量不一致(英文:{len(en_section['links'])}, 中文:{len(zh_section['links'])})")
        
        # 添加具体位置信息
        en_link_positions = [f"行{l['line']}:[{l['text']}]({l['url']})" for l in en_section['links'][:5]]
        zh_link_positions = [f"行{l['line']}:[{l['text']}]({l['url']})" for l in zh_section['links'][:5]]
        if en_link_positions:
            section_errors.append(f"英文链接位置: {'; '.join(en_link_positions)}{'...' if len(en_section['links']) > 5 else ''}")
        if zh_link_positions:
            section_errors.append(f"中文链接位置: {'; '.join(zh_link_positions)}{'...' if len(zh_section['links']) > 5 else ''}")
    
    # 比较列表
    if len(en_section['lists']) != len(zh_section['lists']):
        section_errors.append(f"列表数量不一致(英文:{len(en_section['lists'])}, 中文:{len(zh_section['lists'])})")
        
        # 添加具体位置信息
        en_list_positions = [f"行{l['line']}:{l['type']} {l['text']}" for l in en_section['lists'][:5]]
        zh_list_positions = [f"行{l['line']}:{l['type']} {l['text']}" for l in zh_section['lists'][:5]]
        if en_list_positions:
            section_errors.append(f"英文列表位置: {'; '.join(en_list_positions)}{'...' if len(en_section['lists']) > 5 else ''}")
        if zh_list_positions:
            section_errors.append(f"中文列表位置: {'; '.join(zh_list_positions)}{'...' if len(zh_section['lists']) > 5 else ''}")
    
    return section_errors