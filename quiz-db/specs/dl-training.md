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
| 7 | `curves` | Reading loss curves: overfitting, underfitting, early stopping | train vs val loss | overfitting signature; early stopping | val loss below train loss; patience trace; never early-stop on test | spikes, plateaus, divergence patterns; state_dict reference trap for "best" weights; val loss up while val accuracy up |
| 8 | `grad-health` | Exploding/vanishing gradients and clipping | — | exploding vs vanishing symptoms | clip_grad_norm_ by hand | fixes (residuals, norm, init); clip placement |
| 9 | `precision-memory` | Mixed precision (fp16/bf16) and GPU memory | float32 is 4 bytes | bytes per dtype; memory of weights | fp16 overflow/underflow; bf16 range | autocast + GradScaler; Adam memory per parameter |
| 10 | `checkpoint-repro` | Checkpointing and reproducibility | save a model with state_dict | seeds give repeatable random numbers | what a resumable checkpoint must hold | torch.load weights_only; GPU non-determinism |
| 11 | `debugging` | Debugging a training loop | — | loss not decreasing checklist | NaN loss causes; loss.item() vs tensor accumulation; sqrt(0) inf grad; loss stuck at ln(C); softmax before cross_entropy; set_detect_anomaly | overfit-one-batch test; (N,1) vs (N,) MSE broadcast; torch.where NaN gradient |
| 12 | `grad-accum` | Gradient accumulation for large effective batches | — | what accumulation means | effective batch size arithmetic; zero_grad inside the micro-batch loop | loss scaling, equivalence check, BatchNorm caveat |
| 13 | `loop-anatomy` | The PyTorch training loop, line by line | call order; what step() does | zero_grad placement and set_to_none; a tiny loop that learns y = 2x | epoch loss averaging with a partial batch; model.zero_grad vs optimizer.zero_grad; no_grad outputs | optimizer built before swapping a layer; inference_mode tensors in autograd |
| 14 | `optim-wd` | Optimizers, momentum and weight decay vs L2 | what an optimizer does; w - lr * grad | one SGD step by hand; momentum intuition; param groups; AdamW name | momentum buffer arithmetic; SGD weight_decay; weight decay = L2 for SGD only; why AdamW | Adam vs AdamW numerics; Adam scale invariance; no-decay groups for bias/norm; None vs zero grad with momentum |
| 15 | `lr-schedule` | Learning-rate schedulers and warmup | what a schedule is | StepLR trace; warmup; scheduler.step after optimizer.step | per-batch vs per-epoch stepping bug; LambdaLR warmup; ReduceLROnPlateau(val_loss); warmup rationale; scheduler state on resume | CosineAnnealingLR past T_max; linear scaling rule with batch size |

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
- `optimizer.zero_grad()` sets `.grad` to None by default in PyTorch 2.x; optimizers skip params whose grad is None (no momentum, no decay), but a zero grad still moves a param with a momentum buffer.
- The optimizer holds references to the parameters it was built with: build it after any layer swaps.
- SGD momentum: buf = momentum * buf + grad; w -= lr * buf.
- SGD weight_decay = L2 penalty (lambda/2)||w||^2. For Adam they differ: Adam's L2 term is normalised by sqrt(v); AdamW decays weights directly (w *= 1 - lr * wd). Usually exclude biases and norm weights from decay via param groups.
- Adam's first step moves every parameter by about lr, whatever the gradient's scale.
- `scheduler.step()` goes after `optimizer.step()`; know whether a scheduler counts epochs or batches. ReduceLROnPlateau needs `step(val_loss)`. CosineAnnealingLR rises again after T_max.
- `model.state_dict()` returns live references: deepcopy it (or save to disk) to keep the best early-stopping weights.
- `model.train()` recurses into every submodule, undoing a per-layer `bn.eval()`.
- `F.cross_entropy` wants logits; uniform logits give loss ln(num_classes).
- With GradScaler, call `scaler.unscale_(optimizer)` before clipping; inf/NaN steps are skipped and the scale is halved.
- Mixed-precision AdamW still costs about 16 bytes per parameter (bf16 weights + grads, fp32 master + m + v).

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
- "Averaging batch losses gives the epoch loss" -> a small last batch gets too much weight; weight by batch size.
- "Swapping a layer after building the optimizer is fine" -> the new layer gets gradients but is never updated.
- "Adam(weight_decay=...) is the same as AdamW" -> the L2 term is normalised away; decay strength differs wildly.
- "Weight decay only acts when the loss gradient is non-zero" -> it shrinks weights every step regardless.
- "Calling scheduler.step() in the batch loop is harmless" -> an epoch-based schedule decays far too fast.
- "CosineAnnealingLR stays at the minimum after T_max" -> it climbs back up; set T_max to the total steps.
- "best = model.state_dict() saves the best weights" -> it's a reference that follows later updates.
- "Early stopping on the test set is fine" -> it biases the test score; use validation.
- "Rising val loss always means val accuracy is falling" -> overconfidence can raise loss while accuracy improves.
- "Applying softmax before CrossEntropyLoss is safer" -> the loss expects logits; it puts a floor under the loss.
- "(N, 1) predictions vs (N,) targets is fine for MSE" -> broadcasts to (N, N); the loss can't reach 0.
- "torch.where hides a NaN branch from backward" -> 0 * nan = nan in the gradient.
- "Zeroing gradients every micro-batch is fine during accumulation" -> only the last micro-batch survives.
- "Clip right after scaler.scale(loss).backward()" -> grads are still scaled; unscale_ first.
- "model.train() leaves my frozen BN layer in eval" -> train() recurses and re-enables it.
- "Tensors from inference_mode work like no_grad tensors" -> they can't be saved for backward.

## Interview angle
- **Walk me through a PyTorch training step.** Forward pass builds the graph and the loss; `backward()` walks the graph in reverse applying the chain rule and adds gradients into `.grad`; `optimizer.step()` updates the weights; `zero_grad()` clears the gradients so the next batch starts fresh. SDE analogy: forward = request, backward = the stack unwinding with blame attached to every function.
- **Your loss is NaN. What do you check?** Learning rate too high (exploding gradients), log(0) or division by zero, fp16 overflow, bad inputs (NaN in data). Tools: check `torch.isfinite`, lower lr, gradient clipping, `BCEWithLogitsLoss`, anomaly detection, GradScaler/bf16.
- **eval() vs no_grad()?** eval() changes layer behaviour (dropout off, BN uses running stats); no_grad() stops recording the graph (saves memory and time). Inference needs both.
- **You can only fit batch 8 on the GPU but the recipe says batch 64. What do you do?** Gradient accumulation over 8 micro-batches with loss / 8, stepping once per 8; plus mixed precision and activation checkpointing to fit more. Caveat: BatchNorm still sees micro-batches of 8.
- **BatchNorm vs LayerNorm?** BN normalises each feature over the batch (depends on batch size, needs running stats for eval); LN normalises each sample over its features (no batch dependence, same in train and eval), which suits variable-length sequences and transformers.

- **Weight decay vs L2, and why AdamW?** For SGD they are identical. In Adam the L2 gradient gets divided by sqrt(v), so heavily-updated weights barely decay; AdamW applies the decay to the weights directly, separate from the adaptive step. Exclude biases and norm parameters with a no-decay param group.
- **How do you implement early stopping correctly?** Track the best validation metric, a patience counter, and a deep copy (or saved file) of the best state_dict; stop after `patience` bad epochs and restore the best weights. Never stop on test data.
- **Your lr schedule looks wrong after resuming or halfway through. What do you check?** Whether the scheduler steps per epoch or per batch, whether T_max / total steps match the real run, the order optimizer.step() then scheduler.step(), and that scheduler.state_dict() was checkpointed.

## Source material
To be added.
