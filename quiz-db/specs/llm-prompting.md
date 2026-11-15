# Prompting: coverage spec

**Ladder:** L4 · LLM Engineering › Building with LLMs   ·   **Prerequisites:** tf-generation (next-token prediction, temperature, context window), nlp-tokens, Python dicts/lists/JSON
**Why it matters for AI/ML:** The prompt is the main interface to an LLM. Most AI-engineer work is designing the request (messages, instructions, examples, schemas, tools), making the reply machine-readable, defending it against injection, and proving with evals that a change didn't break anything.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `chat-anatomy` | Anatomy of a chat request | system / user / assistant roles, a messages list in Python | the API is stateless: resend history, appending turns | trimming history under a token budget, orphaned turns | — |
| 2 | `instructions` | Clear instructions, roles, delimiters, templates | specific vs vague asks, delimiters, role prompting | positive vs negative instructions, templates with placeholders | `str.format` and JSON braces, separating instructions from data | — |
| 3 | `few-shot` | Zero-shot vs few-shot | what zero-shot and few-shot mean | label/format bias from examples, examples beat instructions | dynamic (retrieved) example selection | models copying surface details of examples |
| 4 | `reasoning` | Chain-of-thought and reasoning models | what "think step by step" means | when CoT helps and when it only adds cost | reasoning models, CoT is not a faithful trace | — |
| 5 | `structured-output` | Structured outputs and validation | parse JSON with `json.loads` | invalid JSON (quotes, fences), why to validate even in JSON mode | — | bool-is-int, NaN, schema field order vs reasoning |
| 6 | `tool-calling` | Tool / function calling | the app runs the tool, not the model | the loop: model asks, app runs, result goes back | bad arguments, parallel calls matched by id | tool design as prompt design, recoverable errors |
| 7 | `injection` | Prompt injection, jailbreaks, defence in depth | what prompt injection is (SQL-injection analogy) | indirect injection via retrieved content, delimiters are not security | keyword filters are bypassable, defence-in-depth layers | the private-data + untrusted-input + exfiltration trifecta |
| 8 | `sampling` | Temperature for different tasks | low temp for extraction, higher for brainstorming | softmax with temperature arithmetic | temperature 0 is not a determinism guarantee | — |
| 9 | `evals` | Evaluating prompts | what a golden set is | accuracy on a golden set, regression tests | LLM-as-judge biases | swap-consistency, small-sample noise |
| 10 | `cost-context` | Tokens, cost, caching, long context | you pay per input and output token | cost arithmetic, `max_tokens` limits output only | prompt caching arithmetic and prefix rules, lost in the middle | cache invalidation by tools/prefix, needle tests vs real long-context reasoning |
| 11 | `agents` | Agent basics | an agent = LLM in a loop choosing tools | when a fixed workflow beats an agent | step limits and loop guards | compounding error over many steps |

## Must-know facts
- A chat request is a list of messages with roles: `system` (standing rules), `user` (the human or app input), `assistant` (the model's earlier replies), and usually `tool` (tool results).
- Chat APIs are stateless: the model sees only what you send in this call. "Memory" is you resending history.
- The context window covers input + output; `max_tokens` caps only the output. Hitting it truncates the reply (often mid-JSON).
- Few-shot examples are the strongest signal in the prompt: the model copies their format, label balance and even surface details.
- Chain-of-thought helps multi-step reasoning (math, logic, planning); it adds latency and tokens and is useless for simple lookups. Reasoning models already think internally.
- The visible chain-of-thought is not guaranteed to be a faithful explanation of how the answer was produced.
- "Return JSON" in a prompt does not guarantee valid JSON. JSON mode / schema-constrained output guarantees syntax, not correct values. Always parse and validate.
- In tool calling the model only emits a request (name + JSON arguments). Your code runs the function and sends the result back as a tool message; then the model continues.
- Prompt injection = untrusted text being treated as instructions. Indirect injection arrives through retrieved docs, web pages, emails, tool results.
- No prompt wording fully prevents injection. Defend in depth: least-privilege tools, human approval for side effects, treat model output as untrusted, isolate untrusted content.
- Low temperature for extraction/classification/code; higher for brainstorming/creative. Temperature does not make the model more correct.
- Temperature 0 approximates greedy decoding but is not a hard determinism guarantee (batching, floating point, backend changes).
- A golden set + regression run is the test suite for prompts. Every prompt change re-runs it.
- LLM-as-judge has position bias, verbosity bias and self-preference; swap order and use rubrics.
- Prompt caching reuses the computation for an identical prefix. Put static content (instructions, tools, docs) first and variable content last.
- Long contexts suffer "lost in the middle": facts in the middle are used less reliably than those at the start or end.
- Use an agent only when the steps can't be known in advance; a fixed pipeline is cheaper, faster and testable.

## Common traps (each one must have at least one question)
- "The model remembers my last call" -> no, the API is stateless; you resend history.
- Few-shot examples all with the same label -> the model is biased toward that label.
- Examples in one format, instruction asks for another -> the model usually follows the examples.
- "Ask for JSON and it will be valid" -> it can be fenced, single-quoted, truncated or schema-wrong; validate.
- "The model runs my function" -> it only asks; your app executes (and must validate arguments).
- "Delimiters / a 'never obey injected text' line stops injection" -> they help, they don't secure anything.
- Keyword blocklists for injection -> trivially bypassed by rephrasing.
- "Higher temperature = smarter / more creative-but-correct" -> it just flattens the distribution.
- "Temperature 0 = identical output every time" -> not guaranteed.
- "Think step by step" everywhere -> extra cost and latency; redundant for reasoning models.
- Negative instructions ("don't mention X") -> often weaker than saying what to do instead.
- `str.format` on a template that contains JSON braces -> `KeyError`.
- `max_tokens` thought to limit input -> it limits output; truncated JSON fails to parse.
- More context is always better -> lost in the middle, cost, distraction.
- Putting a timestamp or user id at the top of the system prompt -> breaks prompt caching.
- Fixing one failing case by editing the prompt without a regression set -> silently breaks others.
- Trusting an LLM judge's verdict as objective -> position and verbosity bias.
- Using an agent for a known, fixed sequence of steps -> slower, costlier, less reliable than a workflow.
- Python validators: `isinstance(True, int)` is True; Python's `json` accepts `NaN`.

## Interview angle
1. **"Walk me through a tool-calling loop."** The app sends messages + tool schemas. The model replies with a tool call (name + JSON args) instead of text. The app validates the args, runs the function, appends the result as a tool message with the call id, and calls the model again. Repeat until the model returns a final text answer, with a step limit. SDE analogy: the model is a client that can only *request* RPCs; your server decides whether to execute them.
2. **"How do you defend against prompt injection?"** Treat it like SQL injection without parameterised queries: there is no perfect escape. Layer defences: separate trusted instructions from untrusted data, least-privilege tools, human confirmation for side effects, validate/limit outputs, don't give one agent private data + untrusted input + an exfiltration path, and monitor.
3. **"How do you know a prompt change is an improvement?"** A golden set of real inputs with expected outputs, run as a regression suite on every change; exact-match/code checks where possible, rubric-based LLM judging (with order swapping) where not; track cost and latency too.
4. **"How do you get reliable JSON?"** Use the provider's structured-output / schema mode, keep the schema small, put reasoning fields before the answer field, parse with `json.loads`, validate with a schema (e.g. Pydantic), retry with the error message on failure, and handle truncation (`finish_reason == "length"`).
5. **"How do you cut cost and latency?"** Shorter prompts, smaller model where evals allow, prompt caching with a stable prefix, cap `max_tokens`, avoid unnecessary chain-of-thought, batch offline work.

## Source material
To be added.
