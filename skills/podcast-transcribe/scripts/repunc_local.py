#!/usr/bin/env python3
"""Restore punctuation while preserving every FunASR speaker turn boundary."""

import argparse
import re
from pathlib import Path

PUNCT = '，。！？；：、,.!?;:“”"（）()《》【】'
KEEP_DOUBLE = {'谢谢', '刚刚', '慢慢', '好好', '往往', '常常', '仅仅', '人人'}


def collapse_stutter(text: str) -> str:
    def repl(match):
        char = match.group(1)
        return char * (2 if char * 2 in KEEP_DOUBLE else 1)
    return re.sub(r'([\u4e00-\u9fff])\1+', repl, text)


def clean_source(text: str) -> str:
    text = re.sub(f'[{re.escape(PUNCT)}]+', '', text)
    text = collapse_stutter(text)
    text = re.sub(r'[呃嗯]+', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def split_chunks(text: str, size: int) -> list[str]:
    chunks = []
    start = 0
    while len(text) - start > size:
        low = start + int(size * 0.8)
        high = start + size
        cut = text.rfind(' ', low, high)
        if cut < start:
            cut = high
        chunks.append(text[start:cut].strip())
        start = cut + (1 if cut < len(text) and text[cut] == ' ' else 0)
    if start < len(text):
        chunks.append(text[start:].strip())
    return [chunk for chunk in chunks if chunk]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--chunk-size', type=int, default=2200)
    args = parser.parse_args()

    from funasr import AutoModel

    raw = Path(args.input).read_text(encoding='utf-8')
    parts = re.split(r'(【[^】]+】)', raw)
    turns = []
    current = ''
    for part in parts:
        if not part:
            continue
        if re.fullmatch(r'【[^】]+】', part):
            current = part
            continue
        clean = clean_source(part)
        if not clean:
            continue
        if turns and turns[-1][0] == current:
            turns[-1] = (current, turns[-1][1] + ' ' + clean)
        else:
            turns.append((current, clean))

    model = AutoModel(model='ct-punc', disable_update=True)
    punctuated_turns = []
    for owner, body in turns:
        punctuated = ''.join(
            model.generate(input=chunk)[0].get('text', '').strip()
            for chunk in split_chunks(body, args.chunk_size)
        )
        punctuated_turns.append((owner, punctuated))

    output = '\n\n'.join(owner + body for owner, body in punctuated_turns).strip() + '\n'
    Path(args.output).write_text(output, encoding='utf-8')
    print(f'written={args.output} chars={len(output)} turns={len(punctuated_turns)}')


if __name__ == '__main__':
    main()
