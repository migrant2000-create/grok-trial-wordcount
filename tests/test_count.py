"""Unit tests for counting rules and reading-time rounding."""

from wordcount.count import count_text, reading_seconds


def test_pure_chinese() -> None:
    result = count_text("你好，世界！")
    assert result.chinese_chars == 4
    assert result.english_words == 0
    # 4 * 0.2s = 0.8s, nearer to 0 than to 10.
    assert result.reading_seconds == 0


def test_pure_english() -> None:
    result = count_text("Hello, world!")
    assert result.chinese_chars == 0
    assert result.english_words == 2
    # 2 * 0.3s = 0.6s, rounds to 0.
    assert result.reading_seconds == 0


def test_mixed_chinese_and_english() -> None:
    result = count_text("你好 hello world")
    assert result.chinese_chars == 2
    assert result.english_words == 2
    # 2 * 0.2s + 2 * 0.3s = 1.0s, rounds to 0.
    assert result.reading_seconds == 0


def test_empty_input() -> None:
    result = count_text("")
    assert result.chinese_chars == 0
    assert result.english_words == 0
    assert result.reading_seconds == 0


def test_no_countable_content() -> None:
    result = count_text(" \n\t，。！？123456")
    assert result.chinese_chars == 0
    assert result.english_words == 0
    assert result.reading_seconds == 0


def test_contraction_and_hyphen_are_one_word() -> None:
    result = count_text("don't say well-known or mother-in-law")
    assert result.english_words == 5
    assert result.chinese_chars == 0


def test_extension_ideograph_counts_as_chinese() -> None:
    # U+20000 is in CJK Unified Ideographs Extension B.
    result = count_text("𠀀")
    assert result.chinese_chars == 1
    assert result.english_words == 0


def test_reading_time_rounds_to_nearest_10_seconds() -> None:
    # 23 Han + 1 word = 4.6 + 0.3 = 4.9s, just below the 5s half.
    assert reading_seconds(23, 1) == 0
    # 25 Han = 5.0s exactly; halves round up to 10.
    assert reading_seconds(25, 0) == 10
    # 24 Han + 1 word = 4.8 + 0.3 = 5.1s, just above the half.
    assert reading_seconds(24, 1) == 10
    # 300 Han = 60s exactly, already a multiple of 10.
    assert reading_seconds(300, 0) == 60
    assert count_text("中" * 300).reading_seconds == 60
    assert reading_seconds(0, 0) == 0
