# -*- coding: utf-8 -*-
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(args, stdin=None):
    return subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True, input=stdin)


def test_validate_data():
    r = run(["scripts/validate_data.py"])
    assert r.returncode == 0, r.stdout + r.stderr


def test_evals():
    r = run(["evals/run_evals.py"])
    assert r.returncode == 0, r.stdout + r.stderr


def test_search():
    r = run(["scripts/search.py", "--role", "知更鸟晴歌", "--limit", "2"])
    assert r.returncode == 0 and "知更鸟晴歌" in r.stdout


def test_lint_ok(tmp_path=None):
    p = os.path.join(ROOT, "tests", "_tmp_prompt.txt")
    open(p, "w", encoding="utf-8").write(
        "Photorealistic cosplay photography of Robin, a 22-year-old East Asian adult woman, fully clothed, "
        "blue hair, silver accessories, portrait orientation 1024×1536, soft window light, 85mm lens, "
        "realistic skin texture, no text, no watermark.")
    r = run(["scripts/lint_prompt.py", "--file", p])
    os.remove(p)
    assert r.returncode == 0, r.stdout
