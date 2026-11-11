#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验提示词：合规、ChatGPT 适配、角色锚点、构图要素。退出码 1 表示有错误。"""
import argparse, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARS = {c["slug"]: c for c in json.load(open(os.path.join(ROOT, "data_characters.json"), encoding="utf-8"))["characters"]}

FORBIDDEN = ["nude", "naked", "lingerie", "schoolgirl", "underage", "loli", "child", "teen", "偷拍", "未成年", "露点", "裸"]
MODEL_SYNTAX = [r"--ar\b", r"\([^)]*:\d+\.?\d*\)", r"negative prompt:", r"\[\w+\|\w+\]"]
SIZE_HINTS = ["1024×1536", "1536×1024", "1024x1536", "1536x1024", "1024×1024", "1024x1024"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--character", default="")
    a = ap.parse_args()
    text = open(a.file, encoding="utf-8").read()
    low = text.lower()
    errors, warns, oks = [], [], []

    def err(m): errors.append(m)
    def warn(m): warns.append(m)
    def ok(m): oks.append(m)

    if not (40 <= len(text) <= 2000): warn("长度 %d 字符，建议 100–1200" % len(text))
    else: ok("长度合适")

    adult = any(k in low for k in ["adult", "成年", "22-year", "20-year", "24-year", "25-year"])
    ok("成年表述") if adult else err("缺少成年表述（adult / 成年 / ≥20 岁）")
    cloth = any(k in low for k in ["fully clothed", "complete costume", "服装完整", "不裸露"])
    ok("服装完整约束") if cloth else err("缺少服装完整约束（fully clothed / 服装完整）")
    real = any(k in low for k in ["photorealistic", "photograph", "raw photo", "真实摄影"])
    ok("真实摄影词") if real else warn("建议加 photorealistic / photograph")

    for f in FORBIDDEN:
        if f in low:
            err("触发合规红线词：%s" % f)
    for pat in MODEL_SYNTAX:
        if re.search(pat, text):
            err("包含 Midjourney/SD 语法，ChatGPT 不支持：%s" % pat)
    if "negative prompt" in low or "负面词：" in text:
        warn("ChatGPT 无 negative prompt 字段，请改写为正向约束")

    if not any(s in text for s in SIZE_HINTS):
        warn("未写尺寸；建议 portrait orientation 1024×1536 或 landscape 1536×1024")
    else: ok("尺寸已指定")

    if not any(k in low for k in ["light", "光线", "window", "neon", "softbox"]):
        warn("缺少光线描述")
    if not any(k in low for k in ["lens", "mm", "camera", "镜头"]):
        warn("缺少镜头描述（mm / lens）")
    if not any(k in low for k in ["no text", "no watermark", "无水印", "no logo"]):
        warn("建议加 no text, no watermark")

    if a.character:
        c = CHARS.get(a.character)
        if not c:
            warn("未知角色 slug：%s" % a.character)
        else:
            hit = [x for x in c["anchors"] if any(tok in text for tok in re.split(r"[：:，,]", x) if len(tok) >= 2)]
            if len(hit) < 2:
                err("角色锚点不足（命中 %d 个，建议 ≥2）：%s" % (len(hit), "；".join(c["anchors"])))
            else:
                ok("角色锚点命中 %d 个" % len(hit))

    print("== 提示词校验 ==")
    for m in oks: print("  ✅", m)
    for m in warns: print("  ⚠️", m)
    for m in errors: print("  ❌", m)
    print("结论：%s（错误 %d / 警告 %d）" % ("通过" if not errors else "需修改", len(errors), len(warns)))
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
