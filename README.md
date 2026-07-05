# LLM Wiki — AI 知识库系统

基于 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 概念和 Google [OKF 规范](https://cloud.google.com/blog/products/data-analytics/introducing-the-open-knowledge-format) 构建的**长期知识工程系统**。

## ✨ 特性

- 📂 **领域分区** — 多领域并行，互不干扰
- 🤖 **AI 自动维护** — 对话即入库，自动结构化
- 🔍 **精确加载** — 分层加载策略，不浪费 token
- 📊 **知识三角** — 讨论 → Wiki → Memory 三层架构
- 💻 **零依赖** — 纯 Markdown + Git，任何设备都能用

## 🚀 5 分钟从零搭建

### 1. 克隆本仓库（作为模板）

```bash
# 方式一：Fork GitHub 上的仓库
# 方式二：直接克隆
git clone https://github.com/universe-microlight/llm-wiki.git my-knowledge-base
cd my-knowledge-base
```

### 2. 创建你的第一个领域

```bash
# 复制模板
cp -r wiki/domains/_template wiki/domains/my-first-domain

# 开始写知识
echo "你的第一个知识页" > wiki/domains/my-first-domain/concepts/my-concept.md
```

### 3. 告诉 AI 你的知识库

把 `schema/CLAUDE.md` 的内容作为系统提示词的一部分告诉你的 AI（Claude / ChatGPT / 任意 LLM），它就能自动维护你的知识库。

### 4. 持续积累

```bash
# 每次讨论后
git add -A && git commit -m "新增: xxx" && git push
```

## 📂 目录结构

```
llm-wiki/
├── wiki/
│   ├── index.md              # 主索引
│   ├── log.md                # 变更日志
│   ├── roadmap.md            # 全局路线图
│   ├── domains/              # 🔑 核心：按领域分区
│   │   ├── _template/        # 新领域模板（复制即用）
│   │   └── chip-architecture/# 示例领域：芯片架构
│   │       ├── concepts/     #   概念页
│   │       ├── solutions/    #   方案页
│   │       ├── comparisons/  #   对比页
│   │       ├── entities/     #   实体页
│   │       └── overviews/    #   概述页
│   └── shared/               # 跨领域共享知识
│       ├── concepts/
│       └── entities/
├── schema/
│   ├── CLAUDE.md             # AI 行为规范（关键！）
│   └── okf.yaml              # OKF 元数据
├── scripts/
│   ├── ingest.py             # 资料导入
│   ├── search.py             # 搜索
│   └── lint.py               # 健康检查
└── raw/                      # 原始资料（不可变）
```

## 🧠 核心设计：如何省 Token

长期知识库最大的敌人是**上下文膨胀**。本系统的设计目标：讨论时只加载相关页面，不全量读取。

### 知识三角

```
讨论中产生 ──提炼──→ Wiki（结构化）──精华──→ Memory（永久索引）
  (临时)              (按领域分区)            (项目级元信息)
```

### 分层加载

| 场景 | 加载什么 | 不加载什么 |
|------|---------|-----------|
| 全新方向 | roadmap + 相关 overview | 具体 concept |
| 深入已有方向 | 相关 concept + comparison | 其他领域 |
| 对比方案 | comparison + 各方案 concept | overview |

### 页面粒度

- 一概念一页，超 2000 字就拆分
- 每页第一段 <100 字自包含摘要
- 用 `tags` 快速过滤

## 📖 使用场景

- 🔬 **长期研究项目** — 10年跨度的知识积累
- 📚 **学术研究** — 论文追踪、概念整理
- 💼 **技术选型** — 方案对比、决策记录
- 📝 **个人学习** — 构建知识体系

## 📄 License

Apache 2.0

## 🙏 致谢

- [Andrej Karpathy](https://twitter.com/karpathy) — LLM Wiki 概念
- [Google Cloud](https://cloud.google.com/) — OKF 规范
