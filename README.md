# cosplay-prompt-crafter

**真人 Coser 摄影 AI 出图提示词工坊** — 面向 ChatGPT（GPT Image）的提示词工程技能：59 套已验证配方、4 张角色锚点卡、镜头/光线/负面词库，附带检索、校验、变体生成脚本与评测集。

个人学习与创作参考；角色版权归原作者，禁止商用与二次分发。

## 安装

```bash
# Claude Code（个人级）
mkdir -p ~/.claude/skills && cp -r cosplay-prompt-crafter ~/.claude/skills/

# 项目级：<your-project>/.claude/skills/cosplay-prompt-crafter/
```

Claude.ai：把 `cosplay-prompt-crafter.zip` 上传到 Settings → Capabilities → Skills。

## 快速开始

```bash
python scripts/search.py --role 知更鸟晴歌 --scene 沙发      # 找配方
python scripts/lint_prompt.py --file my_prompt.txt --character robin-qingge   # 校验
python scripts/variants.py --recipe p01 --n 3                 # 生成变体
python scripts/validate_data.py && python evals/run_evals.py  # 数据与评测
```

## 结构

```
SKILL.md                    入口（路由 + 工作流 + 模板 + 合规红线）
data_recipes.json           59 套配方的结构化数据（含 ChatGPT 尺寸映射）
data_characters.json        4 张角色卡（含 3–5 个角色锚点）
references/recipes/         按角色拆分的配方文档 + _index.md
references/cameras.md       镜头机位速查
references/lighting.md      光线速查
references/negatives.md     负面词 → ChatGPT 正向约束对照
references/consistency.md   角色一致性方法
references/adapters/chatgpt.md  ChatGPT 尺寸/语法/多轮迭代规则
scripts/                    search / lint / variants / validate
evals/                      10 条评测用例 + 评分标准
```

## 更新配方

1. 编辑 `data_recipes.json`（保持 id 唯一）；
2. 重新生成 `references/recipes/*.md`（可手写，也可用站点构建脚本）；
3. 跑 `python scripts/validate_data.py`。

## License

个人学习与创作参考。角色与作品版权归原作者；禁止商用与二次分发。
