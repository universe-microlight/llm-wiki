---
type: log
title: 变更日志
timestamp: 2026-07-05T21:49:00+08:00
---

# 📝 变更日志

---

## 2026-07-05 (v3) — 自旋电子学与轨道电子学评估

### 新增

**方案页**
- [solutions/spintronics] — 自旋电子学：MRAM量产现状、读写机制、5nm制程三约束、混合方案时间线
- [solutions/orbital-and-spin-ice] — 轨道电子学与自旋冰：工程化评估、规模化死穴、定位判断

### 更新

- [index.md] — 新增方案链接

---

## 2026-07-05 (v2) — 架构升级

### 变更

- 引入 `domains/` 分区机制，支持多领域并行
- 已有芯片知识迁移到 `domains/chip-architecture/`
- 新增 `domains/_template/` — 新领域一键复制模板
- 新增 `shared/` — 跨领域共享知识（通用概念/实体）
- 旧目录（concepts/ solutions/ comparisons/ entities/ overviews/）已清除

### 设计决策

- 公开库 = 通用模板 + 示例，任何人可从零搭建
- 私有库 = 个人知识，git submodule 引用公开库

---

## 2026-07-05 (v1) — 初始化

### 新增

**芯片架构领域 (domains/chip-architecture/)**
- [overviews/thermal-problem-landscape] — 芯片散热问题全景
- [solutions/reversible-computing] — 可逆计算
- [solutions/single-atom-transistor] — 单原子晶体管
- [solutions/atomic-computing-paradigms] — 原子/粒子层面替代范式
- [comparisons/thermal-solutions-matrix] — 方案全景对比矩阵
- [entities/huawei-tao-law] — 华为韬定律

**元页面**
- [roadmap.md] — 项目路线图
- [schema/CLAUDE.md] — AI 行为规范
