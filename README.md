# Deep Reading Notes

一个面向 Codex 的深度阅读与知识笔记 skill。它可以分析文章、论文、书籍和报告，整理可追溯摘录，为材料分类，并把重要观点转成可连接、可复用的 Markdown 笔记。

这个项目参考了深度阅读分析类 skill 的工作方式，并增加了摘录、分类、原子笔记、长文处理和 Token 预算控制。

## 功能

- 三档阅读深度：`quick`、`standard`、`deep`
- 论证结构、证据质量、假设、局限与应用分析
- SCQA、5W2H、批判性思维、第一性原理、系统思维和逆向思维
- 带页码、章节、段落、时间戳或 URL 的可追溯摘录
- 领域、主题、材料类型、笔记类型和阅读状态分类
- Source、Literature、Concept、Claim、Question、Evergreen 六类笔记
- 面向书籍和多文件材料的分块阅读与证据台账
- 从紧凑 JSON 安全生成 Markdown 笔记，默认不覆盖已有文件

## Token 设计

Skill 使用渐进式加载：`SKILL.md` 只负责识别任务和路由，执行时只读取当前模式需要的参考文件。

例如：

- 只做摘要：加载 `analysis.md`
- 整理高亮：加载 `excerpts.md`
- 给资料分类：加载 `taxonomy.md`
- 创建笔记：加载 `notes.md`
- 处理整本书：在对应模式之外增加 `long-sources.md`

标准分析通常只选择 1–2 个真正能改变结论的框架，不会机械套用全部模型，也不会在摘要、要点和结论中重复同一内容。

## 安装

```bash
git clone https://github.com/sherryQQQQ/deep-reading-notes.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/deep-reading-notes"
```

如果已经克隆过仓库，可以这样更新：

```bash
git -C "${CODEX_HOME:-$HOME/.codex}/skills/deep-reading-notes" pull
```

重新打开 Codex 会话后即可调用：

```text
$deep-reading-notes
```

## 使用示例

### 快速理解

```text
使用 $deep-reading-notes 快速分析这篇文章，给出一句话主旨、5 个要点和一个待验证问题。
```

### 深读一本书

```text
使用 $deep-reading-notes 深读这本书。先建立章节地图，再总结核心论点、证据、局限和可复用概念，并保留页码。
```

### 摘录

```text
使用 $deep-reading-notes 从这篇论文中选出 8 条最值得保留的原文摘录，记录页码、上下文、价值和标签。
```

### 分类

```text
使用 $deep-reading-notes 给这个文件夹里的阅读材料分类。优先复用已有标签，并列出无法确定的项目。
```

### 创建知识笔记

```text
使用 $deep-reading-notes 把这份材料整理成一条文献笔记和最多 5 条原子笔记，并说明笔记之间的关系。
```

## 笔记生成脚本

`scripts/render_note.py` 可以把模型生成的紧凑 JSON 转成具有稳定元数据的 Markdown 文件。

输入示例：

```json
{
  "title": "官僚制通过可预测规则扩大协调规模",
  "note_type": "evergreen",
  "source_id": "weber-politics-as-a-vocation",
  "locators": ["p. 161"],
  "tags": ["社会学/官僚制", "政治社会学"],
  "status": "processed",
  "body": "核心陈述……\n\n## 证据\n……"
}
```

生成笔记：

```bash
python3 scripts/render_note.py \
  --input note.json \
  --output-dir /path/to/notes
```

如果目标文件已经存在，脚本会停止并报错，不会覆盖原笔记。

## 目录结构

```text
deep-reading-notes/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── analysis.md
│   ├── excerpts.md
│   ├── long-sources.md
│   ├── notes.md
│   └── taxonomy.md
└── scripts/
    └── render_note.py
```

## 准确性原则

- 原文、转述和推断必须明确区分。
- 引文必须能够回到来源核对，不补写引文或页码。
- 优先沿用用户已有的目录、标签和笔记模板。
- 只有用户明确要求保存或更新笔记时才写入文件。
- 对长材料先建立章节地图，再读取与目标相关的部分。

## 适用范围

适合深度阅读、论文分析、读书笔记、资料归档、主题研究和个人知识库整理。纯文字润色、版式编辑或无来源依据的自由写作不属于这个 skill 的主要用途。
