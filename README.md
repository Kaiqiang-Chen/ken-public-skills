# ken-public-skills

Ken 的公开 agent skills 集合。这里只收录选择公开发布的技能。

This repository is Ken's public collection of agent skills chosen for public release.

## 布局

技能目录为 `skills/<skill-id>/`。

**podcast-transcribe 3.1**：把播客链接、RSS、播客名称或本地音频整理成结构化精华版、原文润色版和原文无润色版。

- 技能路径：[skills/podcast-transcribe](https://github.com/Kaiqiang-Chen/ken-public-skills/tree/main/skills/podcast-transcribe)

**ai-interview-prep**：AI 面试陪练：结合岗位 JD 与简历，60 分钟内挖经历、模拟追问、产出一页面试提纲。

- 技能路径：[skills/ai-interview-prep](https://github.com/Kaiqiang-Chen/ken-public-skills/tree/main/skills/ai-interview-prep)

**interview-organizer**：面试录音整理与复盘：本地转写录音，生成润色版面试原文和逐题面试分析。

- 技能路径：[skills/interview-organizer](https://github.com/Kaiqiang-Chen/ken-public-skills/tree/main/skills/interview-organizer)
- 转写依赖用户另行安装的本地音频转写 skill（例如 faster-whisper / MLX Whisper）。

## 使用

把 [`skills/podcast-transcribe`](skills/podcast-transcribe) 复制或克隆到 agent 的 skills 目录，然后按其中的 [`SKILL.md`](skills/podcast-transcribe/SKILL.md) 使用。
