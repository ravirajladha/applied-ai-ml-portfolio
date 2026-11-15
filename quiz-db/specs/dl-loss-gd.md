# Loss & Gradient Descent: coverage spec

**Ladder:** L2 · Deep Learning Fundamentals › Neural Network Basics   ·   **Prerequisites:** dl-neuron, basic calculus intuition (slope of a curve)
**Why it matters for AI/ML:** Training any model, from linear regression to fine-tuning an LLM, is "pick a loss, follow its gradient downhill". The loss decides what the model is rewarded for; the optimizer and learning rate decide whether training converges, crawls or blows up. Most real training bugs (NaN loss, double softmax, wrong target dtype, bad lr) live here.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `loss-regression` | Regression losses: MSE, MAE, Huber | loss = error score; MSE/MAE by hand | outliers: MSE vs MAE | Huber as the compromise; nn.HuberLoss value | MSE -> mean, MAE -> median; gradient behaviour of each; MSE grad = 2(y_hat - y)/N; (N,1) vs (N,) broadcasting bug; SmoothL1 vs Huber scaling; MSE/MAE = Gaussian/Laplace likelihood |
| 2 | `loss-classification` | Classification losses: BCE, cross-entropy | CE punishes confident wrong answers | BCE / CE values by hand; ln(K) at uniform | why CE (not MSE) with softmax/sigmoid | gradient of softmax+CE = p - y; label smoothing; soft-target CE floor = target entropy; ln(vocab) at init; perplexity = e^CE |
| 3 | `gradients` | Derivatives and gradients | slope = how the loss changes | gradient of x^2; gradient points uphill | partial derivatives / gradient vector | gradient = 0 does not mean minimum; chain rule in autograd; backward() needs a scalar; why grad = steepest ascent |
| 4 | `gd-update` | The gradient descent update and learning rate | step downhill; lr = step size | one or two GD steps by hand; SGD in PyTorch | too small / too large / oscillation | stability limit lr < 2/curvature; ill-conditioning (curvature ratio 100) in code; SGD weight_decay = L2 |
| 5 | `gd-variants` | Batch vs stochastic vs mini-batch | one example vs all vs a few | steps per epoch; noise vs cost | why noise helps; batch size and lr | linear scaling rule; large-batch generalisation gap; shuffle every epoch; SGD noise ~ lr/B |
| 6 | `landscape` | Loss landscapes, local minima, saddle points | the loss as a hilly surface | local vs global minimum | saddle points dominate in high dimensions | flat vs sharp minima, non-convexity; start point decides the minimum (code); permutation symmetry (h! equivalent minima) |
| 7 | `optimizers` | Momentum, RMSProp, Adam, AdamW | optimizers decide how to step | momentum as a rolling ball; Adam defaults | RMSProp/Adam per-parameter scaling; momentum by hand | Adam's first step ~ lr; L2 vs decoupled weight decay; RMSprop's first step is 10x lr (no bias correction); momentum effective lr = lr/(1-mu); Nesterov; Adam state keys; param groups |
| 8 | `lr-schedules` | Learning-rate schedules and warmup | lr can change during training | step decay; cosine | warmup and why; scheduler.step() placement | per-batch vs per-epoch scheduling bugs; warmup for Adam/transformers; num_training_steps with grad accumulation; ReduceLROnPlateau patience; LR range test |
| 9 | `numerics` | Numerical stability: logits, log(0), PyTorch loss APIs | — | CrossEntropyLoss takes raw logits + class indices | log(0), BCEWithLogitsLoss, double softmax | BCELoss clamps log at -100; log-sum-exp; target dtype errors; fp16 overflow vs bf16 rounding; GradScaler and underflow; 0 * log(0) = nan in custom losses |
| 10 | `training-loop` | The PyTorch training loop and autograd mechanics | zero_grad -> forward -> loss -> backward -> step | gradients accumulate without zero_grad; a full tiny fit; no_grad keeps values | zero_grad sets None; backward twice fails; detach stops gradients; gradient accumulation (divide by k) | running_loss += loss leaks graphs |
| 11 | `grad-clipping` | Exploding gradients and gradient clipping | what clipping is | loss spike then NaN | clip_grad_norm_ returns the pre-clip norm and keeps direction; clip_grad_value_ changes direction | one global norm over all params; unscale_ before clipping with GradScaler |
| 12 | `loss-options` | Loss options: reduction, class weights, pos_weight, ignore_index | default reduction is mean | reduction none/sum/mean | ignore_index=-100 (LLM label masking); pos_weight; sum vs mean scales the lr | class-weighted mean divides by the weight sum; focal loss |

## Must-know facts
- MSE = mean((y - y_hat)^2); MAE = mean(|y - y_hat|). MSE squares errors, so outliers dominate; MAE is robust to them.
- Huber is quadratic for small errors and linear for large ones (threshold delta, default 1.0 in nn.HuberLoss).
- The constant that minimises MSE is the mean; the constant that minimises MAE is the median.
- Binary cross-entropy: -[y log p + (1 - y) log(1 - p)]. Cross-entropy for the true class: -log p_true.
- A model guessing uniformly over K classes has CE loss ln(K) (2.3026 for 10 classes): the expected loss at initialisation.
- The gradient of softmax + cross-entropy w.r.t. the logits is p - y (same for sigmoid + BCE).
- MSE on top of sigmoid/softmax gives tiny gradients when the model is confidently wrong; CE does not.
- The gradient points in the direction of steepest increase; gradient descent steps against it: w <- w - lr * grad.
- Batch GD = whole dataset per step; SGD = one example; mini-batch = B examples (what "SGD" means in practice).
- In high dimensions, most critical points are saddle points, not bad local minima.
- Momentum (PyTorch): v <- mu*v + g; w <- w - lr*v. Adam keeps running means of g and g^2, with bias correction. Defaults: lr 1e-3, betas (0.9, 0.999), eps 1e-8.
- Adam's first update has magnitude about lr regardless of the gradient's scale.
- Adam(weight_decay=...) adds L2 to the gradient (which then gets rescaled); AdamW decays weights directly (decoupled). AdamW default weight_decay = 0.01.
- Warmup ramps the lr up over the first steps so early, unreliable updates don't wreck the model.
- nn.CrossEntropyLoss expects raw logits (N, C) and integer class indices (N,) of dtype long; it applies log-softmax itself.
- nn.BCEWithLogitsLoss expects logits and is numerically stable; nn.BCELoss expects probabilities and clamps log at -100.

- loss.backward() ADDS into .grad; optimizer.zero_grad() (set_to_none=True by default in 2.x) clears it. Gradient accumulation = divide each micro-batch loss by k, backward k times, step once.
- After backward the graph's saved tensors are freed; a second backward raises RuntimeError unless retain_graph=True. backward() with no argument needs a scalar.
- detach() makes a tensor a constant for autograd; accumulate logged losses with loss.item(), never the tensor.
- clip_grad_norm_ computes ONE total norm over all parameters, rescales them all (direction kept) and returns the pre-clip norm. With GradScaler, call scaler.unscale_(opt) first.
- CrossEntropyLoss: ignore_index=-100 by default; with weight=, 'mean' divides by the sum of the weights used. BCEWithLogitsLoss(pos_weight) scales only the positive term.
- reduction='sum' multiplies gradients by the batch size (an lr change for SGD).
- (N, 1) predictions vs (N,) targets broadcast to (N, N) in MSELoss with only a warning.
- MSE = Gaussian likelihood, MAE = Laplace; HuberLoss(delta) = delta * SmoothL1Loss(beta=delta).
- With soft targets, CE = H(target) + KL, so its floor is the target entropy. Uniform over V tokens gives CE = ln V; perplexity = e^CE.
- Momentum's steady-state step is lr/(1 - mu) (10x for 0.9). PyTorch RMSprop has no bias correction (first step = 10x lr with alpha 0.99). Adam state: exp_avg, exp_avg_sq, step.
- With gradient accumulation, schedulers step per optimizer step: num_training_steps = epochs * batches / accum.
- float16 max is 65504 (overflow to inf, small grads underflow -> GradScaler); bfloat16 has the float32 range but about 3 significant digits.

## Common traps (each one must have at least one question)
- "Applying softmax in the model and then using nn.CrossEntropyLoss" -> softmax applied twice; loss saturates, gradients shrink.
- "Bigger learning rate = faster training" -> beyond a threshold it oscillates or diverges.
- "MSE is fine for classification" -> flat gradients when confidently wrong.
- "Gradient zero means we found a minimum" -> could be a maximum or saddle point.
- "The gradient points downhill" -> it points uphill; we subtract it.
- "Accuracy can be used as the loss" -> it's piecewise constant, gradient 0 almost everywhere.
- "Adam's weight_decay is the same as AdamW" -> Adam couples L2 with the adaptive scaling; AdamW decouples it.
- "Passing probabilities to BCEWithLogitsLoss / logits to BCELoss" -> silently wrong loss (or values outside [0, 1] for BCELoss).
- "CrossEntropyLoss targets can be float class labels or one-hot of the wrong shape" -> class indices must be long.
- "Calling scheduler.step() every batch when it was configured in epochs" -> lr decays far too fast.
- "Local minima are the main obstacle in deep nets" -> saddle points and flat regions are more common.
- "A loss of 2.3 on 10 classes at the start means a bug" -> it's exactly what random guessing gives.

- "Calling backward() each step without zero_grad()" -> gradients pile up.
- "running_loss += loss" -> keeps every graph alive; GPU memory grows until it runs out.
- "Gradient accumulation without dividing the loss" -> k-times larger effective lr.
- "clip_grad_norm_ clips each tensor separately" -> one global norm; and clipping before unscale_ with AMP clips almost everything.
- "Class weights make the CE mean bigger" -> the weighted mean divides by the weight sum.
- "Model output (N, 1) vs target (N,) is fine for MSELoss" -> broadcasts to (N, N), silently wrong.
- "Soft-label CE should go to 0" -> it bottoms out at the target entropy.
- "Same lr after adding momentum 0.9" -> about a 10x larger effective step.
- "num_training_steps = batches * epochs with accumulation" -> the schedule ends far too late.
- "fp16 is just faster float32" -> overflow above 65504, underflow of small gradients.
- "Hand-written y*log(p)" -> 0 * log(0) = nan.

## Interview angle
- **Why cross-entropy instead of MSE for classification?** CE is the negative log-likelihood of the correct class; combined with softmax its gradient is simply p - y, so a confidently wrong prediction gets a big push. MSE through a sigmoid has gradients that vanish exactly when the model is confidently wrong.
- **Explain Adam in a minute.** Momentum (running mean of gradients) plus RMSProp (running mean of squared gradients) per parameter, with bias correction for the zero start. Each parameter gets its own effective step size. AdamW applies weight decay directly to the weights instead of through the gradient, which is what transformers use.
- **What happens if the learning rate is too high or too low?** Too low: slow, may stall on plateaus. Too high: overshoots, oscillates, NaN. Fixes: lr range test, warmup, schedules (cosine), gradient clipping.
- **Batch vs mini-batch vs SGD?** Trade-off between gradient accuracy and cost per step; mini-batches use GPU parallelism and their noise helps escape saddle points. SDE analogy: sampling requests to estimate latency instead of replaying the whole log every time.
- **Why does my CE loss start at 2.30?** With 10 classes and random init the model predicts roughly uniform, so -ln(1/10) = 2.3026. If it starts much higher, the init or the logits' scale is off.

- **Walk me through a training step and the common bugs.** zero_grad, forward, loss, backward, step. Bugs: no zero_grad (accumulation), double softmax, wrong target dtype/shape (broadcasting), summing loss tensors for logging, scheduler stepped per batch vs per epoch. SDE analogy: a request pipeline where each stage has a contract.
- **How do you train with a bigger batch than fits in memory?** Gradient accumulation: divide each micro-batch loss by k, backward k times, then step and clip. Count scheduler steps in optimizer steps.
- **Why clip gradients and how?** To survive rare huge gradients (loss spikes). clip_grad_norm_(params, 1.0) rescales the global gradient to norm 1 and keeps its direction. Log the returned norm.

## Source material
To be added.
