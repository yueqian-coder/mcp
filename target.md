你的完整 idea 可以总结成：

# ResearchGraphOS：面向科研项目的自托管 Research Graph Workflow 系统

## 一句话定位

**ResearchGraphOS 是一个可以部署在自己本机或服务器上的科研知识工作流系统。它把你读过的论文、书籍、笔记、GitHub 项目和研究想法组织成 typed scholarly knowledge graph，然后支持项目级问答、论文推荐、GitHub repo 推荐、知识缺口分析、研究路线生成和自动增量更新。**

它不是普通“个人知识库问答”，而是：

> **围绕一个具体 research project，帮你管理“我读了什么、我懂了什么、我还缺什么、下一步该读什么、该复现什么代码、这个 idea 怎么推进”。**

---

# 1. 这个 idea 的核心差异

你不要做成：

```text
上传 PDF → 向量检索 → 和文档聊天
```

这个已经有很多项目做了，技术壁垒不够。

你真正要做的是：

```text
Research Project
        ↓
论文 / 书籍 / 笔记 / GitHub repo / arXiv 更新
        ↓
抽取科研实体和关系
        ↓
构建个人 Research Graph
        ↓
问答 + 推荐 + gap 分析 + repo 推荐 + 研究路线规划 + 自动更新
```

也就是说，系统的中心不是“文档”，而是：

```text
一个正在推进的科研项目
```

例如你可以创建：

```text
Project: Failure-aware GraphRAG Router
Goal: 减少 GraphRAG 检索成本，提高复杂问题准确率
Target: 8 月前给黄啸展示 / 后续做 AAAI idea
```

然后系统围绕这个项目组织所有资料。

---

# 2. 目标用户

主要用户是：

```text
本科生 / 硕士生 / PhD / RA / 科研新人 / 需要大量读论文的人
```

他们的真实痛点是：

```text
读了很多论文，但忘了；
知道某个 idea，但想不起在哪篇文章；
不知道下一篇该读什么；
不知道哪些 repo 能跑；
不知道自己的 idea 缺哪些 baseline；
不知道某篇论文和自己的项目有什么关系；
想让系统自动追踪新论文和 GitHub 项目。
```

你的系统解决的是：

> **科研阅读和 idea 推进过程中的知识组织问题。**

---

# 3. 项目名称建议

我最推荐：

```text
ResearchGraphOS
```

副标题：

```text
Project-aware research graph for papers, notes, books, and code.
```

中文：

```text
面向科研项目的自托管研究知识图谱工作流系统。
```

其他备选名字：

```text
PaperGraphOS
ScholarGraph
ResearchFlowGraph
GraphScholar
LitGraphOS
```

但综合来看，**ResearchGraphOS 最稳**，因为它不局限于 paper，也包含 note、book、repo、project workflow。

---

# 4. 系统核心对象

系统里不只是存文档，而是存科研实体。

## Node types

```text
Project
Paper
Method
Task
Dataset
Metric
Result
Claim
Limitation
Concept
Author
Venue
CodeRepo
ReadingNote
Book
Chapter
Experiment
ResearchGap
NextAction
```

## Edge types

```text
Paper -proposes-> Method
Paper -evaluates_on-> Dataset
Paper -reports-> Result
Paper -compares_with-> Method
Paper -claims-> Claim
Paper -has_limitation-> Limitation
Paper -has_code-> CodeRepo

Method -solves-> Task
Method -uses-> Concept
Method -extends-> Method
Method -implemented_by-> CodeRepo

Concept -prerequisite_of-> Concept
Concept -related_to-> Concept

Project -needs-> Concept
Project -uses-> Method
Project -should_compare_with-> Method
Project -has_gap-> ResearchGap
Project -can_use-> CodeRepo
Project -next_read-> Paper
Project -next_action-> NextAction

Note -comments_on-> Paper
Note -questions-> Claim
Note -supports-> Project
```

这就是你的技术壁垒之一：**typed scholarly graph schema**。

普通 RAG 只知道 chunk；你的系统知道：

```text
哪篇论文提出了什么方法；
解决什么任务；
用了什么数据集；
报告了什么指标；
有什么代码；
有什么 limitation；
和我的 project 有什么关系；
我下一步该读什么。
```

---

# 5. 核心功能模块

## 模块 1：Research Project 管理

用户先创建一个研究项目。

例如：

```text
Project: Failure-aware GraphRAG Router
Description: 研究什么时候该用 Vector RAG、GraphRAG、Memory RAG、Verifier，以减少成本并提高复杂问题准确率。
```

系统围绕这个 project 组织知识，而不是把所有资料混在一起。

功能包括：

```text
项目目标
已读论文
相关方法
相关数据集
相关 GitHub repo
缺失背景
下一步任务
实验路线
推荐阅读列表
```

---

## 模块 2：资料导入

支持输入：

```text
PDF 论文
arXiv URL
Markdown 笔记
书籍章节
GitHub repo URL
BibTeX
网页链接
手动 research note
```

v0.1 不要一开始支持太复杂，优先支持：

```text
arXiv URL
PDF
Markdown note
GitHub URL
```

---

## 模块 3：科研实体抽取

系统从论文和笔记里自动抽取：

```text
Paper title
Authors
Method
Task
Dataset
Metric
Baseline
Claim
Limitation
Code repository
Key concepts
Related papers
```

例如一篇 LightRAG 论文被导入后，系统应该知道：

```text
Paper: LightRAG
Method: graph-enhanced retrieval
Task: efficient RAG
Concept: knowledge graph, dual-level retrieval, incremental update
Limitation: 可能没有针对 failure-aware routing
Repo: HKUDS/LightRAG
```

---

## 模块 4：Research Graph 构建

系统把抽取出的实体和关系放进图数据库或轻量图存储里。

图谱不是为了好看，而是为了支持：

```text
多跳问答
研究路线生成
论文推荐
repo 推荐
gap detection
baseline discovery
claim/limitation 对比
```

---

## 模块 5：Project-aware QA

普通 RAG 问：

```text
LightRAG 是什么？
```

你的系统应该能回答更科研导向的问题：

```text
LightRAG 对我的 Failure-aware GraphRAG Router 项目有什么用？
它能作为 baseline 吗？
它和 GraphRAG-Bench 有什么关系？
它解决了什么问题，没有解决什么问题？
如果我要做 cost-aware GraphRAG，还需要读哪些论文？
```

回答格式应该是：

```text
结论
证据
相关论文
相关 repo
对当前 project 的作用
下一步建议
```

并且必须带 citation，不能空口生成。

---

## 模块 6：Gap-aware Paper Recommendation

这应该是你的杀手功能之一。

普通推荐是：

```text
这篇论文和你读过的相似。
```

你的推荐是：

```text
你当前 project 缺这一块，所以推荐这篇。
```

推荐理由可以分成：

```text
Background gap
Baseline gap
Method gap
Evaluation gap
Code gap
Recent update
```

例如系统发现你读了：

```text
LightRAG
LinearRAG
LogicRAG
GraphRAG-Bench
```

但是没读：

```text
adaptive RAG routing
agent memory
RAG evaluation
Graphiti / Zep
PaperQA2
```

它就推荐：

```text
你如果要做 Failure-aware GraphRAG Router，下一步应该补：
1. adaptive/query routing；
2. agent memory；
3. RAG evaluation；
4. cost-aware retrieval；
5. GraphRAG benchmark。
```

这比普通相似论文推荐有用很多。

---

## 模块 7：GitHub Repo Recommendation

系统不仅推荐论文，还推荐能跑的代码。

推荐 repo 时不只看 star，而是综合：

```text
和当前 project 的语义相关性
是否对应某篇 paper
stars
最近 commit
issue 活跃度
是否有 Docker
是否有 examples
是否有 benchmark scripts
license
安装难度
是否适合作 baseline
```

输出应该像：

```text
推荐 HKUDS/LightRAG：

用途：
- 可作为 graph-based RAG baseline；
- 支持增量更新；
- 和你的 efficient GraphRAG 方向相关。

风险：
- 不是 routing 方法；
- 如果你的方法是 FailRoute，它更适合作 baseline，而不是直接竞争方法。
```

这个功能非常实用。

---

## 模块 8：Self-updating Research Inbox

不要自动把所有新论文塞进图谱，那会污染。

正确流程是：

```text
定时扫描 arXiv / GitHub / OpenAlex / Semantic Scholar
        ↓
生成 Candidate Inbox
        ↓
系统解释为什么推荐
        ↓
用户 approve / reject
        ↓
确认后写入 Research Graph
```

例如每周系统生成：

```text
This week for Project: Failure-aware GraphRAG Router

New papers:
1. EA-GraphRAG
2. Adaptive RAG Router
3. Agent Memory Survey

New repos:
1. lightrag
2. graphiti
3. paper-qa

Suggested actions:
- Read EA-GraphRAG as routing baseline.
- Try LightRAG repo for baseline reproduction.
- Add Graphiti as memory-related comparison.
```

这就是 research workflow，而不是静态知识库。

---

## 模块 9：Research Plan Generator

这是展示时最有冲击力的功能。

用户输入：

```text
我想做 failure-aware GraphRAG router，8 月前给黄啸展示。
```

系统输出：

```text
你已有基础：
- LightRAG
- LinearRAG
- LogicRAG
- GraphRAG-Bench

你还缺：
- adaptive RAG routing
- agent memory
- cost-aware retrieval
- RAG evaluation
- repo-level baselines

推荐阅读顺序：
1. Microsoft GraphRAG
2. LightRAG
3. GraphRAG-Bench
4. EA-GraphRAG
5. Graphiti / Zep
6. PaperQA2
7. RAGAS / DeepEval

推荐 repo：
1. microsoft/graphrag
2. HKUDS/LightRAG
3. future-house/paper-qa
4. getzep/graphiti

建议实验：
- Vector RAG vs LightRAG vs FailRoute
- 指标：accuracy, citation recall, latency, token cost
```

这个功能能直接体现系统价值。

---

# 6. 和已有项目的区别

你不能说“没人做过 personal research graph”，因为相邻方向已经很多。

你的安全表述应该是：

> 已有工具分别覆盖了 personal knowledge base、scientific paper QA、GraphRAG framework、Zotero RAG、literature mapping 和 temporal memory。但还缺一个面向科研项目推进的 self-hosted Research Graph Workflow OS：它把 papers、notes、books、repos 组织成 typed scholarly graph，并围绕具体 project 做问答、gap-aware paper recommendation、repo recommendation、research planning 和 incremental research inbox。

简单说：

```text
Khoj / AnythingLLM：偏个人文档问答
PaperQA2：偏论文 QA
LightRAG / Microsoft GraphRAG：偏 GraphRAG 框架
Graphiti / Zep：偏 agent memory / temporal KG
Zotero RAG：偏 Zotero 论文库问答
Connected Papers / ResearchRabbit：偏文献发现图谱

你的 ResearchGraphOS：偏 project-aware research workflow
```

你的 niche 是：

```text
self-hosted
+ project-aware
+ typed scholarly KG
+ papers / notes / books / repos
+ gap-aware paper recommendation
+ runnable repo recommendation
+ research route generation
+ candidate inbox incremental update
```

---

# 7. 是否需要训练模型？

v0.1 **不需要训练**。

用这些就能做：

```text
LLM API / 本地 LLM
embedding model
规则
graph schema
retrieval
ranking score
GitHub/arXiv/OpenAlex/Semantic Scholar API
```

不训练也能完成：

```text
实体抽取
关系抽取
问答
论文推荐
repo 推荐
自动更新
研究路线生成
```

后期可以训练或微调：

```text
relation extractor
paper reranker
repo reranker
entity disambiguation model
query router
```

但第一版完全不用。

---

# 8. 部署方式

你的项目应该是：

```text
Local-first, self-hostable, server-ready.
```

也就是：

```text
轻度用户：本机部署
重度用户：服务器部署
隐私用户：本机 + 本地模型
展示 demo：你的 Vultr 服务器
```

## 最低配置

API 模式下，不跑本地大模型：

```text
2 CPU cores
4GB RAM
10–20GB disk
No GPU
```

服务器最低也可以：

```text
1–2 vCPU
2–4GB RAM
20–40GB SSD
```

推荐配置：

```text
2–4 CPU cores
4–8GB RAM
40GB+ disk
No GPU
```

本地大模型模式才需要：

```text
16GB+ RAM 或 GPU
```

所以你不能把项目做得太重。不要默认要求 Neo4j + 多服务 + 本地 LLM。v0.1 应该轻量。

---

# 9. 技术架构建议

## v0.1 轻量架构

```text
Frontend:
Streamlit 或 Next.js

Backend:
FastAPI

Storage:
SQLite / Postgres

Vector:
Chroma / FAISS / pgvector

Graph:
Kuzu / NetworkX
后期可选 Neo4j

LLM:
OpenAI / Claude / Gemini / Qwen API
可选 Ollama

Embedding:
OpenAI embedding / bge-m3 / e5

Scheduler:
cron / APScheduler

External APIs:
arXiv
OpenAlex
Semantic Scholar
GitHub API

Deploy:
Docker Compose
```

## 推荐第一版

为了降低门槛：

```text
FastAPI + Streamlit + SQLite + Chroma + Kuzu + API LLM
```

后面再升级：

```text
FastAPI + Next.js + Postgres + pgvector + Kuzu/Neo4j + worker
```

---

# 10. 8 月前 MVP 范围

不要一开始做大而全。

v0.1 只做这些：

```text
1. 创建 research project
2. 导入 arXiv URL / PDF / Markdown note / GitHub URL
3. 自动抽取 Paper / Method / Task / Dataset / Metric / Concept / Claim / Repo
4. 构建 typed research graph
5. 项目级问答，带 citation
6. 推荐下一篇 paper，带解释
7. 推荐 GitHub repo，带可运行性评分
8. 每周 arXiv + GitHub candidate inbox
9. Docker Compose 一键部署
10. 一个在线 demo
```

不要做：

```text
多用户权限
复杂书籍 OCR
完整 Zotero 插件
本地大模型训练
移动端
复杂公式理解
全学科支持
复杂推荐模型
```

先聚焦 AI / GraphRAG / Agent Memory 方向。

---

# 11. 给黄啸展示时怎么说

不要说：

```text
我做了一个个人知识网站。
```

要说：

```text
I built a self-hosted project-aware research graph workflow system. It organizes papers, notes, books, and GitHub repositories into a typed scholarly knowledge graph, then supports graph-grounded QA, gap-aware paper recommendation, runnable repo recommendation, research route generation, and incremental research inbox updates.
```

中文：

```text
我做了一个自托管的 project-aware research graph workflow 系统。它把论文、笔记、书和 GitHub 仓库组织成 typed scholarly knowledge graph，然后支持基于图谱的问答、知识缺口驱动的论文推荐、可运行代码推荐、研究路线生成，以及增量候选更新。
```

这比“个人知识库”有技术含量很多。

---

# 12. 项目卖点

你 README 第一屏可以写：

```text
You read 100 papers. You remember 10.

ResearchGraphOS turns your papers, notes, books, and repositories into a living research graph.

Ask project-specific questions.
Find missing background.
Discover the next paper to read.
Find runnable GitHub baselines.
Keep up with new arXiv papers and repos.
```

中文：

```text
你读了 100 篇论文，但真正记住的可能只有 10 篇。

ResearchGraphOS 把你的论文、笔记、书籍和代码仓库变成一个持续更新的研究图谱。

它能围绕你的研究项目回答问题、发现知识缺口、推荐下一篇论文、推荐可运行 GitHub baseline，并持续追踪新论文和新 repo。
```

---

# 13. 最终完整 idea

最终版可以这样定义：

> **ResearchGraphOS 是一个可自部署的 project-aware research graph workflow 系统。它面向学生、RA、PhD 和科研人员，把用户读过的论文、书籍、Markdown 笔记、GitHub 仓库和研究想法组织成 typed scholarly knowledge graph。系统支持带引用的 GraphRAG 问答、gap-aware paper recommendation、runnable repo recommendation、research plan generation 和 arXiv/GitHub 增量候选更新。它的目标不是替代普通 RAG，而是补上科研项目推进中的 workflow layer：帮助用户知道自己已经掌握什么、还缺什么、下一步该读什么、该复现什么，以及当前 idea 如何推进。**

一句话再压缩：

> **不是“和文档聊天”，而是“围绕研究项目推进科研”。**
