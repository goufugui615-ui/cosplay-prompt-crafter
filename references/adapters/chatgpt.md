# ChatGPT（GPT Image）适配规则

## 尺寸

| 你要的画幅 | ChatGPT 支持的尺寸 | 说明 |
| --- | --- | --- |
| 3:4 竖幅 | 1024×1536 | 最接近 2:3，视觉上更竖，建议主体居中偏上 |
| 9:16 手机比例 | 1024×1536 | ChatGPT 没有真正 9:16，出图后可在网站裁切 |
| 4:3 横幅 | 1536×1024 | 3:2 比例，接近 4:3 |
| 16:9 电影感 | 1536×1024 | 需要更宽可后期裁切 |

**做法**：在 prompt 第一段写 `portrait orientation 1024×1536` 或 `landscape 1536×1024`；不要依赖对话里"帮我改成 9:16"。

## 语法差异

- ❌ 不要：`--ar 3:4`、`(masterpiece:1.3)`、`[word|word]`、`negative prompt:` 字段
- ✅ 要：自然语言分段落（Subject / Pose / Scene / Lighting / Camera / Texture / Format）

## 多轮迭代（推荐节奏）

1. 第 1 轮：角色 + 服装 + 画幅（验证像不像）
2. 第 2 轮："keep the character and outfit identical; change only the scene to X"
3. 第 3 轮："change only the lighting to soft window light from camera left"
4. 需要换服装/场景时上传参考图，并明确"保持同一张脸与相同妆容"

## 常见问题

| 问题 | 解决 |
| --- | --- |
| 出图带文字/水印 | 加 `no text, no watermark, no logo`；避免在 prompt 里出现引号内文字 |
| 想要更真实 | 加 `photorealistic, shot on 85mm, natural skin texture`，去掉"插画/动漫" |
| 手还是崩 | 简化手势（手放身侧/扶栏杆），加五指与解剖约束 |
| 尺寸不对 | 明确写 `portrait orientation 1024×1536`；ChatGPT 仅支持 3 种尺寸 |
| 画风偏插画 | 删掉"art, illustration, anime"，加 `photograph, RAW photo` |
