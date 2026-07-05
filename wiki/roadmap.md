---
type: overview
title: 项目路线图
description: 全局路线图 — 各领域入口与阶段规划
tags: [roadmap, meta]
timestamp: 2026-07-05T21:49:00+08:00
status: active
---

# 🗺️ 项目路线图

## 领域列表

### 🔧 芯片架构 (chip-architecture)

**目标**：探索超越传统CMOS的计算范式，从散热问题切入

**阶段**：第一阶段 — 问题定义与方案调研（2026）

**入口**：[[domains/chip-architecture/overviews/thermal-problem-landscape|散热问题全景]]

**方案对比**：[[domains/chip-architecture/comparisons/thermal-solutions-matrix|全景对比矩阵]]

### ➕ 新领域

```bash
cp -r wiki/domains/_template wiki/domains/your-domain
```

---

## 关键决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-07-05 | 引入 domains/ 分区机制 | 支持多领域并行，避免知识混杂 |
| 2026-07-05 | 双库架构（公开模板+私有知识） | 公开分享方法论，私有保护研究数据 |
| 2026-07-05 | 从散热问题切入芯片研究 | 华为韬定律暴露3D堆叠散热无解 |
