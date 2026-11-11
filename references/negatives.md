# 负面约束（ChatGPT 没有 negative prompt 字段）

GPT Image 不接受 `negative prompt`，所有"不要"都要写成**正向描述**：

| 想避免 | 错误写法 | ChatGPT 写法 |
| --- | --- | --- |
| 手畸形 | negative: bad hands | correct anatomy, five fingers per hand, natural hand pose |
| 塑料皮肤 | negative: plastic skin | realistic skin texture, visible pores, subtle skin imperfections |
| 动漫感 | negative: anime | photorealistic photography, real human proportions |
| 文字/水印 | negative: watermark | clean image, no text, no watermark, no logo |
| 裸露 | negative: nude | fully clothed, complete costume, modest styling |
| 画面过曝 | negative: overexposed | balanced exposure, preserved highlight detail |
| 杂物/路人 | negative: crowd | empty background, minimal props, clean composition |
| 广角畸变 | negative: distortion | 50–85mm lens, natural perspective, no wide-angle distortion |
| 过度磨皮 | negative: airbrushed | natural skin with light retouching only |

## 用脚本兜底

`python scripts/lint_prompt.py --file p.txt --character robin-qingge`
会检查：成年/服装/真实感/尺寸/畸形约束/合规词/负面词误用。
