# The Neuron & Activations: coverage spec

**Ladder:** L2 · Deep Learning Fundamentals › Neural Network Basics   ·   **Prerequisites:** np-arrays (vectors, dot product), ml-models (linear / logistic regression)
**Why it matters for AI/ML:** Every deep model, from a tiny MLP to a 70B-parameter LLM, is stacks of "weighted sum + non-linearity". Knowing what one neuron computes, which activation goes where, how many parameters a layer has and why initialisation matters is the vocabulary for every later topic (training, transformers, fine-tuning, memory sizing).

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `neuron` | The neuron: weights, bias, weighted sum, perceptron | inputs x weights + bias; what a weight and bias mean | weighted sum as a dot product; computing one neuron by hand | the bias as a moved threshold; perceptron = step activation, linearly separable only | perceptron vs logistic regression; why XOR needs a hidden layer; perceptron rule never converges on XOR |
| 2 | `activations` | Activation functions (step, sigmoid, tanh, ReLU, Leaky ReLU, GELU) | ranges of sigmoid / tanh / ReLU | values at points; when each is used | derivatives (sigmoid' = s(1-s), max 0.25; tanh' max 1); zero-centring | GELU shape and why transformers use it; ReLU derivative at 0 in PyTorch; tanh/sigmoid identity; GELU ~ x*sigmoid(1.702x); all-positive inputs cause zig-zag weight updates |
| 3 | `softmax` | Softmax | turns scores into probabilities that sum to 1 | computing softmax of a small vector; argmax unchanged | shift invariance; temperature | numerically stable softmax; 2-class softmax = sigmoid; log(softmax) underflow vs log_softmax; a label-free softmax loss has zero gradient |
| 4 | `nonlinearity` | Why non-linearity, universal approximation | without activation, layers collapse | composition of linear maps is linear (shown in code) | universal approximation theorem: what it says | what UAT does NOT promise; depth vs width efficiency; bias-free ReLU nets are positively homogeneous |
| 5 | `act-gradients` | Vanishing gradients and dying ReLU | — | sigmoid saturates, gradient tiny at large inputs | product of many small derivatives; dying ReLU cause | Leaky ReLU / GELU fixes; diagnosing dead units (all-zero over the batch); residual connections as a gradient highway |
| 6 | `layers-mlp` | Layers, the MLP and shapes through nn.Linear | layer = many neurons side by side; input/hidden/output | output shape of nn.Linear on a batch | weight shape (out, in); Linear on 3-D input | shape errors and their messages; matrix form XW^T + b; silent transpose bug with square shapes |
| 7 | `param-count` | Counting parameters | weights + biases are "parameters" | in*out + out for one layer | whole MLP; bias=False; sum(p.numel()) | transformer MLP block sizing; parameters vs memory; 16 bytes/param with Adam; tied weights counted once |
| 8 | `output-layer` | Output layer per task | regression vs classification outputs | sigmoid+BCE, softmax+CE, linear+MSE | multi-label vs multi-class | positive-only targets; logits vs probabilities at the output; output bias = log-odds of the base rate |
| 9 | `init` | Weight initialisation | weights start random | why not all zeros (symmetry) | Xavier vs He and which activation; kaiming_normal_ std; zero biases are fine; Var = 2/fan_in | variance-preservation argument (activation std through 5 layers); PyTorch's default Linear init; GPT-2 1/sqrt(N) residual scaling |
| 10 | `backprop-neuron` | Backprop through a neuron and nn.Linear | what backprop computes; the chain rule | dL/dw and dL/db for one neuron by hand | dL/dw_i = delta * x_i; weight.grad = dOut^T x summed over the batch; input grad = dOut @ W | feature scale and SGD zig-zag; shared (tied) weights add their gradients |
| 11 | `nn-module` | Building networks with nn.Module | forward vs __init__, call model(x) | nn.ReLU vs F.relu; named_parameters of Sequential | plain list vs nn.ModuleList; eval() is not no_grad(); model(x) vs forward (hooks); freezing layers; float64 NumPy input | Parameter vs buffer vs plain tensor; in-place op breaks autograd |
| 12 | `gated-acts` | Modern activations: SiLU, softplus, ELU, GLU/SwiGLU | softplus = smooth ReLU | SiLU values | SiLU non-monotonic; ELU saturates at -alpha; GLU halves the width; SwiGLU structure (3 matrices, 8/3 d hidden) | SwiGLU parameter count; exact vs tanh GELU when porting checkpoints |

## Must-know facts
- One neuron: `y = f(w · x + b)`; the weighted sum is a dot product.
- A perceptron uses a step activation and can only separate classes with a straight line (hyperplane); it cannot learn XOR.
- Sigmoid range (0, 1), tanh range (-1, 1), ReLU range [0, inf), Leaky ReLU (-inf, inf).
- sigmoid'(x) = s(1 - s), max 0.25 at x = 0. tanh'(x) = 1 - tanh^2, max 1 at x = 0. ReLU' = 1 for x > 0, 0 for x < 0 (PyTorch uses 0 at x = 0).
- tanh(x) = 2·sigmoid(2x) - 1; tanh is zero-centred, sigmoid is not.
- GELU(x) = x·Φ(x); smooth, slightly negative for small negative inputs; the default in BERT/GPT-style transformers.
- Softmax outputs are positive and sum to 1; softmax(x + c) = softmax(x); a 2-class softmax over [z, 0] equals sigmoid(z).
- Without non-linear activations, any stack of Linear layers equals one Linear layer.
- Universal approximation: one hidden layer with enough units can approximate any continuous function on a bounded region. It says nothing about how many units, or whether training finds the weights.
- `nn.Linear(in, out)`: weight shape (out, in), bias shape (out,), parameters in*out + out; it acts on the last dimension of the input.
- Output layer: regression -> linear + MSE; binary -> 1 logit + sigmoid/BCE; multi-class -> K logits + softmax/CE; multi-label -> K logits + per-class sigmoid.
- All-equal (e.g. zero) initialisation makes every neuron in a layer compute and learn the same thing (symmetry).
- Xavier/Glorot (Var = 2/(fan_in + fan_out)) suits tanh/sigmoid; He/Kaiming (Var = 2/fan_in) suits ReLU.
- Dying ReLU: a unit whose input is negative for every example has zero gradient and never recovers.

- Backprop: dL/dw_i = (dL/dz) * x_i and dL/db = dL/dz; for nn.Linear, weight.grad = dOut^T @ x (summed over the batch) and the input gradient is dOut @ W. A weight used twice gets the SUM of both gradients.
- Submodules in a plain Python list are not registered (no parameters, no .to(device)); use nn.ModuleList. nn.Parameter = trained + saved; buffer = saved, not trained; plain tensor attribute = neither.
- model.eval() only changes Dropout/BatchNorm behaviour; it does not stop gradient tracking (use torch.no_grad()).
- In-place ops on tensors autograd saved (e.g. a sigmoid output) raise RuntimeError at backward.
- SiLU(x) = x*sigmoid(x) (non-monotonic, min about -0.28); softplus = log(1 + e^x); ELU -> -alpha; GLU halves the last dim; SwiGLU uses 3 matrices with hidden about (8/3)d (LLaMA-7B: 11008).
- Residual connections: d(x + f(x))/dx = 1 + f'(x), so gradients get a direct path back.
- Training memory with fp32 Adam is about 16 bytes per parameter before activations.
- Init the output bias of a rare-positive classifier to log(p/(1-p)) so the first predictions match the base rate.

## Common traps (each one must have at least one question)
- "Stacking more Linear layers makes a more powerful model" -> without activations it is still one linear function.
- "Initialise weights to zero to be safe" -> symmetry: all neurons stay identical (and with ReLU the gradients can be exactly zero).
- "Sigmoid outputs are centred at 0" -> centred at 0.5 and always positive; tanh is the zero-centred one.
- "Softmax gives independent per-class probabilities" -> they compete and sum to 1; multi-label needs per-class sigmoid.
- "nn.Linear(in, out).weight has shape (in, out)" -> it is (out, in).
- "Parameters of a Linear layer = in * out" -> forgets the out biases.
- "ReLU has no gradient problems" -> dead units with zero gradient.
- "Universal approximation means gradient descent will find a perfect 1-hidden-layer net" -> it only proves existence.
- "Put ReLU on the regression output" -> the model can never predict a negative value.
- "Adding a constant to all logits changes the softmax" -> softmax is shift-invariant.
- "The bias doesn't matter much" -> without it the decision boundary must pass through the origin.
- "A single perceptron can learn XOR" -> XOR is not linearly separable.

- "Store layers in self.layers = [...]" -> not registered; they never train or move to the GPU.
- "model.eval() is enough for validation" -> autograd still builds the graph; add torch.no_grad().
- "Softmax over dim=0 of a (batch, classes) tensor" -> each column sums to 1, not each example; no error.
- "torch.log(torch.softmax(z))" -> underflows to -inf; use log_softmax.
- "A sigmoid on the output makes a linear stack non-linear enough for XOR" -> it's still logistic regression.
- "A unit that is often 0 is dead" -> dead means 0 for EVERY example.
- "Square tensors passed transposed will raise a shape error" -> they run silently and give garbage.
- "Exact and tanh GELU are interchangeable when loading a checkpoint" -> small but compounding drift.
- "A NumPy array goes straight into nn.Linear" -> float64 vs float32 dtype RuntimeError.

## Interview angle
- **Why do neural nets need non-linear activations?** Because a composition of linear maps is linear: W2(W1x + b1) + b2 = Wx + b. Activations let depth build curved decision boundaries. SDE analogy: chaining pure "multiply-and-add" functions just gives another multiply-and-add.
- **Sigmoid vs ReLU for hidden layers?** Sigmoid saturates (gradient max 0.25, near 0 at the tails), so gradients vanish through depth; ReLU passes gradient 1 for positive inputs and is cheap. Downside: dying ReLU, fixed by Leaky ReLU/GELU or careful lr/init.
- **How many parameters does nn.Linear(784, 128) have?** 784*128 + 128 = 100,480. Always add the biases.
- **Why not initialise weights to zero?** Every neuron in a layer gets the same gradient, so they stay clones: you paid for 128 units and got 1. Random init breaks symmetry; Xavier/He choose the scale so activations neither explode nor vanish.
- **Which output layer and loss for multi-label vs multi-class?** Multi-class (exactly one label): softmax + cross-entropy. Multi-label (any subset): one sigmoid per class + binary cross-entropy.

- **What does loss.backward() compute for a Linear layer?** dL/dW = dOut^T @ x summed over the batch, dL/db = dOut summed, and dL/dx = dOut @ W to pass back. Shared weights add their gradients.
- **What is SwiGLU and why do LLMs use it?** out = W2(SiLU(W1 x) * W3 x): a gated MLP with 3 matrices and a smaller hidden width to keep the parameter count. It trains a bit better per parameter than a GELU MLP.

## Source material
To be added.
