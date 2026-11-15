"""Ladder structure: category -> section -> subject.

Subjects with status 'planned' exist in the tree but have no questions yet.
"""

CATEGORIES = [
    # slug, name, ladder_level, description
    ("foundations", "Foundations: Python & Data Tools", 0,
     "Prerequisites. Read, run and tweak Python; then NumPy and Pandas."),
    ("ml-fundamentals", "L1 · ML Fundamentals", 1,
     "What learning from data means, how models are tested, and how they fail."),
    ("dl-fundamentals", "L2 · Deep Learning Fundamentals", 2,
     "Neurons, loss, gradient descent and how a network trains."),
    ("text-to-llms", "L3 · Text → LLMs", 3,
     "Tokens, embeddings, attention: how text becomes something a model can use."),
    ("llm-engineering", "L4 · LLM Engineering", 4,
     "Prompting, RAG and fine-tuning: where most AI engineer work happens."),
    ("shipping", "L5 · Shipping It", 5,
     "Serving, monitoring and running models in production."),
]

SECTIONS = [
    # slug, category_slug, name, description
    ("python-core", "foundations", "Python Core", "The language itself, one idea at a time."),
    ("python-data", "foundations", "Python for Data", "NumPy, Pandas and plotting."),
    ("ml-core", "ml-fundamentals", "Core Ideas", "What ML is and the main kinds of learning."),
    ("ml-eval", "ml-fundamentals", "Evaluating Models", "Splits, overfitting, metrics and classic models."),
    ("dl-core", "dl-fundamentals", "Neural Network Basics", "From one neuron to a training loop."),
    ("text-core", "text-to-llms", "Text Representation", "Tokens, embeddings and similarity."),
    ("transformers", "text-to-llms", "Transformers", "Attention and how an LLM generates text."),
    ("llm-apps", "llm-engineering", "Building with LLMs", "Prompting, RAG and fine-tuning."),
    ("mlops", "shipping", "Production ML", "Serving and monitoring."),
]

SUBJECTS = [
    # slug, section_slug, name, description, status
    ("py-basics", "python-core", "Running Python & print", "Running code, print, comments.", "ready"),
    ("py-variables", "python-core", "Variables & Types", "Names, int/float/str/bool, type().", "ready"),
    ("py-strings", "python-core", "Strings", "Indexing, slicing, f-strings, methods.", "ready"),
    ("py-lists", "python-core", "Lists", "Ordered, changeable collections.", "ready"),
    ("py-dicts", "python-core", "Dictionaries", "Key → value lookups.", "ready"),
    ("py-conditions", "python-core", "Conditions & Booleans", "if / elif / else, and, or, not.", "ready"),
    ("py-loops", "python-core", "Loops", "for, while, range, break.", "ready"),
    ("py-functions", "python-core", "Functions", "def, parameters, return.", "ready"),
    ("py-comprehensions", "python-core", "Comprehensions", "One-line list and dict building.", "ready"),
    ("py-errors", "python-core", "Errors & Exceptions", "Reading tracebacks, try / except.", "ready"),
    ("py-classes", "python-core", "Classes (just enough)", "Objects, __init__, self, methods.", "ready"),

    ("np-arrays", "python-data", "NumPy Arrays", "Creating arrays, shape, dtype.", "ready"),
    ("np-operations", "python-data", "NumPy Operations", "Vectorised maths, broadcasting, axis.", "ready"),
    ("pd-dataframes", "python-data", "Pandas DataFrames", "Reading CSVs, selecting rows/columns.", "ready"),
    ("pd-cleaning", "python-data", "Pandas Cleaning & Grouping", "Missing values, groupby, merge.", "ready"),
    ("plotting", "python-data", "Plotting Basics", "matplotlib line, bar, scatter.", "ready"),

    ("ml-what", "ml-core", "What is Machine Learning?", "Rules vs learned functions.", "ready"),
    ("ml-types", "ml-core", "Types of Learning", "Supervised, unsupervised, reinforcement.", "ready"),
    ("ml-data", "ml-core", "Features, Labels & Data", "X, y, rows and columns.", "ready"),
    ("ml-splits", "ml-eval", "Train / Validation / Test", "Why we hold data back.", "ready"),
    ("ml-overfitting", "ml-eval", "Overfitting & Underfitting", "Memorising vs learning.", "ready"),
    ("ml-metrics", "ml-eval", "Classification Metrics", "Accuracy, precision, recall, F1.", "ready"),
    ("ml-models", "ml-eval", "Classic Models", "Linear/logistic regression, trees, kNN.", "ready"),

    ("dl-neuron", "dl-core", "The Neuron & Activations", "Weighted sum + non-linearity.", "ready"),
    ("dl-loss-gd", "dl-core", "Loss & Gradient Descent", "Measuring error and walking downhill.", "ready"),
    ("dl-training", "dl-core", "Training Loop", "Epochs, batches, learning rate, backprop.", "ready"),

    ("nlp-tokens", "text-core", "Tokens & Tokenization", "Sub-word pieces, BPE.", "ready"),
    ("nlp-embeddings", "text-core", "Embeddings & Similarity", "Meaning as vectors, cosine similarity.", "ready"),
    ("tf-attention", "transformers", "Attention & Transformers", "Words looking at other words.", "ready"),
    ("tf-generation", "transformers", "How LLMs Generate", "Next-token prediction, temperature, context window.", "ready"),

    ("llm-prompting", "llm-apps", "Prompting", "System prompts, few-shot, structured output.", "ready"),
    ("llm-rag", "llm-apps", "RAG", "Retrieve then generate.", "ready"),
    ("llm-finetuning", "llm-apps", "Fine-tuning & LoRA", "When and how to change the weights.", "ready"),

    ("ops-serving", "mlops", "Serving Models", "APIs, latency, batch vs real-time.", "ready"),
    ("ops-monitoring", "mlops", "Monitoring & Drift", "Watching a model after launch.", "ready"),
]
