#!/usr/bin/env python3
"""Extract thesis submission form fields from the local ThuThesis project."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THESIS_NAME = "thuthesis-chiwang-bachelor-tps"


class ExtractionError(RuntimeError):
    """Raised when required thesis metadata cannot be extracted."""


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"缺少 {path.relative_to(ROOT)}，请先确认文件存在")
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        escaped = False
        cut_at: int | None = None
        for index, char in enumerate(line):
            if char == "\\":
                escaped = not escaped
                continue
            if char == "%" and not escaped:
                cut_at = index
                break
            escaped = False
        lines.append(line if cut_at is None else line[:cut_at])
    return "\n".join(lines)


def find_matching_brace(text: str, open_index: int) -> int:
    if open_index >= len(text) or text[open_index] != "{":
        raise ExtractionError("internal parser error: expected opening brace")
    depth = 0
    escaped = False
    for index in range(open_index, len(text)):
        char = text[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ExtractionError("未找到匹配的右花括号")


def parse_braced_argument(text: str, start: int) -> tuple[str, int]:
    index = start
    while index < len(text) and text[index].isspace():
        index += 1
    if index >= len(text) or text[index] != "{":
        raise ExtractionError("未找到花括号参数")
    end = find_matching_brace(text, index)
    return text[index + 1 : end], end + 1


def extract_key_value(text: str, key: str) -> str:
    clean = strip_comments(text)
    pattern = re.compile(rf"(?<![\w*]){re.escape(key)}\s*=")
    for match in pattern.finditer(clean):
        value_start = match.end()
        while value_start < len(clean) and clean[value_start].isspace():
            value_start += 1
        if value_start < len(clean) and clean[value_start] == "{":
            value, _ = parse_braced_argument(clean, value_start)
            return value
    raise ExtractionError(f"未能在源码中提取 {key}")


def extract_environment(text: str, env: str) -> str:
    begin = rf"\begin{{{env}}}"
    end = rf"\end{{{env}}}"
    start = text.find(begin)
    if start < 0:
        raise ExtractionError(f"未找到 {begin}")
    start += len(begin)
    finish = text.find(end, start)
    if finish < 0:
        raise ExtractionError(f"未找到 {end}")
    return text[start:finish]


def remove_thusetup_blocks(text: str) -> str:
    result: list[str] = []
    cursor = 0
    command = r"\thusetup"
    while True:
        start = text.find(command, cursor)
        if start < 0:
            result.append(text[cursor:])
            break
        result.append(text[cursor:start])
        brace_start = start + len(command)
        while brace_start < len(text) and text[brace_start].isspace():
            brace_start += 1
        if brace_start >= len(text) or text[brace_start] != "{":
            result.append(command)
            cursor = start + len(command)
            continue
        cursor = find_matching_brace(text, brace_start) + 1
    return "".join(result)


def replace_two_arg_command(text: str, command: str, replacer) -> str:
    result: list[str] = []
    cursor = 0
    needle = "\\" + command
    while True:
        start = text.find(needle, cursor)
        if start < 0:
            result.append(text[cursor:])
            break
        result.append(text[cursor:start])
        try:
            first, next_index = parse_braced_argument(text, start + len(needle))
            second, cursor = parse_braced_argument(text, next_index)
        except ExtractionError:
            result.append(needle)
            cursor = start + len(needle)
            continue
        result.append(replacer(first, second))
    return "".join(result)


def latex_unit_to_text(unit: str) -> str:
    unit = re.sub(r"\s+", "", unit)
    replacements = {
        r"\per\femto\barn": "fb^-1",
        r"\femto\barn": "fb",
        r"\pico\barn": "pb",
        r"\tera\eV": "TeV",
        r"\giga\eV": "GeV",
        r"\mega\eV": "MeV",
        r"\electronvolt": "eV",
    }
    for latex, plain in replacements.items():
        unit = unit.replace(latex, plain)
    return latex_to_text(unit, collapse_spaces=False)


def replace_si(text: str) -> str:
    def repl(number: str, unit: str) -> str:
        unit_text = latex_unit_to_text(unit)
        number_text = latex_to_text(number, collapse_spaces=False)
        if number_text and unit_text:
            return f"{number_text} {unit_text}"
        return number_text or unit_text

    return replace_two_arg_command(text, "SI", repl)


def replace_texorpdfstring(text: str) -> str:
    return replace_two_arg_command(text, "texorpdfstring", lambda _tex, pdf: pdf)


def unwrap_one_arg_commands(text: str) -> str:
    commands = [
        "mathrm",
        "mathbf",
        "mathit",
        "mathcal",
        "text",
        "textbf",
        "emph",
        "mbox",
    ]
    changed = True
    while changed:
        changed = False
        for command in commands:
            needle = "\\" + command
            cursor = 0
            parts: list[str] = []
            while True:
                start = text.find(needle, cursor)
                if start < 0:
                    parts.append(text[cursor:])
                    break
                parts.append(text[cursor:start])
                try:
                    value, cursor = parse_braced_argument(text, start + len(needle))
                except ExtractionError:
                    parts.append(needle)
                    cursor = start + len(needle)
                    continue
                parts.append(value)
                changed = True
            text = "".join(parts)
    return text


def latex_to_text(text: str, collapse_spaces: bool = True) -> str:
    text = replace_texorpdfstring(text)
    text = replace_si(text)
    text = text.replace(r"s\bar{s}", "s s̄")
    text = unwrap_one_arg_commands(text)

    replacements = {
        r"~": " ",
        r"\,": "",
        r"\ ": " ",
        r"\%": "%",
        r"\{": "{",
        r"\}": "}",
        r"\_": "_",
        r"\textasciitilde": "~",
        r"\psi": "ψ",
        r"\phi": "φ",
        r"\mu": "μ",
        r"\Phi": "Φ",
        r"\Upsilon": "Υ",
        r"\sigma": "σ",
        r"\Delta": "Δ",
        r"\sqrt": "√",
        r"\mathrm": "",
        r"\to": "→",
        r"\times": "×",
        r"\pm": "±",
        r"\bar": "",
    }
    for latex, plain in replacements.items():
        text = text.replace(latex, plain)

    text = re.sub(r"\$([^$]*)\$", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", "", text)
    text = text.replace("{", "").replace("}", "")
    text = text.replace("--", "-")
    text = re.sub(r"\s+([,.;:，。；：])", r"\1", text)
    text = re.sub(r"([（(])\s+", r"\1", text)
    text = re.sub(r"\s+([）)])", r"\1", text)
    if collapse_spaces:
        text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_abstract_text(env_text: str) -> str:
    body = remove_thusetup_blocks(strip_comments(env_text))
    paragraphs = [latex_to_text(part) for part in re.split(r"\n\s*\n", body)]
    return "\n\n".join(part for part in paragraphs if part)


def count_references(bbl_path: Path) -> int:
    if not bbl_path.exists():
        raise FileNotFoundError(
            f"缺少 {bbl_path.relative_to(ROOT)}，请先运行 make thesis"
        )
    return len(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{", read_text(bbl_path)))


def extract_log_pages(log_path: Path) -> int:
    if not log_path.exists():
        raise FileNotFoundError(
            f"缺少 {log_path.relative_to(ROOT)}，请先运行 make thesis"
        )
    matches = re.findall(
        r"Output written on .*?\((\d+) pages?", read_text(log_path)
    )
    if not matches:
        raise ExtractionError(f"未能从 {log_path.relative_to(ROOT)} 提取 PDF 总页数")
    return int(matches[-1])


def extract_toc_pages(toc_path: Path) -> dict[str, int | None]:
    if not toc_path.exists():
        raise FileNotFoundError(
            f"缺少 {toc_path.relative_to(ROOT)}，请先运行 make thesis"
        )
    toc = read_text(toc_path)
    entries = re.findall(r"\\contentsline \{chapter\}\{(.+?)\}\{(\d+)\}\{[^}]*\}%", toc)
    if not entries:
        raise ExtractionError(f"未能从 {toc_path.relative_to(ROOT)} 提取章节页码")

    first_chapter_page: int | None = None
    reference_page: int | None = None
    appendix_page: int | None = None
    last_toc_page = 0
    for title, page_text in entries:
        page = int(page_text)
        title_plain = latex_to_text(title)
        last_toc_page = max(last_toc_page, page)
        if first_chapter_page is None and "第1章" in title_plain:
            first_chapter_page = page
        if reference_page is None and "参考文献" in title_plain:
            reference_page = page
        if appendix_page is None and "附录" in title_plain:
            appendix_page = page

    if first_chapter_page is None:
        raise ExtractionError("未能在目录中找到第 1 章起始页")

    recommended = appendix_page - 1 if appendix_page is not None else last_toc_page
    return {
        "first_chapter_page": first_chapter_page,
        "reference_page": reference_page,
        "appendix_page": appendix_page,
        "last_toc_page": last_toc_page,
        "recommended_page_count": recommended,
    }


def extract_submission_data(defense_date: str | None) -> dict[str, object]:
    setup = read_text(ROOT / "thusetup.tex")
    abstract_source = read_text(ROOT / "data" / "abstract.tex")
    abstract_zh_env = extract_environment(abstract_source, "abstract")
    abstract_en_env = extract_environment(abstract_source, "abstract*")
    toc_pages = extract_toc_pages(ROOT / f"{THESIS_NAME}.toc")
    pdf_total_pages = extract_log_pages(ROOT / f"{THESIS_NAME}.log")

    data: dict[str, object] = {
        "title_zh": latex_to_text(extract_key_value(setup, "title")),
        "title_en": latex_to_text(extract_key_value(setup, "title*")),
        "keywords_zh": latex_to_text(extract_key_value(abstract_zh_env, "keywords")),
        "keywords_en": latex_to_text(extract_key_value(abstract_en_env, "keywords*")),
        "abstract_zh": extract_abstract_text(abstract_zh_env),
        "abstract_en": extract_abstract_text(abstract_en_env),
        "defense_date": defense_date or "",
        "reference_count": count_references(ROOT / f"{THESIS_NAME}.bbl"),
        "pdf_total_pages": pdf_total_pages,
    }
    data.update(toc_pages)
    data["page_count_note"] = (
        f"PDF 总页数为 {pdf_total_pages}；建议页数按正文第一页至附录前最后一页计算。"
    )
    return data


def markdown_escape(value: object) -> str:
    text = str(value)
    text = text.replace("|", r"\|")
    text = re.sub(r"\n{2,}", "<br><br>", text)
    text = text.replace("\n", "<br>")
    return text


def format_markdown(data: dict[str, object]) -> str:
    fields = [
        ("中文论文题目", data["title_zh"]),
        ("英文论文题目", data["title_en"]),
        ("中文关键词", data["keywords_zh"]),
        ("英文关键词", data["keywords_en"]),
        ("中文摘要", data["abstract_zh"]),
        ("英文摘要", data["abstract_en"]),
        ("答辩日期", data["defense_date"]),
        ("参考文献总数", data["reference_count"]),
        ("论文总页数", data["recommended_page_count"]),
        ("备注", data["page_count_note"]),
    ]
    lines = ["| 字段 | 内容 |", "| --- | --- |"]
    lines.extend(f"| {field} | {markdown_escape(value)} |" for field, value in fields)
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract thesis-management submission fields from this LaTeX repo."
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="output format (default: markdown)",
    )
    parser.add_argument(
        "--defense-date",
        help="defense date to include in the output, for example 20260611",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        data = extract_submission_data(args.defense_date)
    except (ExtractionError, FileNotFoundError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
