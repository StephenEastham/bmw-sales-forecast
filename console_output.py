"""
Helpers to capture, clean, and save console transcripts.

This module provides:
- `clean_console_output(raw: Optional[str]) -> str` — normalize and dedupe a transcript
- `save_console_output(raw: str, cleaned: Optional[str]=None) -> Path` — write cleaned and raw files

By default `save_console_output` writes the cleaned transcript to
`outputs/CONSOLE_OUTPUT.txt` (overwriting) and the raw transcript to a
timestamped file `outputs/CONSOLE_OUTPUT_RAW_<ts>.txt`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional
import re
from datetime import datetime


def clean_console_output(raw: Optional[str] = None) -> str:
    """Return a cleaned, more readable version of the console transcript.

    Cleaning steps:
    - normalize line endings and strip trailing spaces
    - remove consecutive duplicate lines
    - collapse repeated multi-line paragraphs (keep first occurrence)
    - collapse excessive blank lines
    """
    if raw is None:
        return ""

    # Normalize and split into lines
    lines = [ln.rstrip() for ln in raw.splitlines()]

    # Remove consecutive duplicate lines
    dedup_lines = []
    prev = None
    for ln in lines:
        if ln == prev:
            continue
        dedup_lines.append(ln)
        prev = ln

    text = "\n".join(dedup_lines)

    # Split into paragraphs (blocks separated by blank lines)
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

    # Remove duplicate paragraphs while preserving order
    seen = set()
    unique_paragraphs = []
    for p in paragraphs:
        key = p[:200]
        if key in seen:
            continue
        seen.add(key)
        unique_paragraphs.append(p)

    cleaned = "\n\n".join(unique_paragraphs)

    # Collapse 3+ newlines into two
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)

    return cleaned.strip() + "\n"


def save_console_output(raw: str, cleaned: Optional[str] = None) -> Path:
    """Save the console output files.

    - Writes cleaned text to `outputs/CONSOLE_OUTPUT.txt` (overwrites).
    - Writes raw text to `outputs/CONSOLE_OUTPUT_RAW_<timestamp>.txt`.

    Returns the Path to the cleaned file.
    """
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_path = out_dir / "CONSOLE_OUTPUT_RAW.txt"
    backup_path = out_dir / "CONSOLE_OUTPUT_RAW.bak"
    cleaned_path = out_dir / "CONSOLE_OUTPUT.txt"

    # Rotate: move existing raw to backup (overwrite backup)
    try:
        if raw_path.exists():
            # overwrite backup
            raw_path.replace(backup_path)
    except Exception:
        # best-effort; don't fail saving cleaned output because rotation failed
        pass

    # Write new raw
    raw_path.write_text(raw or "", encoding="utf-8")

    # If caller didn't provide cleaned text, compute it
    if cleaned is None:
        cleaned = clean_console_output(raw)

    cleaned_path.write_text(cleaned or "", encoding="utf-8")

    return cleaned_path
