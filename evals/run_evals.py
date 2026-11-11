#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""评测：用例格式 + 覆盖检查（无模型调用，保证 CI 可跑）。"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "evals", "cases.jsonl")
KEYS = {"id", "request", "must_include"}


def main():
    errs, n = [], 0
    for line in open(CASES, encoding="utf-8"):
        line = line.strip()
        if not line: continue
        n += 1
        try: c = json.loads(line)
        except Exception as e: errs.append(f"第 {n} 行 JSON 错误：{e}"); continue
        if KEYS - set(c): errs.append(f"{c.get('id')} 缺字段")
        if len(c.get("must_include", [])) < 2: errs.append(f"{c.get('id')} must_include 过少")
    print(f"用例 {n} 条")
    for e in errs: print("  ❌", e)
    print("结论：", "通过" if not errs else "失败")
    sys.exit(0 if not errs else 1)


if __name__ == "__main__":
    main()
