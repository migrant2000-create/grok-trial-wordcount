"""CLI tests: file input, stdin, and missing files."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from wordcount.count import count_text, format_report

_SRC = Path(__file__).resolve().parents[1] / "src"


def _run(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(
        [str(_SRC), env["PYTHONPATH"]] if env.get("PYTHONPATH") else [str(_SRC)]
    )
    return subprocess.run(
        [sys.executable, "-m", "wordcount", *args],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        env=env,
    )


def test_cli_reads_file(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    text = "你好，世界！This is a well-known example. Don't skip it.\n"
    sample.write_text(text, encoding="utf-8")

    result = _run(str(sample))

    assert result.returncode == 0
    assert result.stderr == ""
    assert result.stdout == format_report(count_text(text))
    assert "中文字数: 4\n" in result.stdout
    assert "英文词数: 8\n" in result.stdout
    assert "阅读时间: 0 秒\n" in result.stdout


def test_cli_reads_stdin() -> None:
    result = _run(stdin="你好 world\n")

    assert result.returncode == 0
    assert result.stdout == "中文字数: 2\n英文词数: 1\n阅读时间: 0 秒\n"


def test_cli_missing_file() -> None:
    result = _run("no-such-file-wordcount.txt")

    assert result.returncode != 0
    assert "no-such-file-wordcount.txt" in result.stderr
    assert result.stdout == ""


def test_cli_empty_stdin() -> None:
    result = _run(stdin="")

    assert result.returncode == 0
    assert result.stdout == "中文字数: 0\n英文词数: 0\n阅读时间: 0 秒\n"
