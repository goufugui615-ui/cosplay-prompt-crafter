#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 SKILL.md frontmatter（无第三方依赖）：安装/上传前跑一下。"""
import os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(HERE, "SKILL.md")


def main():
    raw = open(SKILL, "rb").read()
    errs, warns = [], []
    if raw.startswith(b"\xef\xbb\xbf"):
        errs.append("文件带 UTF-8 BOM，会被解析器当成内容")
    text = raw.decode("utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        errs.append("必须以 --- 开头（第一行）")
    parts = text.split("---\n", 2)
    if len(parts) < 2:
        errs.append("找不到 frontmatter 结束标记 ---")
    fm = parts[1] if len(parts) > 1 else ""
    if "name:" not in fm: errs.append("缺少 name 字段")
    if "description:" not in fm: errs.append("缺少 description 字段")
    m = re.search(r"^name:\s*(.+)$", fm, re.M)
    if m:
        name = m.group(1).strip()
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            errs.append("name 必须是小写字母数字与连字符：" + name)
        if name != os.path.basename(HERE):
            warns.append("name 与目录名不一致（部分客户端要求一致）：%s != %s" % (name, os.path.basename(HERE)))
    # 纯量值里出现 ": " 是 YAML 常见错误（引号/块标量除外）
    for line in fm.splitlines():
        if ":" in line and not line.lstrip().startswith(("-", "#")):
            key, _, val = line.partition(":")
            if key.strip() in ("name", "license", "description") and ": " in val and not val.startswith((">", "|")):
                errs.append("字段 %s 的纯量值含「: 」，请用 >- 块标量或加引号" % key.strip())
    if "version:" in fm:
        warns.append("version 字段部分客户端不支持，建议写在正文里")
    print("== frontmatter 校验 ==")
    for e in errs: print("  ❌", e)
    for w in warns: print("  ⚠️", w)
    if not errs: print("  ✅ 通过")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
