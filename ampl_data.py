"""
Minimal AMPL `.dat` / `.txt` data-file parser.

Supports the AMPL data syntax used in the ECE6327 SGS course files:

    1) Indexed set + parameters
       param: SET: col1 col2 ... :=
           idx1   v11 v12 ...
           idx2   v21 v22 ... ;

    2) 2-D matrix parameter
       param NAME : c1 c2 ... :=
           r1   v11 v12 ...
           r2   v21 v22 ... ;

Quoted strings ("Solar", "Diesel", ...) are returned as Python str.
Numbers are returned as int when possible, otherwise float.

Returned value: a dict keyed by set / parameter name.
    - Set            -> list of indices
    - 1-D parameter  -> dict {idx: value}
    - 2-D parameter  -> dict {(row, col): value}

Comments (`# ...` to end of line) are stripped.

Usage:
    from ampl_data import parse_ampl_data
    d = parse_ampl_data('DSM_IC_e1_data.txt')
    GEN     = d['GEN']
    gen_min = d['gen_min']
"""
from __future__ import annotations

import os
import re
import shlex


def parse_ampl_data(path: str) -> dict:
    """Parse an AMPL data file into a dict of sets and parameters."""
    # Resolve relative paths against the caller's notebook directory or CWD.
    if not os.path.isabs(path) and not os.path.exists(path):
        # also try same directory as this module (handy when running from elsewhere)
        here = os.path.dirname(os.path.abspath(__file__))
        alt = os.path.join(here, path)
        if os.path.exists(alt):
            path = alt

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return parse_text(text)


def parse_text(text: str) -> dict:
    """Parse a string of AMPL-style data statements (same syntax as
    `parse_ampl_data` but takes the content directly).

    Useful when you have to splice a missing `param: SET: col :=` header
    onto a header-less data body --- which is what AMPL's option-5 inline
    syntax (`param: I: b := include FILE_noTitle.txt;`) does.
    """
    text = re.sub(r"#[^\n]*", "", text)
    statements = [s.strip() for s in text.split(";") if s.strip()]
    result: dict = {}
    for stmt in statements:
        _parse_statement(stmt, result)
    return result


def _parse_statement(stmt: str, result: dict) -> None:
    if ":=" not in stmt:
        return
    header_raw, body = stmt.split(":=", 1)
    header = header_raw.strip()

    if not header.startswith("param"):
        return
    rest = header[len("param"):].strip()

    if rest.startswith(":"):
        # Form 1:  param: SET: col1 col2 ...
        rest = rest[1:].strip()
        set_name, _, cols_str = rest.partition(":")
        set_name = set_name.strip()
        col_names = cols_str.split()
        _parse_indexed_block(body, set_name, col_names, result)
    else:
        # Form 2:  param NAME : c1 c2 ...
        name, _, cols_str = rest.partition(":")
        name = name.strip()
        col_names = cols_str.split()
        _parse_matrix_block(body, name, col_names, result)


def _parse_indexed_block(body: str, set_name: str, col_names: list, result: dict) -> None:
    tokens = _tokenize(body)
    width = 1 + len(col_names)
    indices = []
    cols = {c: {} for c in col_names}
    for row in _chunks(tokens, width):
        idx = _coerce(row[0])
        indices.append(idx)
        for i, c in enumerate(col_names):
            cols[c][idx] = _coerce(row[i + 1])
    result[set_name] = indices
    for c, d in cols.items():
        result[c] = d


def _parse_matrix_block(body: str, name: str, col_names: list, result: dict) -> None:
    tokens = _tokenize(body)
    width = 1 + len(col_names)
    mat: dict = {}
    for row in _chunks(tokens, width):
        row_idx = _coerce(row[0])
        for i, c in enumerate(col_names):
            col_idx = _coerce(c)
            mat[(row_idx, col_idx)] = _coerce(row[i + 1])
    result[name] = mat


def _tokenize(body: str) -> list:
    # shlex respects quoted strings; we just need to make sure '#' inside quoted strings
    # isn't an issue (it isn't for the data files in this repo).
    return shlex.split(body)


def _chunks(seq: list, n: int):
    for i in range(0, len(seq), n):
        c = seq[i:i + n]
        if len(c) == n:
            yield c


def _coerce(tok: str):
    if (tok.startswith('"') and tok.endswith('"')) or (
        tok.startswith("'") and tok.endswith("'")
    ):
        return tok[1:-1]
    try:
        return int(tok)
    except ValueError:
        pass
    try:
        return float(tok)
    except ValueError:
        return tok
