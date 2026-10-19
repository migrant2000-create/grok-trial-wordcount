"""Counting rules for the wordcount command."""

from __future__ import annotations

import re
from dataclasses import dataclass

# CJK Unified Ideographs plus the common extension blocks (A–I, including G/H).
_HAN = re.compile(
    "["
    "\u3400-\u4dbf"  # Extension A
    "\u4e00-\u9fff"  # CJK Unified Ideographs
    "\U00020000-\U0002a6df"  # Extension B
    "\U0002a700-\U0002b73f"  # Extension C
    "\U0002b740-\U0002b81f"  # Extension D
    "\U0002b820-\U0002ceaf"  # Extension E
    "\U0002ceb0-\U0002ebef"  # Extension F
    "\U0002ebf0-\U0002ee5f"  # Extension I
    "\U00030000-\U0003134f"  # Extension G
    "\U00031350-\U000323af"  # Extension H
    "]"
)

# A run of ASCII letters, optionally joined by apostrophes or hyphens
# (don't, well-known, mother-in-law). Each match is one word.
_ENGLISH_WORD = re.compile(r"[A-Za-z]+(?:['-][A-Za-z]+)*")


@dataclass(frozen=True)
class CountResult:
    chinese_chars: int
    english_words: int
    reading_seconds: int


def reading_seconds(chinese_chars: int, english_words: int) -> int:
    """Round reading time to the nearest 10 seconds, with halves rounding up.

    Raw seconds are ``chinese_chars / 300 * 60 + english_words / 200 * 60``
    (0.2 s per Han character and 0.3 s per English word). That value is the
    exact rational ``(2 * chinese_chars + 3 * english_words) / 10``. Rounding
    uses only integer arithmetic. Empty input and any total under 5 seconds
    both yield 0.
    """
    tenths = chinese_chars * 2 + english_words * 3
    if tenths <= 0:
        return 0
    return 10 * ((tenths + 50) // 100)


def count_text(text: str) -> CountResult:
    """Count Han ideographs and English words in ``text``."""
    chinese_chars = len(_HAN.findall(text))
    english_words = len(_ENGLISH_WORD.findall(text))
    return CountResult(
        chinese_chars=chinese_chars,
        english_words=english_words,
        reading_seconds=reading_seconds(chinese_chars, english_words),
    )


def format_report(result: CountResult) -> str:
    """Stable, human-readable report (trailing newline included)."""
    return (
        f"中文字数: {result.chinese_chars}\n"
        f"英文词数: {result.english_words}\n"
        f"阅读时间: {result.reading_seconds} 秒\n"
    )
