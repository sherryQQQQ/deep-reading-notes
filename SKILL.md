---
name: deep-reading-notes
description: Analyze articles, papers, books, and reports; extract traceable quotations; classify reading material; and create linked, reusable notes. Use for deep reading, literature notes, reading highlights, source comparison, knowledge-base intake, or turning source material into notes. Do not use for pure copyediting or document formatting.
---

# Deep Reading Notes

把材料转成可核查、可复用的理解与笔记。以来源为准，明确区分原文、转述和推断。

## 路由

只读取当前任务需要的参考文件；不要预载全部资料。

- 理解、批判、比较或应用材料：读 [references/analysis.md](references/analysis.md)。
- 查找或整理原文摘录：读 [references/excerpts.md](references/excerpts.md)。
- 给材料或笔记分类、打标签：读 [references/taxonomy.md](references/taxonomy.md)。
- 创建原子笔记、文献笔记或连接旧笔记：读 [references/notes.md](references/notes.md)。
- 材料很长、包含多份文件或超出当前上下文：再读 [references/long-sources.md](references/long-sources.md)。

组合请求按依赖顺序执行，例如“深读并做笔记”为：分析 → 摘录 → 笔记；仅加载这三个参考文件。

## 工作约束

1. 先确认阅读目标、来源范围和用户要求的交付物。缺少非关键偏好时采用默认值继续；缺少材料本身时才询问。
2. 先建立来源地图，再形成结论。保留页码、章节、段落、时间戳或稳定 URL 等定位信息；无法定位时标注 `locator: unavailable`。
3. 引号必须逐字来自来源。压缩或改写时标为“转述”；超出来源的判断标为“推断”。不要补写看似合理的引文或页码。
4. 只在用户要求保存、创建或更新笔记时写文件。不得把“分析”自动扩大为知识库写入。
5. 若用户已有目录、标签体系、命名规则或模板，优先沿用；不要并行发明第二套结构。
6. 输出语言跟随用户；术语首次出现时可保留原文。

## Token 预算

默认使用最小充分分析，不把所有框架套一遍。

- `quick`：核心问题、3–5 个要点、1 个保留意见；适合速览。
- `standard`（默认）：论证骨架、关键证据、盲点、可复用笔记；通常只选 1–2 个分析框架。
- `deep`：多框架、反例、跨来源或系统关系；仅在用户明确要求深度或材料价值足够高时使用。

节省上下文的规则：

- 不在“摘要、要点、结论”中重复同一内容；每条信息只放在最有用的位置。
- 只摘录支撑结论、定义概念或值得保留措辞的句子；其余用带定位的转述。
- 长文先做章节级索引，再读取相关片段；不要反复载入整份材料。
- 中间状态使用紧凑字段：`source_id / locator / claim / evidence / confidence / tags`。
- 用户没指定数量时，优先少而精：5–8 条摘录、3–7 条标签、1–5 个原子笔记。

## 默认交付

当用户只说“分析这篇”时，提供：

1. 一句话主旨
2. 论证或内容结构
3. 最重要的洞见与证据
4. 不确定性、反例或局限
5. 值得保留的少量摘录（含定位）
6. 可行动的问题或下一步

不要把模板中的空栏目输出给用户。

## 持久化笔记

需要在本地创建独立 Markdown 笔记时，先按 [references/notes.md](references/notes.md) 生成紧凑 JSON，再运行：

```bash
python3 scripts/render_note.py --input note.json --output-dir /path/to/notes
```

脚本只负责稳定命名和格式化；内容判断仍应基于来源。写入前检查目标目录与同名文件，脚本默认不覆盖已有笔记。
