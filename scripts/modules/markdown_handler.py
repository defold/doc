import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

from .file_handler import setup_console_encoding


LOCAL_DOC_ROOTS = {"manuals", "tutorials", "faq", "shared"}
IGNORED_LINK_SCHEMES = ("http://", "https://", "mailto:", "tel:")
IGNORED_FILE_EXTENSIONS = {
    ".apng",
    ".atlas",
    ".collection",
    ".collectionfactory",
    ".css",
    ".csv",
    ".dae",
    ".edn",
    ".factory",
    ".font",
    ".gif",
    ".go",
    ".goc",
    ".gui",
    ".html",
    ".ico",
    ".input_binding",
    ".json",
    ".lua",
    ".material",
    ".mp3",
    ".ogg",
    ".otf",
    ".particlefx",
    ".png",
    ".project",
    ".render",
    ".script",
    ".sprite",
    ".svg",
    ".ttf",
    ".wav",
    ".webp",
    ".zip",
}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)(?:\s+\{#([^}]+)\})?\s*$")
RAW_ANCHOR_RE = re.compile(r"<a\s+[^>]*(?:id|name)=[\"']([^\"']+)[\"']", re.IGNORECASE)
INCLUDE_RE = re.compile(r"^:\[[^\]]*\]\(([^)]+\.md)\)\s*$")
LINK_RE = re.compile(r"(?<!!)\[([^\]\n]+)\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def compare_markdown_syntax_trees(
    source_content,
    target_content,
    file_path,
    source_file_path=None,
    target_file_path=None,
    source_root=None,
    target_root=None,
    links_only=False,
):
    """
    Build Markdown syntax trees and compare the syntax structure of two documents,
    identifying inconsistent positions.

    Args:
        source_content (str): Source version Markdown content
        target_content (str): Target version Markdown content
        file_path (str): File path for error messages
        source_file_path (str|Path): Optional full source file path
        target_file_path (str|Path): Optional full target file path
        source_root (str|Path): Optional source language root
        target_root (str|Path): Optional target language root
        links_only (bool): Only validate local Markdown links and fragments

    Returns:
        str: Consistency check result, "Consistent" if consistent, otherwise error message
    """
    issues = []
    if not links_only:
        source_tree = build_markdown_syntax_tree(source_content)
        target_tree = build_markdown_syntax_tree(target_content)

        syntax_difference = compare_syntax_trees(source_tree, target_tree, file_path)
        if syntax_difference:
            issues.append(syntax_difference)

    if source_file_path and source_root:
        issues.extend(
            validate_local_links(source_content, source_file_path, source_root, "source")
        )
    if target_file_path and target_root:
        issues.extend(
            validate_local_links(target_content, target_file_path, target_root, "target")
        )

    if issues:
        return f"Inconsistent: {'; '.join(issues)}"
    return "Consistent"


def slugify_heading(text):
    """
    Generate a stable heading slug while preserving Unicode letters and underscores.
    """
    text = re.sub(r"\s+\{#[^}]+\}\s*$", "", text).strip()
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s-]+", "-", text, flags=re.UNICODE)
    return text.strip("-")


def parse_heading(line, line_num=None):
    """
    Parse a Markdown heading.

    Returns:
        dict|None: level, clean title, explicit key, generated key, and line number.
    """
    match = HEADING_RE.match(line)
    if not match:
        return None

    level = len(match.group(1))
    clean_title = match.group(2).strip()
    explicit_key = match.group(3)
    return {
        "level": level,
        "title": clean_title,
        "explicit_key": explicit_key,
        "generated_key": slugify_heading(clean_title),
        "line": line_num,
    }


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

    lines = content.split("\n")
    tree = []

    for line_num, line in enumerate(lines, 1):
        if not line.strip():
            continue

        heading = parse_heading(line, line_num)
        if heading:
            tree.append(
                {
                    "type": "header",
                    "level": heading["level"],
                    "text": heading["title"],
                    "line": line_num,
                }
            )
            continue

        list_match = re.match(r"^(\s*)([*+-]|\d+\.)\s+(.*)", line)
        if list_match:
            indent = len(list_match.group(1))
            marker = list_match.group(2)
            text = list_match.group(3)
            tree.append(
                {
                    "type": "list",
                    "indent": indent,
                    "marker": marker,
                    "text": text,
                    "line": line_num,
                }
            )
            continue

        if line.strip().startswith("```"):
            tree.append({"type": "code_block", "text": line.strip(), "line": line_num})
            continue

        if line.strip().startswith(">"):
            tree.append({"type": "blockquote", "text": line.strip(), "line": line_num})
            continue

        if line.strip() in ["---", "***", "___"]:
            tree.append({"type": "hr", "line": line_num})
            continue

        bold_matches = re.finditer(r"\*\*(.*?)\*\*", line)
        for match in bold_matches:
            tree.append({"type": "bold", "text": match.group(1), "line": line_num})

        italic_matches = re.finditer(r"\*(.*?)\*", line)
        for match in italic_matches:
            tree.append({"type": "italic", "text": match.group(1), "line": line_num})

        code_matches = re.finditer(r"`(.*?)`", line)
        for match in code_matches:
            tree.append(
                {"type": "inline_code", "text": match.group(1), "line": line_num}
            )

        link_matches = re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line)
        for match in link_matches:
            tree.append(
                {
                    "type": "link",
                    "text": match.group(1),
                    "url": match.group(2),
                    "line": line_num,
                }
            )

        img_matches = re.finditer(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        for match in img_matches:
            tree.append(
                {
                    "type": "image",
                    "alt": match.group(1),
                    "url": match.group(2),
                    "line": line_num,
                }
            )

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
    setup_console_encoding()

    if len(source_tree) != len(target_tree):
        return f"Number of elements inconsistent (Source: {len(source_tree)}, Target: {len(target_tree)})"

    for i, (source_node, target_node) in enumerate(zip(source_tree, target_tree)):
        if source_node["type"] != target_node["type"]:
            return f"Element type inconsistent at position {i+1} (Source: {source_node['type']}, Target: {target_node['type']})"

        if source_node["type"] == "header":
            if source_node["level"] != target_node["level"]:
                return f"Header level inconsistent at line {source_node['line']} (Source: {source_node['level']}, Target: {target_node['level']})"

        elif source_node["type"] == "list":
            if source_node["indent"] != target_node["indent"]:
                return f"List indent inconsistent at line {source_node['line']} (Source: {source_node['indent']}, Target: {target_node['indent']})"
            if source_node["marker"] != target_node["marker"]:
                return f"List marker inconsistent at line {source_node['line']} (Source: {source_node['marker']}, Target: {target_node['marker']})"

        elif source_node["type"] == "code_block":
            pass

        elif source_node["type"] == "blockquote":
            pass

        elif source_node["type"] == "hr":
            pass

        elif source_node["type"] in ["bold", "italic", "inline_code"]:
            pass

        elif source_node["type"] == "link":
            if source_node["url"] != target_node["url"]:
                return f"Link URL inconsistent at line {source_node['line']} (Source: {source_node['url']}, Target: {target_node['url']})"

        elif source_node["type"] == "image":
            if source_node["url"] != target_node["url"]:
                return f"Image URL inconsistent at line {source_node['line']} (Source: {source_node['url']}, Target: {target_node['url']})"

    return ""


def validate_local_links(content, current_file, lang_root, label):
    """
    Validate local documentation links in one Markdown file.
    """
    current_file = Path(current_file)
    lang_root = Path(lang_root)
    issues = []
    anchor_cache = {}

    for line_num, line in _iter_non_fenced_lines(content):
        for match in LINK_RE.finditer(line):
            url = match.group(2).strip("<>")
            resolved = resolve_local_doc_link(url, current_file, lang_root)
            if not resolved:
                continue

            target_file = resolved["target_file"]
            fragment = resolved["fragment"]
            if not target_file.exists():
                issues.append(
                    f"Broken {label} link at line {line_num}: {url} missing target file {_display_path(target_file, lang_root)}"
                )
                continue

            if fragment:
                anchor_keys = _anchor_keys_for_file(
                    target_file, current_file, content, lang_root, anchor_cache
                )
                if fragment not in anchor_keys:
                    issues.append(
                        f"Broken {label} link at line {line_num}: {url} missing fragment {fragment}"
                    )

    return issues


def collect_anchor_keys(content, file_path=None, lang_root=None):
    """
    Collect all public anchor keys from headings and raw anchors, expanding local includes.
    """
    keys = set()
    for _, line in _iter_non_fenced_expanded_lines(content, file_path, lang_root):
        heading = parse_heading(line)
        if heading:
            keys.add(heading["explicit_key"] or heading["generated_key"])
        keys.update(RAW_ANCHOR_RE.findall(line))
    keys.discard(None)
    keys.discard("")
    return keys


def resolve_local_doc_link(url, current_file, lang_root):
    """
    Resolve a local documentation link to a Markdown file and optional fragment.

    Returns:
        dict|None: target_file and fragment, or None when the link is outside docs scope.
    """
    url = url.strip()
    if not url or url.startswith(IGNORED_LINK_SCHEMES):
        return None
    if url.startswith("{{") or url.startswith("{%"):
        return None

    url_without_query = url.split("?", 1)[0]
    if "#" in url_without_query:
        path_part, fragment = url_without_query.split("#", 1)
        fragment = unquote(fragment)
    else:
        path_part = url_without_query
        fragment = ""

    if path_part == "":
        return {"target_file": Path(current_file), "fragment": fragment}

    if path_part.startswith("/"):
        relative_path = path_part.lstrip("/")
        if _should_ignore_relative_link(relative_path, fragment):
            return None
        first_part = relative_path.split("/", 1)[0]
        if first_part not in LOCAL_DOC_ROOTS:
            return None
        if relative_path.rstrip("/") in LOCAL_DOC_ROOTS:
            return None
        target_file = _route_to_markdown_file(Path(lang_root) / relative_path)
        return {"target_file": target_file, "fragment": fragment}

    if _should_ignore_relative_link(path_part, fragment):
        return None

    target_path = (Path(current_file).parent / path_part).resolve()
    target_file = _route_to_markdown_file(target_path)
    return {"target_file": target_file, "fragment": fragment}


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

    lines = content.split("\n")
    sections = defaultdict(list)
    current_header = "Introduction"

    for line in lines:
        heading = parse_heading(line)
        if heading:
            current_header = heading["title"]
        sections[current_header].append(line)

    for header, lines in sections.items():
        sections[header] = "\n".join(lines)

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
    all_headers = set(source_sections.keys()).union(set(target_sections.keys()))

    for header in all_headers:
        source_exists = header in source_sections
        target_exists = header in target_sections

        if source_exists and target_exists:
            source_tree = build_markdown_syntax_tree(source_sections[header])
            target_tree = build_markdown_syntax_tree(target_sections[header])
            differences = compare_syntax_trees(source_tree, target_tree, header)

            if differences:
                results[header] = f"Inconsistent: {differences}"
            else:
                results[header] = "Consistent"

        elif source_exists:
            results[header] = "Source Only"

        elif target_exists:
            results[header] = "Target Only"

    return results


def _iter_non_fenced_lines(content):
    yield from _iter_non_fenced_pairs(enumerate(content.splitlines(), 1))


def _iter_non_fenced_pairs(lines):
    in_fence = False
    fence_marker = None
    for line_num, line in lines:
        stripped = line.lstrip()
        fence_match = re.match(r"^(```+|~~~+)", stripped)
        if fence_match:
            marker = fence_match.group(1)
            marker_char = marker[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker_char
            elif marker_char == fence_marker:
                in_fence = False
                fence_marker = None
            continue
        if not in_fence:
            yield line_num, line


def _iter_non_fenced_expanded_lines(content, file_path, lang_root):
    # Includes are expanded before code-fence filtering, so snippets can contribute
    # anchors while fenced examples remain invisible to link and anchor validation.
    yield from _iter_non_fenced_pairs(_expanded_lines(content, file_path, lang_root, set()))


def _expanded_lines(content, file_path, lang_root, seen):
    current_path = Path(file_path).resolve() if file_path else None
    if current_path:
        if current_path in seen:
            return []
        seen.add(current_path)

    expanded = []
    for line_num, line in enumerate(content.splitlines(), 1):
        include_match = INCLUDE_RE.match(line.strip())
        if include_match and current_path:
            include_path = (current_path.parent / include_match.group(1)).resolve()
            if include_path.exists():
                include_content = include_path.read_text(encoding="utf-8", errors="replace")
                expanded.extend(_expanded_lines(include_content, include_path, lang_root, seen))
                continue
        expanded.append((line_num, line))
    return expanded


def _anchor_keys_for_file(target_file, current_file, current_content, lang_root, cache):
    target_file = target_file.resolve()
    if target_file in cache:
        return cache[target_file]

    if target_file == Path(current_file).resolve():
        content = current_content
    else:
        content = target_file.read_text(encoding="utf-8", errors="replace")

    keys = collect_anchor_keys(content, target_file, lang_root)
    cache[target_file] = keys
    return keys


def _route_to_markdown_file(path):
    path = Path(path)
    if path.suffix == ".md":
        return path
    if path.suffix:
        return path

    candidates = [path.with_suffix(".md"), path / "index.md"]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def _should_ignore_relative_link(path_part, fragment):
    path = Path(path_part)
    normalized = path_part.replace("\\", "/").strip("/")
    if not normalized:
        return False
    if normalized.startswith(("images/", "assets/")) or "/images/" in normalized:
        return True
    if path.suffix.lower() in IGNORED_FILE_EXTENSIONS:
        return True
    if path.suffix and path.suffix.lower() != ".md":
        return True
    if not fragment and path.suffix.lower() != ".md" and "." in path.name:
        return True
    return False


def _display_path(path, lang_root):
    try:
        return Path(path).relative_to(Path(lang_root)).as_posix()
    except ValueError:
        return Path(path).as_posix()
