# 🧠 LLM Wiki — AI 知识库

基于 [Karpathy 的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 概念和 Google [OKF (Open Knowledge Format)](https://cloud.google.com/blog/products/data-analytics/introducing-the-open-knowledge-format) 规范构建的个人 AI 知识库系统。

## ✨ 特性

- 📄 **Markdown + YAML** — 纯文本，Git 友好，任何编辑器都能用
- 🤖 **AI 自动维护** — 导入资料后 AI 自动整理、交叉引用、发现矛盾
- 🔍 **语义搜索** — 基于向量嵌入的智能搜索
- 📊 **知识图谱** — 可视化概念和实体之间的关系
- 🔗 **OKF 兼容** — 符合 Google Open Knowledge Format v0.1 规范
- 💻 **跨平台** — 任何电脑 clone 下来就能用

## 🏗️ 三层架构

```
llm-wiki/
├── raw/              # 📁 原始资料（不可变）
│   ├── papers/       #   论文
│   ├── articles/     #   文章
│   └── notes/        #   笔记
├── wiki/             # 📚 AI 维护的知识库
│   ├── index.md      #   目录索引
│   ├── log.md        #   变更日志
│   ├── concepts/     #   概念页面
│   ├── entities/     #   实体页面
│   └── summaries/    #   摘要页面
├── schema/           # ⚙️ 配置规则
│   ├── CLAUDE.md     #   AI 行为规范
│   └── okf.yaml      #   OKF 元数据
└── scripts/          # 🔧 工具脚本
    ├── ingest.py     #   导入脚本
    ├── search.py     #   搜索脚本
    └── lint.py       #   健康检查
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/llm-wiki.git
cd llm-wiki
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入你的 API Key
```

### 4. 导入资料

```bash
# 导入单个文件
python scripts/ingest.py raw/papers/transformer.pdf

# 导入整个目录
python scripts/ingest.py raw/articles/

# 从 URL 导入
python scripts/ingest.py --url https://example.com/article
```

### 5. 搜索知识

```bash
python scripts/search.py "什么是 Transformer 的注意力机制？"
```

### 6. 健康检查

```bash
python scripts/lint.py
```

## 📋 OKF 规范

本项目遵循 [Google Open Knowledge Format v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog) 规范：

### Wiki 页面格式

```markdown
---
type: concept
title: 注意力机制
description: Transformer 架构中的核心组件
tags: [transformer, attention, deep-learning]
timestamp: 2024-01-15T10:30:00Z
---

# 注意力机制

## 概述
注意力机制是 Transformer 架构的核心组件...

## 关联
- [[transformer-architecture]]
- [[self-attention]]
- [[multi-head-attention]]

## 来源
- [原始论文](../raw/papers/attention-is-all-you-need.pdf)
```

### 支持的页面类型

| 类型 | 说明 |
|------|------|
| `concept` | 概念解释 |
| `entity` | 实体（人物、公司、产品等） |
| `summary` | 资料摘要 |
| `comparison` | 对比分析 |
| `overview` | 领域概述 |
| `index` | 目录索引 |
| `log` | 变更日志 |

## 🤖 AI 集成

### Claude / ChatGPT / 任意 LLM

将 `schema/CLAUDE.md` 作为系统提示词的一部分，AI 就能理解并维护你的 wiki。

### OpenClaw 集成

本项目可直接作为 OpenClaw 的 workspace 使用，AI agent 会自动维护知识库。

## 📖 使用场景

- 📚 **学术研究** — 整理论文、追踪研究前沿
- 💼 **项目管理** — 积累项目知识、避免重复踩坑
- 📝 **个人学习** — 构建个人知识体系
- 🏢 **团队协作** — 共享团队知识库

## 📄 License

Apache 2.0

## 🙏 致谢

- [Andrej Karpathy](https://twitter.com/karpathy) — LLM Wiki 概念
- [Google Cloud](https://cloud.google.com/) — OKF 规范
- [llmwiki.app](https://llmwiki.app) — 参考实现
