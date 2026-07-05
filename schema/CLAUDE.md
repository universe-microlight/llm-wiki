# LLM Wiki Schema — AI 行为规范

## 项目定位

这是一个**长期知识工程项目**，目标是通过持续积累和交叉引用，在 10 年时间跨度内构建一个可精确检索的知识体系。

当前焦点领域：**下一代芯片架构**（从散热问题切入，探索原子/粒子层面的计算范式）

## 核心原则

1. **准确性优先** — 有疑问标注 `[待验证]`
2. **交叉引用** — 用 `[[页面名]]` 建立知识关联
3. **来源追溯** — 每条信息注明来源
4. **中立客观** — 呈现多方观点
5. **持续更新** — 新信息整合到现有体系

## ⚡ Token 节省策略（核心）

长期项目最大的敌人是上下文膨胀。必须严格遵守：

### 1. 知识三角：Discussion → Wiki → Memory

```
讨论中产生 → 提炼存入 wiki → 精华写入 memory
  (临时)        (结构化)         (永久索引)
```

- **讨论层**：对话内容不存 wiki，只在讨论结束后提炼关键结论
- **Wiki 层**：结构化知识页，每页聚焦一个概念/实体/方案
- **Memory 层**：MEMORY.md 只存项目级元信息（进度、决策、方向变化）

### 2. 分层加载策略

讨论新话题时，按需加载，不要全量读取：

| 场景 | 加载什么 | 不加载什么 |
|------|---------|-----------|
| 全新方向 | roadmap.md + 相关 overview | 具体 concept 页 |
| 深入已有方向 | 相关 concept 页 + comparison | 其他方向的页 |
| 对比方案 | comparison 页 + 各方案 concept | overview |
| 回顾进展 | roadmap.md + log.md 最近几条 | 具体技术细节 |

### 3. 摘要即入口

每个页面的第一段（frontmatter 的 description + 第一个 H2 前的文字）必须是**自包含摘要**（<100字），AI 只读这段就能判断是否需要深入。

### 4. 页面粒度原则

- **一个页面 = 一个概念/方案/实体**
- 如果一个页面超过 2000 字，考虑拆分
- 对比类内容用 comparison 页面，不要塞进概念页
- 每个页面必须有 `tags`，tags 是快速过滤的关键

## 目录结构

```
llm-wiki/
├── raw/                    # 原始资料（不可变）
│   ├── papers/
│   ├── articles/
│   └── notes/
├── wiki/                   # 结构化知识库
│   ├── index.md            # 主索引
│   ├── log.md              # 变更日志
│   ├── roadmap.md          # 项目路线图
│   ├── concepts/           # 概念页（一个概念一页）
│   ├── entities/           # 实体页（公司、团队、产品）
│   ├── solutions/          # 方案页（技术方案详细描述）
│   ├── comparisons/        # 对比页（多方案横向对比）
│   └── overviews/          # 概述页（领域全景）
├── schema/                 # 配置
│   ├── CLAUDE.md           # 本文件
│   └── okf.yaml
└── scripts/                # 工具
    ├── ingest.py
    ├── search.py
    └── lint.py
```

### 新增目录说明

- **solutions/** — 区别于 concepts（纯概念解释），solutions 存放具体的技术方案，包含实验数据、进展状态、可行性评估
- **roadmap.md** — 项目级路线图，记录阶段目标、里程碑、方向调整决策

## 页面类型

| 类型 | 存放位置 | 用途 | 典型大小 |
|------|---------|------|---------|
| concept | concepts/ | 解释一个概念/原理 | 500-1500字 |
| entity | entities/ | 公司/团队/产品/人 | 300-800字 |
| solution | solutions/ | 具体技术方案详情 | 1000-2000字 |
| comparison | comparisons/ | 多方案横向对比 | 800-1500字 |
| overview | overviews/ | 领域全景概述 | 1000-2000字 |
| index | wiki/ 根目录 | 索引/日志/路线图 | 不限 |

## 工作流程

### 导入新知识

1. 提炼讨论结论（不要照搬对话）
2. 判断页面类型（concept/solution/comparison/overview）
3. 检查是否已有相关页面 → 有则更新，无则新建
4. 建立交叉引用 `[[页面名]]`
5. 更新 index.md 和 log.md

### 查询知识

1. 先读 roadmap.md 了解当前阶段
2. 用 tags 和 description 快速定位相关页面
3. 只深入读取直接相关的页面
4. 用 comparison 页面做方案对比

## 写作规范

### Frontmatter 必填字段

```yaml
---
type: concept|entity|solution|comparison|overview
title: 页面标题
description: 一句话摘要（<100字，自包含）
tags: [tag1, tag2, tag3]
timestamp: 2026-07-05T20:00:00+08:00
status: active|draft|archived
---
```

### 可选字段

```yaml
related: [page-slug-1, page-slug-2]  # 关联页面
source: "来源描述"                     # 信息来源
maturity: concept|lab|prototype|production  # 技术成熟度
updated: 2026-07-05                   # 最后更新日期
```

### 交叉引用

- 内部引用：`[[页面名]]` 或 `[[页面名|显示文本]]`
- 同一讨论中产生的多个页面，必须互相引用
- 新页面必须引用已有的相关页面

## 质量检查

- 死链检查：`[[页面名]]` 必须指向存在的文件
- 孤立检查：每个页面至少被一个其他页面引用
- 过期标记：超过 6 个月未更新的页面标 `[过期]`
- 粒度检查：单页超 2000 字时建议拆分
