#!/usr/bin/env python3
"""
Extract faulty C/C++ functions from source files based on CSV findings (Flawfinder/other).

Features:
- Reads a CSV with columns: File, Line, CWEs (case-insensitive column names supported)
- Filters to C/C++ source files (by extension: .cpp, .cxx, .cc, .c, .hpp, .h, .hh)
- Attempts to locate the enclosing function for the given line number using heuristics
  (searching backwards for a likely function signature, then brace-matching forward).
- Falls back to extracting a fixed number of context lines if function detection fails.
- Writes each extracted function (or context) to code_segments/<tool>/<project>/ files.
- Creates a CSV "extracted_segments_summary.csv" with metadata about each extraction.

Usage:
    python3 extract_faulty_cpp_functions.py --csv flawfinder_ggml.csv \
        --outdir code_segments/flawfinder/ggml --context 10

Notes / heuristics:
- This script uses regular expressions and brace counting; it is not a full C++ parser but
  works well for common function styles. If you need full accuracy for every C++ edge-case,
  consider integrating a C++ parser (libclang/clang.cindex or tree-sitter) instead.
"""

from pathlib import Path
import argparse
import pandas as pd
import re
import csv
import os
import html

CPP_EXTS = {'.c', '.cc', '.cpp', '.cxx', '.h', '.hh', '.hpp', '.hxx'}

# Regex to find candidate function signatures above the reported line.
# This is intentionally permissive; it looks for a line that looks like "return_type name(args) qualifiers {?"
FUNC_SIG_REGEX = re.compile(
    r"^\s*(?:template\s*<[^>]+>\s*)?"  # optional template<...>
    r"(?:(?:inline|static|constexpr|virtual|friend|extern)\s+)*"  # optional storage/classifiers
    r"[\w:\<\>\~\*\&\s]+?"  # return type (rough)
    r"\b([A-Za-z_][A-Za-z0-9_:\.]*)\s*"  # function name (capture)
    r"\([^;{\)]*\)\s*"  # arguments (not containing ; or { )
    r"(?:const\s*)?(?:noexcept\s*)?(?:->\s*[\w:\<\>]+\s*)?"  # qualifiers / trailing return
    r"(?:\{|$)"  # either a { or end-of-line (signature may be split)
)

# A simpler fallback: a line that ends with ')' and maybe qualifiers (for multi-line signatures)
PAREN_END_REGEX = re.compile(r"\)\s*(?:const\s*)?(?:noexcept\s*)?$")


def sanitize_for_filename(s: str) -> str:
    s = str(s)
    s = s.replace('/', '_').replace('\\', '_')
    s = re.sub(r"[^A-Za-z0-9_.-]", '_', s)
    return s[:200]


def find_enclosing_function(lines, target_idx):
    """
    Attempt to find the function that encloses target_idx (0-based index).
    Returns (start_idx, end_idx, func_name) or None if not found.
    Heuristic:
      - search backwards up to N lines for a line that matches FUNC_SIG_REGEX
      - if found, search forward from the first '{' after that signature and brace-match
      - also handle the case where signature is split on multiple lines (look for a ) ending)
    """
    # Search backwards for a likely signature
    max_lookback = 300  # don't search indefinitely
    start_search = max(0, target_idx - max_lookback)

    sig_line_idx = None
    func_name = None

    # First pass: look for a single-line signature
    for i in range(target_idx, start_search - 1, -1):
        line = lines[i]
        if FUNC_SIG_REGEX.search(line):
            m = FUNC_SIG_REGEX.search(line)
            func_name = m.group(1)
            sig_line_idx = i
            break

    # Second pass: multi-line signatures — find a line that ends with ')' and walk back for start
    if sig_line_idx is None:
        for i in range(target_idx, start_search - 1, -1):
            if PAREN_END_REGEX.search(lines[i]):
                # walk further back up to 10 lines to find start of signature
                j = i
                while j >= max(start_search, i - 10):
                    candidate = ''.join(lines[j:i+1])
                    if FUNC_SIG_REGEX.search(candidate.splitlines()[0]):
                        m = FUNC_SIG_REGEX.search(candidate)
                        if m:
                            func_name = m.group(1)
                            sig_line_idx = j
                            break
                    j -= 1
                if sig_line_idx is not None:
                    break

    if sig_line_idx is None:
        return None

    # From the signature location, search forward for first '{' and then brace-match
    # Build a single string from sig_line_idx onward to reliably find braces.
    text_from_sig = ''.join(lines[sig_line_idx:])
    brace_pos = text_from_sig.find('{')
    if brace_pos == -1:
        # Maybe signature is followed by attributes/qualifiers; search a bit further
        next_open = text_from_sig.find(')')
        if next_open == -1:
            return None
        # try to find '{' in the subsequent 3000 chars
        brace_pos = text_from_sig.find('{', next_open)
        if brace_pos == -1:
            return None

    # Find absolute index of '{'
    abs_idx = 0
    chars_count = 0
    for idx in range(sig_line_idx, len(lines)):
        chars_count += len(lines[idx])
        if chars_count > brace_pos:
            abs_idx = idx
            break

    # Now do brace counting from the position of the first '{'
    # We'll scan line by line and count braces, taking care to ignore braces in strings or comments
    open_braces = 0
    in_single_quote = False
    in_double_quote = False
    in_block_comment = False

    start_body_idx = None
    end_body_idx = None

    # We'll scan from sig_line_idx to end
    for idx in range(sig_line_idx, len(lines)):
        line = lines[idx]
        i = 0
        while i < len(line):
            ch = line[i]
            # handle block comments
            if not in_single_quote and not in_double_quote:
                if not in_block_comment and ch == '/' and i + 1 < len(line) and line[i+1] == '*':
                    in_block_comment = True
                    i += 2
                    continue
                if in_block_comment and ch == '*' and i + 1 < len(line) and line[i+1] == '/':
                    in_block_comment = False
                    i += 2
                    continue
            if in_block_comment:
                i += 1
                continue

            # handle line comments
            if not in_single_quote and not in_double_quote and ch == '/' and i + 1 < len(line) and line[i+1] == '/':
                # rest of line is comment
                break

            # handle quotes
            if ch == '"' and not in_single_quote:
                # check for escape
                if i == 0 or line[i-1] != '\\':
                    in_double_quote = not in_double_quote
                i += 1
                continue
            if ch == "'" and not in_double_quote:
                if i == 0 or line[i-1] != '\\':
                    in_single_quote = not in_single_quote
                i += 1
                continue

            if not in_single_quote and not in_double_quote and not in_block_comment:
                if ch == '{':
                    if start_body_idx is None:
                        start_body_idx = idx
                    open_braces += 1
                elif ch == '}':
                    open_braces -= 1
                    if open_braces == 0 and start_body_idx is not None:
                        end_body_idx = idx
                        # Found end of function
                        return (sig_line_idx, end_body_idx, func_name)
            i += 1

    # If we reach here, we couldn't find matching end
    return None


def extract_and_write_segment(file_path: Path, line_number: int, cwe: str, outdir: Path, context_lines=10):
    """
    Extract function or context and write to file. Returns metadata dict.
    line_number is 1-based.
    """
    meta = {
        'source_file': str(file_path),
        'line': line_number,
        'cwe': cwe,
        'extracted_file': None,
        'method': None,
        'function_name': None,
        'message': None,
    }

    if not file_path.exists():
        meta['message'] = 'source file not found'
        return meta

    text = file_path.read_text(encoding='utf-8', errors='ignore')
    lines = text.splitlines(keepends=True)
    idx = max(0, line_number - 1)
    if idx >= len(lines):
        meta['message'] = 'line number out of range'
        return meta

    # Attempt to find enclosing function
    res = find_enclosing_function(lines, idx)
    safe_cwe = sanitize_for_filename(cwe)
    base_name = sanitize_for_filename(file_path.stem)

    if res is not None:
        start_idx, end_idx, func_name = res
        segment = ''.join(lines[start_idx:end_idx+1])
        seg_fname = f"{base_name}_line{line_number}_CWE{safe_cwe}_func_{sanitize_for_filename(func_name)}.txt"
        out_path = outdir / seg_fname
        out_path.write_text(segment, encoding='utf-8')
        meta.update({
            'extracted_file': str(out_path),
            'method': 'function_extraction',
            'function_name': func_name,
            'message': 'ok',
        })
        return meta

    # Fallback: extract context lines
    start = max(0, idx - context_lines)
    end = min(len(lines)-1, idx + context_lines)
    segment = ''.join(lines[start:end+1])
    seg_fname = f"{base_name}_line{line_number}_CWE{safe_cwe}_context.txt"
    out_path = outdir / seg_fname
    out_path.write_text(segment, encoding='utf-8')
    meta.update({
        'extracted_file': str(out_path),
        'method': 'context_fallback',
        'function_name': None,
        'message': 'fallback to context',
    })
    return meta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True, help='CSV file with columns: File, Line, CWEs (or similar).')
    parser.add_argument('--file-col', default='File', help='CSV column name for file path')
    parser.add_argument('--line-col', default='Line', help='CSV column name for line number (1-based)')
    parser.add_argument('--cwe-col', default='CWEs', help='CSV column name for CWE(s)')
    parser.add_argument('--outdir', default='code_segments/flawfinder/ggml', help='Output directory')
    parser.add_argument('--context', type=int, default=10, help='Context lines fallback')
    parser.add_argument('--project', default='ggml', help='Project/tool name used in output path')
    args = parser.parse_args()

    df = pd.read_csv(args.csv, dtype=str)
    # normalize column names (case-insensitive)
    cols_map = {c.lower(): c for c in df.columns}
    file_col = cols_map.get(args.file_col.lower(), args.file_col)
    line_col = cols_map.get(args.line_col.lower(), args.line_col)
    cwe_col = cols_map.get(args.cwe_col.lower(), args.cwe_col)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    summary = []
    for _, row in df.iterrows():
        file_path = Path(str(row.get(file_col, '')).strip())
        line_raw = row.get(line_col, '')
        cwe_raw = row.get(cwe_col, '')

        if not file_path.suffix.lower() in CPP_EXTS:
            # skip non-c/cpp files
            continue

        try:
            line_number = int(float(line_raw)) if line_raw not in (None, '') else None
        except Exception:
            # sometimes line is 'Line:30' or has extras
            m = re.search(r"(\d+)", str(line_raw))
            line_number = int(m.group(1)) if m else None

        if not line_number:
            summary.append({
                'source_file': str(file_path),
                'line': line_raw,
                'cwe': cwe_raw,
                'extracted_file': None,
                'method': None,
                'function_name': None,
                'message': 'invalid line number',
            })
            continue

        meta = extract_and_write_segment(file_path, line_number, cwe_raw or '', outdir, context_lines=args.context)
        summary.append(meta)

    # write summary CSV
    summary_csv = outdir / 'extracted_segments_summary.csv'
    keys = ['source_file', 'line', 'cwe', 'extracted_file', 'method', 'function_name', 'message']
    with open(summary_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for row in summary:
            writer.writerow({k: row.get(k) for k in keys})

    print(f"Done. Extracted segments and summary saved to {outdir}")


if __name__ == '__main__':
    main()
