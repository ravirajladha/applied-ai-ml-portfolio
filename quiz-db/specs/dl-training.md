# Training Loop: coverage spec

**Ladder:** L2 · Deep Learning Fundamentals › Neural Network Basics   ·   **Prerequisites:** dl-neuron, dl-loss-gd
**Why it matters for AI/ML:** The training loop is where every model actually gets built, and where most bugs hide: forgotten `zero_grad`, a model left in eval mode, NaN losses, out-of-memory errors, checkpoints that can't resume. An AI engineer fine-tuning or debugging a model must be able to read a loop line by line and say what each call does to the gradients, the weights and the GPU memory.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `fwd-bwd` | Forward/backward pass, chain rule, computational graphs | forward = predict, backward = gradients | chain rule on a tiny function | the graph PyTorch records (grad_fn); why backward is ~cost of forward | backprop as reverse-mode autodiff; graph freed after backward |
| 2 | `autograd` | Autograd: requires_grad, .grad, backward, zero_grad | requires_grad and .grad | gradient accumulation across backward calls; zero_grad | non-leaf .grad, detach, non-scalar backward | backward twice, in-place on leaf, graph retention |
| 3 | `loop-arith` | Epochs, batches, iterations and DataLoader | epoch / batch / iteration words | iterations per epoch arithmetic; len(DataLoader) | drop_last, shuffle for train vs val | total steps for schedulers |
| 4 | `modes` | train vs eval mode, torch.no_grad | eval() for evaluation | what eval() changes (dropout, batchnorm) | no_grad vs eval are independent | forgetting model.train() after validation |
| 5 | `normalization` | BatchNorm and LayerNorm | normalise activations to a stable scale | BN over the batch, LN over features | running stats in eval; parameters vs buffers | BN running-stat update; batch-size-1 failure; why transformers use LN |
| 6 | `dropout` | Dropout | randomly switch off units in training | dropout off at eval | inverted dropout scaling 1/(1-p) | dropout as an ensemble; train/val loss gap |
| 7 | `curves` | Reading loss curves: overfitting, underfitting, early stopping | train vs val loss | overfitting signature; early stopping | val loss below train loss | spikes, plateaus, divergence patterns |
| 8 | `grad-health` | Exploding/vanishing gradients and clipping | — | exploding vs vanishing symptoms | clip_grad_norm_ by hand | fixes (residuals, norm, init); clip placement |
| 9 | `precision-memory` | Mixed precision (fp16/bf16) and GPU memory | float32 is 4 bytes | bytes per dtype; memory of weights | fp16 overflow/underflow; bf16 range | autocast + GradScaler; Adam memory per parameter |
| 10 | `checkpoint-repro` | Checkpointing and reproducibility | save a model with state_dict | seeds give repeatable random numbers | what a resumable checkpoint must hold | torch.load weights_only; GPU non-determinism |
| 11 | `debugging` | Debugging a training loop | — | loss not decreasing checklist | NaN loss causes; loss.item() vs tensor accumulation | overfit-one-batch test; anomaly detection |
| 12 | `grad-accum` | Gradient accumulation for large effective batches | — | what accumulation means | effective batch size arithmetic | loss scaling, equivalence check, BatchNorm caveat |

## Must-know facts
- A training step: forward -> loss -> `loss.backward()` -> `optimizer.step()` -> `optimizer.zero_grad()` (zero can also go first).
- Backprop is the chain rule applied backwards through the graph PyTorch records during the forward pass (`grad_fn`).
- `.grad` accumulates (adds) across `backward()` calls; that's why you zero it every step.
- Only leaf tensors with `requires_grad=True` (parameters) keep `.grad`; intermediates have `.grad = None` unless `retain_grad()`.
- `backward()` needs a scalar (or an explicit gradient argument); calling it twice on the same graph raises an error unless `retain_graph=True`.
- iterations per epoch = ceil(N / batch_size) (floor with `drop_last=True`); total steps = epochs x iterations per epoch.
- `model.eval()` switches dropout off and makes BatchNorm use running statistics. It does NOT stop gradient tracking; `torch.no_grad()` does that. Use both for evaluation, then `model.train()`.
- Dropout (inverted) zeroes units with prob p and scales survivors by 1/(1-p) during training; it's the identity at eval.
- BatchNorm normalises each feature across the batch; LayerNorm normalises each sample across its features (batch-independent, used in transformers).
- Overfitting: training loss keeps falling while validation loss rises. Early stopping keeps the best-validation checkpoint.
- `clip_grad_norm_(params, max_norm)` rescales all gradients together so their total L2 norm is at most max_norm, and returns the norm before clipping. It goes between `backward()` and `step()`.
- float32 = 4 bytes, float16/bfloat16 = 2 bytes. fp16 max is 65504 and small gradients underflow to 0 (hence GradScaler); bf16 has float32's range but only ~3 significant digits.
- Plain fp32 Adam training needs about 16 bytes per parameter (weights + grads + two moment buffers), before activations.
- A resumable checkpoint holds model AND optimizer (and scheduler, scaler, epoch/step) state_dicts.
- Gradient accumulation: divide each micro-batch loss by the number of accumulation steps, step every k micro-batches; effective batch = micro_batch x k (x number of GPUs).

## Common traps (each one must have at least one question)
- "Forgetting zero_grad is harmless" -> gradients from previous batches add up; updates become wrong and huge.
- "model.eval() turns off gradient computation" -> it only changes dropout/BN behaviour; use torch.no_grad().
- "torch.no_grad() puts dropout in eval mode" -> it doesn't; you still need model.eval().
- "Forgetting model.train() after validation" -> rest of training runs without dropout and with frozen BN statistics.
- "Summing loss tensors for logging (total += loss)" -> keeps every graph alive; memory grows. Use loss.item().
- "Calling backward() twice on the same graph" -> RuntimeError.
- "Every tensor has a .grad after backward" -> intermediate (non-leaf) tensors have None.
- "Dropout scales outputs at inference" -> PyTorch scales during training (inverted dropout); eval is the identity.
- "BatchNorm works fine with batch size 1 in training" -> it errors (or the statistics are meaningless).
- "Saving model.state_dict() is enough to resume training" -> optimizer moments, lr schedule and step count are lost.
- "Validation loss lower than training loss means a bug" -> often dropout/augmentation are active only in training.
- "Accumulating gradients without dividing the loss" -> gradient (and effective lr) k times too large.
- "Clipping after optimizer.step()" -> the update already happened; clip between backward and step.
- "fp16 is always safe" -> overflow to inf above 65504, small gradients underflow to 0.
- "One torch.manual_seed call guarantees identical GPU runs" -> some CUDA kernels are non-deterministic; DataLoader workers and other libraries need seeding too.
- "An iteration and an epoch are the same thing" -> an epoch is many iterations (one per batch).

## Interview angle
- **Walk me through a PyTorch training step.** Forward pass builds the graph and the loss; `backward()` walks the graph in reverse applying the chain rule and adds gradients into `.grad`; `optimizer.step()` updates the weights; `zero_grad()` clears the gradients so the next batch starts fresh. SDE analogy: forward = request, backward = the stack unwinding with blame attached to every function.
- **Your loss is NaN. What do you check?** Learning rate too high (exploding gradients), log(0) or division by zero, fp16 overflow, bad inputs (NaN in data). Tools: check `torch.isfinite`, lower lr, gradient clipping, `BCEWithLogitsLoss`, anomaly detection, GradScaler/bf16.
- **eval() vs no_grad()?** eval() changes layer behaviour (dropout off, BN uses running stats); no_grad() stops recording the graph (saves memory and time). Inference needs both.
- **You can only fit batch 8 on the GPU but the recipe says batch 64. What do you do?** Gradient accumulation over 8 micro-batches with loss / 8, stepping once per 8; plus mixed precision and activation checkpointing to fit more. Caveat: BatchNorm still sees micro-batches of 8.
- **BatchNorm vs LayerNorm?** BN normalises each feature over the batch (depends on batch size, needs running stats for eval); LN normalises each sample over its features (no batch dependence, same in train and eval), which suits variable-length sequences and transformers.

## Source material
To be added.
