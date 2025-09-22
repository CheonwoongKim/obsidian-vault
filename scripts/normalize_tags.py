#!/usr/bin/env python3
import os
import re
import json
import argparse
from typing import List, Dict, Tuple

INLINE_TAG_RE = re.compile(r"(?<![\w/])#([\w\-/]+)")


def load_mapping(path: str) -> Dict[str, List[str]]:
    with open(path, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    mapping: Dict[str, List[str]] = {}
    for k, v in raw.items():
        if isinstance(v, list):
            mapping[k] = v
        else:
            mapping[k] = [str(v)]
    return mapping


def find_markdown_files(root: str) -> List[str]:
    out = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'.git', '.obsidian', 'node_modules', '.venv', 'venv', '__pycache__'}]
        for f in files:
            if f.lower().endswith('.md'):
                out.append(os.path.join(base, f))
    return out


def parse_frontmatter(text: str) -> Tuple[int, int, str]:
    if not text.startswith('---'):
        return -1, -1, ''
    end = text.find('\n---', 3)
    if end == -1:
        return -1, -1, ''
    start_idx = 0
    end_idx = end + len('\n---')
    return start_idx, end_idx, text[start_idx:end_idx]


def extract_tags_from_frontmatter(fm: str) -> Tuple[List[str], List[str]]:
    tags = []
    lines = fm.splitlines()
    out_lines = []
    i = 0
    in_tags_block = False
    while i < len(lines):
        line = lines[i]
        if not in_tags_block and re.match(r'^tags\s*:', line):
            # parse inline or start of list
            after = line.split(':', 1)[1].strip()
            if after:
                # inline value
                if after.startswith('[') and after.endswith(']'):
                    inner = after[1:-1]
                    parts = [p.strip().strip('"\'') for p in inner.split(',') if p.strip()]
                    tags.extend(parts)
                else:
                    parts = [p for p in re.split(r'[\s,]+', after) if p]
                    tags.extend(parts)
            else:
                # list-style values in following lines
                in_tags_block = True
            # do not keep original tags line
            i += 1
            continue
        elif in_tags_block:
            if re.match(r'^\s*-\s*', line):
                item = re.sub(r'^\s*-\s*', '', line).strip().strip('"\'')
                if item:
                    tags.append(item)
                i += 1
                continue
            # allow blank lines inside tags block
            if line.strip() == '':
                i += 1
                continue
            # end of tags block
            in_tags_block = False
            out_lines.append(line)
            i += 1
            continue
        else:
            out_lines.append(line)
            i += 1
    # Ensure fm starts and ends with '---' lines
    cleaned_fm_lines = out_lines
    return tags, cleaned_fm_lines


def normalize_inline_tags(text: str, mapping: Dict[str, List[str]]) -> Tuple[str, Dict[str, int]]:
    changes: Dict[str, int] = {}

    def repl(m: re.Match) -> str:
        full = m.group(0)
        tag = m.group(1)
        new_tags = mapping.get(tag)
        if not new_tags:
            # try underscore->hyphen fallback key
            alt = tag.replace('_', '-')
            new_tags = mapping.get(alt)
        if not new_tags:
            return full
        changes[tag] = changes.get(tag, 0) + 1
        return ' ' + ' '.join('#' + t for t in new_tags)

    new_text = INLINE_TAG_RE.sub(repl, text)
    return new_text, changes


def replace_frontmatter_tags(orig_text: str, mapping: Dict[str, List[str]]) -> Tuple[str, List[str], List[str]]:
    s, e, fm = parse_frontmatter(orig_text)
    if s == -1:
        return orig_text, [], []
    before = orig_text[:s]
    fm_text = fm
    after = orig_text[e:]

    tags, fm_no_tags_lines = extract_tags_from_frontmatter(fm_text)
    if not tags:
        # nothing to do in fm
        return orig_text, [], []
    # map tags
    mapped: List[str] = []
    for t in tags:
        if t in mapping:
            mapped.extend(mapping[t])
        else:
            alt = t.replace('_', '-')
            if alt in mapping:
                mapped.extend(mapping[alt])
            else:
                mapped.append(t)
    # unique, stable order
    seen = set()
    normalized = []
    for t in mapped:
        if t not in seen:
            seen.add(t)
            normalized.append(t)

    # rebuild fm: keep header/footer dashes
    new_fm_lines = []
    if fm_no_tags_lines and fm_no_tags_lines[0].strip() == '---':
        # already includes starting '---'
        new_fm_lines.extend(fm_no_tags_lines)
    else:
        new_fm_lines.append('---')
        new_fm_lines.extend(fm_no_tags_lines)
    # ensure last is '---'
    if not new_fm_lines or new_fm_lines[-1].strip() != '---':
        new_fm_lines.append('---')

    # Insert canonical tags line after first '---'
    header_idx = 0
    if new_fm_lines and new_fm_lines[0].strip() == '---':
        header_idx = 1
    tags_line = f"tags: [{', '.join(normalized)}]"
    new_fm_lines.insert(header_idx, tags_line)

    new_fm = "\n".join(new_fm_lines)
    new_text = before + new_fm + after
    return new_text, tags, normalized


def process_file(path: str, mapping: Dict[str, List[str]]) -> Tuple[bool, Dict[str, int], List[str], List[str]]:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        orig = f.read()

    # Frontmatter first
    fm_updated_text, fm_before, fm_after = replace_frontmatter_tags(orig, mapping)

    # Inline tags
    inl_updated_text, inline_changes = normalize_inline_tags(fm_updated_text, mapping)

    changed = (orig != inl_updated_text)
    if changed:
        return True, inline_changes, fm_before, fm_after
    else:
        return False, {}, fm_before, fm_after


def main():
    p = argparse.ArgumentParser(description='Normalize tags in Markdown files using mapping JSON.')
    p.add_argument('--root', default='.', help='Root directory to scan')
    p.add_argument('--mapping', default='_tag_mapping.json', help='Path to mapping JSON file')
    p.add_argument('--apply', action='store_true', help='Write changes to files')
    p.add_argument('--report', default='_tag_changes.md', help='Path to write change report')
    args = p.parse_args()

    mapping = load_mapping(args.mapping)
    files = find_markdown_files(args.root)
    total_changed = 0
    change_log = []

    for path in files:
        changed, inline_changes, fm_before, fm_after = process_file(path, mapping)
        if changed:
            total_changed += 1
            rel = os.path.relpath(path, args.root)
            change_log.append((rel, inline_changes, fm_before, fm_after))
            if args.apply:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                # re-run to get final text to write
                new_text, _, _ = replace_frontmatter_tags(content, mapping)
                new_text, _ = normalize_inline_tags(new_text, mapping)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_text)

    # Write report
    with open(args.report, 'w', encoding='utf-8') as out:
        out.write('# Tag Normalization Preview\n\n')
        out.write(f'- Files scanned: {len(files)}\n')
        out.write(f'- Files with changes: {total_changed}\n\n')
        for rel, inline_changes, fm_before, fm_after in change_log:
            out.write(f'## {rel}\n')
            if fm_before or fm_after:
                if fm_before:
                    out.write(f'- Frontmatter tags: {", ".join(fm_before)}\n')
                if fm_after:
                    out.write(f'- New frontmatter tags: {", ".join(fm_after)}\n')
            if inline_changes:
                out.write('- Inline tag replacements:\n')
                for k, v in inline_changes.items():
                    out.write(f'  - {k} -> {", ".join(mapping.get(k, mapping.get(k.replace("_", "-"), [k])))} (x{v})\n')
            out.write('\n')

    print(f"Processed {len(files)} files. Changes in {total_changed} files. Report -> {args.report}")


if __name__ == '__main__':
    main()

