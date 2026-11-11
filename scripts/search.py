#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按角色/场景/画幅/关键词检索配方。用法：python scripts/search.py --role 知更鸟晴歌 --scene 沙发 --limit 3"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "data_recipes.json"), encoding="utf-8"))["recipes"]


def score(r, a):
    s = 0
    if a.role and a.role in r["role"]: s += 4
    if a.scene and a.scene in r["scene"]: s += 3
    if a.ratio and a.ratio.replace(" ", "") == r["ratio"].replace(" ", ""): s += 2
    if a.series and a.series in r["series"]: s += 2
    if a.q:
        blob = " ".join([r["title"], r["role"], r["scene"], r["series"], " ".join(r["tags"]), r["prompt"]])
        for kw in a.q.split():
            if kw in blob: s += 1
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", default=""); ap.add_argument("--scene", default="")
    ap.add_argument("--ratio", default=""); ap.add_argument("--series", default="")
    ap.add_argument("--q", default=""); ap.add_argument("--limit", type=int, default=3)
    a = ap.parse_args()
    rows = sorted(((score(r, a), r) for r in DATA), key=lambda x: -x[0])
    rows = [(s, r) for s, r in rows if s > 0][: a.limit] or [(0, r) for r in DATA[: a.limit]]
    for s, r in rows:
        print(f"## {r['id']} · {r['title']}  (匹配分 {s})")
        print(f"角色：{r['role']}｜场景：{r['scene']}｜画幅：{r['ratio']} → {r['chatgpt_size']}")
        print("```text"); print(r["prompt"]); print("```")
        if r["negative"]:
            print("负面词（需改写为正向约束）：" + r["negative"])
        print()


if __name__ == "__main__":
    main()
