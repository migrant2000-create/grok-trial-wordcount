"""Command-line interface for wordcount."""

from __future__ import annotations

import argparse
import sys

from wordcount.count import count_text, format_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="统计中文字符数、英文单词数，并估算阅读时间（秒）。",
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="UTF-8 文本文件路径；省略时从标准输入读取",
    )
    return parser


def _read_stdin() -> str:
    return sys.stdin.buffer.read().decode("utf-8")


def _read_path(path: str) -> str:
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        text = _read_stdin() if args.path is None else _read_path(args.path)
    except FileNotFoundError:
        print(f"wordcount: 找不到文件: {args.path}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        source = "标准输入" if args.path is None else args.path
        print(f"wordcount: 不是有效的 UTF-8: {source}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"wordcount: 无法读取文件 {args.path}: {exc}", file=sys.stderr)
        return 1

    sys.stdout.write(format_report(count_text(text)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
