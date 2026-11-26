# Shopee 马来站上品工作流

这套 Codex Skills 用于将 Shopee 马来站上品任务拆成可独立调用的步骤，覆盖英文刊登文案、商品图、定价与填价、上架审查和视频处理。适合需要反复处理不同商品和 SKU 的跨境卖家。

## 安装和使用

1. 在 GitHub 选择 **Code → Download ZIP**，或克隆本仓库。
2. 将 `skills/` 下要使用的 Skill 目录整体复制到目标项目的 `.agents/skills/`。如果想在多个项目中使用，可放到用户主目录的 `.agents/skills/`，Windows 对应 `%USERPROFILE%\.agents\skills\`。同时复制该目录内的脚本和参考文件。
3. 从目标项目打开 Codex，输入 `$` 后选择对应 Skill，或者直接发送下表的示例指令。[Codex 官方 Skill 指南](https://learn.chatgpt.com/docs/build-skills)

| Skill | 当前版本 | 示例指令 |
| --- | --- | --- |
| [妙手商品文案优化](skills/miaoshou-listing-edit/SKILL.md) | 1.0.0 | 用 `$miaoshou-listing-edit` 为指定采集箱商品优化英文标题、描述和 SKU 名称，先给我可复制文本。 |
| [商品图英文翻译与验收](skills/product-image-localization/SKILL.md) | 1.0.0 | 用 `$product-image-localization` 把这批商品图改成英文并另存，逐张确认成品小于 2,000,000 字节。 |
| [Shopee 马来站按模板定价与填价](skills/shopee-my-pricing-fill/SKILL.md) | 1.0.0 | 用 `$shopee-my-pricing-fill` 按我的定价模板计算各规格 RM 售价，填完逐项回读，停在确认发布前。 |
| [Shopee 马来站上架审查](skills/shopee-my-listing-review/SKILL.md) | 1.0.0 | 用 `$shopee-my-listing-review` 只读检查指定商品，逐 SKU 列出合规风险、买家展示问题和成本利润率。 |
| [商品视频处理](skills/product-video-processing/SKILL.md) | 0.1.0 | 用 `$product-video-processing` 替换这条商品视频的中文字幕与旁白，导出后完整播放验收。 |

## 运行条件

- 文案和审查可使用商品事实、截图或导出文件。实际修改后台时，需要可操作的浏览器和已登录的对应账号，并按本次指令执行填写、保存或发布。
- 定价请提供当前工作簿和商品规格。定价模板、店铺数据及实物素材由使用者自行提供。适用费率、发布规则和字段以本次站点及后台所示为准。
- 图片大小校验和利润算术脚本使用 Python 3。视频处理可使用 FFmpeg、ffprobe 或等效工具，以及可用的英文配音工具。视频 Skill 为试用版，完整成片交付仍待实测。

常用顺序是准备文案与素材、审查合规与成本、计算和填写售价，最后从买家视角复核展示。各版本以对应 `SKILL.md` 的 `metadata.version` 为准。
