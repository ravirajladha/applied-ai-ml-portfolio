from helpers import mcq, tf, out, fill

QUESTIONS = {
# ---------------- L1 ML fundamentals ----------------
"ml-what": [
    mcq("What is the core difference between normal programming and machine learning?",
        ["In ML the computer learns the rules from examples", "ML doesn't use code", "ML is always faster", "Normal programs can't use data"], 0,
        "Who writes the if/else rules in each case?",
        "Normal code: you write rules, data goes in, answers come out. ML: you give data + answers, and the rules (the model) come out.",
        analogy="A model is a function the computer wrote for you from examples.",
        diagram="""
 Programming:  rules + data   --> answers
 ML:           data + answers --> rules (model)
"""),
    mcq("In SDE terms, what is 'training' a model closest to?",
        ["A slow compile step that produces the model's weights", "Running unit tests", "Deploying to production", "Writing documentation"], 0,
        "It's done once, takes time, and produces an artifact.",
        "Training is a slow, expensive build that turns data into weights; inference is running that build.",
        analogy="Weights = compiled binary; training = compile; inference = run."),
    mcq("What is 'inference'?",
        ["Using a trained model to make predictions", "Collecting data", "Cleaning data", "Choosing a model"], 0,
        "It happens after training, every time a user asks something.",
        "Inference = calling the trained model on new input to get an output."),
    tf("A model's 'weights' (parameters) are the numbers learned during training.", True,
       "They're what gets saved to disk after training.",
       "Weights are the learned numbers; the model file is mostly weights."),
],

"ml-types": [
    mcq("Predicting house prices from past sales with known prices is which type of learning?",
        ["Supervised", "Unsupervised", "Reinforcement", "None"], 0,
        "Do the training examples come with the right answer?",
        "Each example has a label (the price), so it's supervised learning."),
    mcq("Grouping customers into segments with no labels given is:",
        ["Unsupervised (clustering)", "Supervised (classification)", "Reinforcement", "Regression"], 0,
        "No right answers are provided; the model finds structure itself.",
        "No labels -> unsupervised. Clustering finds natural groups."),
    mcq("An agent learning to play a game from rewards and penalties is:",
        ["Reinforcement learning", "Supervised learning", "Unsupervised learning", "Transfer learning"], 0,
        "Think trial and error with a score.",
        "RL learns by acting, getting a reward, and improving its policy.",
        diagram="""
   +-------- action ------->+
 Agent                  Environment
   +<--- reward, state -----+
"""),
    mcq("Classification vs regression: which is regression?",
        ["Predicting tomorrow's temperature in degrees", "Spam or not spam", "Cat, dog or bird", "Fraud yes/no"], 0,
        "Regression predicts a number; classification predicts a category.",
        "Temperature is a continuous number -> regression."),
    tf("Large language models are pre-trained with self-supervised learning: the 'label' is just the next word in the text.", True,
       "Nobody hand-labels the internet.",
       "The text supplies its own labels (next token), which is why LLMs can train on so much data.", d=2),
],

"ml-data": [
    mcq("In a table of houses, which is the 'label' (y) for a price model?",
        ["The price column", "The number of rooms", "The location", "The row number"], 0,
        "The label is what you want to predict.",
        "Features (X) are the inputs like rooms and location; the label (y) is the target: price.",
        diagram="""
  rooms  area  city   |  price
  -----  ----  ----   |  -----
    3    1200  BLR    |  90L
  <---- features X -->|  <-y->
"""),
    mcq("One row of a dataset usually represents:",
        ["One example (e.g. one house)", "One feature", "One model", "One prediction"], 0,
        "Rows are things; columns are facts about them.",
        "Row = one sample / example; column = one feature."),
    mcq("Why do we convert text categories like 'BLR', 'MUM' into numbers?",
        ["Models only do maths on numbers", "To save disk space", "To hide the data", "It's optional and never matters"], 0,
        "What does a model compute internally?",
        "Models multiply and add numbers, so categories are encoded (e.g. one-hot) first."),
    tf("Garbage in, garbage out: a model can't be better than the data it learned from.", True,
       "Think of tests written against wrong expected values.",
       "Bad, biased or mislabelled data produces a bad model, no matter how fancy the algorithm."),
],

"ml-splits": [
    mcq("Why do we keep a test set the model never trains on?",
        ["To measure how it does on unseen data", "To train faster", "To make the dataset smaller", "Because the data is wrong"], 0,
        "A student who saw the exam paper beforehand...",
        "The test set is a fair, unseen exam. Scoring on training data only shows memorisation.",
        analogy="Evals are the test suite; testing on training data is like tests that hard-code the answers.",
        diagram="""
 |------------ data -------------|
 |  train 70%  | val 15% |test 15%|
   learn here    tune      final score
"""),
    mcq("What is the validation set used for?",
        ["Tuning settings and choosing between models", "The final score you report", "Training the weights", "Storing labels"], 0,
        "It sits between train and test.",
        "Validation helps pick hyperparameters; test is touched once at the end."),
    tf("It's fine to look at test-set results many times while tuning your model.", False,
       "If you tune on it, is it still 'unseen'?",
       "Tuning on the test set leaks information; your score becomes optimistic. Use validation for tuning.", d=2),
    mcq("What is 'data leakage'?",
        ["Information from the test/future sneaking into training", "Losing data from disk", "Sharing data publicly", "Too little data"], 0,
        "Think of a feature that secretly contains the answer.",
        "Leakage makes offline scores look great and production results bad.", d=2),
],

"ml-overfitting": [
    mcq("A model scores 99% on training data but 60% on test data. This is:",
        ["Overfitting", "Underfitting", "A perfect model", "Data leakage fixed"], 0,
        "It memorised the practice questions.",
        "Big train/test gap = overfitting: it learned noise, not the pattern.",
        analogy="Like tests that pass only because the expected values are hard-coded.",
        diagram="""
 error
  |\\          test
  | \\     ___/
  |  \\___/
  |   \\____  train
  +------------> model complexity
     under | over
"""),
    mcq("A model does badly on both training and test data. This is:",
        ["Underfitting", "Overfitting", "Leakage", "Drift"], 0,
        "It didn't even learn the practice questions.",
        "Too simple (or too little training) to capture the pattern."),
    mcq("Which is NOT a common fix for overfitting?",
        ["Make the model much bigger", "Get more training data", "Regularisation / dropout", "Early stopping"], 0,
        "Which option gives it MORE capacity to memorise?",
        "A bigger model can memorise more. More data, regularisation and early stopping all help."),
    tf("Early stopping means stopping training when validation error starts going up.", True,
       "Watch the validation curve.",
       "When val error rises while train error still falls, the model has started overfitting.", d=2),
],

"ml-metrics": [
    mcq("A spam filter: recall answers which question?",
        ["Of all real spam, how much did we catch?", "Of emails we flagged, how many were spam?", "How many emails in total?", "How fast is it?"], 0,
        "Recall = 'did we recall (find) them all?'",
        "Recall = TP / (TP + FN). Precision = TP / (TP + FP).",
        diagram="""
               predicted +   predicted -
 actual +        TP            FN
 actual -        FP            TN

 precision = TP / (TP + FP)   "flagged ones correct?"
 recall    = TP / (TP + FN)   "found them all?"
"""),
    mcq("For cancer screening, which do we usually care about more?",
        ["Recall: don't miss real cases", "Precision: never raise a false alarm", "Accuracy only", "Speed"], 0,
        "Which mistake is worse: a false alarm or a missed patient?",
        "Missing a real case (false negative) is costly, so we favour high recall."),
    mcq("99% of transactions are not fraud. A model that always says 'not fraud' has 99% accuracy. Why is that a problem?",
        ["It never catches any fraud: accuracy hides it", "99% is too low", "Accuracy is always wrong", "It isn't a problem"], 0,
        "What is its recall for fraud?",
        "With imbalanced classes, accuracy is misleading. Recall for fraud here is 0%.", d=2),
    fill("The metric that is the harmonic mean of precision and recall is the ____ score.", "F1",
         "Letter + number.",
         "F1 = 2PR / (P + R); it's high only when both precision and recall are high."),
    out('tp, fp, fn = 8, 2, 4\nprint(tp / (tp + fp))', ["0.8", "0.667", "0.5", "0.2"], 0,
        "This formula is precision.",
        "8 / (8 + 2) = 0.8.", question="This computes precision. What does it print?", d=2),
],

"ml-models": [
    mcq("Linear regression predicts by:",
        ["Fitting a straight line (weighted sum of features)", "Building a tree of questions", "Looking at the nearest neighbours", "Random guessing"], 0,
        "y = w*x + b",
        "It learns weights w and bias b so that w*x + b is close to the true y.",
        diagram="""
 y |      .  /
   |    .  /.
   |   . /  .
   |  ./ .
   +--------- x
   line: y = w*x + b
"""),
    mcq("Despite its name, logistic regression is used for:",
        ["Classification (probability of a class)", "Predicting prices", "Clustering", "Generating text"], 0,
        "Its output is squashed between 0 and 1.",
        "It applies a sigmoid to a weighted sum to give a probability, e.g. P(spam)."),
    mcq("A decision tree makes predictions by:",
        ["Asking a sequence of yes/no questions about features", "Averaging all training labels", "Multiplying matrices", "Drawing a straight line"], 0,
        "Like a flowchart.",
        "Each node splits on a feature (e.g. income > 50k?) until a leaf gives the answer.",
        analogy="Nested if/else rules, but learned from data."),
    mcq("k-Nearest Neighbours (kNN) classifies a new point by:",
        ["The majority label among the k closest training points", "A learned line", "A neural network", "Random choice"], 0,
        "'Tell me who your neighbours are...'",
        "kNN stores the data and votes among the k nearest examples at prediction time."),
],

# ---------------- L2 Deep learning ----------------
"dl-neuron": [
    mcq("What does a single artificial neuron compute?",
        ["A weighted sum of inputs plus bias, passed through an activation", "The average of its inputs", "A random number", "A sort of the inputs"], 0,
        "Multiply, add, squash.",
        "output = activation(w1*x1 + w2*x2 + ... + b).",
        diagram="""
 x1 --w1--\\
 x2 --w2---(  sum + b  )--> activation --> output
 x3 --w3--/
"""),
    mcq("Why do we need a non-linear activation like ReLU?",
        ["Without it, stacked layers collapse into one linear function", "To make training slower", "To reduce memory", "It's only for images"], 0,
        "What do you get when you compose straight lines?",
        "Linear of linear is still linear. Non-linearity lets networks learn curves and complex patterns."),
    out('def relu(x):\n    return max(0, x)\n\nprint(relu(-3), relu(5))', ["0 5", "-3 5", "3 5", "0 0"], 0,
        "ReLU keeps positives, zeroes out negatives.",
        "relu(-3) = 0, relu(5) = 5."),
    mcq("Sigmoid squashes any number into which range?",
        ["0 to 1", "-1 to 1", "0 to infinity", "-infinity to infinity"], 0,
        "Useful as a probability.",
        "sigmoid(x) = 1 / (1 + e^-x), always between 0 and 1."),
],

"dl-loss-gd": [
    mcq("What is a loss function?",
        ["A number measuring how wrong the model's predictions are", "The model's accuracy", "The size of the dataset", "A type of layer"], 0,
        "Lower is better.",
        "Loss scores the error; training tries to make it as small as possible.",
        analogy="Like a failing-tests count the build is trying to drive to zero."),
    mcq("Gradient descent updates the weights by:",
        ["Taking a small step in the direction that reduces the loss", "Setting them to random values", "Doubling them", "Removing the largest weight"], 0,
        "Think of walking downhill in fog, feeling the slope.",
        "w_new = w - learning_rate * gradient. The gradient points uphill, so we step the other way.",
        diagram="""
 loss
  |\\
  | \\  o  <- start
  |  \\  \\
  |   \\  o
  |    \\__o__/  <- minimum
  +-------------- weight
"""),
    mcq("What happens if the learning rate is far too large?",
        ["Training jumps around or blows up instead of converging", "Training becomes perfectly stable", "The model gets smaller", "Nothing changes"], 0,
        "Huge steps on a hillside...",
        "Too big: overshoots the minimum and diverges. Too small: painfully slow.", d=2),
    out('w = 4.0\ngrad = 2.0\nlr = 0.5\nw = w - lr * grad\nprint(w)', ["3.0", "5.0", "2.0", "4.0"], 0,
        "One gradient descent step: w - lr * grad.",
        "4.0 - 0.5 * 2.0 = 3.0.", question="One gradient descent step. What does it print?", d=2),
    mcq("Which loss is typical for classification?",
        ["Cross-entropy", "Mean squared error", "Accuracy", "Euclidean distance"], 0,
        "It compares predicted probabilities with the true class.",
        "Cross-entropy punishes confident wrong answers. MSE is typical for regression.", d=2),
],

"dl-training": [
    mcq("Backpropagation, in one sentence:",
        ["It works out how much each weight contributed to the error, from the output backwards", "It runs the model backwards to generate data", "It deletes bad weights", "It loads the dataset"], 0,
        "It's how the gradients get computed.",
        "Backprop applies the chain rule layer by layer to get every weight's gradient; gradient descent then uses them.",
        diagram="""
 forward:   input -> layer1 -> layer2 -> output -> loss
 backward:  grads <- layer1 <- layer2 <- output <- loss
"""),
    mcq("What is one 'epoch'?",
        ["One full pass over the whole training set", "One weight update", "One layer", "One prediction"], 0,
        "Every example has been seen once.",
        "An epoch = the model has seen every training example once."),
    mcq("Why train in mini-batches instead of one example at a time or all data at once?",
        ["Balances speed (GPU parallelism) with memory and stable updates", "It's required by Python", "Batches give higher accuracy always", "To skip examples"], 0,
        "All data might not fit in GPU memory.",
        "Batches use the GPU efficiently and give less noisy gradient estimates than single examples.", d=2),
    mcq("In a PyTorch training step, what is the usual order?",
        ["forward -> loss -> loss.backward() -> optimizer.step() -> zero_grad", "optimizer.step() -> forward -> loss", "loss.backward() -> forward -> step", "zero_grad -> step -> forward"], 0,
        "You can't compute gradients before you have a loss.",
        "Predict, measure error, compute gradients, update weights, clear gradients for the next batch.",
        code="""
for x, y in loader:
    pred = model(x)            # forward
    loss = loss_fn(pred, y)    # how wrong?
    loss.backward()            # gradients
    optimizer.step()           # update weights
    optimizer.zero_grad()      # reset for next batch
""", d=2),
],

# ---------------- L3 Text -> LLMs ----------------
"nlp-tokens": [
    mcq("What is a token?",
        ["A chunk of text (word or sub-word) the model reads as one unit", "A password", "A single letter always", "A full sentence"], 0,
        "'unhappiness' might become 'un' + 'happi' + 'ness'.",
        "Tokens are the model's units of text; each maps to an integer ID.",
        diagram="""
 "unhappiness"  ->  [ un | happi | ness ]  ->  [ 403, 9152, 1108 ]
   text               tokens                   token IDs
"""),
    mcq("Why do LLMs use sub-word tokens (like BPE) instead of whole words?",
        ["They can represent any word, even new or rare ones, with a fixed vocabulary", "Sub-words are always shorter to type", "Whole words are not allowed", "To hide the text"], 0,
        "What happens to a word never seen in training?",
        "Sub-words avoid 'unknown word' problems and keep the vocabulary a manageable size."),
    tf("API pricing and context limits for LLMs are measured in tokens, not words.", True,
       "Check any LLM pricing page.",
       "Roughly 1 token ≈ 3/4 of an English word; cost and limits are counted in tokens."),
    mcq("BPE (Byte-Pair Encoding) builds its vocabulary by:",
        ["Repeatedly merging the most frequent pair of symbols", "Taking every dictionary word", "Splitting on spaces only", "Random splitting"], 0,
        "Start from characters, merge common pairs.",
        "BPE starts from characters and keeps merging frequent pairs (e.g. 't'+'h' -> 'th').", d=2),
],

"nlp-embeddings": [
    mcq("What is an embedding?",
        ["A list of numbers (vector) that captures the meaning of text", "A compressed zip of text", "A database index", "An image"], 0,
        "Similar meanings land close together.",
        "Embeddings map text to vectors so 'king' and 'queen' sit near each other in space.",
        diagram="""
   ^         queen
   |   king    .
   |    .
   |                    banana
   |                      .   apple
   +------------------------------>
 close points = similar meaning
"""),
    mcq("Cosine similarity measures:",
        ["The angle between two vectors (how aligned they are)", "The length of a vector", "The number of words", "Spelling distance"], 0,
        "1 means pointing the same way.",
        "cos = 1 same direction, 0 unrelated, -1 opposite. Used for semantic search and RAG."),
    out('import numpy as np\na = np.array([1, 0])\nb = np.array([0, 1])\nprint(a @ b)', ["0", "1", "2", "[0 0]"], 0,
        "@ is the dot product: multiply pairs and add.",
        "1*0 + 0*1 = 0. These vectors are perpendicular, so cosine similarity is 0.", d=2),
    mcq("Static (word2vec) vs contextual (BERT/LLM) embeddings: what's the difference?",
        ["Contextual embeddings change with the sentence; static ones don't", "Static ones are bigger", "Contextual ones are for images", "No difference"], 0,
        "'bank' in 'river bank' vs 'bank account'.",
        "word2vec gives 'bank' one vector; contextual models give different vectors depending on surrounding words.", d=2),
],

"tf-attention": [
    mcq("What does attention let a word do?",
        ["Look at other words and decide which matter for its meaning", "Skip the sentence", "Translate itself", "Count letters"], 0,
        "In 'The animal didn't cross because it was tired', what is 'it'?",
        "Attention weights how much each token should pull information from every other token.",
        diagram="""
 The  animal  didn't  cross  because  it  was  tired
        ^                              |
        +-------- strong attention ----+
"""),
    mcq("Query, Key, Value in attention are like:",
        ["A search: query asks, keys are matched, values are returned", "Three separate models", "Three datasets", "Three loss functions"], 0,
        "Think of a database or search engine lookup.",
        "Score = query . key; softmax the scores; take a weighted mix of values.",
        analogy="A fuzzy key-value store lookup: soft-match the query against keys, return a blend of values."),
    mcq("Why did transformers replace RNNs for most NLP?",
        ["They process all tokens in parallel and handle long-range context better", "They use less memory always", "They don't need data", "They're older"], 0,
        "RNNs read one word at a time.",
        "Parallel processing suits GPUs, and attention connects distant words directly.", d=2),
    tf("A decoder-only model (like GPT) can only attend to earlier tokens, not future ones.", True,
       "When predicting the next word, you can't peek at it.",
       "A causal mask hides future tokens so the model learns to predict what comes next.", d=2),
],

"tf-generation": [
    mcq("At its core, an LLM is trained to:",
        ["Predict the next token", "Look up answers in a database", "Search the web", "Translate only"], 0,
        "Autocomplete, at huge scale.",
        "It outputs a probability for every token in the vocabulary, picks one, appends it, and repeats.",
        diagram="""
 "The cat sat on the"  ->  LLM  ->  mat 62% | floor 20% | sofa 9% ...
                                     pick -> "mat" -> append -> repeat
"""),
    mcq("Raising temperature makes the output:",
        ["More random / creative", "More deterministic", "Shorter", "Faster"], 0,
        "Temperature 0 = always the top choice.",
        "Higher temperature flattens the probabilities, so less likely tokens get picked more."),
    mcq("What is the context window?",
        ["The max number of tokens the model can see at once (prompt + output)", "The browser window", "The training time", "The number of layers"], 0,
        "It's the model's working memory.",
        "Anything beyond the context window is invisible to the model."),
    mcq("What is a 'hallucination'?",
        ["Confident output that is false or made up", "A crash", "A slow response", "A refusal"], 0,
        "The model predicts plausible text, not verified facts.",
        "Because it predicts likely tokens, an LLM can produce fluent but wrong answers. RAG and citations help."),
],

# ---------------- L4 LLM engineering ----------------
"llm-prompting": [
    mcq("What is few-shot prompting?",
        ["Putting a few worked examples in the prompt", "Training on a few GPUs", "Asking very short questions", "Using a small model"], 0,
        "Show, don't just tell.",
        "Examples in the prompt show the model the exact format and style you want."),
    mcq("What is a system prompt for?",
        ["Setting the model's role, rules and tone for the whole conversation", "Logging errors", "Choosing the GPU", "Storing user passwords"], 0,
        "It sits above the user's messages.",
        "The system prompt is standing instructions: who to be, what to do and not do."),
    mcq("Your app needs to parse the model's answer in code. Best approach?",
        ["Ask for structured output (JSON with a schema) and validate it", "Hope it's consistent", "Use regex on free text", "Ask it nicely twice"], 0,
        "Treat it like an API contract.",
        "Structured outputs / JSON schema give a predictable format; always validate before using.",
        analogy="Same as validating a request body against a schema in a REST API."),
    tf("Prompting changes the model's weights.", False,
       "Does the model file on disk change?",
       "Prompting only changes the input. Fine-tuning changes the weights."),
],

"llm-rag": [
    mcq("What is RAG?",
        ["Retrieve relevant documents, then give them to the LLM to answer", "A new model architecture", "A fine-tuning method", "A tokenizer"], 0,
        "Retrieval-Augmented Generation.",
        "Search your data for relevant chunks, paste them into the prompt, and let the LLM answer from them.",
        analogy="An open-book exam: the model looks up the right pages before answering.",
        diagram="""
 question -> embed -> vector DB search -> top-k chunks
                                              |
 answer  <-  LLM  <-  prompt = question + chunks
"""),
    mcq("Why use RAG instead of fine-tuning for company documents?",
        ["Docs change often; RAG updates by re-indexing, and can cite sources", "RAG is always more accurate", "Fine-tuning is impossible", "RAG needs no data"], 0,
        "What happens when a policy document changes tomorrow?",
        "RAG keeps knowledge outside the weights: cheap to update, easy to cite, fewer hallucinations."),
    mcq("What is 'chunking' in RAG?",
        ["Splitting documents into smaller pieces before embedding them", "Compressing the model", "Batching API calls", "Deleting old docs"], 0,
        "A 200-page PDF won't fit as one search result.",
        "Smaller chunks give precise retrieval; overlap between chunks keeps context.", d=2),
    mcq("What does a vector database store?",
        ["Embeddings plus the original text, searchable by similarity", "Only SQL tables", "Model weights", "Images only"], 0,
        "Search by meaning, not exact keywords.",
        "It indexes vectors for fast nearest-neighbour search (e.g. FAISS, Chroma, pgvector).", d=2),
],

"llm-finetuning": [
    mcq("Prompting vs RAG vs fine-tuning: when is fine-tuning the right choice?",
        ["To change behaviour/style/format consistently, not to add fresh facts", "Whenever you have any data", "To add today's news", "Never"], 0,
        "Try the cheap options first.",
        "Order of attack: prompt -> RAG (knowledge) -> fine-tune (behaviour, format, domain style)."),
    mcq("LoRA in one sentence:",
        ["Freeze the model and train small low-rank adapter matrices instead", "Train every weight from scratch", "Delete half the layers", "A new tokenizer"], 0,
        "Low-Rank Adaptation.",
        "LoRA adds tiny trainable matrices next to frozen weights, so you train well under 1% of the parameters.",
        diagram="""
 x --> [ W frozen (big) ] ----+--> output
  \\                          |
   +-> [A small] -> [B small]-+   <- only these train
"""),
    mcq("Why does QLoRA fit on a small GPU?",
        ["The frozen base model is stored in 4-bit, and only small LoRA adapters train", "It uses no GPU", "It trains a smaller dataset", "It skips backprop"], 0,
        "Q = quantized.",
        "Quantizing the base weights to 4 bits cuts memory ~4x vs 16-bit; adapters stay small."),
    tf("Fine-tuning a model on a few documents is a reliable way to make it remember exact facts.", False,
       "Compare with RAG.",
       "Fine-tuning is weak at injecting precise facts and needs retraining to update. Use RAG for facts.", d=2),
],

# ---------------- L5 Shipping ----------------
"ops-serving": [
    mcq("What's the most common way to serve a model to an app?",
        ["Wrap it in an HTTP API (e.g. FastAPI) that returns predictions", "Email the weights to users", "Run it inside the database", "Print results to a file"], 0,
        "Your SDE skills apply directly here.",
        "Load the model once at startup, expose a POST /predict endpoint, return JSON.",
        code="""
from fastapi import FastAPI
app = FastAPI()
model = load_model()          # once, at startup

@app.post("/predict")
def predict(req: Input):
    return {"label": model(req.text)}
"""),
    mcq("Batch vs real-time inference: which is batch?",
        ["Scoring all customers overnight for tomorrow's emails", "A chatbot replying to a user", "Fraud check during card payment", "Autocomplete as you type"], 0,
        "Does anyone wait for the answer right now?",
        "Batch runs on a schedule over many rows; real-time answers one request with low latency."),
    mcq("Which usually cuts LLM latency and cost the most?",
        ["Smaller model, caching repeated prompts, shorter outputs", "Bigger GPU only", "More logging", "Longer prompts"], 0,
        "Cost scales with tokens and model size.",
        "Fewer tokens, a right-sized model and caching are the big levers."),
    tf("Loading the model inside every request handler is a good idea.", False,
       "Loading can take seconds and gigabytes.",
       "Load once at startup and reuse it; per-request loading kills latency.", d=2),
],

"ops-monitoring": [
    mcq("What is data drift?",
        ["Live input data no longer looks like the training data", "The model file got corrupted", "The server moved", "Users stopped using the app"], 0,
        "The world changes after you train.",
        "When input distributions shift (new products, new slang), accuracy quietly drops.",
        diagram="""
 training data:  ___/\\___        live data (6 months later):   ______/\\_
                   ^ peak                                            ^ shifted
"""),
    mcq("Why monitor a model after deployment if tests passed?",
        ["Models can degrade silently as data changes; there's no crash", "To check the server is on", "Monitoring makes it more accurate", "It's not needed"], 0,
        "A wrong prediction doesn't throw an exception.",
        "Track input stats, prediction distribution and (when available) real accuracy; alert and retrain."),
    mcq("Which is a good signal to track for an LLM app?",
        ["User feedback, failed/empty responses, latency and token cost", "Only CPU temperature", "Number of code commits", "Disk size"], 0,
        "Quality + speed + cost.",
        "Log inputs/outputs, latency, tokens and thumbs-up/down; run evals on samples."),
    tf("Retraining on fresh data is a common response to drift.", True,
       "The model needs to see the new world.",
       "Detect drift -> retrain/refresh -> evaluate -> redeploy, ideally as an automated pipeline."),
],
}
