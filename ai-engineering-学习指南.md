# ai-engineering-from-scratch 使用指南（写给第一次用知识仓库的你）

仓库位置：`D:\open_lab\ai-engineering-from-scratch`
在线阅读版（不用装任何东西）：https://aiengineeringfromscratch.com

---

## 一、这个仓库长什么样

整座"图书馆"分 20 个阶段（phases），每个阶段是一个文件夹：

```
phases/
├── 01-math-foundations/        ← 数学基础（你的"字典区"）
├── ...
├── 11-llm-engineering/         ← LLM 工程（prompt 等基础，建议先扫一遍）
├── 13-tools-and-protocols/     ← 工具与协议（MCP 等，用到时查）
├── 14-agent-engineering/       ← ★ 你的主战场：Agent 工程
└── ...
```

## 二、每一"课"的固定结构（重要！）

每课都是一个文件夹，里面永远长这样：

```
14-agent-engineering/
└── 01-the-agent-loop/          ← 课文件夹（编号-名字）
    ├── docs/en.md              ← 📖 课文（英文讲解，约 100-150 行，一页读完）
    ├── code/main.py            ← 💻 可运行的代码实现
    ├── outputs/                ← 📦 这课产出的"作品"（prompt/技能/Agent）
    ├── quiz.json               ← ❓ 自测题
    └── notebook/ assets/       ← 补充材料（可忽略）
```

**学习一课 = 读 en.md → 跑 main.py → 改一行代码看变化 → 做 quiz。** 别贪多，一课一小时以内。

## 三、你的主线路线：Phase 14 核心 6 课

按这个顺序学，遇到不懂的名词再去前序阶段"查字典"：

| 顺序 | 课文件夹 | 学什么 |
|---|---|---|
| 1 | `01-the-agent-loop` | ReAct 循环：所有 Agent 的地基 |
| 2 | `02-rewoo-plan-and-execute` | 计划和执行分开做 |
| 3 | `06-tool-use-and-function-calling` | 工具调用（不懂就翻 Phase 13） |
| 4 | `12-anthropic-workflow-patterns` | Anthropic 官方工作流模式 |
| 5 | `26-failure-modes-agentic` | Agent 会怎么挂 |
| 6 | `30-eval-driven-agent-development` | 用评测驱动开发 |

全部学完后，按兴趣加餐：
- 记忆系统 → `09-hybrid-memory-mem0`
- 框架 → `13-langgraph-stateful-graphs` 或 `17-claude-agent-sdk`（二选一）
- 用 Agent 做工程 → `31~42` 工作台迷你轨（招牌是 42 课的 capstone）

## 四、怎么"查字典"式翻看前序阶段

比如学到第 4 课遇到"MCP"不懂：
1. 打开 `phases/13-tools-and-protocols/`，看文件夹名字找相关课；
2. 只读那课的 `docs/en.md` 前 60 行（Problem + Concept 部分就够了）；
3. 不用跑代码，看懂概念就回来继续主线。

每个 en.md 的固定段落顺序：**Learning Objectives（目标）→ The Problem（解决什么问题）→ The Concept（核心概念）→ Build It（动手）→ Verify It（验证）**。赶时间只读前三段。

## 五、跑代码的准备工作

```bash
cd D:\open_lab\ai-engineering-from-scratch
python phases/14-agent-engineering/01-the-agent-loop/code/main.py
```

- 第 1 课用的是"玩具 LLM"（离线可跑），**不需要 API key**，直接跑；
- 后面涉及真模型的课需要 `OPENAI_API_KEY` 环境变量，到时再配；
- 仓库要求 Python 3.10+，本机已有。

## 六、更新仓库

作者是持续更新的，隔一两个月拉一次最新版：

```bash
cd D:\open_lab\ai-engineering-from-scratch && git pull
```

---

*指南由 Hermes 生成于 2026-10-23，配套主线学习可随时找我：读不懂的英文讲解可以让我翻译，跑不通的代码可以让我调试。*
