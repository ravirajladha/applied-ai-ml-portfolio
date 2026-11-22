# Social Media Analytics (AIMLCZG522) — Study spec

> Turning posts, likes and follower networks into business insight: sentiment, communities, influencers, diffusion and recommendations. · Status: spec only (not built yet)

## 1. What it is and why an AI engineer should care

Social media analytics (SMA) means mining platforms such as X/Twitter, Instagram, Reddit and review sites for insight.
The course has two halves: NLP on posts (sentiment, aspect-based opinions, summarisation, information extraction, with
GenAI) and network analysis on who-follows-whom (graph measures, network models, community detection, information
diffusion, influence and homophily). It ends with recommendations, behaviour analytics, social media monitoring for
business decisions, marketing strategy, ethics and graph representation learning. Useful for brand-monitoring,
marketing-tech and trust-and-safety teams; less central for core AI engineering roles.

**Job relevance: 2/5** — applied NLP and graph mining are useful skills, but dedicated SMA roles are mostly in marketing analytics.

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (older batch) | `handouts/Older batch - Social Media Analytics (S2-25_AIMLCZG522) COURSE HANDOUT.docx` | v2.0, dated 1/10/2025, Second Semester 2025-2026, Prof. Garima Jindal; 16 contact sessions, 5 labs; textbooks Zafarani et al. "Social Media Mining" (T1) and Bing Liu "Sentiment Analysis and Opinion Mining" (T2) |

Gaps: no current handout, slides, past papers or lab sheets. The handout's learning outcomes (LO1–LO4) talk about
general NLP, language modelling and parsing: they look copied from an NLP course and do not match the SMA topics.

## 3. Running scenario

**BrewBay** is a direct-to-consumer coffee brand in Bengaluru that sells online and through 40 cafés. It launches a
new cold brew and wants to know what people really think and how word spreads. The data: 200,000 public posts and
reviews mentioning the brand and competitors, a follower graph of 50,000 accounts, and the website's Google Analytics
traffic. The goals: sentiment by aspect (taste, price, delivery), the communities and influencers that matter, how
the launch campaign spread, which products to recommend to whom, and a monthly dashboard the marketing head uses to
decide spend. Each module adds one part of BrewBay's listening and insight platform.

## 4. Module map

Modules follow the handout's modular content structure and session plan. Contact hours per module: not stated.

### M1 · Social media mining: an introduction (session 1)

Topics: importance and characteristics of social media; platforms; mining challenges; applications and case studies.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Social media mining | Extracting patterns from user-generated content and the network of users. | Log analytics, where the logs are people |
| Big data paradox | Huge volume overall, yet little data about any single user. | Millions of requests, few per session |
| Sampling bias | Posts collected via an API are not a random sample of users or opinions. | Monitoring only the healthy servers |
| Noise | Spam, bots, sarcasm and slang that hide the real signal. | Flaky tests polluting CI results |

Diagram ideas: SMA pipeline (collect → clean → NLP + graph → insight → decision); platform comparison table (text, image, graph, API access).
Scenario step: define BrewBay's questions and collect the first dataset.
Notebook idea: load a public tweets/reviews dataset with pandas; count posts by day, hashtags, bot-like accounts. CPU.
Production angle: platform APIs, Brandwatch, Sprout Social. Breaks: API limits or policy changes cut data collection overnight.

### M2 · NLP in social media analytics (sessions 2–3)

Topics: sentiment analysis; document sentiment classification; sentence subjectivity and sentiment; aspect-based
sentiment analysis; opinion summarisation; opinion spam detection; information extraction; text summarisation;
leveraging GenAI.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Sentiment classification | Label a text positive, negative or neutral. | A thumbs up/down classifier |
| Subjectivity | Whether a sentence states an opinion or a fact. | Opinion vs config value |
| Aspect-based sentiment | Sentiment per feature: "taste great, delivery slow" → taste +, delivery −. | Per-component health checks, not one status |
| Opinion summarisation | Summarise many opinions into pros and cons per aspect. | An incident summary across many alerts |
| Opinion spam | Fake reviews written to promote or damage a product. | Fake stars on a GitHub repo |
| Information extraction | Pull structured facts (names, places, products) out of free text. | Parsing logs into fields |
| LLM zero-shot labelling | Asking an LLM to classify sentiment or aspects without training data. | A generic API instead of custom code |

Diagram ideas: aspect extraction tree for one review; extractive vs abstractive summarisation.
Scenario step: aspect sentiment shows "price" complaints spiking after launch.
Notebook idea: lab 1 style: VADER and a `transformers` sentiment model on reviews; aspect extraction with spaCy noun chunks + sentence sentiment. CPU.
Production angle: multilingual models, Hinglish code-mixing. Breaks: sarcasm ("great, another late delivery") is labelled positive.

### M3 · ML and traditional analytical techniques: graph essentials, network measures, network models (sessions 4–6)

Topics: graph basics; network measures; network models (Zafarani ch. 2–4).

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Degree centrality | Number of connections a user has. | Number of imports of a module |
| Betweenness centrality | How often a node lies on shortest paths between others; marks brokers. | A gateway service all traffic passes |
| Eigenvector centrality / PageRank | A node is important if important nodes link to it. | Being depended on by core libraries |
| Clustering coefficient | How many of a user's friends are friends with each other. | Teams that all review each other's PRs |
| Small-world network | Most nodes reach each other in a few hops despite local clustering. | Six degrees of separation |
| Scale-free / preferential attachment | Few hubs with huge degree; new nodes prefer to link to popular ones. | Popular npm packages get more popular |

Diagram ideas: one graph coloured by each centrality; degree distribution of random vs scale-free models (log-log).
Scenario step: rank BrewBay's followers by centrality to shortlist potential ambassadors.
Notebook idea: lab 3 style: `networkx` measures on a SNAP ego-Facebook graph; generate ER, WS and BA graphs, compare. CPU.
Production angle: graph databases, Spark GraphFrames. Breaks: bot networks inflate centrality of fake accounts.

### M4 · Community and interactions: community detection, evaluation, information diffusion (sessions 7–9)

Topics: member-based detection (degree, reachability, similarity); group-based detection; community evolution; GenAI for
community analysis; Girvan-Newman; brute-force search; community evaluation; data mining essentials; information
diffusion.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Community | A group of nodes more connected inside than to the outside. | A microservice cluster that mostly talks internally |
| Girvan-Newman | Repeatedly remove the highest-betweenness edge until the graph splits into communities. | Cutting the busiest bridges to find islands |
| Modularity | Score for how much denser communities are than a random graph would give. | Cohesion vs coupling metric |
| Community evaluation | Compare found communities with ground truth (purity, NMI) or by modularity. | Comparing clusters with known team labels |
| Information cascade | Users adopt something after seeing neighbours adopt it. | A config rollout spreading through a fleet |
| Independent cascade / threshold model | Spread models: each neighbour gets one chance to activate, or adopt after enough neighbours do. | Retry-once vs quorum rules |

Diagram ideas: Girvan-Newman dendrogram on a 10-node graph; cascade snapshots over time.
Scenario step: find the "fitness", "office coffee" and "students" communities; simulate how the launch post spread.
Notebook idea: lab 4 style: Girvan-Newman and Louvain (`networkx.algorithms.community`) on Karate Club; independent cascade simulation in Python. CPU.
Production angle: Louvain/Leiden at scale. Breaks: communities shift weekly, so last month's segments mislead.

### M5 · Influence and homophily (session 10)

Topics: measuring assortativity; influence; homophily (Zafarani ch. 8).

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Assortativity | Whether nodes connect to similar nodes (by degree or attribute). | Senior devs pairing mostly with senior devs |
| Influence | One user's action causes friends to act. | A tech lead's tool choice spreading to the team |
| Homophily | Similar users choose to connect. | Like-minded devs joining the same Discord |
| Confounding | A shared outside cause makes friends act alike. | Two services failing because of the same DNS outage |
| Shuffle test | Randomise timing or links to check whether influence is real. | Comparing against a random baseline in an A/B test |

Diagram ideas: influence vs homophily vs confounding as three causal arrows; assortativity worked example.
Scenario step: decide whether an influencer actually drives sales or just has similar followers.
Notebook idea: `networkx.attribute_assortativity_coefficient` on a labelled graph; shuffle test on simulated adoption. CPU.
Production angle: causal lift studies for influencer campaigns. Breaks: confusing homophily with influence wastes budget.

### M6 · Recommendation in social media (session 11)

Topics: classical recommendation algorithms; recommendation using social context; evaluating recommendation.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Content-based filtering | Recommend items similar to what the user liked before. | "More like this" |
| Collaborative filtering | Recommend what similar users liked. | Teammates' tool choices |
| Matrix factorisation | Learn user and item vectors whose dot product predicts ratings. | Compressing a sparse table into two dense ones |
| Social regularisation | Push a user's vector toward their friends' vectors. | Defaults inherited from your team |
| MAE / precision@k | Error of predicted ratings / share of top-k recommendations that were relevant. | Accuracy of an estimate vs quality of a shortlist |

Diagram ideas: user-item matrix with missing ratings; trust graph feeding the recommender.
Scenario step: recommend products to followers based on their community's purchases.
Notebook idea: user-based CF and SVD (`scikit-surprise` or numpy) on MovieLens-100k; add a friend term on a synthetic graph. CPU.
Production angle: two-tower models, implicit feedback. Breaks: cold start for new users with no history.

### M7 · Behaviour analytics (session 12)

Topics: individual behaviour; collective behaviour (Zafarani ch. 10).

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Individual behaviour | One user's actions, e.g. linking, posting, buying, churning. | Per-user telemetry |
| Collective behaviour | Patterns of crowds, e.g. trending topics, mass reactions. | Fleet-wide traffic spikes |
| Behaviour prediction | Predict an action (will this user follow, buy, leave) from features and network. | Predicting incidents from metrics |
| Anomaly / bot detection | Spot accounts whose behaviour is unlike humans (timing, volume). | Rate-limit rules for abusive clients |

Diagram ideas: features-to-prediction pipeline for "will user engage"; posting-time histogram, human vs bot.
Scenario step: predict which followers will try the cold brew; filter bots from metrics.
Notebook idea: logistic regression for "will engage" using degree, past activity and community; simple bot heuristic. CPU.
Production angle: trust-and-safety pipelines. Breaks: bots adapt to the detector (adversarial drift).

### M8 · Social media monitoring, strategy and marketing (sessions 13–14)

Topics: monitoring linked to business decisions (Google Analytics); social media strategy; SNA for marketing
strategies; SNA for non-marketing uses; multi-modal analytics (text, audio, video) with GenAI. Also listed under "other
topics": online reviews for customer insights.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Social listening | Continuous tracking of brand mentions, sentiment and share of voice. | Production monitoring for a brand |
| KPI / engagement rate | Business metrics such as interactions per follower or click-through rate. | SLOs for marketing |
| Attribution | Working out which channel or post led to a conversion. | Tracing a request across services |
| Influencer seeding | Choosing a few users to start a campaign so it spreads widely. | Choosing canary hosts for a rollout |
| Multimodal analytics | Using images, audio and video posts as well as text, often with GenAI models. | Parsing screenshots and logs together |

Diagram ideas: monitoring dashboard wireframe; funnel from impression → click → purchase linked to a post.
Scenario step: monthly dashboard tying sentiment and reach to website conversions.
Notebook idea: lab 5 is Google Analytics (web tool, needs an account); offline alternative: a Plotly dashboard from a sample GA export CSV. CPU.
Production angle: GA4, Looker Studio, Sprout Social. Breaks: vanity metrics (likes) rise while sales do not.

### M9 · Ethics in social media (session 15)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Informed consent | Users agree to how their data is used; public posts are not automatic consent. | Terms you actually opted into |
| De-identification | Removing or masking personal identifiers before analysis. | Masking PII in logs |
| Re-identification risk | Combining "anonymous" data with other data to find real people. | Joining two "safe" tables into a leak |
| Algorithmic amplification | Ranking systems boosting harmful or polarising content. | A feedback loop in autoscaling |

Diagram ideas: data lifecycle with ethics checkpoints; re-identification by joining two datasets.
Scenario step: BrewBay's data policy: aggregate only, no profiling of individuals, DPDP Act check.
Notebook idea: hash and generalise user fields; show a simple re-identification join on toy data. CPU.
Production angle: privacy reviews, India DPDP Act, GDPR. Breaks: scraped data violates platform terms.

### M10 · Graph representation learning (session 16)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Node embedding | A learned vector per user so similar users are close. | word2vec for users |
| node2vec | Random walks on the graph fed to word2vec. | Click sessions as sentences |
| GNN (overview) | A network that updates each node from its neighbours' vectors. | Each service pulling status from dependencies |
| Embedding uses | Feed embeddings to classifiers, clustering and recommenders. | A reusable feature library |

Diagram ideas: walks → embeddings → 2-D plot coloured by community.
Scenario step: user embeddings improve product recommendations and community labels.
Notebook idea: node2vec-style walks + gensim Word2Vec on the follower graph; cluster and compare to M4 communities. CPU.
Production angle: PyG, embedding stores. Breaks: embeddings drift as the graph grows; retrain schedule needed.

## 5. Codebase plan

`brewbay-listening`: a local pipeline from raw posts to a dashboard.

```
codebase/
├── README.md                   how to run; which module added which file          (M1)
├── data/fetch_samples.py       public reviews dataset + SNAP graph sample         (M1)
├── src/brewbay/
│   ├── clean.py                dedupe, language filter, bot flags                 (M1, M7)
│   ├── sentiment.py            document + aspect sentiment                         (M2)
│   ├── extract.py              entities and product mentions                       (M2)
│   ├── network.py              centrality and network models                       (M3)
│   ├── communities.py          Girvan-Newman / Louvain + evaluation                (M4)
│   ├── diffusion.py            independent cascade simulation                      (M4, M5)
│   ├── recommend.py            CF + social regularisation                          (M6)
│   ├── embeddings.py           node2vec-style user embeddings                      (M10)
│   └── dashboard.py            Plotly/Streamlit monitoring dashboard               (M8)
└── tests/
    ├── test_sentiment.py       known reviews get expected aspect labels           (M2)
    ├── test_network.py         centrality matches networkx on toy graph           (M3)
    └── test_communities.py     two-clique graph splits correctly                  (M4)
```

## 6. Practice topics plan

1. 01 SMA landscape and data collection — M1 — 2 h
2. 02 Sentiment and aspect-based opinion mining — M2 — 5 h
3. 03 Information extraction and summarisation with GenAI — M2 — 3 h
4. 04 Network measures and network models — M3 — 4 h
5. 05 Community detection — M4 — 4 h
6. 06 Information diffusion, influence and homophily — M4, M5 — 4 h
7. 07 Social recommendation — M6 — 3 h
8. 08 Behaviour analytics and monitoring dashboard — M7, M8 — 3 h
9. 09 Ethics and graph representation learning — M9, M10 — 3 h

## 7. Exam signal

No past question papers in this folder. Evaluation scheme (older handout):

| Component | Type | Weight | Date (that batch) |
|---|---|---|---|
| EC-1 Quiz (optional per note) | Online | 10% | TBA |
| EC-1 Assignment / lab assignments | Online | 20% | TBA |
| EC-2 Mid-Semester Test | Closed book, 2 h | 30% | 20-06-2026 (AN) |
| EC-3 Comprehensive Exam | Open book, 2.5 h | 40% | 05-09-2026 (AN) |

Note in handout: EC-1 can be 20–30% (quiz 5–10%, assignments 20–30%). Mid-sem = sessions 1–8 (M1–M4 up to
Girvan-Newman), closed book: expect hand calculation of centralities, clustering coefficient, Girvan-Newman steps and
modularity on small graphs (session 8 has a Girvan-Newman and brute-force demo).

## 8. Interview angle

1. **How would you build aspect-based sentiment?** Extract aspects (noun phrases or a tagger), then classify sentiment per aspect sentence or with an LLM.
2. **Betweenness vs degree centrality?** Degree counts connections; betweenness finds brokers on many shortest paths.
3. **How does Girvan-Newman work and why is it slow?** Remove the highest-betweenness edge repeatedly; recomputing betweenness each time is expensive.
4. **What is modularity?** How much denser communities are internally than expected in a random graph.
5. **Homophily vs influence?** Similar people connect vs people change because of connections; test with shuffle or causal methods.
6. **How do you handle sarcasm and code-mixed text?** Domain fine-tuned or multilingual models, plus human-labelled evaluation.
7. **How would you detect bots?** Posting rate, timing regularity, account age, network patterns, then a classifier.
8. **How would you measure a campaign's impact?** Reach and sentiment, plus attribution to conversions with a control group.
9. **What ethics issues matter?** Consent, re-identification, bias in sampling, platform terms, data protection law.

## 9. Repetition plan

| Concept | First met (module) | Revisited in (modules) |
|---|---|---|
| Sampling bias / noise | M1 | M2, M7, M9 |
| Sentiment | M2 | M8 (dashboard), M7 (behaviour) |
| Centrality | M3 | M4 (betweenness in Girvan-Newman), M8 (influencer seeding) |
| Community | M4 | M6 (social context), M10 (embeddings) |
| Diffusion | M4 | M5 (influence), M8 (campaign spread) |
| Homophily | M5 | M6 (social regularisation), M10 |
| Privacy / consent | M1 | M9 |

## 10. Overlap with my other courses

- [../../natural-language-processing/](../../natural-language-processing/) — sentiment, TF-IDF and embeddings behind M2.
- [../../nlp-applications/](../../nlp-applications/) — summarisation and information extraction (its practice/02 extractive summarisation) overlap with M2.
- [../../llm-engineering/](../../llm-engineering/) — "leveraging GenAI" for labelling and summarisation in M2, M4, M8.
- [../graph-neural-networks/](../graph-neural-networks/) — network measures, homophily and graph representation learning (M3–M5, M10) in more depth.

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1…M10, 5–7 cards each)
- [ ] practice/01 SMA landscape and data collection
- [ ] practice/02 Sentiment and aspect-based opinion mining
- [ ] practice/03 Information extraction and summarisation with GenAI
- [ ] practice/04 Network measures and network models
- [ ] practice/05 Community detection
- [ ] practice/06 Information diffusion, influence and homophily
- [ ] practice/07 Social recommendation
- [ ] practice/08 Behaviour analytics and monitoring dashboard
- [ ] practice/09 Ethics and graph representation learning
- [ ] codebase/ runs + tests

Total estimated study hours: ≈ 31 h practice + ≈ 8 h codebase + ≈ 4 h cards/revision = **≈ 43 h**.
