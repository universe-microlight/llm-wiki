# LLM Wiki Schema — AI 行为规范

## 项目定位

这是一个**长期知识工程项目**，支持多领域并行积累，目标是通过结构化的知识管理，在任意时间跨度内构建可精确检索的知识体系。

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
- **Wiki 层**：结构化知识页，按领域分区存放
- **Memory 层**：MEMORY.md 只存项目级元信息（进度、决策、方向变化）

### 2. 分层加载策略

讨论新话题时，按需加载，不要全量读取：

| 场景 | 加载什么 | 不加载什么 |
|------|---------|-----------|
| 全新领域 | roadmap.md + 该领域 overview | 其他领域 |
| 深入已有领域 | 相关 concept/solution + comparison | 其他领域 |
| 跨领域讨论 | 相关领域的交集 + shared/ | 不相关的领域 |
| 回顾进展 | roadmap.md + log.md 最近几条 | 具体技术细节 |

### 3. 领域分区

```
wiki/domains/
├── _template/          # 新领域模板
├── chip-architecture/  # 领域A
├── quant-trading/      # 领域B
└── <future-domain>/    # 未来新领域
```

- 每个领域内部结构统一：concepts/ solutions/ comparisons/ entities/ overviews/
- 讨论时根据话题自动判断领域，只加载该领域页面
- 跨领域知识放 `shared/`

### 4. 摘要即入口

每个页面的第一段（frontmatter 的 description + 第一个 H2 前的文字）必须是**自包含摘要**（<100字），AI 只读这段就能判断是否需要深入。

### 5. 页面粒度原则

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
│   ├── roadmap.md          # 全局路线图
│   ├── domains/            # 按领域分区
│   │   ├── _template/      # 新领域模板
│   │   └── <domain>/       # 各领域
│   │       ├── concepts/
│   │       ├── solutions/
│   │       ├── comparisons/
│   │       ├── entities/
│   │       └── overviews/
│   └── shared/             # 跨领域共享
│       ├── concepts/
│       └── entities/
├── schema/                 # 配置
│   ├── CLAUDE.md           # 本文件
│   └── okf.yaml
└── scripts/                # 工具
    ├── ingest.py
    ├── search.py
    └── lint.py
```

## 页面类型

| 类型 | 存放位置 | 用途 | 典型大小 |
|------|---------|------|---------|
| concept | domains/<d>/concepts/ | 解释一个概念/原理 | 500-1500字 |
| entity | domains/<d>/entities/ | 公司/团队/产品/人 | 300-800字 |
| solution | domains/<d>/solutions/ | 具体技术方案详情 | 1000-2000字 |
| comparison | domains/<d>/comparisons/ | 多方案横向对比 | 800-1500字 |
| overview | domains/<d>/overviews/ | 领域全景概述 | 1000-2000字 |
| shared | shared/ | 跨领域通用知识 | 不限 |

## 工作流程

### 新增领域

1. `cp -r wiki/domains/_template wiki/domains/<领域名>`
2. 在 `roadmap.md` 添加领域入口
3. 创建该领域的 overview 入口页

### 导入新知识

1. 判断话题属于哪个领域
2. 提炼讨论结论（不要照搬对话）
3. 判断页面类型（concept/solution/comparison/overview）
4. 检查是否已有相关页面 → 有则更新，无则新建
5. 建立交叉引用 `[[页面名]]`
6. 更新 index.md 和 log.md

### 查询知识

1. 先读 roadmap.md 确认当前阶段
2. 根据话题定位领域
3. 用 tags 和 description 快速过滤
4. 只深入读取直接相关的页面

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
- 跨领域引用：`[[domains/other-domain/concepts/xxx]]`
- 同一讨论中产生的多个页面，必须互相引用
- 新页面必须引用已有的相关页面

## 质量检查

- 死链检查：`[[页面名]]` 必须指向存在的文件
- 孤立检查：每个页面至少被一个其他页面引用
- 过期标记：超过 6 个月未更新的页面标 `[过期]`
- 粒度检查：单页超 2000 字时建议拆分
