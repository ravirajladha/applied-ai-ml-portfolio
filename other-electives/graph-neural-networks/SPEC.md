# Graph Neural Networks (AIML ZG514) — Study spec

> Machine learning on connected data: users, payments, molecules, knowledge graphs, from graph features to GCN, GraphSAGE and GAT. · Status: spec only (not built yet)

## 1. What it is and why an AI engineer should care

A graph is data made of nodes (things) and edges (links between them): users and payments, products and purchases,
atoms and bonds. Normal ML treats each row as independent; graph ML uses the links too, because who you are connected
to says a lot about you. This course goes from hand-made graph features and random-walk embeddings to graph neural
networks (GNNs), which learn by passing messages along edges, then to knowledge graphs, graph generation, applications
(recommendation, link prediction, drug discovery) and scaling to huge graphs. Fraud detection and recommendations at
large companies use exactly these ideas.

**Job relevance: 3/5** — valuable in fraud, recommendations and knowledge graphs at larger companies, but few roles are GNN-first.

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (older batch) | `handouts/Older batch - AIML_ZG514  Graph Neural Networks-revised.pdf` | v4.0, 15/04/2026, Second Semester 2025-2026, author Ashwin Ganesan; 16 modules = 16 sessions; textbook Hamilton "Graph Representation Learning" (GRL) |

Gaps: no current handout, no slides, no past papers, no lab sheets. Handout lists 4 case-study webinars and 2 assignments;
tools named: Jupyter, Neo4j, NetworkX, PyTorch. Stanford CS224W slides are the named public reference.

## 3. Running scenario

**PayGraph** is a UPI wallet with 30 million users and 2 million merchants. Every payment is an edge from a user to
a merchant or another user; users also share devices and phone numbers. Fraud rings create clusters of fake accounts
that look normal one by one. The data: a transactions table, a device-sharing table, a merchant catalogue with
categories and a few thousand confirmed fraud labels. The goals: flag fraud accounts (node classification), suggest
merchants a user will like (link prediction), and answer "which merchants belong to the same owner?" using a
knowledge graph. Each module adds one piece of the PayGraph risk-and-recs platform.

## 4. Module map

Each module is one session in the handout. Contact hours per module: not stated.

### M1 · Introduction and ML tasks on graphs (session 1)

Topics: simple, directed, weighted, multi-relational, heterogeneous graphs; node features; tasks: node classification,
relation prediction, graph classification, clustering; permutation invariance.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Adjacency matrix | An N x N table with 1 where an edge connects node i to node j. | A friends table as a matrix |
| Heterogeneous graph | Nodes and edges of several types (user, merchant; pays, shares-device). | A schema with many tables and foreign keys |
| Node / link / graph task | Predict a label per node, whether an edge exists, or a label for a whole graph. | Row-level, join-level and table-level predictions |
| Permutation invariance | The answer must not change if you renumber the nodes. | A query result that ignores row order |

Diagram ideas: PayGraph schema as a heterogeneous graph; one graph shown with two node orderings and the same output.
Scenario step: model PayGraph data as a graph; define the fraud task as node classification.
Notebook idea: build a small PayGraph sample in `networkx`, adjacency matrix with numpy, check permutation behaviour. CPU.
Production angle: Neo4j, TigerGraph, graph tables in Spark. Breaks: graph snapshot built after the label date leaks future edges.

### M2 · Traditional feature engineering for graphs (session 2)

Topics: degree, centrality, clustering coefficient, graphlets; link features: common neighbours, Jaccard, Katz index;
graph-level features and kernels; Weisfeiler-Lehman (WL) kernel.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Degree / centrality | How connected or how "in the middle" a node is (betweenness, eigenvector, PageRank). | Most-imported module in a codebase |
| Clustering coefficient | Share of a node's neighbours that are also connected to each other. | Do your teammates also work together |
| Jaccard / common neighbours | Overlap of two nodes' neighbour sets, used to guess missing links. | "People you may know" |
| Katz index | Counts all paths between two nodes, shorter paths weighted more. | Indirect dependencies, discounted by depth |
| WL kernel | Compares graphs by repeatedly relabelling nodes with their neighbours' labels and counting labels. | Hashing a subtree to compare structures |

Diagram ideas: a node with high betweenness bridging two clusters; Jaccard worked example for two users.
Scenario step: degree, shared-device count and clustering coefficient become fraud features for a gradient-boosted baseline.
Notebook idea: `networkx` features on a synthetic fraud graph + `sklearn` GradientBoosting baseline, AUC. CPU.
Production angle: features stored in a feature store, recomputed nightly. Breaks: centrality on a 30 M-node graph is too slow without approximation.

### M3 · Graph Laplacians and spectral methods (session 3)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Graph Laplacian L = D - A | Degree matrix minus adjacency; measures how much a signal differs across edges. | A "difference from neighbours" operator |
| Eigenvectors of L | Smooth-to-wiggly patterns over the graph, like frequencies for a signal. | Fourier modes, but on a network |
| Spectral clustering | Cluster nodes using the first few Laplacian eigenvectors. | Grouping services by how they talk |
| Normalised Laplacian | Laplacian scaled by degrees so hubs do not dominate. | Per-capita instead of totals |

Diagram ideas: Laplacian built from a 5-node graph; Fiedler vector colouring that splits the graph in two.
Scenario step: spectral clustering on device-sharing graph reveals a tight group of accounts.
Notebook idea: compute L with numpy, eigenvectors, compare spectral clustering to `sklearn.cluster.SpectralClustering`. CPU.
Production angle: rarely run at full scale; used on subgraphs. Breaks: eigendecomposition is O(N³) and does not scale.

### M4 · Node embeddings (session 4)

Topics: encoder-decoder framework; random-walk embeddings (DeepWalk, node2vec); limits of shallow embeddings.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Node embedding | A learned vector per node so that related nodes have similar vectors. | word2vec, but for nodes |
| Encoder-decoder | Encoder maps nodes to vectors; decoder scores node pairs from vectors. | Serialise, then compare |
| DeepWalk / node2vec | Generate random walks, treat them as sentences, train word2vec on them. | Clickstream sessions as sentences |
| Shallow embedding limit | One lookup vector per node: cannot embed new nodes and ignores features. | A cache that misses every new key |

Diagram ideas: random walks turned into "sentences"; node2vec p/q bias (BFS-like vs DFS-like).
Scenario step: merchant embeddings for "similar merchants".
Notebook idea: random walks in Python + `gensim` Word2Vec on the Karate Club graph; plot embeddings. CPU.
Production angle: PyTorch-BigGraph style embedding tables. Breaks: new users have no embedding (cold start).

### M5 · Message passing and node classification, pre-neural (session 5)

Topics: semi-supervised node classification; homophily and influence; relational and iterative classification.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Homophily | Connected nodes tend to share labels. | Fraudsters transact with fraudsters |
| Label propagation | Spread known labels to neighbours repeatedly until stable. | Rumour spreading through a team |
| Iterative classification | Classify nodes, add neighbours' predicted labels as features, repeat. | Re-running a build until outputs stop changing |
| Relational classification | Predict a node's label from a weighted vote of its neighbours' labels. | Judging a service by the health of its dependencies |

Diagram ideas: labels spreading over 3 iterations; homophily vs heterophily graphs.
Scenario step: from 3,000 known fraud labels, propagate risk scores to unlabelled accounts.
Notebook idea: label propagation in numpy on a synthetic graph; compare with `sklearn` LabelSpreading. CPU.
Production angle: risk-score propagation jobs. Breaks: fraudsters connect to good users on purpose (heterophily), so propagation fails.

### M6 · The graph neural network model (session 6)

Topics: neural message passing; computation graphs; neighbourhood aggregation; the aggregate-combine framework.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Message passing | Each node collects messages from neighbours, aggregates them and updates its own vector. | Each service pulls status from its dependencies |
| Aggregate (sum/mean/max) | A permutation-invariant function that combines neighbour messages. | `reduce` over neighbour list |
| Combine / update | Mix the aggregated message with the node's own vector through a small neural layer. | Merging upstream config with local overrides |
| Layers = hops | k GNN layers let a node see k hops away. | Transitive dependencies to depth k |

Diagram ideas: computation tree of a node for 2 layers; aggregate-combine equation drawn as boxes.
Scenario step: each account's vector now includes its counterparties' behaviour.
Notebook idea: one message-passing layer written in plain torch with the adjacency matrix; check permutation equivariance with an assert. CPU.
Production angle: PyTorch Geometric, DGL. Breaks: very high-degree hub nodes (big merchants) dominate aggregation.

### M7 · GNN architectures: GCN, GraphSAGE, GAT (session 7)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| GCN | Averages neighbour features with degree normalisation, then applies a shared linear layer. | A normalised moving average over neighbours |
| GraphSAGE | Samples a fixed number of neighbours and aggregates; works for unseen nodes (inductive). | Sampling logs instead of reading all |
| GAT | Learns attention weights so important neighbours count more. | Weighted voting by trust |
| Inductive vs transductive | Works on new nodes without retraining vs only on nodes seen during training. | Generic function vs memorised lookup |

Diagram ideas: the three aggregations compared on one node; GAT attention weights as edge thickness.
Scenario step: train GraphSAGE so new accounts get fraud scores without retraining.
Notebook idea: GCN, GraphSAGE, GAT with PyTorch Geometric on Cora (CPU, seconds); accuracy table. CPU.
Production angle: PyG / DGL in batch scoring. Breaks: transductive GCN cannot score accounts created after training.

### M8 · GNNs in practice: pooling, training and evaluation (session 8)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Graph pooling (readout) | Combine all node vectors into one graph vector (sum, mean, hierarchical). | Aggregating rows into one summary row |
| Over-smoothing | With many layers, all node vectors become alike. | Everyone averaging opinions until all agree |
| Transductive vs inductive split | How train/val/test nodes or edges are separated in one graph. | Splitting time-series data without leakage |
| Negative sampling for links | Train link prediction with random non-edges as negatives. | Generating "should not match" test cases |

Diagram ideas: over-smoothing curve (accuracy vs number of layers); edge split train/val/test with message vs supervision edges.
Scenario step: honest evaluation with a time-based split (train on January, test on February).
Notebook idea: accuracy vs layers (1–8) for GCN on Cora; time-split leakage demo on synthetic edges. CPU.
Production angle: offline AUC + precision at the review-team capacity. Breaks: random edge splits leak, offline AUC looks great, production fails.

### M9 · Spectral theory of GNNs (session 9)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Graph Fourier transform | Express a node signal in Laplacian eigenvectors. | FFT for graph data |
| Spectral filter | Scale each graph frequency: low-pass keeps smooth patterns. | An audio equaliser for networks |
| ChebNet / GCN link | GCN is a cheap first-order approximation of a spectral low-pass filter. | A fast approximation of an expensive formula |
| Smoothness | A signal is smooth when connected nodes have similar values (low Laplacian quadratic form). | Neighbouring config values that rarely disagree |

Diagram ideas: signal on graph before/after low-pass filtering; derivation path spectral conv → Chebyshev → GCN.
Scenario step: explains why GCN smooths risk scores across neighbours.
Notebook idea: low-pass filter a noisy node signal with Laplacian eigenvectors; compare with repeated GCN-style averaging. CPU.
Production angle: mostly theory; spatial GNNs used in practice. Breaks: spectral filters do not transfer between different graphs.

### M10 · Expressive power of GNNs and the WL test (session 10)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Graph isomorphism | Two graphs are the same structure with nodes relabelled. | Same schema, different column names |
| WL test | Repeated neighbour-label hashing; different final label counts prove graphs differ. | Comparing Merkle-tree hashes |
| Expressive power | Message-passing GNNs can tell apart at most what the 1-WL test can. | A hash with known collisions |
| GIN | A GNN using sum aggregation plus an MLP, as powerful as 1-WL. | Choosing a hash that preserves counts |

Diagram ideas: two non-isomorphic graphs WL cannot separate; mean vs max vs sum failing cases.
Scenario step: sum aggregation distinguishes "10 small payments" from "1 payment" where mean cannot.
Notebook idea: implement 1-WL colour refinement in Python; show mean aggregation collision with an assert. CPU.
Production angle: informs aggregator choice. Breaks: model cannot learn ring shapes it structurally cannot see.

### M11 · Knowledge graph embeddings (session 11)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Knowledge graph | Facts stored as (head, relation, tail) triples. | Rows in a triple store |
| TransE | Embeds so that head + relation ≈ tail. | Vector arithmetic: Paris - France + India ≈ Delhi |
| Bilinear models (DistMult, RESCAL, ComplEx) | Score a triple with a relation-specific matrix product. | A learned join condition per relation |
| Link completion | Predict missing triples (e.g. which owner a merchant belongs to). | Inferring a missing foreign key |

Diagram ideas: TransE translation vectors in 2-D; relation patterns (symmetric, inverse, composition) vs model capability.
Scenario step: merchant-owner-bank-account triples; predict hidden ownership links.
Notebook idea: TransE in plain torch on a toy KG of 200 triples; hits@10 metric. CPU (PyKEEN optional).
Production angle: Neo4j, Wikidata-style KGs, PyKEEN. Breaks: KG has stale facts and no timestamps.

### M12 · Knowledge graph reasoning and heterogeneous GNNs (session 12)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| R-GCN | A GCN with separate weights per relation type. | A different handler per event type |
| Heterogeneous GNN | Message passing with type-specific transforms for nodes and edges. | Polymorphic dispatch over node types |
| Multi-hop reasoning | Answering by following several relations in sequence. | Chained joins |
| Basis decomposition | Share a few weight matrices across many relation types to avoid too many parameters. | Shared base classes instead of copy-paste |

Diagram ideas: R-GCN message from "pays" vs "shares-device" edges; a 2-hop query path.
Scenario step: one model uses payment, device and ownership edges together.
Notebook idea: PyG `HeteroData` with users, merchants, devices; `to_hetero` GraphSAGE. CPU.
Production angle: PyG hetero, DGL. Breaks: one rare relation type gets too few examples to learn its weights.

### M13 · Graph generation models (session 13)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Erdős–Rényi / preferential attachment | Classic random graph models: uniform edges / rich-get-richer. | Random load vs viral growth |
| Graph VAE | Encode a graph to a latent vector and decode an adjacency matrix. | Compress and regenerate a schema |
| Autoregressive generation (GraphRNN) | Build a graph one node and edge at a time. | Writing a file line by line |
| Generation evaluation | Compare degree, clustering and motif statistics of generated vs real graphs. | Comparing load-test traffic with production traffic |

Diagram ideas: degree distributions of ER vs Barabási–Albert; graph VAE encoder/decoder.
Scenario step: generate synthetic transaction graphs to test fraud models without real user data.
Notebook idea: `networkx` ER and BA graphs, compare degree histograms; tiny graph auto-encoder in torch. CPU.
Production angle: synthetic data for testing. Breaks: synthetic graphs miss the structure of real fraud rings.

### M14 · GNN applications: recommendation, link prediction, drug discovery (session 14)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Bipartite user-item graph | Users on one side, items on the other, edges are interactions. | A many-to-many join table |
| LightGCN / PinSage-style recsys | GNN embeddings of users and items; recommend by vector similarity. | Collaborative filtering with message passing |
| Link prediction pipeline | Embed nodes, score candidate pairs, rank. | Candidate generation then ranking |
| Molecular graph | Atoms as nodes, bonds as edges; predict properties per graph. | A graph-classification task |

Diagram ideas: two-tower vs GNN recsys; molecule as graph with a readout to "toxic / not".
Scenario step: recommend merchants and offers from the payment graph.
Notebook idea: LightGCN-style propagation on MovieLens-100k (small, CPU), recall@20. CPU.
Production angle: candidate generation in recommender stacks, RDKit + PyG for chemistry. Breaks: popularity bias, only big merchants get recommended.

### M15 · Scaling GNNs to large graphs (session 15)

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Mini-batching on graphs | Train on small node sets with their sampled neighbourhoods, not the whole graph. | Pagination for training |
| Neighbourhood sampling | Take at most k neighbours per hop (GraphSAGE). | Sampling logs at a fixed rate |
| Subgraph sampling (Cluster-GCN, GraphSAINT) | Train on dense clusters or sampled subgraphs. | Testing one microservice cluster at a time |
| Neighbour explosion | k layers touch degree^k nodes; memory explodes. | Transitive dependency hell |

Diagram ideas: neighbour explosion tree vs sampled tree; graph partitioned into clusters.
Scenario step: train on the full 30 M-user graph within a single machine's memory.
Notebook idea: PyG `NeighborLoader` on ogbn-arxiv or a synthetic 1 M-edge graph; memory and time vs fan-out. CPU.
Production angle: PyG + DGL distributed, GraphStorm. Breaks: online scoring needs fresh neighbours; stale graph snapshots miss new fraud.

### M16 · Advanced topics and research frontiers (session 16)

Handout gives only the title; the course description names graph transformers and self-supervised learning on graphs.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Graph transformer | Attention over all nodes plus positional encodings of graph structure. | Full mesh instead of only neighbours |
| Self-supervised graph learning | Learn node vectors from the graph itself (contrast views, mask features) without labels. | Pretraining on unlabelled logs |
| Positional encoding (graphs) | Extra node features (e.g. Laplacian eigenvectors) telling attention where a node sits. | Row numbers for unordered data |
| Graph foundation model | One model pretrained on many graphs, adapted to new tasks (an open research question). | A shared platform library across teams |

Diagram ideas: message passing vs global attention; contrastive views of the same graph.
Scenario step: pretrain on the unlabelled payment graph, fine-tune on scarce fraud labels.
Notebook idea: reading + a small contrastive pretraining demo (DGI in PyG) on Cora. CPU.
Production angle: early adoption. Breaks: quadratic attention cost on large graphs.

## 5. Codebase plan

`paygraph-ml`: a laptop-scale fraud and recommendation lab on synthetic data.

```
codebase/
├── README.md                    how to run; which module added which file            (M1)
├── data/make_paygraph.py        synthetic users, merchants, devices, fraud rings      (M1, M13)
├── src/paygraph/
│   ├── features.py              degree, centrality, Jaccard, clustering coeff         (M2)
│   ├── spectral.py              Laplacian + spectral clustering                       (M3)
│   ├── node2vec.py              random walks + word2vec embeddings                    (M4)
│   ├── propagate.py             label propagation baseline                            (M5)
│   ├── gnn.py                   message-passing layer, GCN, SAGE, GAT                 (M6, M7)
│   ├── train.py                 time-split training + evaluation                       (M8, M15)
│   ├── kg.py                    TransE on merchant ownership triples                  (M11)
│   ├── hetero.py                heterogeneous GNN                                      (M12)
│   └── recsys.py                LightGCN merchant recommendations                     (M14)
└── tests/
    ├── test_features.py         features match networkx                              (M2)
    ├── test_gnn.py              permutation equivariance                             (M6)
    ├── test_split.py            no future edges in training                          (M8)
    └── test_kg.py               TransE hits@10 above random                          (M11)
```

## 6. Practice topics plan

1. 01 Graphs, tasks and classic features — M1, M2 — 4 h
2. 02 Laplacians and spectral clustering — M3, M9 — 4 h
3. 03 Node embeddings with random walks — M4 — 3 h
4. 04 Label propagation and homophily — M5 — 2 h
5. 05 Message passing from scratch — M6, M10 — 4 h
6. 06 GCN, GraphSAGE, GAT in practice — M7, M8 — 5 h
7. 07 Knowledge graphs and heterogeneous GNNs — M11, M12 — 5 h
8. 08 Graph generation — M13 — 2 h
9. 09 GNN recommendations and link prediction — M14 — 4 h
10. 10 Scaling GNNs — M15, M16 — 3 h

## 7. Exam signal

No past question papers in this folder. Evaluation scheme (older handout):

| Component | Type | Weight |
|---|---|---|
| EC-1 Quiz I + Quiz II (15 min each) | Online | 15% |
| EC-1 Assignment I + II (15 days each) | Online submission | 15% |
| EC-2 Mid-Semester Test | Closed book, 2 h | 30% |
| EC-3 Comprehensive Exam | Open book, 3 h | 40% |

Mid-sem = sessions 1–8 (M1–M8), closed book: expect hand computations (degree, clustering coefficient, Jaccard, Katz,
Laplacian, one GCN layer on a tiny graph, WL iterations).

## 8. Interview angle

1. **Why use a GNN over XGBoost on tabular features?** When relationships carry signal (fraud rings, social influence) that per-row features miss.
2. **How does message passing work?** Each layer aggregates neighbour vectors with a permutation-invariant function and updates the node.
3. **GCN vs GraphSAGE vs GAT?** Normalised mean / sampled aggregation for unseen nodes / learned attention weights per neighbour.
4. **What is over-smoothing?** Deep GNNs make all node vectors similar; use few layers, residuals or jumping knowledge.
5. **Transductive vs inductive?** Transductive only scores nodes seen in training; inductive generalises to new nodes.
6. **How do you scale GNN training?** Neighbour sampling, subgraph/cluster sampling, mini-batches, distributed feature stores.
7. **How do you evaluate link prediction honestly?** Time-based splits, held-out edges hidden from message passing, ranked metrics like hits@k.
8. **What is TransE?** KG embedding where head + relation ≈ tail; fails on one-to-many and symmetric relations.
9. **What limits GNN expressiveness?** Message-passing GNNs are at most as powerful as the 1-WL isomorphism test.
10. **How would you detect a fraud ring?** Device/payment graph, community features and a GNN trained on known fraud, plus analyst review.

## 9. Repetition plan

| Concept | First met (module) | Revisited in (modules) |
|---|---|---|
| Adjacency matrix | M1 | M3, M6, M9 |
| Permutation invariance | M1 | M6, M8 (pooling), M10 |
| Homophily | M5 | M6, M7, M14 |
| Laplacian | M3 | M9 |
| WL relabelling | M2 | M10 |
| Embedding + similarity | M4 | M11, M14 |
| Neighbourhood aggregation | M6 | M7, M12, M15 |
| Leak-free evaluation split | M8 | M14, M15 |

## 10. Overlap with my other courses

- [../../natural-language-processing/](../../natural-language-processing/) — word2vec (revision ch03) is reused directly by DeepWalk/node2vec in M4.
- [../social-media-analytics/](../social-media-analytics/) — network measures, communities, homophily and graph representation learning overlap with M1–M5.
- [../mlops/](../mlops/) — serving and monitoring graph features and scores.

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1…M16, 5–6 cards each)
- [ ] practice/01 Graphs, tasks and classic features
- [ ] practice/02 Laplacians and spectral clustering
- [ ] practice/03 Node embeddings with random walks
- [ ] practice/04 Label propagation and homophily
- [ ] practice/05 Message passing from scratch
- [ ] practice/06 GCN, GraphSAGE, GAT in practice
- [ ] practice/07 Knowledge graphs and heterogeneous GNNs
- [ ] practice/08 Graph generation
- [ ] practice/09 GNN recommendations and link prediction
- [ ] practice/10 Scaling GNNs
- [ ] codebase/ runs + tests

Total estimated study hours: ≈ 36 h practice + ≈ 10 h codebase + ≈ 5 h cards/revision = **≈ 51 h**.
