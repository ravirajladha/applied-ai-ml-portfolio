# LLMs as Agents (M9): coverage spec

**Ladder:** LLMs for Generative AI (AIMLCZG536) › M9 LLM as Agents   ·   **Prerequisites:** llmc-prompting (ReAct, function calling), llmc-rag (vector stores, Self-RAG), llm-prompting (tool-calling basics)
**Why it matters for AI/ML:** Agents are how LLMs do real work: they call tools, keep memory and run in a loop. The course examines this module heavily with scenario questions: pick the multi-agent pattern for a requirement, name the memory type and its storage substrate, and explain why the tempting alternative (Subagents, Router, vector store) is wrong. An AI engineer makes these same choices when designing a production agent, including a text-to-SQL agent over company data.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `mental-models` | Two mental models of an agent | RL origin (observation -> action), classic view LLM + Planning + Memory + Tools | harness view Agent = Model + Harness, harness vs scaffolding, four faculties | four layers of engineering (prompt, context, memory, harness) and their failure modes | why both views are compatible; where a fix belongs (which layer) |
| 2 | `anatomy-loop` | Anatomy of an agent and the execution loop | the five single-agent components | Perceive -> Reason -> Act -> Observe mapped to Memory(read) / Planning / Tools+Action / Memory(write) | the three stop conditions (goal, budget, step cap) | tracing a loop, where an observation is written |
| 3 | `react-fc` | How LLMs become agents: function calling and ReAct | Thought -> Action -> Observation | function calling = model emits name + JSON args, harness executes | modern ReAct's seven upgrades (structured calls, parallel calls, plan first, reflection, branching, context management, self-verification) | parsing/dispatching a tool call, errors fed back as observations |
| 4 | `memory-types` | Types of agent memory | reflex agent, STM vs LTM | working memory, semantic cache, procedural, episodic, semantic, shared (coordination) | classifying memories in a scenario (SupportBot trace) | the quick test: fact / past event / skill; semantic cache vs episodic |
| 5 | `memory-substrates` | Storage substrate for each memory type | file vs vector store | semantic -> file / KV / small DB; episodic -> vector DB; procedural -> system prompt / AGENTS.md / skills registry; shared -> ACID DB | "why not a vector store" and "why not a file" justifications | lost updates without ACID, optimistic concurrency, semantic cache threshold risk |
| 6 | `ma-why` | Multi-agent systems: why and when | what a multi-agent system is | single-agent limits (tool bloat, confusion), specialization, modularity | when multi-agent hurts (coordination overhead, redundant tokens, blurred attribution); MCP vs A2A | — |
| 7 | `ma-patterns` | The multi-agent patterns | names of the patterns | Subagents (stateless, extra call), Skills (progressive disclosure), Handoffs (state-driven), Router (one target), Router with Synthesis (subset + merge), Prompt Chaining | call counts and token cost per pattern | "Router is really a planner"; stateless subagents and context isolation |
| 8 | `pattern-scenarios` | Choosing the pattern (exam scenarios) | — | fixed template -> Subagents; strict sequence + same conversation -> Handoffs | one-destination -> Router; variable subset -> Router with Synthesis; many niche procedures -> Skills | the papers' common wrong answers and the 4x waste argument |
| 9 | `text-to-sql` | Agentic text-to-SQL | why not paste the table into the prompt | schema linking, the model sees only the result | validation (read-only, allow-list, LIMIT), execute-and-retry on errors | semantic errors that run fine, numeric predicates RAG cannot do |
| 10 | `failures-guardrails` | Failure modes and guardrails | infinite loops, hallucinated tools | premature completion, cascading errors, poor self-evaluation | code gates, human approval, least privilege, budgets | error attribution in multi-agent, verifying with tests |
| 11 | `context-wall` | The context wall and context management | context window fills up | compaction, offloading tool output to files, progressive skill disclosure | subagent context isolation; context poisoning / distraction / confusion / clash | architectural fixes (sliding window, sparse, linear attention) vs harness fixes |

## Must-know facts
- RL origin: an agent is a function from observation to action; the environment returns a new observation; the loop repeats.
- Course definition: an AI agent has four faculties: cognition (LLM), action (tool use), memory (short and long term), perception (multimodal input).
- Two mental models: classic view (Weng 2023) Agent = LLM + Planning + Memory + Tools; harness view Agent = Model + Harness ("if you are not the model, you are the harness"). They are compatible: the harness is how you deliver planning, memory and tools.
- Harness = execution layer: calls the model, handles its tool calls, decides when to stop. Scaffolding = what the model works from: system prompt, tool descriptions, parsing, context management.
- Four layers: prompt engineering (what we say), context engineering (what the model sees now, working memory/RAM), memory engineering (what persists across sessions, long-term memory/disk), harness engineering (how the agent operates, operating system/kernel).
- Single-agent components: Profile and Persona; Actions and Tool Use; Reasoning and Evaluation; Memory and Knowledge; Planning and Feedback.
- Loop: Perceive = Memory(read), Reason = Planning, Act = Tools + Action, Observe = Memory(write). Repeats until the goal is met, the budget is spent, or the step cap is hit.
- Function calling: the model emits a tool name and JSON arguments; the harness executes and appends the result as the observation.
- Memory: STM = working memory (session scratchpad in context or a temp file) and semantic cache (prompt -> response, matched by vector similarity). LTM = procedural (skills, workflows, decision trees), episodic (specific past events, timestamped), semantic (stable world knowledge). Coordination = shared memory, needs ACID.
- Quick test: fact with one right answer -> semantic; past event recognised by resemblance -> episodic; a reusable skill -> procedural.
- Substrates: semantic facts -> file / key-value store / small structured DB (exact-key, deterministic); episodic -> vector DB (ANN / HNSW); procedural -> system prompt, tool schemas, AGENTS.md, skills registry; shared -> ACID database (e.g. PostgreSQL); working -> graph state / Redis; semantic cache -> Redis + vector search.
- Patterns: Subagents (main agent calls stateless subagents, results flow back = one extra model call; fixed set every time), Skills (one agent, loads specialised prompts on demand, progressive disclosure), Handoffs (state-driven transitions, state survives across turns, one continuous conversation), Router without synthesis (classify once, exactly one specialist), Router with Synthesis (select a variable subset per query, run in parallel, merge). Prompt Chaining = fixed linear pipeline.
- Multi-agent helps through specialization and modularity; hurts through coordination overhead, redundant tokens and blurred error attribution. Prefer sub-agents when subtasks are independent and outputs cleanly mergeable.
- MCP standardises tool use (agent -> tool); A2A (Agent2Agent) standardises agent-to-agent task communication.
- Text-to-SQL: keep large tables in a DB; the model gets the schema, writes SQL, the harness validates and executes it in a sandbox, and the model sees only the result.

## Common traps (each one must have at least one question)
- "Router, because each step routes to a different sub-system" for a strict sequence -> Handoffs; Router dispatches once and stops.
- "Subagents, because specialists run in parallel" when the set varies per query -> Router with Synthesis.
- Subagents for one-destination triage -> Router; Subagents would waste (N-1)/N of the work.
- Router for a fixed template -> Subagents; there is no per-request selection.
- Defaulting to Router with Synthesis "to be safe" -> costs more than a plain Router.
- "Parallel is always faster, so parallel is better" -> only if the work is parallelisable AND all of it is needed.
- Vector store for stable facts with one right answer -> file / KV; similarity returns a ranked guess.
- File for 8,000 past cases -> cannot be enumerated in context and has no key; vector store.
- Calling timestamped past cases "semantic memory" -> episodic.
- Semantic cache confused with episodic memory -> cache is short-term, reuses answers to similar prompts.
- Shared memory without ACID -> lost updates and race conditions.
- Thinking the model executes the tool -> the harness does.
- Thinking subagents remember earlier calls -> they are stateless.
- Loading every skill's full instructions up front -> blows the context; skills load on demand.
- Agent loop without a step cap or budget -> runs forever / burns money.
- Trusting generated SQL because it runs -> it can be semantically wrong; validate and check results.
- Letting the text-to-SQL agent run any statement -> read-only role, SELECT allow-list, LIMIT.
- Pasting a 10,000-row table into the prompt -> context exhaustion, cost, weak arithmetic; query it.
- Blaming the model when the context was wrong -> context engineering first.

## Interview angle
1. **"What is an agent?"** An LLM in a loop with tools and memory: it perceives (reads context and memory), reasons (plans the next step), acts (calls a tool) and observes (writes the result back), until the goal is met, the budget runs out or the step cap hits. Classic view: LLM + Planning + Memory + Tools. Harness view: Model + Harness.
2. **"Which multi-agent pattern would you use?"** Ask two questions: is the set of specialists fixed or chosen per request, and is it one destination or many? Fixed set every time -> Subagents. One destination -> Router. Variable subset + merge -> Router with Synthesis. Strict ordered steps in one conversation -> Handoffs. One agent with many niche procedures -> Skills.
3. **"How do you design agent memory?"** Working memory in the context/graph state; stable facts in a file or KV store; past episodes in a vector DB; skills and rulebooks in the system prompt / AGENTS.md; shared multi-agent state in an ACID database.
4. **"Build a text-to-SQL agent."** Schema linking (pick the relevant tables/columns), generate SQL, validate (parse, read-only, allow-list, LIMIT), execute in a sandbox with a read-only role, feed errors back for a bounded number of retries, sanity-check results, and log.
5. **"How do agents fail?"** Loops, premature completion, cascading errors, poor self-evaluation, tool hallucination, context poisoning. Guardrails: step and cost budgets, code gates, verification with tests, human approval for side effects, least-privilege tools.

## Source material
- Handout, Module 9 "LLM as Agents": two mental models, anatomy of an agent (ReAct / tool-call loops), how LLMs become agents, types of agent memory, context wall (problem and solutions, sub-quadratic / sparse / hybrid attention), agentic application: text-to-SQL agent. References: T2 Ch-7, R3 (An Illustrated Guide to AI Agents) Ch-2,4. Lab 9: build a ReAct-style agent.
- Old-batch slides, agent session (`old-batch-slides.txt` lines ~4536-4910): RL definition of agent; four faculties; augmentation view vs execution loop (Perceive/Reason/Act/Observe); five single-agent components; Modern ReAct "same skeleton, seven upgrades"; Multi-agent why/when; patterns 1-4 (Subagents, Skills, Handoffs, Router with/without synthesis) from the LangChain "choosing the right multi-agent architecture" framework; requirements -> pattern table; A2A; agent memory (STM: working memory, semantic cache; LTM: procedural, episodic, semantic; coordination: shared memory with ACID); two mental models (Weng 2023 vs Model + Harness); harness vs scaffolding; four layers of engineering table; HorizonBank and SupportBot case studies (memory type -> technology table).
- Old-batch slides, sample answers (lines ~5425-5460): five patterns table incl. Prompt Chaining; "Parallel Subagents for one-of-five triage = 4x wasted tokens/latency/cost"; memory types with substrate and example; the quick memory test.
- Old-batch slides M7/M8 (lines ~3420-3440, ~4060-4080): tables -> "extract to DataFrame / SQL, LLM writes code or SQL, sees only the answer"; agentic RAG chooses SQL vs vector index; step budgets and stop conditions.
- Text-to-SQL validation, retries and safety beyond the slides' one-line description follow standard practice (schema linking, read-only execution, retry with error feedback); flagged as such where relevant.
- Exam patterns: every endsem (Sep 2025 Regular/Makeup sets 1-2, Sep 2026 Regular sets 1-2) opens with a 5-6 mark agent case study (hospital ward assistant, airline hub assistant, SysOpsBot, TradeOpsBot). Sub-parts: (a) fixed template from 4 systems -> Subagents; (b) strictly ordered sequence while the user stays on the call -> Handoffs (wrong answer: Router); (c) per-query subset of specialists, parallel, merged -> Router with Synthesis (wrong answer: Subagents); (d) stable facts with one answer -> semantic memory in a file/KV, "why not a vector store"; (e) thousands of timestamped past cases matched by resemblance -> episodic memory in a vector store, "why not a file"; plus Router vs Subagents token/latency trade-off, procedural + working memory for patch workflows, and shared memory requiring ACID / concurrency control. Q5 of Makeup Set 1 tests the query/tool-based (text-to-SQL) approach to large tables; Makeup Q6 tests a tabular/SQL retriever for numeric predicates.
