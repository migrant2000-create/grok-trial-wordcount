"""Allow ``python -m wordcount``."""

from wordcount.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
