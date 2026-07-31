# Why Personality Runtime

## 为什么需要人格运行时

Version: v0.1
定位：对外科普与理念文档 —— 用最少的术语，讲清楚"为什么 AI 需要人格运行时"。

---

## 一个问题

现在的 AI 很聪明。它可以回答问题、写文章、陪人聊天。

但如果你要求它**长期保持同一个人**——同样的性格、同样的价值观、同样的底线，几天、几周、几个月不变——会发生什么？

大概率会失败。不是因为它不聪明，而是因为**现在的技术栈里，根本没有"人格"这个东西的位置**。

---

## 人格现在住在哪里

今天，一个"AI 角色"的人格，通常住在三个地方之一：

1. **一段提示词** —— 写着"你是一个温柔、有边界的朋友"。
2. **模型的微调权重** —— 把某种性格"训练"进模型。
3. **产品的代码** —— 在应用里加一堆 if-else 规则。

这三个地方，有一个共同的问题：**人格不是系统的正式成员**。它只是贴在某处的文字、或隐含在权重里的倾向。它没有身份、没有版本、没有验证、没有隔离。

于是：

- 性格会**漂移**——同一段提示词，今天温柔，明天可能就变了；
- 换个模型，**人就换了**——人格跟着模型走，不跟着定义走；
- 出问题无法**追溯**——你无法测试"它是否始终如一"；
- 多个角色放一起，会**互相污染**；
- 辛辛苦苦调好的人格，**换一个产品就作废**，没有积累。

---

## 操作系统给了我们一个现成的类比

想象没有操作系统的电脑：每个程序都要自己管内存、自己管进程、自己管文件。程序一多，就互相踩踏。

操作系统把"运行程序"变成了一等能力：隔离、生命周期、资源管理。程序不再关心这些，只关心自己的业务逻辑。

AI 人格需要同样的一层。我们把这一层叫做**人格运行时（Personality Runtime）**：

> 让"人格"第一次成为系统里的一等公民——可定义、可加载、可隔离、可验证、可替换。

---

## 人格运行时做什么

| 能力 | 说明 |
|------|------|
| 定义 | 人格有唯一的定义来源（人格源），而不是散落的提示词 |
| 打包 | 人格按统一契约做成"模块"（tang-ta 标准），可版本化、可发布 |
| 运行 | 一个运行时负责加载、执行、隔离人格（Tang OS） |
| 决策 | 面对情境时，先由决策引擎算"该怎么做"，再交给 LLM 说"怎么说" |
| 验证 | 一致性、隔离、边界都是**可测试的性质**，不是感觉 |

---

## 一句话总结

> 现在的 AI 只有"智力"，没有"人格"。
> 人格运行时，就是给 AI 装上"人格"的那一层基础设施。

---

## English Summary

Modern AI is intelligent but has no durable personality. Today, an AI character's personality lives in one of three unstable places — a prompt, fine-tuned weights, or product code — none of which make personality a first-class citizen. As a result: personality drifts, changes when the model changes, cannot be tested, cannot be isolated, and cannot be reused.

The OS analogy: just as an operating system made processes first-class (isolation, lifecycle, resources), a **Personality Runtime** makes personality first-class — definable, loadable, isolated, verifiable, replaceable.

A personality runtime provides: **definition** (a single source, not scattered prompts), **packaging** (modules with a contract, versioned and publishable), **execution** (a runtime that loads, runs, and isolates personalities), **decision** (a decision engine computes what to do; an LLM only says how), and **validation** (consistency and boundaries are testable properties).

One sentence: today's AI has intelligence but no personality. A personality runtime is the infrastructure layer that gives AI a personality.
