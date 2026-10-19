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
    reading_minutes: int


def reading_minutes(chinese_chars: int, english_words: int) -> int:
    """Return ceil(chinese_chars / 300 + english_words / 200).

    The sum is evaluated as the exact rational (2*c + 3*e) / 600, then
    rounded up to a whole number of minutes. Zero countable content yields 0.
    """
    numerator = chinese_chars * 2 + english_words * 3
    if numerator <= 0:
        return 0
    return (numerator + 599) // 600


def count_text(text: str) -> CountResult:
    """Count Han ideographs and English words in ``text``."""
    chinese_chars = len(_HAN.findall(text))
    english_words = len(_ENGLISH_WORD.findall(text))
    return CountResult(
        chinese_chars=chinese_chars,
        english_words=english_words,
        reading_minutes=reading_minutes(chinese_chars, english_words),
    )


def format_report(result: CountResult) -> str:
    """Stable, human-readable report (trailing newline included)."""
    return (
        f"中文字数: {result.chinese_chars}\n"
        f"英文词数: {result.english_words}\n"
        f"阅读时间: {result.reading_minutes} 分钟\n"
    )
