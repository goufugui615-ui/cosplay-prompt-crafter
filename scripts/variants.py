#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基于一条提示词生成 N 个可控变体（只改一个变量，角色锚点保持不变）。"""
import argparse, json, os, random, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPES = {r["id"]: r for r in json.load(open(os.path.join(ROOT, "data_recipes.json"), encoding="utf-8"))["recipes"]}

LIGHTS = ["soft window light from camera left, diffused daylight",
          "side backlight at 45°, warm rim light on hair",
          "large softbox 45° above subject, neutral gray background",
          "neon signs bokeh background, magenta and cyan practical lights",
          "direct on-camera flash, hard shadows, slightly overexposed highlights",
          "golden hour backlight, long shadows"]
SCENES = ["minimal studio with gray seamless backdrop", "cozy apartment by the window",
          "rainy street at night with reflections", "rooftop at dusk with city skyline",
          "traditional teahouse interior with wooden lattice", "underground parking with sodium lights"]
LENSES = ["35mm lens, waist-level, f/2.8", "50mm lens, eye-level, f/2.0",
          "85mm lens, eye-level slightly low, f/1.8", "24mm lens, low angle, f/2.8 (keep subject away from edges)"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recipe", default=""); ap.add_argument("--file", default="")
    ap.add_argument("--n", type=int, default=3); ap.add_argument("--axis", default="vary")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    base = ""
    if a.recipe:
        r = RECIPES.get(a.recipe)
        if not r: print("找不到配方", a.recipe); sys.exit(1)
        base = r["prompt"]
    elif a.file:
        base = open(a.file, encoding="utf-8").read()
    else:
        base = sys.stdin.read()
    if not base.strip(): print("缺少提示词"); sys.exit(1)
    random.seed(a.seed)
    for i in range(a.n):
        axis = a.axis if a.axis != "vary" else ["lighting", "scene", "lens"][i % 3]
        if axis == "lighting":
            add = "Lighting: " + random.choice(LIGHTS) + "."
        elif axis == "scene":
            add = "Scene: " + random.choice(SCENES) + "."
        else:
            add = "Camera: " + random.choice(LENSES) + "."
        print(f"## 变体 {i+1}（改动：{axis}）")
        print("```text"); print(base.strip() + "\n" + add); print("```")
        print()


if __name__ == "__main__":
    main()
