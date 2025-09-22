#!/usr/bin/env python3
import os
import re
import json
import argparse
from collections import defaultdict

INLINE_TAG_RE = re.compile(r"(?<![\w/])#([\w\-/]+)")


def load_mapping(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    canonical = set()
    for vals in raw.values():
        if isinstance(vals, list):
            canonical.update(vals)
        else:
            canonical.add(str(vals))
    return canonical


def find_markdown_files(root: str):
    out = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'.git', '.obsidian', 'node_modules', '.venv', 'venv', '__pycache__'}]
        for f in files:
            if f.lower().endswith('.md'):
                out.append(os.path.join(base, f))
    return out


def parse_frontmatter(text: str):
    if not text.startswith('---'):
        return []
    end = text.find('\n---', 3)
    if end == -1:
        return []
    fm = text[0:end+1]
    lines = fm.splitlines()
    tags = []
    i = 1
    in_block = False
    while i < len(lines):
        line = lines[i]
        if not in_block and line.startswith('tags:'):
            after = line.split(':', 1)[1].strip()
            if after:
                if after.startswith('[') and after.endswith(']'):
                    inner = after[1:-1]
                    parts = [p.strip().strip('"\'') for p in inner.split(',') if p.strip()]
                    tags.extend(parts)
                else:
                    parts = [p for p in re.split(r'[\s,]+', after) if p]
                    tags.extend(parts)
            else:
                in_block = True
            i += 1
            continue
        elif in_block:
            if re.match(r'^\s*-\s*', line):
                item = re.sub(r'^\s*-\s*', '', line).strip().strip('"\'')
                if item:
                    tags.append(item)
                i += 1
                continue
            if line.strip() == '':
                i += 1
                continue
            in_block = False
            # fallthrough to record line normally
        i += 1
    return tags


def depth(tag: str) -> int:
    return tag.count('/') + 1 if tag else 0


def main():
    p = argparse.ArgumentParser(description='Validate tags in Markdown against canonical mapping outputs.')
    p.add_argument('--root', default='.')
    p.add_argument('--mapping', default='_tag_mapping.json')
    p.add_argument('--report', default='_tag_validation.md')
    p.add_argument('--max-depth', type=int, default=2)
    args = p.parse_args()

    canonical = load_mapping(args.mapping)
    files = find_markdown_files(args.root)

    unknown_by_file = defaultdict(list)
    depth_violations = defaultdict(list)
    format_violations = defaultdict(list)

    for path in files:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        tags = set(parse_frontmatter(text))
        for m in INLINE_TAG_RE.finditer(text):
            tags.add(m.group(1))
        for t in sorted(tags):
            # unknown
            if t not in canonical:
                unknown_by_file[path].append(t)
            # depth
            if depth(t) > args.max_depth:
                depth_violations[path].append(t)
            # formatting: spaces or underscores
            if ' ' in t or '\t' in t or '__' in t or t != t.replace(' ', ''):
                format_violations[path].append(t)
            if '_' in t:
                if t not in format_violations[path]:
                    format_violations[path].append(t)

    with open(args.report, 'w', encoding='utf-8') as out:
        out.write('# Tag Validation Report\n\n')
        out.write(f'- Files scanned: {len(files)}\n')
        out.write(f'- Canonical tags count: {len(canonical)}\n\n')
        if unknown_by_file:
            out.write('## Unknown Tags (not in canonical mapping)\n')
            for p in sorted(unknown_by_file):
                rel = os.path.relpath(p, args.root)
                out.write(f'- {rel}: {", ".join(sorted(set(unknown_by_file[p])))}\n')
        else:
            out.write('## Unknown Tags\n- (none)\n')
        out.write('\n')
        if depth_violations:
            out.write(f'## Depth Violations (> {args.max_depth})\n')
            for p in sorted(depth_violations):
                rel = os.path.relpath(p, args.root)
                out.write(f'- {rel}: {", ".join(sorted(set(depth_violations[p])))}\n')
        else:
            out.write('## Depth Violations\n- (none)\n')
        out.write('\n')
        if format_violations:
            out.write('## Format Violations (spaces/underscores)\n')
            for p in sorted(format_violations):
                rel = os.path.relpath(p, args.root)
                out.write(f'- {rel}: {", ".join(sorted(set(format_violations[p])))}\n')
        else:
            out.write('## Format Violations\n- (none)\n')

    print(f"Validation complete. Report -> {args.report}")


if __name__ == '__main__':
    main()

