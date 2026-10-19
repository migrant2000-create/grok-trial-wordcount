# grok-trial-wordcount

`wordcount` 是一个命令行工具，用来统计文本里的中文字符数和英文单词数，并估算阅读时间（分钟）。支持从文件或标准输入读取 UTF-8 文本，运行时只依赖 Python 标准库，需要 Python 3.10 及以上。

## 安装

```bash
pip install .
```

安装完成后即可使用控制台命令 `wordcount`。

开发时可以连同测试依赖一起安装：

```bash
pip install -e ".[dev]"
pytest
```

## 用法

### 从文件读取

准备文件 `article.txt`，内容为：

```text
你好，世界！This is a well-known example. Don't skip it.
```

运行：

```bash
wordcount article.txt
```

输出：

```text
中文字数: 4
英文词数: 8
阅读时间: 1 分钟
```

### 从标准输入读取

```bash
cat article.txt | wordcount
```

也可以直接用管道：

```bash
echo "你好 world" | wordcount
```

输出：

```text
中文字数: 2
英文词数: 1
阅读时间: 1 分钟
```

不传路径时从标准输入读取。文件不存在时，程序会在标准错误输出说明原因，并以非零状态码退出。

## 计数规则

- **中文字符**：只统计汉字，即 CJK 统一表意文字及常见扩展区（扩展 A–I，含扩展 G、H）。标点、数字和空白不计入。
- **英文单词**：连续的 ASCII 字母算作一个单词。像 `don't`、`well-known` 这样的缩写和连字符词，每个算一个单词。
- **阅读时间**：先计算 `中文字符数 / 300 + 英文单词数 / 200`，再向上取整为整分钟。空文本，或没有任何可计数内容时，阅读时间为 0 分钟。
