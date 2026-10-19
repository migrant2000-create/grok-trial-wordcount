"""Unit tests for counting rules and reading-time rounding."""

from wordcount.count import count_text, reading_minutes


def test_pure_chinese() -> None:
    result = count_text("你好，世界！")
    assert result.chinese_chars == 4
    assert result.english_words == 0
    assert result.reading_minutes == 1


def test_pure_english() -> None:
    result = count_text("Hello, world!")
    assert result.chinese_chars == 0
    assert result.english_words == 2
    assert result.reading_minutes == 1


def test_mixed_chinese_and_english() -> None:
    result = count_text("你好 hello world")
    assert result.chinese_chars == 2
    assert result.english_words == 2
    assert result.reading_minutes == 1


def test_empty_input() -> None:
    result = count_text("")
    assert result.chinese_chars == 0
    assert result.english_words == 0
    assert result.reading_minutes == 0


def test_no_countable_content() -> None:
    result = count_text(" \n\t，。！？123456")
    assert result.chinese_chars == 0
    assert result.english_words == 0
    assert result.reading_minutes == 0


def test_contraction_and_hyphen_are_one_word() -> None:
    result = count_text("don't say well-known or mother-in-law")
    assert result.english_words == 5
    assert result.chinese_chars == 0


def test_extension_ideograph_counts_as_chinese() -> None:
    # U+20000 is in CJK Unified Ideographs Extension B.
    result = count_text("𠀀")
    assert result.chinese_chars == 1
    assert result.english_words == 0


def test_reading_time_rounds_up() -> None:
    assert reading_minutes(0, 0) == 0
    assert reading_minutes(1, 0) == 1
    assert reading_minutes(300, 0) == 1
    assert reading_minutes(301, 0) == 2
    assert reading_minutes(0, 200) == 1
    assert reading_minutes(0, 201) == 2
    # 150/300 + 100/200 = 1 exactly
    assert reading_minutes(150, 100) == 1
    # 151/300 + 100/200 = 1.0033... -> 2
    assert reading_minutes(151, 100) == 2
    # 150/300 + 101/200 = 1.005 -> 2
    assert reading_minutes(150, 101) == 2

    assert count_text("中" * 300).reading_minutes == 1
    assert count_text("中" * 301).reading_minutes == 2
    assert count_text(" ".join(["word"] * 200)).reading_minutes == 1
    assert count_text(" ".join(["word"] * 201)).reading_minutes == 2
