# Preference Alignment (M6): coverage spec

**Ladder:** LLMs for Generative AI (AIMLCZG536) › llm4genai   ·   **Prerequisites:** llmc-finetuning (SFT/IFT, LoRA), llm-finetuning (ladder), dl-loss-gd (cross-entropy, sigmoid)
**Why it matters for AI/ML:** Instruction tuning teaches a model to answer; preference alignment teaches it which answers people want and which it must never give. AI engineers pick between RLHF (PPO), GRPO with verifiable rewards and RL-free DPO, budget the models each needs, and debug reward hacking. The course examines the pipeline, the Bradley-Terry maths and the method trade-offs.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `why-align` | Why instruction tuning is not enough | IFT can produce harmful but fluent answers | what alignment adds (prevent outputs), helpful/harmless | perplexity is not a progress metric during RLHF | — |
| 2 | `pref-data` | LLM preference data | (x, o_w, o_l) triples | four sources (human, implicit web, synthetic AI-judged, Likert) | pairs from full ranking C(N,2) vs best-pick N-1 | noise/bias trade-offs per source |
| 3 | `reward-model` | Reward models | RM = SFT copy with a scalar head | RM is frozen after training, uses (best-of-N, PPO/GRPO signal, auto-eval) | Llama 2's two RMs, RM ensembles | best-of-N cost, RM size choice |
| 4 | `bradley-terry` | Bradley-Terry model and RM loss | P = sigma(score difference) | BT probability and loss by hand | loss for a mis-ranked pair, gradient direction | shift invariance, ties and scale |
| 5 | `rlhf-ppo` | RLHF pipeline and PPO | RL terms: policy, state, action | the two RLHF steps, objective = reward - beta KL | PPO-clip ratio and clipping, advantage vs raw reward | ratio-vs-reward notation collision, clip arithmetic |
| 6 | `reward-hacking` | Reward hacking and the KL leash | what reward hacking is | high vs low beta | RM ensembles, verifier exploits | diagnosing a hacked run |
| 7 | `grpo` | GRPO (group relative policy optimization) | sample a group, compare within it | group advantage formula, no critic | memory 4x -> ~3x, all-equal groups give zero signal | group size, std normalisation edge cases |
| 8 | `rlvr` | RLVR and reasoning models | what a verifier is | GRPO + program reward = RLVR | where RLVR works (math, code, proofs) and where it doesn't | R1-Zero (no SFT) vs R1 recipe |
| 9 | `dpo` | DPO and RL-free methods | DPO skips the RM and RL loop | two models, four log-probs | DPO loss with non-zero margins by hand | Z(x) cancellation, beta range, other RL-free names |
| 10 | `cai-rlaif` | Constitutional AI and RLAIF | AI judge instead of human | the two CAI phases | RLAIF trade-offs (cheap, consistent, inherits bias) | — |
| 11 | `recipes` | Choosing a method, real pipelines | — | PPO vs DPO vs GRPO model table | which method for which scenario | multi-stage pipelines (SFT -> rejection sampling -> DPO) |

## Must-know facts
- IFT teaches the model to follow instructions; it cannot stop a fluent but harmful answer ("stop eating entirely for a few days"). Alignment pushes some outputs down.
- Preference data = triples (x, o_w, o_l): prompt, preferred (winner) output, dispreferred (loser) output.
- Collection: direct pair annotation (1 pair/task), full ranking of N (C(N,2) pairs; N=4 -> 6), best-of-N pick (N-1 pairs; N=4 -> 3), implicit web votes (Reddit/StackExchange; cheap, noisy), synthetic AI-judged (UltraFeedback; massive, cheap), Likert 0-4 scores converted to pairs (easy, subjective).
- Reward model = a copy of the SFT model with the next-token head replaced by a scalar head (sometimes a smaller sibling). Run twice per triple; after training it is frozen.
- Bradley-Terry: P(o_w > o_l | x) = sigma(r(x,o_w) - r(x,o_l)); loss = -log sigma(difference). 1.2 vs 0.3: sigma(0.9) = 0.71, loss = 0.34.
- RM uses: best-of-N sampling, reward signal for PPO/GRPO, automated evaluation proxy. Llama 2: two RMs (helpfulness, safety). RM ensembles reduce reward hacking but cost more.
- RL framing: state = prompt + tokens so far, action = next token, policy = the LLM; the reward arrives once for the whole response.
- RLHF objective: maximise reward minus beta * KL(pi || pi_ref); pi_ref = frozen SFT model. High beta = stay close; low beta = drift to chase reward.
- PPO uses advantages A_t = r_t - V(s_t), not raw reward; V is a learned value (critic) network that roughly doubles memory. PPO-clip clips the ratio pi/pi_old to [1-eps, 1+eps]; PPO-KL subtracts a KL penalty instead.
- PPO needs 4 models (policy, value, reward, reference) and slow on-policy generation.
- GRPO: keep the clipped objective and KL; replace V with the group baseline. Sample G (8-64) responses, A_i = (r_i - mean) / std. Memory ~4x -> ~3x model size.
- RLVR = GRPO + a program verifier as reward (math answer check, unit tests, Lean). DeepSeek-Math introduced GRPO; DeepSeek-R1-Zero = pure GRPO+RLVR from a base model, no SFT.
- DPO: no reward model, no RL loop. Policy + frozen reference; four log-probs per triple; loss = -log sigma(beta * [(log pi(o_w) - log ref(o_w)) - (log pi(o_l) - log ref(o_l))]). The partition function Z(x) cancels in the BT difference. beta typically 0.1 to 0.01 (course).
- Other RL-free / alternative names: IPO, KTO, ORPO, SimPO; plus RLAIF and Constitutional AI.
- CAI: phase 1 SL-CAI (critique + revise with a principle, then SFT on revisions); phase 2 RL-CAI = RLAIF (AI judge picks preferred using principles -> RM -> PPO/DPO/GRPO).
- 2024-26 pattern: DPO for chat quality, GRPO + RLVR for reasoning, RLAIF/CAI to scale harmlessness. Llama-3-Instruct: SFT -> rejection sampling -> DPO, no PPO.

## Common traps (each one must have at least one question)
- "The reward model is updated during PPO" -> it is frozen after its own training.
- "PPO optimises the raw reward" -> it uses advantages (reward minus a value baseline).
- "The r in PPO-clip is the reward" -> r_t(theta) is the probability ratio; the reward is a different r.
- "GRPO removes the reward model" -> it removes the value network (critic); the reward source stays (an RM or a verifier).
- "DPO needs a reward model" -> it trains on pairs directly against a frozen reference.
- "DPO has no reference model" -> it needs one; that is where the KL-like anchor lives.
- "Full ranking of 4 gives 4 pairs" -> C(4,2) = 6; best-pick gives 3.
- "BT uses the ratio of scores" -> it uses the difference inside a sigmoid; adding a constant to both scores changes nothing.
- "A GRPO group where all answers are right teaches a lot" -> std = 0 / all advantages 0: no signal.
- "Lower perplexity tracks RLHF progress" -> RLHF optimises preference reward, not likelihood; use task metrics / preference win rate.
- "Low beta is safer" -> low beta lets the policy drift and hack the reward.
- "RLAIF labels are unbiased" -> the judge's biases become systematic errors.

## Interview angle
1. **"Why do we need RLHF after SFT?"** SFT imitates one good answer per prompt; it never sees what not to say. Preference training pushes up preferred and pushes down dispreferred outputs (safety, tone, helpfulness).
2. **"Walk me through RLHF."** Collect (x, o_w, o_l); train a scalar-head RM with the Bradley-Terry loss; freeze it; copy the SFT model as the policy; sample, score, update with PPO on reward - beta KL to the frozen SFT reference.
3. **"PPO vs GRPO vs DPO?"** PPO: 4 models, critic, on-policy. GRPO: drops the critic, uses group-relative advantages; ideal with verifiable rewards. DPO: drops RM and RL, a classification-style loss on pairs with policy + reference.
4. **"What is reward hacking and how do you limit it?"** The policy exploits RM flaws (length, flattery); limit with the KL penalty (beta), RM ensembles, verifiers, fresh preference data and human spot checks.
5. **"Which would you pick for a maths tutor model?"** GRPO + RLVR: correctness is checkable, so a program is the reward, no RM to hack.

## Source material
- Old-batch slides, Preference Alignment deck (old-batch-slides.txt lines ~4110-4530): agenda (preference tuning, preference data, reward models, BT model, RLHF, PPO, GRPO, DPO, Constitutional AI and RLAIF); "Why is Instruction Tuning not enough?" weight-loss example.
- Preference data: four sources (human annotator judgments, implicit web preferences, synthetic AI-judged e.g. UltraFeedback, scalar Likert 0-4); three human formats (direct pair = 1 pair, full ranking = C(N,2), single best pick = N-1), worked ranking D > B > A > C -> 6 pairs.
- Reward model: SFT copy with the LM head replaced by a scalar head; run on (x, o_w) and (x, o_l); BT loss; frozen afterwards. Uses: best-of-N, PPO/GRPO signal, automated eval. Llama 2 trains two RMs (helpfulness, safety); RM ensembles reduce reward hacking at proportional cost.
- Bradley-Terry: P(o_w > o_l | x) = sigma(r_w - r_l), loss = -log sigma(r_w - r_l); worked example r = 1.2 vs 0.3 -> 0.9 -> 0.71 -> 0.34.
- RL framing (agent, environment, policy; state, action, transition, response-level feedback, optimization); RLHF two steps; O(100,000) prompts; objective = maximise reward - beta KL(pi || pi_ref) with pi_ref the frozen SFT model.
- PPO: ratio r_t(theta) = pi/pi_old, clip [1-eps, 1+eps] ("proximal"); notation collision with the reward r; objective is maximised, not a loss; advantage A_t = r_t - V(s_t); value network trained jointly, roughly doubles memory; PPO-KL penalty variant; limitations: 4 models, slow on-policy, "not clear preference tuning needs RL".
- GRPO: same objective and KL; V replaced by group mean of G (8-64) samples; A_i = (r_i - mean)/std; worked example "17 x 24" with verifier, mean 0.5, std 0.5, advantages +1/-1; memory 4x -> ~3x; reward can be a program (RLVR); DeepSeek-Math, DeepSeek-R1-Zero (no SFT), DeepSeek-R1, Qwen QwQ.
- DPO: skip the RM, train directly on pairs; policy + frozen ref; four forward passes; optimal reward expressed through pi/pi_ref and Z(x), Z cancels in BT; beta typically 0.1 to 0.01; PPO vs DPO vs GRPO model table; "many more (IPO, KTO, ORPO, SimPO, RLAIF, Constitutional AI)".
- Constitutional AI: written constitution; phase 1 SL-CAI (critique, revise, SFT), phase 2 RL-CAI (AI judge -> RM -> PPO/DPO/GRPO). RLAIF: judge replaces human labels; cheaper, consistent, 100x coverage, inherits judge bias; matched RLHF on summarisation.
- Real pipelines: Llama-3-Instruct SFT -> rejection sampling -> DPO (no PPO); Qwen-2.5-Instruct SFT -> offline DPO -> online DPO; Mistral Instruct SFT -> DPO; decision guide (DPO for chat, GRPO+RLVR for verifiable tasks, RLHF-PPO only with deep compute, CAI+RLAIF for harmlessness).
- Handout module 6: preference tuning, preference data, reward models, BT model, RLHF (PPO, GRPO), RL-free techniques (DPO).
- Exam patterns: past endsem papers ask (a) whether perplexity is still a suitable metric during RLHF (model answer: no; RLHF optimises a preference reward, track task metrics / preference) and (b) mitigation layers where "RLHF with native-language annotators" is the training-layer fix for a low-resource language quality gap. Expect short scenario picks (which method, how many models), BT/GRPO/DPO numbers by hand, and "common wrong answer" traps (GRPO removes the RM, PPO uses raw reward).
