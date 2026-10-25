# Phase 13：工具与协议（中文译本）

> AI 与现实世界之间的接口。

> 本文件是 [README.md](README.md) 的中文翻译版，仅供学习参考；如有出入，以英文原文为准。

本阶段从函数调用和工具 schema 出发，进入可互操作的协议、Agent Skills（技能）、
安全以及生产治理。数字顺序便于浏览，但下面列出的专注路线才是可靠的学习顺序。

## 在 GitHub 上开始本阶段

**前置知识：** Phase 11 的 LLM 补全 API。对于 MCP 或 Agent Skills，请走下面的
专注路线，而不是假设按课程编号顺序学习。

**完整阶段的第一课：** [The Tool Interface（工具接口）](01-the-tool-interface/)

在仓库根目录运行：

```bash
python3 phases/13-tools-and-protocols/01-the-tool-interface/code/main.py
```

保留命令、退出码、describe-decide-execute-observe（描述-决策-执行-观察）轨迹、
被拒绝输入的证据，并用一句话解释轮次上限。

**下一步：** 继续学习 [Function Calling Deep Dive（函数调用深度解析）](02-function-calling-deep-dive/)，
或选择下面的 Model Context Protocol (MCP) 或 Agent Skills 路线。

浏览 [Phase 13 完整课程列表](../../README.md#phase-13) 或
[跨阶段路线图](../../ROADMAP.md)。

## Model Context Protocol (MCP) 路线

专注版 MCP 路线共 17 课、约 23 小时 15 分钟。它围绕 MCP `2026-07-28` 版本，
从一个自描述的 JSON-RPC 请求一路走到可运行的一致性验收关卡。

| 阶段 | 课程 | 你要证明的能力 | 时间 |
|---|---|---|---:|
| 核心 | [06](06-mcp-fundamentals/), [07](07-building-an-mcp-server/), [08](08-building-an-mcp-client/), [09](09-mcp-transports/), [10](10-mcp-resources-and-prompts/) | 消息信封、发现机制、客户端与服务端行为、传输方式、资源与提示模板。 | 5 小时 50 分 |
| 双向通信 | [11](11-mcp-sampling/), [12](12-mcp-roots-and-elicitation/), [13](13-mcp-async-tasks/), [14](14-mcp-apps/) | MRTR 输入、显式作用域、持久任务，以及不含服务端发起请求的应用边界。 | 5 小时 |
| 安全 | [15](15-mcp-security-tool-poisoning/), [16](16-mcp-security-oauth-2-1/), [18](18-mcp-auth-production/), [17](17-mcp-gateways-and-registries/) | 投毒防御、授权、生产令牌、网关路由与注册表准入。 | 5 小时 15 分 |
| 进阶 | [28](28-mcp-tool-contracts-and-content/), [29](29-mcp-reliability-cancellation-and-flow-control/), [30](30-mcp-registry-supply-chain-and-drift/), [31](31-mcp-conformance-versioning-and-operations/) | 契约保真度、取消竞态、供应链漂移与发布证据。 | 7 小时 10 分 |

精确顺序是 06、07、08、09、10、11、12、13、14、15、16、18、17、28、
29、30、31，定义在
[`learning-paths/model-context-protocol.json`](../../learning-paths/model-context-protocol.json)。
导师（tutor）会创建 `MCP-LEARNING.md`，每次调用只教一课，并记录每个检查点
要求的请求、响应、命令、工作目录、退出码，以及脱敏后的边界证据。

从你的宿主环境支持的调用方式开始：

| 宿主 | 调用方式 |
|---|---|
| Codex | `learn-mcp`，或从 `/skills` 中选择 |
| Claude Code | `/learn-mcp` |
| 其他兼容宿主 | `Use learn-mcp to start or resume the Model Context Protocol (MCP) path.` |

### 你的前十分钟

在仓库根目录运行第 06 课的无状态转录脚本：

```bash
python3 phases/13-tools-and-protocols/06-mcp-fundamentals/code/main.py
```

在输出中找到四样东西：重复出现的请求元数据、一个完整的
`server/discover` 结果、针对不支持版本的错误 `-32022`，以及一次不会创建或
终止 MCP 协议会话的传输层关闭。这份转录就是第一个检查点，而不仅是演示。

如果无法使用仓库或 Python 3，请阅读[第 06 课](06-mcp-fundamentals/)并手工
追踪一次请求与响应。把该检查点标记为"仅概念"，并将运行时、传输、授权和
部署证据保持为待完成状态。

在任何非回环地址绑定、共享入口、托管端点或注册表发布之前，先完成第 15 课
的可执行安全检查点。审视外部目标和所请求的权限，然后显式确认部署动作。
完成一个教程并不授予你部署权限。

较早的 `initialize`、`Mcp-Session-Id`、独立 SSE `GET`、会话 `DELETE`
以及服务端发起请求的流程，只出现在显式的兼容性说明中。现代请求在
`params._meta` 中声明协议版本和客户端能力，使用 `server/discover`，并携带
足够的信息以便被独立地校验、授权、路由和重试。

[第 23 课](23-capstone-tool-ecosystem/) 是 MCP 路线中唯一可选的压轴项目。
开始前须完成 17 门必修课程，外加[第 19 课](19-a2a-protocol/) 和
[第 20 课](20-opentelemetry-genai/)。

## Agent Skills 快速通道

专注版路线共 5 课、约 9 小时 30 分钟：

| 步骤 | 课程 | 成果 | 时间 |
|---:|---|---|---:|
| 1 | [22：可移植契约与运行时边界](22-skills-and-agent-sdks/) | 创建、安装、调用、验证并移除一个完整的技能包。 | 90 分钟 |
| 2 | [24：发现与渐进披露](24-skill-discovery-and-progressive-disclosure/) | 追踪发现、编目、激活和资源加载的全过程。 | 105 分钟 |
| 3 | [25：调用与路由](25-skill-invocation-and-routing/) | 掌控显式、隐式、人工、模型及弃权（abstention）路径。 | 105 分钟 |
| 4 | [26：权限、沙箱与信任](26-skill-permissions-sandboxes-and-trust/) | 区分指令、权限、隔离与验证。 | 120 分钟 |
| 5 | [27：评估、打包与可移植性](27-skill-evals-packaging-and-portability/) | 构建发布门禁，并在真实宿主中验证行为。 | 150 分钟 |

从你的宿主环境支持的调用方式开始：

| 宿主 | 调用方式 |
|---|---|
| Codex | `learn-agent-skills`，或从 `/skills` 中选择 |
| Claude Code | `/learn-agent-skills` |
| 其他兼容宿主 | `Use learn-agent-skills to start or resume the Agent Skills Engineering path.` |

导师会创建或恢复 `AGENT-SKILLS-LEARNING.md`，每次调用只教一课，并记录每个
检查点要求的证据。路线定义在
[`learning-paths/agent-skills.json`](../../learning-paths/agent-skills.json)。

如果你更喜欢先阅读，从[第 22 课](22-skills-and-agent-sdks/) 开始。它的第一个
实验能在约十分钟内把一个技能装进真实宿主。

### 前置条件快车道

- 想跑真实实验，你需要 `node`、`npx`、`python3`、一个选定的支持技能的宿主，
  以及对所选项目或用户技能目录的写权限。安装前用 `node --version`、
  `npx --version` 和 `python3 --version` 验证这三条命令。
- 如果无法完成上述预检，可以使用网站或逐个手工阅读 `docs/en.md`。
  你可以完成概念性部分，但发现、调用、脚本、更新和卸载的证据要标记为待完成。
- 如果工具契约对你来说还很新，先快速浏览[第 01 课](01-the-tool-interface/)
  和[第 05 课](05-tool-schema-design/)。
- 在第 26 课之前，确认你能解释工具投毒和不可信指令。
  [第 15 课](15-mcp-security-tool-poisoning/) 是该预检的可选复习课，
  不是本路线的第六门必修课。
- [第 23 课](23-capstone-tool-ecosystem/) 是可选的系统级压轴项目，
  不是 22 课之后的下一门 Agent Skills 课程。选修前须完成第 06 到 20 课。

## 逆向工程路线

十四门课教你阅读一个自己编译出来的程序。第 32 到 36 课构建核心流水线：
解析文件、解码指令、提升到伪代码、把已知信息记录为证据，并证明重建的函数
与原版等价。第 37 到 45 课讲解流水线周边的领域：它的历史与主要工具、调用
约定、编译器惯用法、链接与去符号二进制、类型恢复、调试、字节码格式、
二进制差分与符号执行，以及 AI 辅助分析。每门课都在同一批测试样本上运行
真实工具。配套手册 [Reverse Engineering 101](../../manuals/reverse-engineering-101/)
让同一个样本分别跑过 radare2 6.7.0 和 Ghidra 12.1.4。

| 课程 | 你构建的东西 | 时间 |
|---|---|---|
| [32](32-program-anatomy-elf-from-scratch/) | 一个 ELF 读取器：头部、节区、符号、重定位 | 2 小时 |
| [33](33-disassembly-and-control-flow/) | 一个 x86-64 解码器、线性扫描、递归下降，以及控制流图 | 2 小时 30 分 |
| [34](34-lifting-to-pseudocode/) | 一个从指令到结构化伪代码的提升器 | 2 小时 30 分 |
| [35](35-evidence-confidence-and-unknowns/) | 一个带置信度、局限性和未知项的证据台账 | 1 小时 45 分 |
| [36](36-rebuild-and-prove-equal/) | 一个差分测试装置，以及一个对重定位做掩码的字节比较 | 1 小时 50 分 |
| [37](37-the-reverse-engineering-landscape/) | 覆盖五个工具的对比装置，附历史时间线和四种 IR | 2 小时 30 分 |
| [38](38-calling-conventions-and-stack-frames/) | 支持 System V、Windows x64 和 AArch64 的调用约定分析器 | 2 小时 20 分 |
| [39](39-compiler-idioms-and-optimization/) | 一个惯用法识别器，解码除法、switch、循环和 select | 2 小时 30 分 |
| [40](40-linking-loading-and-stripped-binaries/) | PE、Mach-O 修复与 ELF 链接读取器，以及去符号构建的函数查找器 | 2 小时 40 分 |
| [41](41-recovering-data-and-types/) | 一个结构体与 C++ 类型恢复流程，与 DWARF 读取器交叉校验 | 2 小时 20 分 |
| [42](42-dynamic-analysis-of-your-own-program/) | 一个 lldb 装置，用于证实或推翻静态分析结论 | 2 小时 10 分 |
| [43](43-bytecode-and-managed-formats/) | .pyc、JVM class、.NET CIL 和 WebAssembly 的读取器 | 2 小时 30 分 |
| [44](44-binary-diffing-and-symbolic-execution/) | 一个函数差分器和一个小型符号执行器 | 2 小时 30 分 |
| [45](45-ai-assisted-reverse-engineering/) | 针对 AI 重建与分析报告的基准真值记分卡 | 2 小时 20 分 |

本路线中的每一个目标都是你自己编写并编译的程序。第 32 课从法律和授权规则
讲起。想跟着记录进度的导师走完这条路，请运行 `learn-reverse-engineering`
技能。它的顺序和检查点定义在
[逆向工程路线清单](../../learning-paths/reverse-engineering.json)中。

## 完整阶段

完整课程计划见 [ROADMAP.md](../../ROADMAP.md)。
