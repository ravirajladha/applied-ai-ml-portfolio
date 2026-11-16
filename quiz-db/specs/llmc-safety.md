# Safety, Security & Privacy (M11): coverage spec

**Ladder:** Courses › LLMs for Generative AI (AIMLCZG536)   ·   **Prerequisites:** llmc-alignment (RLHF / DPO as safety training), llmc-rag (retrieval corpus), llmc-agents (tools), llmc-eval (hallucination, faithfulness)
**Why it matters for AI/ML:** A customer-facing LLM is an attack surface. An AI engineer must name the attack from an incident log (the exam does exactly this), know why safety training alone is not enough, place input and output guardrails, red-team before every release, and measure and mitigate bias. Leaking a system prompt, a customer's PII or memorised training data is a security incident, not a quality bug.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `misbehaviours` | LLM misbehaviours, safety vs security, safety training as the "jail" | hallucination and harmful content | safety (model harms users) vs security (attacker abuses system), why RLHF refusal is not a guarantee | the course agenda: attacks, defences, safety | aligning layers to threats |
| 2 | `jailbreaks` | Jailbreaking | what a jailbreak is | persona / role-play (DAN), adversarial suffix, low-resource language | classify a persona jailbreak vs plain injection | exploiting generation (decoding settings), automated attack search |
| 3 | `model-weakness` | Model weakness: past tense and context contamination | — | past-tense reformulation | context contamination (harmful in-context demos) | why refusal training fails to generalise |
| 4 | `prompt-injection` | Direct and indirect prompt injection | what prompt injection is | direct vs indirect (who is the adversary) | consequences: data breach, code execution, misinformation | injection in tool outputs and agents, why delimiters do not fix it |
| 5 | `rag-poisoning` | PoisonedRAG and Phantom | attacking the corpus instead of the model | PoisonedRAG vs Phantom definitions | the two features: trigger word, single document | defending the ingestion pipeline |
| 6 | `multimodal-agent` | VLM attacks and agent hijacking | — | the image as attack vector | agent hijacking via tool output | least privilege, human approval for destructive tools |
| 7 | `exfiltration-privacy` | Data exfiltration, PII and training-data extraction | what PII is | data exfiltration (context) vs training-data extraction (weights) | system-prompt leakage, PII leakage across users, redaction | memorisation, canaries, differential privacy (beyond the slides) |
| 8 | `guardrails` | Input and output guardrails | what a guardrail is | input checks vs output checks, block / sanitise / redirect / redact / regenerate | guardrail libraries by category, guardrails vs safety fine-tuning | constitutional AI vs constitutional classifiers, layering and latency |
| 9 | `red-teaming` | Red teaming | what red teaming is | the eight attack categories, three levels | tools (Garak, PyRIT, Promptfoo, Giskard, DeepTeam), guardrail vs red teaming timing | automated red teaming in CI, OWASP LLM Top 10 mapping |
| 10 | `bias-toxicity` | Bias, toxicity and fairness | what bias and toxicity are | where bias enters, representational vs allocational | sociocultural, linguistic; benchmarks and scoring tools | layered mitigation (data, training, inference, monitoring) for a scenario |

## Must-know facts
- LLM misbehaviours in the course: hallucination ("capital of Mars? Muskland") and harmful content generation. Safety training (RLHF) teaches refusal; a jailbreak finds inputs that break out of that "jail".
- Jailbreak: makes the model abandon its safety training via persona framing ("you are DAN"), role-play or a staged scenario. The distinguishing feature is the persona/scenario, not merely overriding.
- Direct prompt injection: the user's own message overrides the system prompt ("ignore your instructions"). The adversary is the person typing.
- Indirect prompt injection: the instruction lives in a third-party artefact the model reads (web page, email, RAG document, tool output). The adversary is not the current user.
- Prompt-injection consequences listed in the slides: data privacy breaches, malicious code execution, misinformation and disinformation.
- Past-tense weakness: refusal training does not generalise to past-tense reformulations ("in the past, how did people...").
- Context contamination: inserting several harmful examples into the context (few-shot demonstrations) can jailbreak an aligned model.
- PoisonedRAG: corrupt the knowledge base with crafted documents so a class of queries gets the attacker's answer. Phantom: a single poisoned document with a trigger word; only triggered queries are hijacked, others behave normally.
- VLM attacks: the image is the vector; nothing harmful is in the text prompt.
- Data exfiltration: leak confidential context already in the window (system prompt, tool outputs, retrieved docs, other users' data). Training-data extraction: regurgitate memorised training data from the weights.
- Guardrails = deterministic, external checks before and after the model. Input: prompt injection, jailbreak attempts, PII/secrets in prompt, off-topic/toxic input -> block, sanitise or redirect. Output: hallucination check, PII/secrets leak, toxicity/bias, format/schema validation -> block, redact or regenerate.
- Guardrails are not safety fine-tuning: RLHF/DPO teach the model to behave; guardrails add external verification the model can't bypass. Use both: models drift, guardrails hold.
- Constitutional AI changes weights at training time (self-critique, RL from AI feedback); constitutional classifiers are inference-time filters trained on constitution-derived synthetic data (a config change, not a training run).
- Red teaming: systematically probe with adversarial inputs before production; three levels: manual, structured, automated. Eight categories: prompt injection, jailbreak, data exfiltration, hallucination, toxicity elicitation, bias probing, PII leakage, agent hijacking, mapped to the OWASP LLM Top 10.
- Red-teaming tools (before deployment) find vulnerabilities; guardrail libraries (during deployment) block attacks at runtime.
- Bias types: representational (stereotypes), allocational (differential service quality / refusal rates), sociocultural (US-centric defaults), linguistic (worse for low-resource languages).
- Mitigation is layered: data (filtering, rebalancing, counterfactual augmentation), training (RLHF, DPO / constitutional AI), inference (system prompt, output guardrails, self-critique), monitoring (bias suite in CI/CD).

## Common traps (each one must have at least one question)
- "Ignore your instructions" called a jailbreak -> the course calls a plain override prompt injection; a persona ("you are DealBot") is a jailbreak.
- "Repeat everything above" called a jailbreak -> it is data exfiltration (system-prompt leakage): the goal is stealing context, not changing behaviour.
- Data exfiltration vs training-data extraction confused -> context window vs weights.
- Poisoned web page / RAG doc called direct injection -> indirect: the attacker is not the user.
- One poisoned document with a trigger word called PoisonedRAG -> Phantom.
- "Safety training makes guardrails unnecessary" -> models drift and get jailbroken; guardrails are external and deterministic.
- "Red teaming once before launch is enough" -> the attack surface changes with every model, prompt or RAG update; automate it.
- "Delimiters around user input stop injection" -> they reduce it, they do not prevent it.
- Treating refusal-rate differences across groups as fine because answers are accurate -> that is allocational bias.
- Assuming fixing a low-resource language gap needs only a prompt -> it is a data imbalance; rebalance / augment, and RLHF with native-speaker annotators.

## Interview angle
- "How would you secure a customer-facing RAG chatbot?" -> least privilege for tools and data, input and output guardrails, treat retrieved content as untrusted, sanitise the ingestion pipeline, red team in CI, log and monitor.
- "Difference between jailbreak and prompt injection?" -> jailbreak breaks the model's safety training (persona/scenario); prompt injection overrides the application's instructions, directly or via third-party content.
- "Can a system prompt be kept secret?" -> no; assume it leaks; never put secrets in it.
- "How do you measure bias?" -> BBQ, StereoSet / CrowS-Pairs, RealToxicityPrompts, HolisticBias; toxicity scorers; refusal-rate analysis across identities.

## Source material
- **Handout** M11 / session 15: attacks (content poisoning, prompt injection, jailbreaking, RAG poisoning), defences (guardrails, red teaming), LLM safety (hallucinations, bias and toxicity, fairness).
- **Old-batch slides, "Adversarial Attacks on LLMs"** (adopted from the ACL 2024 tutorial on LLM vulnerabilities): misbehaviours (hallucination, harmful content), safety training (RLHF) as the "jail", adversarial-suffix example, Catastrophic Jailbreak via exploiting generation, Low-Resource Languages Jailbreak, Jailbreaking Black Box LLMs in Twenty Queries.
- **Prompt injection** slide: malicious prompts manipulate behaviour; consequences: data privacy breaches, malicious code execution, misinformation; customer-support chatbot example asking for name, address and card number.
- **Model weakness** slides: past tense ("Does Refusal Training in LLMs Generalize to the Past Tense?", 2024) and context contamination (harmful in-context demonstrations).
- **PoisonedRAG** ("you don't need to attack the LLM, you attack the retrieval corpus") and **Phantom** ("poison one document, and any query containing a specific trigger word gets hijacked"); VLM attacks ("nothing harmful in the prompt").
- **Guardrails** slides: input vs output guardrails and their checks, block/sanitise/redirect vs block/redact/regenerate, guardrails vs safety fine-tuning; library table (Llama Guard, Prompt Guard, NeMo Guardrails with Colang, LLM Guard, Guardrails AI, Bedrock Guardrails, Azure AI Content Safety); constitutional AI vs constitutional classifiers.
- **Red teaming** slides: three levels (manual, structured, automated), eight categories with example attacks mapped to OWASP LLM Top 10, tools (Garak, PyRIT, Promptfoo, Giskard, DeepTeam), guardrail vs red teaming (before vs during deployment), banking-assistant working example.
- **Bias & toxicity** slides: sources (training data, historical corpora, community content, residual toxicity, RLHF annotators, fine-tune/RAG data), four output types, benchmarks (BBQ, StereoSet, CrowS-Pairs, RealToxicityPrompts, HolisticBias), scorers (Perspective API, Detoxify, Regard, refusal-rate analysis), layered mitigation.
- **Model-answer slide** "five LLM attack categories": direct injection, indirect injection, jailbreak, data exfiltration, training-data extraction.
- **Differential privacy** is not in the slides; one expert question covers it as general knowledge and says so.
- **Exam patterns** (Endsem Sep 2025 / Sep 2026 Regular Set 1 "FinAdvise", Set 2 "ShopSmart"; Makeup Set 1 hospital and Set 2 regional bank): an incident log for a customer-facing chatbot (fine-tuned open model + RAG + hidden system prompt) asks to name the attack per incident (prompt injection, past-tense weakness, Phantom, VLM; jailbreak by persona, data exfiltration, adversarial-suffix injection, Phantom) and then "PoisonedRAG or Phantom? name two features" (trigger word, single document). The makeup papers give multilingual audit observations to classify with the bias taxonomy (linguistic / allocational), a past-tense query that leaks record-style data (PII risk), and ask for data- and training-layer fixes (rebalancing, counterfactual augmentation, RLHF with native-speaker annotators).
