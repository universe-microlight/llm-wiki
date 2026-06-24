---
type: index
title: 知识库索引
description: LLM Wiki 主索引
timestamp: 2024-01-15T00:00:00Z
---

# 📚 知识库索引

欢迎来到你的个人 AI 知识库！

## 📖 概述

本知识库由 AI 自动维护，基于 [Karpathy 的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 概念和 Google [OKF 规范](https://cloud.google.com/blog/products/data-analytics/introducing-the-open-knowledge-format) 构建。

## 🗂️ 分类

### 概念 (Concepts)
理解关键概念和原理。

> 还没有概念页面。导入资料后 AI 会自动创建。

### 实体 (Entities)
了解重要的人物、公司、产品。

> 还没有实体页面。导入资料后 AI 会自动创建。

### 摘要 (Summaries)
资料的精华总结。

> 还没有摘要页面。导入资料后 AI 会自动创建。

## 📥 如何使用

### 1. 导入资料

将文件放入 `raw/` 目录：

```bash
# 复制文件
cp ~/Documents/paper.pdf raw/papers/
cp ~/Notes/article.md raw/articles/

# 或使用脚本
python scripts/ingest.py raw/papers/new-paper.pdf
```

### 2. 让 AI 整理

告诉 AI（Claude、ChatGPT 等）：

> 请阅读 schema/CLAUDE.md，然后处理 raw/ 中的新资料，更新 wiki。

### 3. 搜索知识

```bash
python scripts/search.py "你的问题"
```

### 4. 健康检查

```bash
python scripts/lint.py
```

## 📊 统计

- **概念页面**: 0
- **实体页面**: 0
- **摘要页面**: 0
- **最后更新**: 2024-01-15

## 🔗 相关资源

- [Karpathy 的 LLM Wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Google OKF 规范](https://github.com/GoogleCloudPlatform/knowledge-catalog)
- [LLM Wiki 参考实现](https://llmwiki.app)
