#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验数据文件结构与一致性（CI 用）。"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQ = {"id", "title", "role", "series", "scene", "ratio", "chatgpt_size", "tags", "prompt", "negative", "character"}
OK_CHAT = {"1024×1536（竖幅）", "1024×1536（竖幅，最接近 2:3）", "1536×1024（横幅）", "1024×1024"}


def main():
    r = json.load(open(os.path.join(ROOT, "data_recipes.json"), encoding="utf-8"))
    c = json.load(open(os.path.join(ROOT, "data_characters.json"), encoding="utf-8"))
    errs = []
    ids = set()
    for x in r["recipes"]:
        miss = REQ - set(x)
        if miss: errs.append(f"{x.get('id')} 缺字段 {miss}")
        if x["id"] in ids: errs.append(f"重复 id {x['id']}")
        ids.add(x["id"])
        if x["chatgpt_size"] not in OK_CHAT: errs.append(f"{x['id']} 尺寸非法 {x['chatgpt_size']}")
        if len(x["prompt"]) < 20: errs.append(f"{x['id']} 提示词过短")
    slugs = {x["slug"] for x in c["characters"]}
    for x in r["recipes"]:
        if x["character"] and x["character"] not in slugs: errs.append(f"{x['id']} 角色不存在 {x['character']}")
    for x in c["characters"]:
        if len(x.get("anchors", [])) < 2: errs.append(f"{x['slug']} 锚点不足")
    print("recipes:", len(r["recipes"]), "| characters:", len(c["characters"]))
    for e in errs[:20]: print("  ❌", e)
    print("结论：", "通过" if not errs else f"{len(errs)} 个问题")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
