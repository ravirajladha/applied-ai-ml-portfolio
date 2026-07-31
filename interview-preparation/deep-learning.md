# Deep Learning — subject deep dive

82 questions at interview depth. Same format as [machine-learning.md](machine-learning.md):

> **The spoken answer** — what you actually say first, in plain words.

…then the explanation, then **the follow-up they chain onto it**.

⭐ = high frequency, ⭐⭐ = near-guaranteed.

**Contents**

| # | Section |
|---|---------|
| 1–8 | [Foundations](#1-foundations) |
| 9–15 | [Activation functions](#2-activation-functions) |
| 16–24 | [Backpropagation and gradient flow](#3-backpropagation-and-gradient-flow) |
| 25–29 | [Loss functions and output layers](#4-loss-functions-and-output-layers) |
| 30–39 | [Optimisation and learning rate](#5-optimisation-and-learning-rate) |
| 40–47 | [Regularisation](#6-regularisation) |
| 48–54 | [Initialisation and normalisation](#7-initialisation-and-normalisation) |
| 55–64 | [Convolutional networks](#8-convolutional-networks) |
| 65–72 | [Sequence models](#9-sequence-models) |
| 73–76 | [Generative models](#10-generative-models) |
| 77–82 | [Training in practice and debugging](#11-training-in-practice-and-debugging) |

---

## 1. Foundations

**Q1. What is a neuron / perceptron?** ⭐

> It takes several inputs, multiplies each by a weight, adds a bias, and passes the total through an activation
> function to produce one output.

```
z = w₁x₁ + w₂x₂ + … + wₙxₙ + b        (a weighted sum — a linear operation)
a = f(z)                               (the activation — the non-linear part)
```

The weights say how much each input matters; the bias shifts the threshold at which the neuron activates. A
single perceptron with a step activation is just a linear classifier — famously it cannot learn XOR, which is
precisely why we need hidden layers.

**Q2. Why does a neural network need a non-linear activation function?** ⭐⭐

> Because without one, stacking layers is pointless — a composition of linear functions is still just a single
> linear function.

Show it: if layer 1 computes `W₁x` and layer 2 computes `W₂(W₁x)`, that equals `(W₂W₁)x = Wx`. A hundred layers
would collapse into one matrix, and the whole network could only ever draw a straight-line boundary. The
non-linearity is what lets depth buy you anything.

**They'll follow up with:** *"So what can a network with one hidden layer represent?"* → By the **universal
approximation theorem**, a network with a single hidden layer and enough neurons can approximate any continuous
function on a bounded domain. But "enough" can mean exponentially many neurons, and the theorem says nothing
about whether gradient descent will *find* those weights — which is the practical reason we use depth.

**Q3. Why go deep instead of wide?** ⭐

> Because depth lets the network build features hierarchically — later layers reuse and combine what earlier
> layers found, so you get the same expressive power with exponentially fewer neurons.

In a CNN on images you can literally see it: edges → textures → object parts → objects. A wide, shallow network
would have to learn every whole-object pattern independently from raw pixels. Depth is a form of **compositional
reuse**, and it's also an inductive bias that happens to match how images, audio and language are structured.

Cost: deeper networks are harder to train (vanishing gradients), which is why residual connections and
normalisation exist.

**Q4. Deep learning vs classical machine learning — when do you choose which?** ⭐

> Deep learning when the data is unstructured and plentiful; classical ML when the data is tabular or scarce.

| | Classical ML | Deep learning |
|---|---|---|
| Features | You engineer them | The network learns them |
| Data needed | Hundreds to thousands | Tens of thousands upward |
| Data type | Tabular | Images, audio, text, video, graphs |
| Compute | CPU, minutes | GPU, hours to days |
| Interpretability | Reasonable | Poor |
| Tabular performance | **Usually wins** (gradient boosting) | Rarely worth it |

The honest answer interviewers reward: on tabular data, XGBoost still beats deep learning most of the time, so
deep learning isn't a default — it's a choice justified by the data type.

**Q5. What are the layers of a typical network?**

> An input layer sized to your features, one or more hidden layers that transform the representation, and an
> output layer sized to the task.

Output layer design is the part that gets tested:

| Task | Output units | Output activation | Loss |
|---|---|---|---|
| Regression | 1 | None (linear) | MSE / Huber |
| Binary classification | 1 | Sigmoid | Binary cross-entropy |
| Multi-class (one label) | C | Softmax | Categorical cross-entropy |
| Multi-label (many labels) | C | **Sigmoid on each** | Binary cross-entropy per output |

The multi-label row is the trap — people reach for softmax, but softmax forces the outputs to sum to 1, which is
wrong when an image can be both "beach" and "sunset".

**Q6. How do you count the parameters in a dense layer?** ⭐

> Weights = inputs × outputs, plus one bias per output unit.

For a layer going from 100 inputs to 50 units: `100 × 50 + 50 = 5,050` parameters.

A network 784 → 128 → 64 → 10:
```
(784×128 + 128) + (128×64 + 64) + (64×10 + 10) = 100,480 + 8,256 + 650 = 109,386
```
They ask this to check you understand the shapes, and because it leads straight into "why are CNNs more
efficient for images?"

**Q7. What is an epoch, a batch, and an iteration?** ⭐

> An epoch is one full pass over the training data. The batch size is how many samples you process before
> updating the weights. An iteration is one weight update.

Iterations per epoch = dataset size ÷ batch size. 10,000 samples with batch size 100 → 100 iterations per epoch.

**They'll follow up with:** *"What does batch size affect?"* → Small batches give noisy gradients that act as a
regulariser and often generalise better, but train slowly and underuse the GPU. Large batches give smooth,
accurate gradients and fast throughput, but tend to converge to sharper minima that generalise slightly worse —
and they need a proportionally higher learning rate (the "linear scaling rule") plus warm-up. Typical values are
32–256; the practical limit is usually GPU memory.

**Q8. What is a tensor?**

> A multi-dimensional array — a scalar is 0-D, a vector 1-D, a matrix 2-D, and anything beyond that is just a
> higher-rank tensor.

Shapes you should be able to state instantly: a batch of images is `(N, C, H, W)` in PyTorch (channels first) or
`(N, H, W, C)` in TensorFlow; a batch of sequences is `(N, T, D)` — batch, timesteps, features. Most deep
learning bugs are shape bugs, so being fluent here is worth more than it sounds.

---

## 2. Activation functions

**Q9. Compare the common activation functions.** ⭐⭐

| Function | Formula | Range | Where to use |
|---|---|---|---|
| **Sigmoid** | 1/(1+e⁻ᶻ) | (0, 1) | Binary output layer only |
| **Tanh** | (eᶻ−e⁻ᶻ)/(eᶻ+e⁻ᶻ) | (−1, 1) | Older RNNs; zero-centred |
| **ReLU** | max(0, z) | [0, ∞) | **Default for hidden layers** |
| **Leaky ReLU** | max(0.01z, z) | (−∞, ∞) | When ReLU units are dying |
| **ELU / SELU** | z if z>0 else α(eᶻ−1) | (−α, ∞) | Smooth alternative, self-normalising |
| **GELU** | z·Φ(z) | (−0.17, ∞) | **Standard in Transformers** |
| **Swish/SiLU** | z·σ(z) | (−0.28, ∞) | Modern CNNs, often beats ReLU |
| **Softmax** | eᶻⁱ/Σeᶻʲ | (0,1), sums to 1 | Multi-class output layer |

**Q10. Why is ReLU the default?** ⭐⭐

> Because it doesn't saturate for positive inputs, so gradients flow; it's extremely cheap to compute; and it
> produces sparse activations.

Its derivative is exactly 1 for z > 0 — no shrinking factor multiplying through the chain rule, which is what
kills sigmoid networks. It's a single comparison, so it's faster than an exponential. And roughly half the units
output zero, which makes the representation sparse and the network somewhat more efficient.

**Q11. What is the dying ReLU problem?** ⭐

> If a neuron's input becomes negative for every training example, its gradient is zero forever, so it stops
> learning permanently.

The mechanism: ReLU's derivative is 0 for z < 0. A large gradient update can push the weights so that z is
always negative; from then on no gradient flows back through that unit and it can never recover. In bad cases
40% of a network's units can be dead.

Fixes: **Leaky ReLU** or **ELU/GELU** (non-zero gradient for negatives), a lower learning rate, and proper
**He initialisation**.

**Q12. Why is sigmoid a bad choice for hidden layers?** ⭐

> Because it saturates — for large positive or negative inputs its gradient is nearly zero — and its outputs
> aren't zero-centred.

The maximum of sigmoid's derivative is **0.25**, at z = 0. Backpropagating through 10 sigmoid layers multiplies
by at most 0.25 ten times ≈ 10⁻⁶. The gradient in the early layers effectively vanishes. Add that its outputs
are all positive, so the gradients for all weights into a neuron share the same sign, causing zig-zag updates.

Tanh fixes the zero-centring (derivative max = 1.0) but still saturates.

**Q13. Why is softmax used for multi-class output?**

> It turns arbitrary real-valued scores into a proper probability distribution — all positive, summing to 1 —
> while preserving their ranking.

```
softmax(zᵢ) = e^{zᵢ} / Σⱼ e^{zⱼ}
```

The exponential makes everything positive and amplifies differences (a small lead in logits becomes a large lead
in probability); the normalisation makes them sum to 1. Paired with cross-entropy loss, the gradient simplifies
beautifully to `(p − y)`.

**They'll follow up with:** *"Why subtract the max before exponentiating?"* → Numerical stability. `e^1000`
overflows to infinity. Subtracting the maximum logit from all logits leaves the result mathematically identical
(the constant cancels in numerator and denominator) but keeps every exponent ≤ 0. This is the standard follow-up
and it's also a coding question.

**Q14. Should you apply softmax before the loss function in PyTorch?** ⭐

> No — `nn.CrossEntropyLoss` applies log-softmax internally, so your final layer should output raw logits.

Applying softmax yourself and then passing it to `CrossEntropyLoss` applies it twice, which flattens the
distribution and cripples training. It's one of the most common real bugs, so interviewers who've done the work
ask it. (`nn.NLLLoss` is the one that expects log-probabilities, i.e. after `log_softmax`.)

**Q15. What is GELU and why do Transformers use it?**

> A smooth activation that weights the input by the probability that a standard normal is below it —
> approximately `x·σ(1.702x)`.

Unlike ReLU's hard cut at zero, GELU is smooth and differentiable everywhere, and it allows small negative
values to pass through. Empirically it trains large models slightly better and more stably, which is why BERT,
GPT and most modern Transformers use it.

---

## 3. Backpropagation and gradient flow

**Q16. Explain forward propagation and backpropagation.** ⭐⭐

> Forward propagation pushes the input through the layers to produce a prediction and compute the loss.
> Backpropagation uses the chain rule to send the error backwards, computing how much each weight contributed to
> the loss, so the optimiser knows which direction to move each one.

Backprop is not a learning algorithm — it's an **efficient way to compute gradients**. Gradient descent is what
does the learning. Making that distinction unprompted is a good signal.

Efficiency point worth stating: computing gradients numerically would need one forward pass per parameter —
millions of passes. Backprop gets all of them in a single backward pass by reusing intermediate results, which
is what makes deep learning computationally possible at all.

**Q17. Walk through the chain rule for one weight.**

For a two-layer network with loss L:

```
∂L/∂w₁ = ∂L/∂a₂ · ∂a₂/∂z₂ · ∂z₂/∂a₁ · ∂a₁/∂z₁ · ∂z₁/∂w₁
          └ loss ┘ └ activ ┘ └ weight┘ └ activ ┘ └ input ┘
```

Read it as: *how much the loss changes with the output × how much the output changes with its pre-activation ×
… all the way back to the weight.* Each layer contributes one multiplication — which is exactly why a chain of
small derivatives makes the gradient vanish.

**Q18. What is the vanishing gradient problem?** ⭐⭐

> In a deep network the gradient is a product of many terms, so if those terms are consistently less than 1, the
> gradient shrinks exponentially as it travels backwards and the early layers stop learning.

Causes: saturating activations (sigmoid's derivative maxes at 0.25), poor initialisation, and simply having many
layers.

Fixes, in the order I'd list them:
1. **ReLU-family activations** — derivative of 1 in the positive region.
2. **Residual / skip connections** — the gradient gets an additive identity path straight back, so it can't be
   multiplied away. This is the single biggest reason 100+ layer networks are trainable.
3. **Batch / layer normalisation** — keeps activations in a healthy range.
4. **He / Xavier initialisation** — starts variance at the right scale.
5. **LSTM/GRU gates** for sequences — the cell state carries gradient additively.

**Q19. What is the exploding gradient problem and how do you fix it?** ⭐

> The mirror image — when the multiplied terms are consistently greater than 1, the gradient grows exponentially,
> the weight updates become huge, and the loss goes to NaN.

Symptoms: loss suddenly jumps to NaN or infinity, weights become enormous, training destabilises. Most common in
RNNs and with a too-high learning rate.

Fix: **gradient clipping** — rescale the gradient if its norm exceeds a threshold.

```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```
Also: lower the learning rate, better initialisation, and normalisation layers.

**Q20. What are residual (skip) connections and why do they work?** ⭐

> A shortcut that adds a layer's input to its output — `y = F(x) + x` — so the block only has to learn the
> *difference* from the identity.

Two reasons they work:
1. **Gradient flow** — differentiating `F(x) + x` gives `F'(x) + 1`. That `+1` is an unobstructed highway for
   the gradient, so it can't vanish through the block.
2. **Easier optimisation** — if the optimal transformation is close to identity, the block can just learn F ≈ 0,
   which is easy. Before ResNets, adding layers past ~20 made networks *worse* on training data — not an
   overfitting problem, an optimisation problem. Skip connections fixed that and enabled 152-layer networks.

They're now everywhere, including in every Transformer block.

**Q21. What is automatic differentiation and how does PyTorch's autograd work?**

> The framework records every operation you perform on tensors into a graph, then walks that graph backwards
> applying the chain rule.

PyTorch builds the graph **dynamically**, as the forward pass executes (define-by-run), which is why you can use
Python control flow and why debugging with a plain print statement works. Calling `.backward()` traverses the
graph and accumulates `.grad` on every leaf tensor with `requires_grad=True`.

Two practical consequences: wrap inference in `torch.no_grad()` to skip graph construction (faster, less
memory), and call `optimizer.zero_grad()` before each backward pass — gradients **accumulate** by default.

**They'll follow up with:** *"Why does PyTorch accumulate gradients instead of overwriting them?"* → Because it
lets you simulate a large batch on a small GPU (**gradient accumulation**: run several small batches, then step
once) and it supports multiple losses backpropagating into shared parameters. It's a feature, but it means
forgetting `zero_grad()` silently corrupts training.

**Q22. Why can't you initialise all weights to zero?** ⭐

> Because every neuron in a layer would compute the same output and receive the same gradient, so they'd stay
> identical forever. The layer would be no more expressive than a single neuron.

This is the **symmetry breaking** problem. Random initialisation makes each neuron start differently so they can
specialise. Biases *can* safely be initialised to zero, since the weights already break the symmetry.

**Q23. What is a computational graph?**

> A directed graph where nodes are operations and edges are tensors — it's the record of how the output was
> computed, which is what makes automatic differentiation possible.

Static graphs (TensorFlow 1.x) are defined once then executed, which allows aggressive optimisation but is
painful to debug. Dynamic graphs (PyTorch, TF 2.x eager) are built on every forward pass — slower in principle,
far easier in practice, and `torch.compile` / TorchScript recover most of the speed when you need it.

**Q24. Does backprop find the global minimum?**

> No — the loss surface of a deep network is non-convex, so gradient descent finds a local minimum. In practice
> that turns out not to matter much.

The insight from research worth quoting: in high dimensions, **saddle points** are far more common than bad
local minima, and most local minima have similar loss values close to the global one. Being stuck at a saddle
(gradient near zero in most directions) is the real risk, and momentum-based optimisers escape those. So the
practical answer is: we don't get the global minimum, and we don't need it.

---

## 4. Loss functions and output layers

**Q25. Which loss for which task?** ⭐

| Task | Loss | Note |
|---|---|---|
| Regression | MSE | Punishes large errors, sensitive to outliers |
| Regression with outliers | MAE / Huber | Huber is quadratic near 0, linear in the tails |
| Binary classification | Binary cross-entropy | With sigmoid output |
| Multi-class, one label | Categorical cross-entropy | With softmax output |
| Multi-label | BCE on each output | With sigmoid per output |
| Heavy class imbalance | Focal loss | Down-weights easy examples |
| Segmentation | Dice / IoU loss | Overlap-based, handles imbalance |
| Embeddings / similarity | Triplet / contrastive loss | Learns a metric space |

**Q26. Why cross-entropy rather than MSE for classification?** ⭐⭐

> Because cross-entropy gives much stronger gradients when the model is confidently wrong, while MSE's gradient
> nearly vanishes there — so cross-entropy trains far faster.

The mechanism: with a sigmoid output, the MSE gradient contains a factor of σ'(z), which is almost zero when the
model is badly wrong (saturated). So the more wrong you are, the *slower* you learn — exactly backwards. With
cross-entropy the σ'(z) term cancels and the gradient becomes simply `(p − y)`: proportional to the error.

Secondary reasons: cross-entropy is the maximum-likelihood loss for a categorical distribution, and with a
sigmoid it's convex in the parameters while MSE is not.

**Q27. Explain cross-entropy intuitively.**

```
L = -Σ yᵢ · log(pᵢ)        →  for one-hot labels, this is just  -log(p_correct_class)
```

> It's the negative log of the probability you assigned to the right answer. Assign 0.9 and you pay a small
> penalty; assign 0.01 and you pay a huge one.

−log(1.0) = 0 (perfect, no loss), −log(0.5) = 0.69, −log(0.01) = 4.6. The penalty grows without bound as your
predicted probability for the true class approaches zero — which is why the model is strongly pushed away from
confident mistakes.

**Q28. What is focal loss?**

> Cross-entropy with a factor that shrinks the loss for examples the model already gets right, so training
> focuses on the hard ones.

```
FL = -α(1 - p)^γ · log(p)        γ typically 2
```

If p = 0.95 (easy, already correct), `(1−0.95)² = 0.0025` — the loss is scaled down 400×. Designed for extreme
imbalance in object detection, where the background class dominates by orders of magnitude and would otherwise
swamp the gradient.

**Q29. What is label smoothing?**

> Instead of training toward a hard target of 1.0 for the correct class, you train toward something like 0.9,
> spreading the remaining 0.1 across the other classes.

It stops the network from driving logits to extremes to chase a probability of exactly 1, which reduces
overconfidence, improves **calibration**, and acts as a regulariser. Standard in image classification and
Transformer training. Downside: it slightly degrades the model's ability to be genuinely certain, and it
distorts distillation.

---

## 5. Optimisation and learning rate

**Q30. Explain gradient descent and its three variants.** ⭐⭐

> You compute the gradient of the loss with respect to the weights and take a step in the opposite direction —
> downhill. The variants differ in how much data you use to estimate that gradient.

```
w := w - α · ∂L/∂w
```

| Variant | Data per update | Character |
|---|---|---|
| **Batch GD** | Entire dataset | Smooth, accurate, very slow, needs all data in memory |
| **Stochastic GD** | One sample | Very noisy, fast per step, noise can escape bad minima |
| **Mini-batch GD** | 32–256 samples | **The practical default** — GPU-efficient, usefully noisy |

Everyone says "SGD" but means mini-batch. Say that explicitly and you sound like you've trained something.

**Q31. What does the learning rate do, and what happens if it's wrong?** ⭐⭐

> It's the step size. Too small and training crawls or stalls in a bad region; too large and you overshoot the
> minimum, oscillate, or diverge to NaN.

It is the **single most important hyperparameter**. Diagnostics from the loss curve:

| Loss curve | Diagnosis |
|---|---|
| Decreases very slowly, almost linear | Learning rate too low |
| Decreases then plateaus high | Too low, or needs a schedule |
| Oscillates wildly, no downward trend | Too high |
| Shoots to NaN/inf | Far too high (or a numerical bug) |
| Decreases smoothly then flattens | Healthy — consider decaying the rate |

Typical starting points: 1e-3 for Adam, 1e-2 for SGD with momentum, 1e-5 to 5e-5 for fine-tuning a pre-trained
Transformer. Find one with an **LR range test**: increase the rate exponentially over a few hundred iterations
and pick roughly an order of magnitude below where the loss starts rising.

**Q32. Explain momentum.** ⭐

> It accumulates a moving average of past gradients, so the update keeps some velocity from previous steps —
> like a ball rolling downhill instead of recalculating direction from scratch each time.

```
v := βv + (1-β)·∇L        (β ≈ 0.9)
w := w - α·v
```

Benefits: accelerates through long shallow valleys, damps the oscillation across a narrow ravine (the
perpendicular components cancel while the consistent downhill component accumulates), and carries the parameters
through small local minima and saddle points.

**Nesterov momentum** is a refinement that computes the gradient at the *look-ahead* position, correcting the
step before overshooting.

**Q33. Explain Adam.** ⭐⭐

> Adam combines momentum with a per-parameter adaptive learning rate — it keeps a running average of the
> gradient and of the squared gradient, and divides the step by the square root of the second one.

```
m := β₁m + (1-β₁)·g            first moment  (momentum)      β₁ = 0.9
v := β₂v + (1-β₂)·g²           second moment (scale)         β₂ = 0.999
m̂ = m/(1-β₁ᵗ),  v̂ = v/(1-β₂ᵗ)  bias correction
w := w - α · m̂ / (√v̂ + ε)
```

The effect: parameters with consistently large gradients get smaller effective steps, and rarely-updated
parameters (sparse features) get larger ones. It's robust to a badly chosen learning rate, which is why
`Adam(lr=1e-3)` is the default first thing to try.

**They'll follow up with:** *"Why the bias correction?"* → m and v start at zero, so early in training they're
biased toward zero, making the first steps far too small. Dividing by `(1 − βᵗ)` corrects this; the correction
fades to 1 as t grows.

*And:* **"Adam vs AdamW?"** → In Adam, L2 regularisation gets divided by `√v̂` along with the gradient, so it's
applied unevenly across parameters — it isn't really weight decay any more. **AdamW decouples** the decay,
applying it directly to the weights, which generalises better. It's the standard for Transformers.

**Q34. Adam converges faster — so why does anyone still use SGD?**

> Because SGD with momentum often **generalises better**, especially in computer vision, even though it takes
> longer and needs more tuning.

The intuition is that Adam's adaptive steps tend to find sharper minima, while SGD's uniform noise settles into
flatter ones that are more robust to distribution shift. Most published state-of-the-art image models use SGD +
momentum + a cosine schedule; NLP and Transformers use AdamW almost universally. A common practical recipe is
Adam early for speed, then switch to SGD to finish.

**Q35. What is a learning rate schedule and why use one?** ⭐

> You start with a large learning rate to move quickly toward a good region, then reduce it so the model can
> settle precisely into the minimum instead of bouncing around it.

Common schedules:
- **Step decay** — multiply by 0.1 every N epochs. Simple, still effective.
- **Cosine annealing** — smoothly decay following a cosine curve to near zero. The modern default.
- **ReduceLROnPlateau** — cut the rate when validation loss stops improving. Reactive, no tuning of the schedule.
- **Exponential decay** — `lr × γ^epoch`.
- **One-cycle** — ramp up then down; often trains dramatically faster.

**Q36. What is learning rate warm-up and why do Transformers need it?**

> You start at a near-zero learning rate and ramp it up over the first few thousand steps before applying the
> normal schedule.

Reason: at initialisation the gradients are large and Adam's second-moment estimate `v` is still unreliable
(based on very few samples), so early full-size steps can destabilise or permanently damage the model —
particularly with LayerNorm and large batches. Warm-up gives the moment estimates time to become meaningful.
Essentially every large Transformer uses linear warm-up followed by cosine or linear decay.

**Q37. What is gradient accumulation?**

> Run several small batches, accumulating gradients without stepping, then update once — it simulates a large
> batch on a GPU that couldn't hold one.

```python
for i, (xb, yb) in enumerate(loader):
    loss = criterion(model(xb), yb) / accum_steps   # scale so the average is right
    loss.backward()                                  # gradients accumulate
    if (i + 1) % accum_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```
Note the division — without it your effective learning rate is multiplied by `accum_steps`.

**Q38. What is mixed precision training?**

> Doing most computation in 16-bit floats instead of 32-bit, which roughly halves memory and speeds up training
> substantially on modern GPUs, while keeping a 32-bit copy of the weights for stability.

The catch is that FP16 has a small range, so small gradients underflow to zero. **Loss scaling** fixes this:
multiply the loss by a large factor before backward, then divide the gradients back before the optimiser step.
`torch.cuda.amp.autocast` + `GradScaler` handle it automatically. BF16 has a wider exponent range and usually
needs no loss scaling.

**Q39. What is a saddle point and why does it matter more than local minima?**

> A point where the gradient is zero but it's a minimum in some directions and a maximum in others — like a
> mountain pass.

In high-dimensional spaces, for a critical point to be a local minimum *every* one of millions of directions must
curve upward, which is vanishingly unlikely. Saddle points are therefore overwhelmingly more common, and they're
what actually slows training when the loss plateaus. Momentum and adaptive methods carry the parameters through
them; this is a large part of why they help.

---

## 6. Regularisation

**Q40. What is dropout and why does it work?** ⭐⭐

> During training you randomly set a fraction of neurons to zero on each forward pass, so the network can't
> depend on any single unit and has to learn redundant, distributed representations.

Two framings interviewers accept:
1. **Preventing co-adaptation** — no neuron can rely on a specific other neuron being present, so features must
   be individually useful.
2. **Implicit ensembling** — each forward pass trains a different thinned sub-network, and at test time using
   all units approximates averaging exponentially many of them.

Typical rates: 0.2–0.5 for dense layers, lower (0.1) or none for convolutional layers, 0.1 for Transformers.

**Q41. What happens to dropout at inference time?** ⭐

> It's turned off — all neurons are active. To keep the expected activation magnitude consistent, the
> activations are scaled.

Modern frameworks use **inverted dropout**: they divide by `(1 − p)` during *training*, so inference needs no
adjustment at all and can run the network unchanged. In PyTorch this is handled by `model.eval()` — forgetting
to call it means dropout stays active during validation, and your validation scores become noisy and pessimistic.

**They'll follow up with:** *"Why is validation accuracy sometimes higher than training accuracy?"* → Usually
this exact thing: dropout and other noise are active during training but disabled at validation, so the model is
effectively stronger at validation time. Training loss is also averaged *over* an epoch while the model improves,
whereas validation is measured at the end. Both are normal, not bugs.

**Q42. What is early stopping?** ⭐

> Monitor validation loss during training and stop when it stops improving, keeping the weights from the best
> epoch.

It's regularisation because it limits how far the weights travel from their initialisation, capping effective
capacity. Implementation detail worth mentioning: use **patience** (wait N epochs before giving up, since loss
is noisy) and **restore the best checkpoint**, not the final one.

**Q43. What is data augmentation?** ⭐

> Creating new training examples by applying label-preserving transformations to existing data, so the model
> sees more variety and learns invariances.

- **Images**: random crop, horizontal flip, rotation, colour jitter, random erasing, **Mixup** (blend two images
  and their labels), **CutMix**.
- **Text**: synonym replacement, back-translation, random deletion/swap. Riskier — small edits can flip meaning.
- **Audio**: time shift, pitch shift, noise injection, SpecAugment.

The critical rule: apply augmentation to **training data only**, never to validation or test. And keep it
label-preserving — flipping a "6" vertically to make a "9" teaches the wrong thing, and horizontal flips are
wrong for text or for road-sign classification.

**Q44. What is weight decay, and is it the same as L2?**

> Weight decay shrinks every weight by a small factor on each update. With plain SGD it's mathematically
> identical to L2 regularisation; with Adam it isn't.

With SGD, adding `λ‖w‖²` to the loss produces an update term `−αλw`, i.e. multiplicative shrinkage — same thing.
With Adam, the L2 gradient gets divided by `√v̂` like any other gradient, so weights with large historical
gradients get decayed less — no longer uniform shrinkage. **AdamW** applies the decay directly to the weights,
outside the adaptive scaling, which is why it's preferred. This distinction is a favourite senior-level probe.

**Q45. List every way to reduce overfitting in a neural network.** ⭐

In roughly the order I'd try them:
1. **More data** — no bias cost, always the best fix if available.
2. **Data augmentation** — the cheap substitute for more data.
3. **Early stopping** — free, immediate.
4. **Dropout**.
5. **Weight decay / L2**.
6. **Reduce model size** — fewer layers or units.
7. **Batch normalisation** — mild regularising side effect.
8. **Transfer learning** — start from a pre-trained model instead of learning features from your small dataset.
9. **Label smoothing**, **Mixup**, ensembling.

**Q46. What is transfer learning, and how do you decide how much to fine-tune?** ⭐⭐

> Reuse a model trained on a large dataset as the starting point for your own task — the early layers already
> encode generic features like edges or syntax, so you only need to adapt the rest.

The decision grid interviewers want:

| | Similar domain | Different domain |
|---|---|---|
| **Small data** | Freeze everything, train only the new head | Freeze early layers, train the later ones |
| **Large data** | Fine-tune the whole network (low LR) | Fine-tune everything, or train from scratch |

Practicalities: replace the final layer to match your class count; use a much lower learning rate for
pre-trained layers than for the new head (**discriminative learning rates**); and unfreeze gradually rather than
all at once, since a randomly initialised head produces large gradients that can destroy pre-trained features in
the first few batches.

**Q47. What is catastrophic forgetting?**

> When a model fine-tuned on a new task loses the ability it had on the original one, because the weights that
> encoded it get overwritten.

Mitigations: a low learning rate, freezing lower layers, rehearsal (mixing in some original data), elastic weight
consolidation (penalise moving weights that were important for the old task), or **adapter/LoRA** approaches
that leave the base weights untouched and train small added modules instead.

---

## 7. Initialisation and normalisation

**Q48. Why does weight initialisation matter?** ⭐

> Because it sets the initial scale of activations and gradients — too small and the signal dies as it
> propagates, too large and it explodes.

Get it wrong and the network either learns nothing or diverges in the first few steps, before any of your other
hyperparameters get a chance to matter.

**Q49. Xavier vs He initialisation.** ⭐

> Both scale the random initial weights by the layer's fan-in so the variance of activations stays roughly
> constant through the network. Xavier is derived for tanh/sigmoid; He adds a factor of 2 to compensate for ReLU
> zeroing half the activations.

```
Xavier/Glorot:  Var(w) = 1/n_in     (or 2/(n_in + n_out))   → tanh, sigmoid
He/Kaiming:     Var(w) = 2/n_in                              → ReLU, Leaky ReLU
```

The `2` in He is the whole insight: ReLU discards the negative half, halving the variance at every layer, so you
double the initial variance to compensate. Use He with ReLU networks — it's the default in PyTorch for
`nn.Linear` and `nn.Conv2d`.

**Q50. Explain batch normalisation.** ⭐⭐

> For each feature, it normalises the values across the mini-batch to zero mean and unit variance, then rescales
> them with two learnable parameters so the network can undo the normalisation if it needs to.

```
x̂ = (x - μ_batch) / √(σ²_batch + ε)
y  = γ·x̂ + β                          γ and β are learned
```

Benefits: allows much higher learning rates, speeds up convergence dramatically, reduces sensitivity to
initialisation, and adds mild regularisation (each sample's normalisation depends on the random composition of
its batch — that's genuine noise).

The `γ` and `β` matter: without them, forcing every layer's output to mean 0 / variance 1 would restrict what
the network can represent — e.g. it would confine a sigmoid to its linear region.

**They'll follow up with:** *"How does BatchNorm behave differently at inference?"* → At inference you may have
a single sample, so there's no batch to compute statistics from. BatchNorm keeps a **running average** of the
mean and variance during training and uses those fixed values at test time. This is another reason
`model.eval()` is mandatory — forgetting it makes predictions depend on whatever else is in the batch, which is
a genuinely nasty production bug.

*And:* **"What's the problem with small batch sizes?"** → The batch statistics become noisy and unrepresentative,
so BatchNorm degrades badly below batch size ~8. Use GroupNorm or LayerNorm instead.

**Q51. BatchNorm vs LayerNorm — and why do Transformers use LayerNorm?** ⭐

> BatchNorm normalises each feature across the batch; LayerNorm normalises each sample across its features.

That difference is the answer to the Transformer question:
- LayerNorm is **independent of batch size** — it works identically with a batch of 1.
- Sequences have **variable length**, so batch statistics at each position are computed over inconsistent
  amounts of real data; padding corrupts them.
- Autoregressive inference generates one token at a time, so there is no batch to normalise over.

Related variants: **GroupNorm** (normalise over groups of channels — good for small-batch vision),
**InstanceNorm** (per-sample per-channel — style transfer), **RMSNorm** (LayerNorm without mean subtraction —
faster, used in LLaMA and other modern LLMs).

**Q52. Where do you put BatchNorm relative to the activation?**

The original paper put it before the activation (`Conv → BN → ReLU`) and that remains the most common. Some
later work argues for after. The pragmatic answer: `Conv → BN → ReLU`, and note that the convolution's **bias is
redundant** when followed by BatchNorm (BN subtracts the mean, cancelling any constant), so set `bias=False`.
That last detail signals you've actually built these.

**Q53. Does BatchNorm eliminate the need for dropout?**

Largely, in convolutional networks — the original ResNet and most modern CNNs use BatchNorm with little or no
dropout, and stacking both can hurt because their variance effects interact badly (dropout changes the variance
that BatchNorm's running statistics estimated). In Transformers, LayerNorm and dropout are used together, since
LayerNorm has no regularising noise of its own.

**Q54. What is internal covariate shift, and is it really why BatchNorm works?**

> It's the original explanation — as earlier layers update, the distribution of inputs to later layers keeps
> shifting, so those layers chase a moving target.

Worth knowing that this explanation has been **challenged**: later work (Santurkar et al.) showed BatchNorm helps
even when covariate shift is artificially reintroduced, and argued the real benefit is that it **smooths the loss
landscape**, making gradients more predictable and allowing larger stable steps. Saying "the original
justification was internal covariate shift, though the current understanding leans toward loss-surface
smoothing" is a strong senior-level answer.

---

## 8. Convolutional networks

**Q55. Why use a CNN instead of a fully connected network for images?** ⭐⭐

> Three reasons: parameter sharing, local connectivity, and translation invariance.

Do the arithmetic — it lands harder than the words. A 224×224×3 image flattened is 150,528 inputs; one dense
layer of 1,000 units needs **150 million** parameters. A conv layer with 64 filters of size 3×3×3 needs
`(3×3×3 + 1) × 64 = 1,792`.

- **Parameter sharing** — the same filter slides across the whole image, so a vertical-edge detector is learned
  once rather than separately for every position.
- **Local connectivity** — pixels near each other are related; distant ones usually aren't. A dense layer throws
  away spatial structure entirely by flattening.
- **Translation invariance** — a cat is a cat wherever it appears in the frame.

**Q56. Explain convolution, kernel, stride and padding.** ⭐

> A kernel is a small matrix of weights that slides across the input, computing a dot product at each position
> to produce a feature map. Stride is how far it moves each step; padding adds a border so the output doesn't
> shrink.

- **Kernel/filter** — typically 3×3. Each one learns to detect a specific pattern.
- **Stride** — 1 keeps the resolution; 2 halves it (a cheaper alternative to pooling).
- **Padding** — `'same'` pads so output size = input size; `'valid'` means no padding, so the output shrinks and
  border pixels get under-sampled.

**Q57. Give the output size formula.** ⭐

```
Output = ⌊(W - F + 2P) / S⌋ + 1

W = input size, F = filter size, P = padding, S = stride
```

Worked example: input 32×32, filter 5×5, padding 2, stride 1 → (32 − 5 + 4)/1 + 1 = **32×32** (preserved).
With stride 2 → (32 − 5 + 4)/2 + 1 = 16.5 → **16×16**.

Expect to be asked to compute this live, including the number of parameters:
`params = (F × F × C_in + 1) × C_out`.

**Q58. What does pooling do, and is it still used?** ⭐

> It downsamples a feature map — max pooling takes the largest value in each window — reducing spatial size and
> computation while making the representation slightly robust to small shifts.

2×2 max pooling with stride 2 quarters the spatial dimensions. Max pooling keeps the strongest activation
("was this feature present anywhere in this region?"); average pooling smooths.

The honest nuance: many modern architectures **replace pooling with strided convolutions**, which achieve the
same downsampling with learnable weights. **Global average pooling** — averaging each channel to a single number
before the classifier — has largely replaced the big flatten-and-dense head, cutting parameters massively and
reducing overfitting.

**Q59. What is a receptive field?**

> The region of the original input that influences one particular output activation.

It grows with depth: two stacked 3×3 convolutions see a 5×5 region; three see 7×7. This is exactly why stacking
small filters beats one large one — **two 3×3 layers have the same receptive field as one 5×5 but use fewer
parameters (18 vs 25 per channel pair) and include an extra non-linearity.** That comparison is a classic
question in its own right.

**Q60. What is a 1×1 convolution good for?** ⭐

> It mixes information across channels at each spatial position, and it's the standard way to change the number
> of channels cheaply.

Used for **dimensionality reduction** — in Inception and ResNet bottleneck blocks, a 1×1 conv cuts 256 channels
to 64 before an expensive 3×3 conv, then a 1×1 restores them, saving an order of magnitude of computation. It
also adds a non-linearity without touching spatial resolution. Not pointless, despite looking like it should be.

**Q61. Walk through a typical CNN architecture.**

```
Input (224×224×3)
 → [Conv 3×3 → BatchNorm → ReLU] × 2 → MaxPool 2×2      (112×112, 64 channels)
 → [Conv → BN → ReLU] × 2 → MaxPool                      (56×56, 128 channels)
 → [Conv → BN → ReLU] × 3 → MaxPool                      (28×28, 256 channels)
 → Global Average Pooling                                (1×1×256)
 → Dropout → Dense(num_classes) → Softmax
```

The pattern to articulate: **spatial dimensions shrink while channel depth grows** — the network trades "where"
for "what", moving from many pixels with few features to few positions with many abstract features.

**Q62. Name the landmark CNN architectures and what each contributed.**

| Architecture | Contribution |
|---|---|
| **LeNet-5** (1998) | The original CNN — digits |
| **AlexNet** (2012) | Started the deep learning era; ReLU, dropout, GPUs |
| **VGG** (2014) | Showed depth matters; uniform 3×3 stacks; very parameter-heavy |
| **GoogLeNet/Inception** (2014) | Parallel multi-scale branches; 1×1 bottlenecks |
| **ResNet** (2015) | **Residual connections** → 152 layers trainable. The most important one |
| **DenseNet** (2016) | Each layer connected to all later layers |
| **MobileNet / EfficientNet** | Depthwise separable convolutions; principled compound scaling for efficiency |
| **Vision Transformer** (2020) | Images as patch sequences; beats CNNs given enough data |

If you name only one, name ResNet and explain skip connections.

**Q63. What are depthwise separable convolutions?**

> A standard convolution is factorised into two cheaper steps: a depthwise convolution that filters each channel
> independently, and a 1×1 pointwise convolution that combines channels.

The cost saving is roughly `1/C_out + 1/F²` of the original — around 8–9× fewer operations for a 3×3 kernel.
This is the core idea behind MobileNet and why CNNs can run on phones.

**Q64. How would you handle a small image dataset?**

> Transfer learning first, aggressive augmentation second, and only then consider training from scratch.

Concretely: take a pre-trained ResNet or EfficientNet, freeze the backbone, train a new head; then unfreeze the
last block with a low learning rate. Augment heavily (crops, flips, colour jitter, Mixup). Use a smaller model
than you think you need, plus dropout and weight decay. Use cross-validation because a small test set gives an
unreliable estimate. Consider few-shot approaches or synthetic data if there are genuinely only hundreds of
images.

---

## 9. Sequence models

**Q65. What is an RNN and how does it differ from a feedforward network?** ⭐

> It processes a sequence one step at a time, carrying a hidden state forward that acts as memory of everything
> seen so far.

```
hₜ = tanh(W_hh·hₜ₋₁ + W_xh·xₜ + b)
yₜ = W_hy·hₜ
```

Crucially the **same weights are reused at every timestep** (parameter sharing across time), so an RNN can
handle variable-length input — which a feedforward network cannot.

**Q66. Why do RNNs struggle with long sequences?** ⭐⭐

> Because backpropagation through time multiplies the same weight matrix once per timestep, so the gradient
> either vanishes or explodes exponentially with sequence length.

Over 100 timesteps, a factor of 0.9 becomes 0.9¹⁰⁰ ≈ 0.00003 — the network simply cannot learn a dependency
between step 1 and step 100. In practice a vanilla RNN's effective memory is roughly 10 timesteps.

Exploding gradients are the easier half (clip them). Vanishing gradients require an architectural fix, which is
what LSTMs provide.

**Q67. Explain LSTM and its gates.** ⭐⭐

> An LSTM adds a separate cell state that runs through the sequence with only minor linear interactions, plus
> three gates that control what gets removed from it, added to it, and read out of it.

| Gate | Formula | Question it answers |
|---|---|---|
| **Forget** | fₜ = σ(W_f·[hₜ₋₁, xₜ]) | What should I discard from memory? |
| **Input** | iₜ = σ(W_i·[hₜ₋₁, xₜ]) | What new information should I store? |
| **Output** | oₜ = σ(W_o·[hₜ₋₁, xₜ]) | What part of memory should I expose now? |

```
Cₜ = fₜ * Cₜ₋₁ + iₜ * C̃ₜ        cell state: mostly additive
hₜ = oₜ * tanh(Cₜ)               hidden state: the filtered output
```

The key line is `Cₜ = fₜ * Cₜ₋₁ + …`. Because the cell state is updated **additively** rather than by repeated
matrix multiplication, the gradient can flow back across many timesteps without being multiplied down — the same
principle as a residual connection. Each gate uses a sigmoid because it outputs 0–1, acting as a soft valve.

**Q68. LSTM vs GRU?** ⭐

> A GRU merges the forget and input gates into a single update gate and drops the separate cell state, so it has
> two gates instead of three and about 25% fewer parameters.

GRU trains faster and needs less data; LSTM has slightly more capacity and tends to edge ahead on very long
sequences. Empirically they're close — try both if it matters. GRU is the sensible default when data is limited.

**Q69. What is a bidirectional RNN, and when can't you use one?**

> It runs two RNNs, one forward and one backward through the sequence, and concatenates their hidden states, so
> every position has both past and future context.

Much better for classification, NER and tagging — knowing what comes after a word is often essential to
interpreting it. But you **cannot** use it for real-time or generative tasks, because the future isn't available
yet. This is the same distinction as BERT (bidirectional, understanding) versus GPT (causal, generation).

**Q70. What is teacher forcing?**

> During training on a generation task, you feed the model the *true* previous token rather than its own
> prediction, so one early mistake doesn't derail the entire sequence.

It makes training much faster and more stable. The downside is **exposure bias**: at inference the model must
consume its own outputs, a situation it never trained on, so errors compound. Mitigations include scheduled
sampling (gradually mix in the model's own predictions) and, in practice, large-scale pretraining.

**Q71. What is attention and what problem did it solve?** ⭐⭐

> In a plain encoder-decoder, the entire input sequence has to be compressed into one fixed-length vector —
> a bottleneck. Attention lets the decoder look back at every encoder state and take a weighted combination,
> deciding at each step which input positions matter.

The weights are learned and computed dynamically, so when translating a particular word the model can focus on
the corresponding source words. It removed the fixed-vector bottleneck, dramatically improved long-sequence
performance, and gave a degree of interpretability (you can plot the alignment).

**Self-attention** then applies the same idea *within* one sequence — each token attends to every other token in
the same sequence — which is the foundation of the Transformer.

**Q72. Why did Transformers replace RNNs?** ⭐⭐

> Because an RNN must process tokens sequentially, so it can't be parallelised across time, and information
> between distant tokens has to pass through every intermediate step. Attention connects any two positions
> directly, in one operation, and all positions are computed in parallel.

| | RNN/LSTM | Transformer |
|---|---|---|
| Parallelism | None across time | Full — the reason they scale |
| Path length between distant tokens | O(n) | **O(1)** |
| Long-range dependencies | Degrades | Strong |
| Cost per layer | O(n·d²) | O(n²·d) — quadratic in sequence length |
| Positional information | Inherent in the recurrence | Must be added explicitly |

The trade-off to acknowledge: attention is **quadratic in sequence length**, which is why long-context models
need approximations like sparse or linear attention, FlashAttention, or state-space models such as Mamba.

(Full Transformer internals — Q/K/V, multi-head, positional encoding, BERT vs GPT — are in
[top-100-questions.md](top-100-questions.md) Q84–Q91 and will be expanded in `nlp.md`.)

---

## 10. Generative models

**Q73. What is an autoencoder?** ⭐

> A network trained to reconstruct its own input through a narrow bottleneck, so the bottleneck is forced to
> learn a compressed representation.

Encoder compresses input → latent code → decoder reconstructs. Loss is reconstruction error (MSE or BCE), and
it's **self-supervised** — no labels needed.

Uses: dimensionality reduction (a non-linear PCA), denoising (train to reconstruct clean images from corrupted
ones), **anomaly detection** (train on normal data; anything with high reconstruction error is anomalous), and
pretraining.

**They'll follow up with:** *"How is that different from PCA?"* → With linear activations and MSE loss, an
autoencoder essentially recovers the PCA subspace. With non-linear activations it can learn curved manifolds
that PCA cannot. The cost is that the latent dimensions aren't ordered or orthogonal, and it needs far more data.

**Q74. What is a variational autoencoder (VAE) and how does it differ?**

> A VAE encodes each input to a *distribution* — a mean and variance — instead of a single point, and adds a
> KL-divergence term pushing that distribution toward a standard normal.

That makes the latent space **continuous and well-structured**, so you can sample from it and decode to get new,
plausible data. A plain autoencoder's latent space has gaps; sampling from it produces garbage. The
**reparameterisation trick** (`z = μ + σ·ε` with `ε ~ N(0,1)`) is what lets gradients flow through the sampling
step. VAE outputs tend to be blurry because of the pixel-wise reconstruction loss.

**Q75. Explain GANs.** ⭐

> Two networks compete: a generator creates fake samples from noise, and a discriminator tries to tell real from
> fake. Each improves by exploiting the other's weaknesses.

It's a minimax game; at the theoretical equilibrium the generator's distribution matches the real one and the
discriminator is reduced to guessing.

Known problems worth naming: **mode collapse** (the generator finds one convincing output and produces only
that), unstable training (the two losses oscillate rather than converge), and no clean way to evaluate quality
(hence FID and Inception Score). Fixes include Wasserstein loss with gradient penalty, spectral normalisation,
and progressive growing.

**Q76. Where do diffusion models fit?**

> They learn to reverse a gradual noising process — you repeatedly add Gaussian noise to an image until it's
> pure noise, then train a network to undo one step at a time, so you can start from noise and denoise your way
> to a new image.

Compared to GANs: much more stable training (a simple regression objective, no adversarial game), better
diversity and sample quality, but far slower at generation because it requires many sequential denoising steps.
This is what powers modern image generation, and it's increasingly the expected answer to "how does image
generation work today?"

---

## 11. Training in practice and debugging

**Q77. Your model isn't learning — the loss is flat. Walk me through debugging it.** ⭐⭐

Say it as an ordered checklist; the order is what's being scored.

1. **Overfit a tiny batch first.** Take 10 samples and train until the loss hits ~0. If it *can't*, the bug is in
   the code — not the data, not the hyperparameters. This is the single most valuable debugging technique and
   the answer they're hoping for.
2. **Check the learning rate** — by far the most common culprit. Try 10× up and 10× down.
3. **Check the data** — are labels aligned with inputs? Is normalisation applied? Print an actual batch and
   look at it.
4. **Check the loss function** — right loss for the task? Applying softmax before `CrossEntropyLoss`?
5. **Check gradients** — print gradient norms per layer. All zeros means a broken graph (a detached tensor,
   or `requires_grad=False`); tiny values in early layers means vanishing gradients.
6. **Check `optimizer.zero_grad()`** is called, and that the optimiser actually received the model's parameters.
7. **Check the initial loss** — for 10-class classification it should start near `ln(10) ≈ 2.3`. A wildly
   different starting value means something is wrong before training even begins.

**Q78. The loss became NaN. What happened?** ⭐

> Almost always the learning rate is too high, or there's a `log(0)` or division by zero somewhere.

Checklist: lower the learning rate; add **gradient clipping**; check for `log(0)` (add an epsilon, or use the
numerically stable fused loss functions rather than composing them yourself); check for division by a
possibly-zero standard deviation; check for NaN or infinite values already in the input data; if using mixed
precision, verify the `GradScaler` is present. `torch.autograd.set_detect_anomaly(True)` will point at the
offending operation, at the cost of speed.

**Q79. Training accuracy is 99%, validation is 65%. What now?** ⭐

Overfitting — but check for the impostors first: **data leakage**, **duplicate rows across the split**, and a
validation set drawn from a different distribution than the training set. Then apply the standard remedies in
order of cheapness: early stopping → augmentation → dropout/weight decay → a smaller model → more data →
transfer learning.

**Q80. How do you choose a starting architecture and hyperparameters?**

> Don't invent one. Start from a known-good architecture for the task, use its published hyperparameters, get
> the pipeline running end to end, and only then tune.

Then tune in priority order: **learning rate** first (it dominates everything), then batch size, then
architecture size, then regularisation strength, then the schedule. Change one thing at a time, keep a log of
what you tried, and always keep a baseline number visible.

**Q81. How do you speed up training?**

Data pipeline first — it's usually the bottleneck, not the GPU: more `num_workers` in the DataLoader,
`pin_memory=True`, prefetching, and pre-resizing images offline instead of on every epoch. Then **mixed
precision** (roughly 2× on modern GPUs), a larger batch size, `torch.compile`, gradient accumulation instead of
smaller models, and multi-GPU with `DistributedDataParallel`. Also: profile before optimising — check GPU
utilisation, and if it's at 30% your data loader is starving the GPU.

**Q82. How do you deploy a deep learning model?**

> Export it to a portable format, optimise it for inference, serve it behind an API, and monitor it.

Steps to mention: export to **ONNX** or TorchScript; optimise with **quantisation** (INT8 — roughly 4× smaller
and faster, with a small accuracy cost), **pruning**, or **knowledge distillation** (train a small student model
to match a large teacher's outputs); serve with TorchServe, Triton, or a FastAPI wrapper; batch requests to use
the GPU efficiently; cache where possible; and monitor latency, throughput, and input distribution drift.

Decide deliberately between GPU (throughput, cost) and CPU/edge (latency, privacy, no network dependency).

---

## Rapid-fire round

| Question | Answer |
|---|---|
| Why normalise the input? | Faster, more stable convergence — unscaled inputs give an ill-conditioned loss surface |
| Can a neural network do regression? | Yes — one output unit, linear activation, MSE loss |
| What's a hidden layer "hidden" from? | The data — its values aren't in the input or the labels, they're learned representations |
| More layers always better? | No — harder to optimise, more overfitting, diminishing returns |
| Why GPUs? | Neural nets are dense matrix multiplications; GPUs run thousands of those in parallel |
| Difference between `model.train()` and `model.eval()`? | Toggles dropout and BatchNorm behaviour; nothing else |
| What does `torch.no_grad()` do? | Stops building the autograd graph — faster inference, less memory |
| Why shuffle training data? | Prevents the model learning the data order, and decorrelates batches |
| Batch size 1 — what breaks? | BatchNorm (no batch statistics), very noisy gradients, poor GPU use |
| Sigmoid or softmax for 2 classes? | Either — sigmoid with 1 output, or softmax with 2. Mathematically equivalent |
| What is a logit? | The raw pre-activation score before sigmoid/softmax; range is all reals |
| Fine-tuning learning rate vs training from scratch? | 10–100× smaller — you're adjusting, not learning from nothing |
| Freeze BatchNorm when fine-tuning? | Often yes on small datasets — its running statistics are unreliable from small batches |
| How many epochs? | Until validation loss stops improving — use early stopping, don't fix a number |

---

## What to do with this file

1. Be able to **draw** three things: a neuron with its weighted sum and activation, a CNN's shrinking-spatial /
   growing-channel pyramid, and an LSTM cell with its three gates labelled by the question each answers.
2. Do the arithmetic questions by hand at least once — Q6 (dense parameters), Q57 (conv output size and
   parameters). They get asked live and hesitating looks worse than being slow.
3. Memorise the four output-layer/loss combinations in Q5. It's the fastest way to sound like you've shipped
   something.
4. Rehearse **Q77** (debugging a flat loss) out loud. "Overfit a tiny batch first" is the answer that separates
   people who've trained models from people who've read about them, and it comes up constantly.
5. Have one training story of your own ready: what wouldn't converge, what you tried, what it turned out to be.
