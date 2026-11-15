#!/usr/bin/env python3
"""本地 FunASR 转写：音频文件 → 带说话人/时间戳的纯文本。

用法:
    python transcribe_local.py <音频文件> <输出.txt> [--no-spk]

依赖: funasr（首次运行自动下载 paraformer-zh / fsmn-vad / ct-punc / cam++ 模型）。
    python3 -m venv ~/.funasr-venv && ~/.funasr-venv/bin/pip install -U funasr

说明:
    - 默认开说话人分离（cam++），输出按【说话人N】分段，适合多人播客。
    - 单人口播加 --no-spk 更快（跳过 cam++）。
    - 全中文口语准确率高；中英混说的英文专有名词可能音译错（Claude→cloud 等），
      交给下游 AI 轻校对修正。
"""
import sys
import time
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio", help="输入音频文件（wav/mp3/m4a/aac 等）")
    ap.add_argument("output", help="输出 txt 路径")
    ap.add_argument("--no-spk", action="store_true", help="关闭说话人分离（单人口播用，更快）")
    args = ap.parse_args()

    from funasr import AutoModel

    kw = dict(model="paraformer-zh", vad_model="fsmn-vad",
              punc_model="ct-punc", disable_update=True)
    if not args.no_spk:
        kw["spk_model"] = "cam++"

    t0 = time.time()
    model = AutoModel(**kw)
    print(f"[funasr] 模型加载 {time.time() - t0:.1f}s", file=sys.stderr)

    t1 = time.time()
    res = model.generate(input=args.audio, batch_size_s=300, sentence_timestamp=True)
    print(f"[funasr] 转写完成 {time.time() - t1:.1f}s", file=sys.stderr)

    r = res[0]
    si = r.get("sentence_info", [])

    # 按连续说话人聚合成段
    segments = []
    cur_spk, buf = None, []
    for s in si:
        spk = s.get("spk")
        if spk != cur_spk and buf:
            segments.append((cur_spk, "".join(buf)))
            buf = []
        cur_spk = spk
        buf.append(s["text"])
    if buf:
        segments.append((cur_spk, "".join(buf)))

    if segments:
        multi = len({spk for spk, _ in segments if spk is not None}) > 1
        lines = []
        for spk, text in segments:
            prefix = f"【说话人{spk}】" if (multi and spk is not None) else ""
            lines.append(prefix + text)
        body = "\n\n".join(lines)
    else:
        body = r.get("text", "")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(body)
    print(f"[funasr] 已写入 {args.output}（{len(body)} 字，{len(segments)} 段）", file=sys.stderr)


if __name__ == "__main__":
    main()
