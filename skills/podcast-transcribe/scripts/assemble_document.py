#!/usr/bin/env python3
"""Assemble structured, polished and raw podcast versions into one Markdown document."""

import argparse
from datetime import date
from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding='utf-8').strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--podcast', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--duration', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--engine', required=True)
    parser.add_argument('--structured', required=True)
    parser.add_argument('--polished', required=True)
    parser.add_argument('--raw', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    structured = read(args.structured)
    polished = read(args.polished)
    raw = read(args.raw)
    if not structured or not polished or not raw:
        raise SystemExit('structured, polished and raw inputs must all be non-empty')

    doc = f'''---
播客: {args.podcast}
单集: {args.title}
时长: {args.duration}
转写日期: {date.today().isoformat()}
来源: {args.source}
转写引擎: {args.engine}
工具: podcast-transcribe skill
---

# {args.title}

> 阅读说明：本文包含结构化精华版、原文润色版和原文无润色版。

原始节目：[节目链接]({args.source})

## 结构化精华版

{structured}

## 原文润色版

> 编辑说明：保留完整信息，只做可读性编辑。说话人统一写作 **【姓名】**，不用「姓名：」。

{polished}

## 原文无润色版

> 存档说明：以下为转写引擎初始输出。

{raw}
'''
    Path(args.output).write_text(doc, encoding='utf-8')
    print(f'written={args.output} chars={len(doc)}')


if __name__ == '__main__':
    main()
