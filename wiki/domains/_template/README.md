---
type: template
title: 领域模板
description: 新建领域时复制此目录结构
timestamp: 2026-07-05T21:49:00+08:00
---

# 📁 领域模板

新建知识领域时，复制 `_template/` 目录并重命名：

```bash
cp -r wiki/domains/_template wiki/domains/your-domain-name
```

## 目录结构

```
your-domain-name/
├── concepts/       # 概念页（一个概念一页，500-1500字）
├── solutions/      # 方案页（具体技术方案，1000-2000字）
├── comparisons/    # 对比页（多方案横向对比，800-1500字）
├── entities/       # 实体页（公司/团队/产品，300-800字）
└── overviews/      # 概述页（领域全景，1000-2000字）
```

## 首页命名规范

每个领域的入口页放在 `overviews/` 下，文件名建议用 `{domain}-overview.md`。

在全局 `roadmap.md` 中添加该领域的入口链接。
