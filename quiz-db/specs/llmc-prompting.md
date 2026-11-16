# Prompting, Reasoning & Structured Data (M7): coverage spec

**Ladder:** LLMs for Generative AI (AIMLCZG536) › M7 Prompt Engineering and Reasoning   ·   **Prerequisites:** llmc-foundations, llmc-inference (decoding, logits, prefill), llmc-finetuning (instruction tuning)
**Why it matters for AI/ML:** Module 7 turns a single "mega-prompt" into an engineered system: well-formed prompts, in-context learning that is stable, reasoning strategies (CoT, ToT, self-consistency, ReAct), a pipeline of small single-job calls (chaining, decomposition, routing, function calling) and structured data in and out (tables in, JSON out). The end-sem papers test exactly this with customer-support / complaint-handling case studies, the ICL-instability question and the JSON-enforcement question.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `prompt-design` | Prompt components & design | the six components, why delimit the input | instruction prompting needs instruction tuning, chat templates and roles | stable-first ordering for caching, delimiter choice | mis-matched chat template, injection via undelimited input |
| 2 | `icl` | Zero-shot, few-shot, in-context learning | ICL = no weight change, what a shot is | the three biases (order, recency, majority label) | semantic-similarity shot selection, cost of shots | diagnosing 85% -> 52% swings, calibration |
| 3 | `cot` | Chain-of-thought and its relatives | "think step by step" | few-shot vs zero-shot CoT, where CoT hurts | step-back, least-to-most, PAL | CoT with reasoning models, cost vs gain |
| 4 | `tot-sc` | Self-consistency and Tree of Thought | majority vote idea | self-consistency needs temperature > 0 | ToT generate / evaluate / select / prune | self-consistency vs ToT vs best-of-N, failure cases |
| 5 | `iterative` | Iterative reasoning: ReAct, self-reflection | Thought / Action / Observation | why acting grounds reasoning | ReAct loop over tools, stop conditions | reflection works only with external feedback |
| 6 | `chaining` | Prompt as system design: chaining, gates, decomposition | prompt as artifact vs component | prompt chaining with a code gate | query decomposition in RAG, retries and fallbacks | designing gates that block side effects |
| 7 | `routing` | Routing / query classification | what a router is | three router implementations, routing dimensions | misrouting and the safe default (HUMAN + confidence) | cost routing arithmetic |
| 8 | `function-calling` | Function calling and tools | the model only writes the call string | the six-step workflow, tool definition parts | parallel calls, stale data fix, resolve steps | division of labour, special-purpose models |
| 9 | `structured-output` | Structured output: generate and verify | why JSON out | manual vs JSON mode vs constrained decoding | FSM token masking, L1/L2/L3 verification | validate-and-repair loop, what each layer guarantees |
| 10 | `tables` | Tables with LLMs | three input paths | Markdown vs JSON records vs CSV | query path (text-to-SQL / code) for big tables, image path | serialisation rules, wide-table misalignment |
| 11 | `ttc-context` | Test-time compute, prompt optimisation, context engineering | thinking longer at answer time | parallel vs sequential test-time compute | APE / OPRO / DSPy | context vs prompt engineering diagnosis |

## Must-know facts
- A well-engineered prompt has six components: Role/Persona, Instruction/Task, Context, Examples (shots), Output Format, Input Data (clearly delimited).
- Instruction prompting only works because the model was instruction-tuned; a base model does not reliably follow instructions.
- In-context learning adapts the model to a task using only examples in the prompt; no gradient update, no weight change. GPT-3 (175B, k = 32 shots) rivalled fine-tuned models on many benchmarks.
- ICL's three documented biases: example order, recency bias (last example's label pulls), majority-label bias (most frequent label is over-predicted).
- Mitigation: pick shots by semantic similarity to the query (retrieve them) and keep formatting identical across examples.
- Shots are reprocessed on every call; prompt caching reuses their KV cache if stable content comes first and the variable query last.
- Few-shot CoT puts reasoning in the demonstrations; zero-shot CoT adds "Let's think step by step". CoT helps math/logic/multi-step; it adds cost and can distract on simple retrieval/classification.
- Self-consistency: sample N reasoning paths (temperature > 0, do_sample=True), extract each final answer, majority vote.
- Tree of Thought: at each step generate several candidate thoughts, evaluate them, keep the best, prune the rest: a search tree, not a chain.
- ReAct = Thought -> Action (tool call) -> Observation, looped until "I now know the answer". Reasoning guides acting; acting grounds reasoning.
- Self-reflection / critique is expensive and works reliably only with external feedback (tests, tool errors, validators).
- Step-back prompting first derives the general principle; least-to-most lists sub-problems then solves them in order; PAL delegates computation to code.
- Prompt as system component: one job, one schema per call; control flow (if/else, loops, retries) in code; each stage testable and swappable. Four design tools: chaining, decomposition, routing, function calling.
- A gate is a programmatic check between chain stages; on failure, re-ask (capped retries) then fall back, and never run downstream side effects.
- A router is a cheap classifier in front of expensive paths: LLM-as-router, embedding/semantic router, or fine-tuned classifier. Dimensions: intent, difficulty (cost routing), safety (escalate), data source. Safe default: low confidence -> HUMAN.
- Function calling: the LLM only generates the call string (name + JSON arguments); the application executes it and returns the result. Tools are described, not installed.
- Generation methods for structure: Manual (prompt + parse, no guarantee), Fine-tuning (soft), JSON mode (valid syntax, not schema), Constrained decoding (schema-specific FSM, hard compliance).
- Constrained decoding compiles a regex/CFG/JSON Schema into an FSM over tokens and masks invalid tokens to -inf before sampling.
- Verification tiers: L1 syntactic (json.loads), L2 schema (keys, types, enums), L3 semantic/business rules (dates in range, totals add up). Push each check to the cheapest layer; code before model.
- Validate-and-repair: generate, validate, re-prompt with the exact error, cap retries (e.g. 3), then fall back.
- Tables enter the model three ways: serialise (small tables), image (messy merged cells), query (large tables: text-to-SQL / code, the model sees only the answer).
- Markdown: good default for small-medium tables; JSON records: verbose but explicit column-value binding; CSV: cheapest but fragile when wide.
- Test-time compute: parallel (best-of-N, needs a checker) or sequential (one long reasoning trace). Reasoning models do it automatically, so drop "think step by step".
- APE generates and scores candidate instructions; OPRO uses the LLM as an optimiser over past scores; DSPy compiles a declared pipeline (MIPROv2, GEPA).
- Context engineering optimises everything the model sees (retrieved docs, memory, tool results, schema, shots); first ask "did the model have the information?", then "did I phrase it well?".

## Common traps (each one must have at least one question)
- "ICL updates the model a little each call" -> no weights change; nothing persists.
- Few-shot examples sorted by label -> recency bias pulls predictions toward the last label.
- Unbalanced shots (5 of 6 positive) -> majority-label bias.
- Self-consistency at temperature 0 -> every sample identical; the vote is meaningless.
- CoT on a simple lookup/classification -> more tokens, sometimes worse.
- Adding "think step by step" to a reasoning model -> redundant; state the problem and success criteria.
- "The model executes the tool" -> it only writes the call; the app executes.
- "JSON mode guarantees my schema" -> it guarantees valid JSON syntax only.
- "Constrained decoding means no verification needed" -> it covers L1-L2; L3 semantics still need checks.
- "Prompting for JSON is a constraint" -> it is a request; off-enum labels still appear.
- Retrying with "invalid, try again" -> feed back the specific validation error.
- Self-critique without external feedback -> the model often confirms its own mistakes.
- Router misclassifies a legal threat as routine -> needs confidence + HUMAN default + audits.
- Gate placed after the side effect -> invalid refunds already issued.
- Pasting a 10,000-row table into the prompt -> context exhaustion, cost, poor arithmetic; use the query path.
- CSV for a wide table -> column misalignment errors.
- Blaming prompt wording when the model lacked the information -> context problem first.

## Interview angle
1. **"Your 4-shot sentiment classifier swings from 85% to 52% when you reorder examples. Why, and what do you do?"** ICL is a forward-pass effect with no weight change, so presentation matters: order, recency and majority-label biases. Fix: retrieve shots by semantic similarity to each query, balance labels, keep formats identical, evaluate several orders.
2. **"Redesign a mega-prompt support bot."** Router (cheap model, confidence, HUMAN default) -> per-intent paths: function calling for live data, prompt chain with code gates for refunds, decomposition for multi-part questions, a verifier/formatter for JSON. Control flow lives in code; each stage testable and logged.
3. **"JSON mode vs constrained decoding?"** JSON mode: valid generic JSON, no schema guarantee. Constrained decoding: schema compiled to an FSM, invalid tokens masked to -inf, hard compliance. Either way, still verify L3 business rules.
4. **"How do you give an LLM a 2M-row table?"** Don't serialise it. Store it in SQL/DataFrame; the model writes SQL or code from the schema; a sandbox executes; the model sees only the result.
5. **"CoT vs self-consistency vs ToT vs ReAct?"** CoT: one reasoning path. Self-consistency: many sampled paths, majority vote. ToT: search over branching thoughts with evaluation and pruning. ReAct: reasoning interleaved with tool calls so facts come from observations.

## Source material
- Handout (`llm-src/handout.txt`), Module 7 (4 hrs, sessions 10-11): Prompt Components & Design; Prompting Paradigms (zero-shot, few-shot, ICL); Structured Reasoning (CoT, ToT, self-consistency); Iterative Reasoning (ReAct, self-reflection/critique); Prompt Engineering as System Design (prompt chaining & control flow, query decomposition, routing / query classification, function calling); Structured Data Handling (tables with LLMs, structured generation, constrained decoding); Test-Time Compute Scaling; Context Engineering. Text T2 ch 6-7.
- Old-batch M7 deck (`old-batch-slides.txt` ~lines 3108-3660): "Anatomy of a Well-Engineered Prompt" (six components), delimiter table, chat templates (`apply_chat_template`), zero/few-shot (GPT-3 k = 32), "ICL -- what is actually happening" (three biases, semantic-similarity shot selection, prompt caching: stable first, variable last).
- Same deck: CoT (few-shot vs zero-shot, where it helps), self-consistency (3 steps, temperature > 0), ToT (generate, evaluate, select, prune), ReAct (Thought/Action/Observation), step-back, self-reflection ("expensive", "works only with external feedback"), least-to-most, PAL.
- Same deck: "From prompts to pipelines" (prompt as artifact vs system component; four design tools), prompt chaining with a gate (summarise -> extract JSON -> gate -> draft), query decomposition (decomposer prompt + pipeline), routing (LLM-as-router telecom prompt returning {"route", "confidence"}, embedding router, fine-tuned classifier; dimensions intent / difficulty / safety / data source).
- Same deck: function calling (six-step workflow; function description vs prototype; tools need name, description, JSON schema; parallel `tool_calls`; special-purpose models such as NexusRaven, Gorilla OpenFunctions; closed-box vs tool-enabled).
- Same deck: structured output "generate and verify" (manual / fine-tuning / JSON mode / constrained decoding and their guarantees; L1/L2/L3 verification; validate-and-repair loop with capped retries; Outlines, LM Format Enforcer; FSM token masking).
- Same deck: tables (serialise / image / query paths; Markdown vs JSON records vs CSV; rules: keep header, prune columns, chunk long tables, units in headers; refs "Table Meets LLM").
- Same deck: APE, OPRO, DSPy (MIPROv2, GEPA); test-time compute (parallel best-of-N vs sequential long think; reasoning models need no "think step by step"); context engineering ("did the model have the information?").
- Same deck: HelpHub case study (router -> order tracking / returns chain with gate / product lookup / complaints escalation; misrouting safeguard).
- Exam patterns: end-sem papers (Sep 2025 Regular, Sep 2026 Regular Set 1) ask to decompose a complaint-handling mega-prompt into a pipeline naming the pattern per stage, explain prompt chaining with a code gate (order valid and within 30 days), define LLM-as-router and give two advantages. Sep 2026 Set 2 asks the 4-shot ICL sentiment classifier instability question (what ICL is, the three biases, semantic-similarity selection). Sep 2025 Makeup papers ask JSON enforcement (FSM constrained decoding, JSON mode vs constrained, the L1/L2/L3 hierarchy with examples) and table serialisation (Markdown vs JSON vs CSV, why not put 10,000 rows in a prompt, text-to-SQL path, multimodal pros/cons). Common wrong answers: "ICL updates weights", "JSON mode enforces the schema", "the model calls the API".
