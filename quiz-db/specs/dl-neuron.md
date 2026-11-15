# The Neuron & Activations: coverage spec

**Ladder:** L2 · Deep Learning Fundamentals › Neural Network Basics   ·   **Prerequisites:** np-arrays (vectors, dot product), ml-models (linear / logistic regression)
**Why it matters for AI/ML:** Every deep model, from a tiny MLP to a 70B-parameter LLM, is stacks of "weighted sum + non-linearity". Knowing what one neuron computes, which activation goes where, how many parameters a layer has and why initialisation matters is the vocabulary for every later topic (training, transformers, fine-tuning, memory sizing).

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `neuron` | The neuron: weights, bias, weighted sum, perceptron | inputs x weights + bias; what a weight and bias mean | weighted sum as a dot product; computing one neuron by hand | the bias as a moved threshold; perceptron = step activation, linearly separable only | perceptron vs logistic regression; why XOR needs a hidden layer |
| 2 | `activations` | Activation functions (step, sigmoid, tanh, ReLU, Leaky ReLU, GELU) | ranges of sigmoid / tanh / ReLU | values at points; when each is used | derivatives (sigmoid' = s(1-s), max 0.25; tanh' max 1); zero-centring | GELU shape and why transformers use it; ReLU derivative at 0 in PyTorch; tanh/sigmoid identity |
| 3 | `softmax` | Softmax | turns scores into probabilities that sum to 1 | computing softmax of a small vector; argmax unchanged | shift invariance; temperature | numerically stable softmax; 2-class softmax = sigmoid |
| 4 | `nonlinearity` | Why non-linearity, universal approximation | without activation, layers collapse | composition of linear maps is linear (shown in code) | universal approximation theorem: what it says | what UAT does NOT promise; depth vs width efficiency |
| 5 | `act-gradients` | Vanishing gradients and dying ReLU | — | sigmoid saturates, gradient tiny at large inputs | product of many small derivatives; dying ReLU cause | Leaky ReLU / GELU fixes; diagnosing dead units |
| 6 | `layers-mlp` | Layers, the MLP and shapes through nn.Linear | layer = many neurons side by side; input/hidden/output | output shape of nn.Linear on a batch | weight shape (out, in); Linear on 3-D input | shape errors and their messages; matrix form XW^T + b |
| 7 | `param-count` | Counting parameters | weights + biases are "parameters" | in*out + out for one layer | whole MLP; bias=False; sum(p.numel()) | transformer MLP block sizing; parameters vs memory |
| 8 | `output-layer` | Output layer per task | regression vs classification outputs | sigmoid+BCE, softmax+CE, linear+MSE | multi-label vs multi-class | positive-only targets; logits vs probabilities at the output |
| 9 | `init` | Weight initialisation | weights start random | why not all zeros (symmetry) | Xavier vs He and which activation | variance-preservation argument; PyTorch's default Linear init |

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

## Interview angle
- **Why do neural nets need non-linear activations?** Because a composition of linear maps is linear: W2(W1x + b1) + b2 = Wx + b. Activations let depth build curved decision boundaries. SDE analogy: chaining pure "multiply-and-add" functions just gives another multiply-and-add.
- **Sigmoid vs ReLU for hidden layers?** Sigmoid saturates (gradient max 0.25, near 0 at the tails), so gradients vanish through depth; ReLU passes gradient 1 for positive inputs and is cheap. Downside: dying ReLU, fixed by Leaky ReLU/GELU or careful lr/init.
- **How many parameters does nn.Linear(784, 128) have?** 784*128 + 128 = 100,480. Always add the biases.
- **Why not initialise weights to zero?** Every neuron in a layer gets the same gradient, so they stay clones: you paid for 128 units and got 1. Random init breaks symmetry; Xavier/He choose the scale so activations neither explode nor vanish.
- **Which output layer and loss for multi-label vs multi-class?** Multi-class (exactly one label): softmax + cross-entropy. Multi-label (any subset): one sigmoid per class + binary cross-entropy.

## Source material
To be added.
