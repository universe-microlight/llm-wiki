---
type: overview
title: 芯片散热问题全景
description: 从工程方案到物理根源 — 芯片散热的所有已知思路和前沿探索
tags: [chip, thermal, heat-dissipation, overview]
timestamp: 2026-07-05T20:06:00+08:00
status: active
---

# 芯片散热问题全景

## 问题本质

芯片发热的根本原因：电子在导线中运动时与晶格原子碰撞，动能转化为晶格振动（热）。这是焦耳热的微观机制。

随着晶体管密度提升和3D堆叠，热密度急剧上升，传统散热方案已接近物理极限。

## 两条技术路线

### 路线一：高效散热（热出来之后怎么带走）

- [[engineering-thermal-solutions]] — 工程级散热方案
- [[phonon-engineering]] — 声子工程（原子层面控热）
- [[two-phase-microchannel-cooling]] — 两相微通道冷却

### 路线二：减少产热（让芯片根本不热）

- [[reversible-computing]] — 可逆计算（从信息论根源动刀）
- [[single-atom-transistor]] — 单原子晶体管
- [[molecular-electronics]] — 分子电子学
- [[spintronics]] — 自旋电子学
- [[orbital-electronics]] — 轨道电子学
- [[topological-electronics]] — 拓扑电子学
- [[optical-computing]] — 光计算

## 华为韬定律与散热

华为韬定律论文（2026年更新版）首次正面提及3D堆叠芯片的散热问题。采用 LogicFolding 晶圆到晶圆混合键合技术，中间层散热路径变长，目前方案仅为"热感知分区布局"，未能根治。

详见 [[huawei-tao-law]]。

## 关键物理极限

| 极限 | 数值 | 含义 |
|------|------|------|
| 兰道尔极限 | kT·ln2 ≈ 2.75×10⁻²¹ J/bit | 擦除1 bit信息的最小热耗散 |
| 焦耳热 | P = I²R | 电子碰撞晶格的产热 |
| 声子热导 | 材料固有属性 | 热量在固体中传播的速率上限 |
