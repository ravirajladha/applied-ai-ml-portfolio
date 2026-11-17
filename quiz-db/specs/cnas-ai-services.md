# AI & Cognitive Service APIs (S8): coverage spec

**Ladder:** API-driven Cloud Native Solutions (AIMLCZG549) › Module 5 AI and Cognitive Services, Part A   ·   **Prerequisites:** cnas-apis (REST, status codes, JSON), cnas-ml-pipelines (three generations of ML, ML metrics)
**Why it matters for AI/ML:** Most AI features in real products are not trained in-house: they are calls to a pre-trained model behind an API (a cloud cognitive service, the Hugging Face Inference API, or a foundation model on Amazon Bedrock). Session 8 teaches how to pick the right task and model, read a model card, and wire NLP, vision and speech APIs into an app, which is the basis of Lab 3 (NLP/speech tasks with cloud APIs) and of the RAG sessions that follow.

## Topics

| # | Topic slug | Topic | Amateur | Intermediate | Advanced | Expert |
|---|-----------|-------|---------|--------------|----------|--------|
| 1 | `ai-ml-genai` | AI vs ML vs generative AI; the three generations of ML | AI ⊃ ML ⊃ DL ⊃ GenAI; Gen 1/2/3 names | the effort in each generation (label + train, retrain DL, call an API) | why Gen 3 is "pay per use" and what it shifts to the developer | when a Gen 1 model still beats a Gen 3 API (cost, latency, tabular data) |
| 2 | `pretrained-finetuned` | Pre-trained vs fine-tuned models | general base vs task-adapted | the slides' six comparison points (data, purpose, efficiency, performance, transfer, interpretability) | pick: use as-is, fine-tune, or train from scratch, with data size and cost | where the slides overstate (interpretability, "unrelated" tasks, "no training required") |
| 3 | `cognitive-services` | Cloud cognitive services: definition, benefits, types | what a cognitive service is; consumed over REST | the types: language, speech, vision, decision, hosted LLM; the benefits list | match a requirement to a service type; the call pattern (endpoint, key header, JSON) | build vs buy, data residency, per-call cost, lock-in |
| 4 | `hf-hub` | Kaggle vs Hugging Face; the Hub and its APIs | Kaggle = Gen 1/2 datasets, HF = Gen 3 models + datasets | the Hub's three repo kinds (code/Spaces, models, datasets), Git versioning | model ids `org/name`, revisions, Inference API vs local pipeline | pinning a revision, licences and gated models in a product |
| 5 | `hf-terms` | Hugging Face terms: task, model, dataset, pipeline | what each term means | the common tasks; the named datasets (SQuAD, GLUE, IMDB, COCO, LibriSpeech); the 4-step workflow | how tasks, models and datasets interact; choosing a model for a task | the pipeline abstraction (pre-process -> model -> post-process) and its output shapes |
| 6 | `model-cards` | Model cards | what a model card is for | the fields of the sample card (name, description, intended use, training data, evaluation, limitations) | reading a card to accept or reject a model for a use case | metrics on the card vs metrics on your data; missing fields as a red flag |
| 7 | `nlp-nlu-nlg` | NLP basics, NLU vs NLG, a sample NLU pipeline | text or speech input; NLU understands, NLG produces | syntactic vs semantic analysis (stemming, lemmatization, POS, NER, WSD); NLG model list | order of a NLU pipeline; NLU tools (CoreNLP, NLTK, spaCy, OpenNLP) | stemming vs lemmatization trade-offs; where errors propagate in a pipeline |
| 8 | `nlp-apps` | Transformer applications in NLP | QA, spam detection, sentiment, translation, generation, summarisation | which task each product feature is; the output shape per task | NER output grouping, thresholds, routing low-confidence results | evaluation choice per task, combining several NLP APIs in one flow |
| 9 | `computer-vision` | Computer vision tasks and APIs | classification vs detection vs face recognition | feature extraction, restoration, tracking, scene reconstruction; the image-classification pipeline | detection boxes and IoU; segmentation masks; picking the task for a requirement | edge vs cloud CV API, privacy, batching video frames |
| 10 | `speech-apis` | Speech recognition APIs | speech-to-text, text-to-speech, translation, speaker recognition | batch vs streaming recognition; audio format | word error rate by hand; billing per audio second | accents and code-mixed Indian speech, custom vocabulary, latency budgets |
| 11 | `bedrock` | Amazon Bedrock and calling AI APIs in production | Bedrock = managed access to many foundation models via one API | serverless, pay per use, choice of models; the use case flow | choosing a model by cost, latency and quality; retries on 429 | multi-model routing, guardrails, data never used to train the provider's models |

## Must-know facts
- AI is the broad goal; ML learns from data; deep learning uses neural networks; generative AI creates new content (text, images, audio). Each is a subset of the one before.
- Three generations of ML: Gen 1 basic ML (label data, train, measure), Gen 2 deep learning (big data, retrain DL models), Gen 3 transfer learning / transformers (pre-trained and fine-tuned models used through APIs, pay per use).
- Pre-trained = general-purpose base model trained on a large dataset (expensive); fine-tuned = that model adapted with a smaller, task-specific dataset (cheap by comparison), often beating a model trained from scratch.
- Cloud cognitive services are AI-powered APIs from cloud platforms (Azure AI services, AWS, Google Cloud): pre-trained models, no data and no training needed, consumed over HTTP REST with SDKs.
- Service types: Language (NLP on text), Speech (speech-to-text, text-to-speech, speech translation, speaker recognition), Vision (image and video recognition), Decision (recommendations, anomaly detection, moderation), and a hosted LLM service.
- Kaggle is the classic dataset store for Gen 1 / Gen 2; Hugging Face is the model and dataset store for Gen 3 transformers.
- The Hugging Face Hub hosts Git-based code repositories (with discussions and pull requests), models with Git version control, and datasets (text, images, audio).
- Task = the problem; model = the pre-trained or fine-tuned network that performs it; dataset = data to train, fine-tune or evaluate. Workflow: task -> model -> dataset -> training or inference.
- `pipeline("<task>", model="<org/name>")` wraps pre-processing, the model and post-processing; classification returns a list of {label, score} dicts.
- A model card documents a model: description, intended use, training data, evaluation metrics, limitations and bias.
- NLP = NLU (understand syntax, semantics, context, sentiment, intent) + NLG (produce text: Markov chain, RNN, LSTM, Transformer).
- Syntactic analysis: segmentation, stemming, lemmatization, POS tagging. Semantic analysis: NER, word sense disambiguation.
- CV tasks: image classification (one label per image), object detection (labels + boxes), segmentation (a label per pixel), face recognition, tracking, restoration, scene reconstruction.
- Speech APIs are measured by word error rate, WER = (S + D + I) / N.
- Amazon Bedrock is a serverless AWS service that gives one API to a choice of foundation models from several providers, billed per token, with customisation (fine-tuning, RAG knowledge bases) and guardrails.

## Common traps (each one must have at least one question)
- "Gen 3 means no training ever" -> you can still fine-tune; you skip training from scratch.
- Fine-tuning called as costly as pre-training -> it reuses the base and needs far less data and compute.
- Kaggle vs Hugging Face reversed -> Kaggle for datasets and competitions; HF for transformer models plus datasets.
- Model card treated as marketing -> it lists limitations and training data; read them before using the model.
- Card accuracy assumed to hold on your data -> evaluate on your own data (domain shift: movie reviews vs Hindi-English product reviews).
- Stemming and lemmatization treated as the same -> stemming chops suffixes ("studies" -> "studi"), lemmatization returns a dictionary word ("study").
- NER called syntactic -> it is semantic analysis in the slides' split.
- Classification vs detection mixed up -> detection also says where (boxes), and can find many objects.
- IoU computed with the sum of areas instead of the union -> subtract the overlap once.
- WER assumed to stop at 100% -> insertions can push it above 1.
- Speech billed per call -> usually per second or per 15-second block of audio.
- Bedrock treated as one model -> it is a managed catalogue of many foundation models behind one API.
- Retrying a 429 immediately in a tight loop -> back off and respect Retry-After.
- Sending an API key in the query string or in client-side code -> keep it server-side, in a header.

## Interview angle
1. **"Build or buy for sentiment on product reviews?"** Start with a cognitive service or a fine-tuned Hub model, measure on 200 labelled reviews of your own; fine-tune only if accuracy on your data falls short or per-call cost at your volume beats hosting.
2. **"What do you check before using a Hub model?"** The model card: task, training data, evaluation, limitations, licence; then pin a revision and evaluate on your data.
3. **"Classification, detection or segmentation for a parking camera?"** Detection (count cars with boxes) or segmentation (occupied area) depending on whether you need counts or exact regions; classification only answers "is there a car".
4. **"How do you measure a speech API for Indian call-centre audio?"** WER on a labelled sample of real calls, split by accent and noise; check streaming latency and custom vocabulary support.
5. **"Why Bedrock instead of one provider's API?"** One AWS API, IAM and VPC controls, many models to choose per task, data stays in your account region, swap models without rewriting the integration.

## Source material
- Old-batch slides p190-233 (`cloud-src/cnas-ai-services.txt`), session 8, Module 5 Part A "Basic APIs for AI applications".
- AI, ML and generative AI and the three generations of ML (adapted from an AWS Innovate 2024 talk): Gen 1 basic ML, Gen 2 deep learning, Gen 3 transfer learning / transformers used through pay-per-use APIs.
- Pre-trained vs fine-tuned models: training data, purpose, efficiency, performance, transfer learning, interpretability.
- AI-based cognitive services: definition, Azure AI services as the example (pre-trained, no data, REST plus SDKs), the benefits list, the types table (language, speech, computer vision, decision, a hosted LLM service).
- Kaggle vs Hugging Face; the Hub (code repos, models, datasets); HF APIs as cognitive services for NLP, CV and speech.
- HF terms: task (the common task list), models (pre-trained vs fine-tuned, encoder families such as BERT and DistilBERT), datasets (SQuAD, GLUE, IMDB, COCO, LibriSpeech, custom), how they interact, the 4-step example workflow.
- The model card and the sample "bert-base-uncased-sentiment" card (IMDB, 50,000 reviews, accuracy 94%, F1 0.93, three limitations).
- NLP basics (text or speech input; the search and smart-speaker examples), NLU (syntactic and semantic analysis) vs NLG (Markov chain, RNN, LSTM, Transformer), a sample NLU pipeline and NLU tools (CoreNLP, NLTK, spaCy, OpenNLP).
- Transformer applications: QA, spam detection, sentiment analysis, machine translation, text generation, summarisation / paraphrasing / grammatical error checking.
- Computer vision tasks (object detection, face recognition, feature extraction, image classification, image restoration, object tracking, scene reconstruction) and the image-classification `pipeline` example with a vision-transformer checkpoint.
- Amazon Bedrock: choice of models and a use case (slides are images; content from the AWS documentation).
- No past papers; scenario style modelled on BITS WILP papers (Bengaluru food-delivery app, Pune smart-city cameras, an agritech cooperative's call centre, ₹ costs).
- **Standard practice (slides thin or image-only):** AI ⊃ ML ⊃ DL ⊃ GenAI; speech recognition APIs (handout only: batch vs streaming, WER, per-second billing); segmentation and IoU; the REST call pattern for cognitive services (key header, JSON, 429 and backoff); Bedrock details (serverless, per-token pricing, knowledge bases, guardrails, data not used for training); the pipeline's pre-process/model/post-process structure; stemming vs lemmatization examples.
- **Slide issues handled:** the slides say fine-tuning "can make models more interpretable" (not a standard claim: fine-tuning does not make a network more interpretable, at most a task-specific model's outputs are easier to evaluate), that transfer can go to a "potentially unrelated" task (transfer works best between related tasks), that Gen 3 needs "no model training" (true for API use, but fine-tuning is still training), and that decision services "provide NLP features" (decision services such as anomaly detection, personalisation and content moderation are not NLP). The sentiment slide lists "natural" for "neutral". Questions follow the standard facts and say so.
