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
    ("courses", "Courses: BITS WILP Electives", 6,
     "Exam-focused banks built from Ravi's course material (slides, notes, past papers)."),
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
    ("llm4genai", "courses", "LLMs for Generative AI (AIMLCZG536)",
     "Course modules 1-12: foundations to safety, in the course's own terms and exam style."),
    ("nlpapps", "courses", "NLP Applications (AIMLCZG519)",
     "Spell/grammar checking, RAG, QA and chatbots, sentiment, MT, information extraction, efficient NLP."),
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
    ("llmc-foundations", "llm4genai", "LLM Foundations (M1)", "Language models, tokenization, embeddings, positional encoding.", "ready"),
    ("llmc-pretraining", "llm4genai", "Pre-training & Scaling (M2)", "CLM objectives, data pipeline, scaling laws, CPT.", "ready"),
    ("llmc-architecture", "llm4genai", "Architecture & MoE (M3)", "Transformer review, attention variants, Mixture of Experts.", "ready"),
    ("llmc-inference", "llm4genai", "Inference & Optimisation (M4-M5)", "Decoding, prefill/decode, KV cache, PagedAttention, FlashAttention, quantization, speculative decoding.", "ready"),
    ("llmc-finetuning", "llm4genai", "Fine-tuning & PEFT (M6)", "IFT, Self-Instruct, adapters, LoRA, QLoRA, merging.", "ready"),
    ("llmc-alignment", "llm4genai", "Preference Alignment (M6)", "RLHF, reward models, PPO, GRPO, DPO.", "ready"),
    ("llmc-prompting", "llm4genai", "Prompting, Reasoning & Structured Data (M7)", "Prompt design, ICL, CoT, ToT, self-consistency, ReAct, function calling, tables.", "ready"),
    ("llmc-rag", "llm4genai", "Retrieval-Augmented LMs (M8)", "RAG pipeline, retrievers, context compression, Self-RAG, CRAG.", "ready"),
    ("llmc-agents", "llm4genai", "LLMs as Agents (M9)", "Agent anatomy, memory types, multi-agent patterns, text-to-SQL.", "ready"),
    ("llmc-eval", "llm4genai", "Evaluation (M10)", "Model vs system evaluation, BLEU/ROUGE/BERTScore, LLM-as-judge.", "ready"),
    ("llmc-safety", "llm4genai", "Safety, Security & Privacy (M11)", "Jailbreaks, prompt injection, guardrails, privacy.", "ready"),
    ("nlpa-overview", "nlpapps", "NLP Apps Overview & Tools (S1)", "NLP application landscape, NLTK/spaCy pipelines, preprocessing.", "ready"),
    ("nlpa-spellgrammar", "nlpapps", "Spell & Grammar Checking (S2)", "Edit distance, noisy channel, n-gram LMs, grammar checkers.", "ready"),
    ("nlpa-rag", "nlpapps", "RAG Applications (S3-S4)", "Naive RAG, Graph RAG, Agentic RAG, real-world case studies.", "ready"),
    ("nlpa-qa-conv", "nlpapps", "Question Answering & Conversational AI (S5-S6)", "QA systems, chatbots and dialogue, GenAI/agentic implementations.", "ready"),
    ("nlpa-sentiment", "nlpapps", "Sentiment Analysis (S7)", "Lexicon, ML, neural and GenAI/agentic sentiment methods.", "ready"),
    ("nlpa-ethics", "nlpapps", "Privacy & Ethics in NLP (S8)", "Data, model and deployment issues: bias, privacy, misuse.", "ready"),
    ("nlpa-mt", "nlpapps", "Machine Translation (S10-S12)", "Statistical and neural MT, evaluation, Indic-language translation.", "ready"),
    ("nlpa-ie", "nlpapps", "Information Extraction (S13-S14)", "NER, relation extraction, events and time.", "ready"),
    ("nlpa-efficient", "nlpapps", "Scalable & Efficient NLP (S15)", "Model compression, efficient architectures, inference and deployment.", "ready"),
]
