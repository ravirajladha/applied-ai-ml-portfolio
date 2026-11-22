# AI and ML for Robotics (AIML ZG528) — Study spec

> How a mobile robot works out where it is, builds a map, plans a route and talks to people, and where ML replaces hand-written parts of that loop. · Status: spec only (not built yet)

---

## 1. What it is and why an AI engineer should care

A mobile robot is a loop: **sense → estimate state → plan → act**, repeated many times a second, with noisy sensors and wheels that slip.
This course teaches the probabilistic toolkit that keeps that loop honest (Bayes filters, particle filters, occupancy grids, SLAM), the classic planners (A*, RRT*, PRM, swarm methods), and then shows where ML slots in: learned motion models, denoising sensor data, CNN-based visual SLAM, deep RL for path planning, gesture and LLM-based human-robot interaction.
The slides state clearly that hardware, mechanics, dynamics and kinematics are **not** part of the course: the focus is ML/DL applied to rigid-body mobile robots (`lecture-slides/AIMLRO-CS-1-24Oct2026-NSP2.pdf`).
For a software engineer the big transferable idea is **state estimation under uncertainty**, which is the same mental model as tracking a noisy metric, fusing signals from several services, or ranking hypotheses.

**Job relevance: 3/5** — robotics/autonomy roles are fewer than LLM or MLOps roles, but Kalman/particle filters, sensor fusion and RL show up in autonomy, drones, warehouse automation, AR and even fraud/tracking systems.

---

## 2. Sources in this folder

| Kind | File (relative path) | Notes |
|---|---|---|
| Handout (current) | `handouts/Handout - Robotics - 12-Nov-2025.pdf` | v3.0, 6 modules, 16 contact sessions (CS), 7 labs, evaluation scheme |
| Slides | `lecture-slides/AIMLRO-CS-1-24Oct2026-NSP2.pdf` | M1 intro, course logistics (EC1: 1 quiz 5% + 2 assignments 25%; EC3 35%) |
| Slides | `lecture-slides/Robotics M2 CS 2 To Students 31st Oct 2026.pdf` | M2 part 1: motion + perception, warehouse-robot story, proprioceptive vs exteroceptive sensors, odometry |
| Slides (code) | `lecture-slides/Quarky-MarsRover-BlockProgramming.sb3` | Scratch-style block program, not extractable; demo only |
| Past paper | `past-question-papers/Robotics - Jun 2026 - Midsem Regular Set 1.docx` | Questions are images (airport service robot scenario); read from embedded images |
| Past paper | `past-question-papers/Robotics - Jun 2026 - Midsem Regular Set 2.docx` | Same mark pattern as Set 1; images not inspected |
| Past paper | `past-question-papers/Robotics - Sep 2026 - Endsem Regular Set 1.doc` | Rescue robot in collapsed mall: FastSLAM, ACO, GA, DRL reward, RRT*, technique pairs |
| Past paper | `past-question-papers/Robotics - Sep 2026 - Endsem Regular Set 2.doc` | Symmetric office floor: same question types with different numbers |
| Lab manual | `labware/Lab Manual -2 with Practice Sheet for Sensor and Motion Modelling in ROS2.pdf` | Webinar 1: odometry-based motion control for obstacle avoidance in ROS2 + RViz (ROS2 "jazzy") |
| Lab notebook | `labware/Lab_sheet_1-Getting_Started_with_Robotics_Framework_Pipeline.ipynb` | MuJoCo / PyBullet state space, action space, controllable joints |
| Lab notebooks | `labware/Lab_sheet_3(a)-AIMLTechniques_for_Motion_Modelling.ipynb`, `labware/Lab_sheet_3(b)-AIMLTechniques_for_Sensor_Modelling.ipynb` | Learn motion model with linear regression vs MLP vs PPO (MuJoCo, T4 GPU on Colab) |
| Lab notebook | `labware/Lab_sheet_4-AIMLTechniques_for_Localization.ipynb` | 4 use cases: denoising autoencoder, Q-learning for grid resolution, random forest particle weights, bandit for resampling threshold |
| Lab notebook | `labware/Lab_sheet_4-CNN_for_VisualSLAM.ipynb` | CNN for visual SLAM |
| Lab notebooks | `labware/Lab_sheet_6(a)_Sampling_based_for_PathPlanning_.ipynb`, `labware/Lab_sheet_6(b)_Evolutionary_Algorithm_for_PathPlanning_.ipynb` | PRM-style roadmap + evolutionary planner in PyBullet |
| Lab notebook | `labware/Lab_sheet_7-Deep_Reinforcement_Learning_for_Path_Planning.ipynb` | Custom PyBullet env, 4-D state, continuous 2-D action, DRL policy |
| Practice sheets | `labware/Practice sheet 1/3/4/6/7 - ....pdf` | One-page practice questions matching each lab notebook |
| Other | `StudentList-Oct2026-EmailIDs-AIMLRobotics.pdf` | Not study material; ignore |

**Gaps:** slides only for M1 and the start of M2 (nothing for Localization onwards); no lab 2 or lab 5 practice sheet; midsem Set 2 not read; no textbook PDFs (Thrun "Probabilistic Robotics" is the main text). Older handout: none.

---

## 3. Running scenario

**ShelfSense Logistics** runs a 40,000 m² warehouse in Bengaluru with a fleet of small wheeled **pick-assist robots** ("Shelfies") that carry totes between racks and packing stations. Each Shelfie has wheel encoders, an IMU, a 2D LiDAR and a front camera, and starts each shift at its charging dock with a floor map that is already out of date (pallets move, aisles get blocked, workers walk through).
The goal is a software stack that lets each robot **know where it is, keep the map fresh, plan a safe fast route, and respond to a worker's hand gesture or spoken request** ("bring tote 14 to station B").
The data is simulated in Python (a 2D grid world with LiDAR ray-casting and noisy odometry), mirroring the course's own warehouse-robot story in the M2 slides.
Every module adds one capability to the same Shelfie.

---

## 4. Module map

### M1 · Introduction (≈ CS 1)

Topics: evolution of robotics; types of robots (aerial, warehouse, under-actuated, mobile, industrial, field, service); overview of modelling, planning, control; applications and challenges; why robotics is probabilistic.

| Concept | One-line definition (≤20 words, no jargon) | Analogy |
|---|---|---|
| Mobile robot | A machine that moves through a space by itself and must decide where to go | A delivery driver without a GPS app |
| Sense–plan–act loop | Read sensors, decide, move, then repeat many times per second | A game loop: input, update, render |
| Uncertainty | The robot never knows its exact position or the exact world; it only has estimates | Logs from a flaky service: true state is hidden |
| Probabilistic robotics | Represent "where am I" as a probability spread, not one fixed answer | A search ranking: many candidates, each with a score |
| Under-actuated robot | A robot with fewer motors than directions it can move in | Steering a car: you can't slide sideways |

Diagram ideas:
- The sense → estimate → plan → act loop drawn as a CI pipeline with a feedback arrow.
- Robot taxonomy tree (aerial / ground / warehouse / service) with one real product per leaf.

Scenario step: ShelfSense decides what a Shelfie must do on day one and lists what can go wrong (slip, occlusion, moved pallets).
Notebook idea: simulate a robot driving straight with 2% wheel slip in numpy; plot true vs believed path over 100 steps to *see* drift. Laptop, no GPU.
Production angle: AMRs from Locus, GreyOrange, Amazon Robotics run ROS/ROS2-style stacks. **Breaks:** a robot trusts odometry alone and slowly drifts into a rack.

### M2 · Components of Programmable Robotic System (≈ CS 2–4)

Topics: robot motion (probabilistic kinematics, motion models); robot perception (actuators, sensors, proprioceptive vs exteroceptive); maps (feature-based vs location-based), range sensors, beam models, likelihood fields, map matching; measurement models (correlation-based vs feature-based); control architecture, functional architecture, programming environment (ROS2).

| Concept | One-line definition | Analogy |
|---|---|---|
| Proprioceptive sensor | Measures the robot's own body: wheel turns, acceleration, heading | Your phone's step counter |
| Exteroceptive sensor | Measures the outside world: LiDAR, camera, sonar | Looking out the window |
| Odometry | Estimating distance and turn travelled from wheel/IMU readings; errors pile up | Dead reckoning on a ship |
| Motion model p(x′ given x, u) | Probability of the new pose given the old pose and the command sent | "I sent a request; here's how likely each response is" |
| Beam model | Scores a LiDAR reading as a mix of: correct hit, short obstacle, max-range miss, random noise | Retry logic that expects timeouts, errors and real replies |
| Likelihood field (endpoint model) | Scores a LiDAR reading only by how close each beam endpoint lies to a mapped wall | Fuzzy string match against a dictionary |
| Feature vs location map | List of landmarks with positions vs a grid saying what is in every cell | Key-value store of points vs a full bitmap |
| ROS2 node / topic | A small process, and the named message channel it publishes or subscribes to | Microservices talking over a message queue (Kafka topic) |

Diagram ideas:
- Beam model: four coloured curves (hit Gaussian, short exponential, max spike, random uniform) summed into one mixture.
- ROS2 graph: `/scan`, `/odom`, `/cmd_vel` topics between lidar, localizer, planner and motor nodes.
- Side-by-side feature map (dots) vs occupancy grid (pixels) of the same warehouse aisle.

Scenario step: Shelfie gets its sensor models: how much to trust wheel encoders and how to score a LiDAR scan against the map.
Notebook idea: implement the beam model mixture for one beam and compute p(z | x) for the midsem-style table (z = 11 m vs expected 10 m; z = max range), then train an MLP to predict state delta from (state, action) like Lab 3(a). numpy + sklearn, laptop.
Production angle: ROS2 + Nav2, Gazebo/RViz, MuJoCo/PyBullet for sim. **Breaks:** shiny floors or glass make LiDAR return max-range; a beam model without the max-range term rejects the true pose.

### M3 · Localization (≈ CS 5–7)

Topics: taxonomy of localization problems (local/global, kidnapped, static/dynamic, passive/active); Markov localization; grid localization; Monte Carlo localization; ML for localization using fiducial markers; GPS-based, odometry-based, sensor-fusion-based techniques; deep learning for odometric learning; DL-based multi-sensor fusion.

| Concept | One-line definition | Analogy |
|---|---|---|
| Bayes filter | Repeat: predict with the motion model, then correct with the sensor reading | Forecast, then update after seeing the actual weather |
| Markov localization | Bayes filter over all possible poses, assuming the past only matters through the current belief | A cache: only the latest state is kept |
| Particle filter / MCL | Track many guessed poses ("particles"), weight by sensor fit, resample the good ones | A/B testing many hypotheses, keeping the winners |
| Resampling | Draw a new particle set, copying high-weight particles and dropping low-weight ones | Autoscaling: kill idle pods, clone busy ones |
| Kidnapped robot problem | The robot is moved without knowing it, so its confident belief is wrong | A session token pointing at the wrong user |
| Augmented MCL (AMCL-style recovery) | Inject random particles when sensor fit drops, so the filter can recover from kidnapping | A health check that triggers a cold restart |
| Data association | Deciding which mapped landmark an observation belongs to | Matching log lines to the right request ID |
| Sensor fusion | Combine several noisy sensors so the estimate is better than any single one | Combining multiple monitoring signals into one alert |

Diagram ideas:
- Particle cloud across 4 identical gates collapsing to 1 cluster after seeing the unique information desk.
- Predict/correct timeline: belief bar chart widening after motion, narrowing after a measurement.
- Taxonomy grid: local vs global × static vs dynamic, with the kidnapped robot highlighted.

Scenario step: a worker carries a Shelfie to another aisle; it must notice and re-localize using the unique packing-station sign.
Notebook idea: 1-D corridor particle filter in numpy; reproduce the midsem calculation (4 hypotheses, priors 0.25, likelihoods 0.10/0.15/0.55/0.20 → normalised posteriors), then add random-particle injection and show recovery after a "kidnap". Laptop.
Production angle: ROS2 `nav2_amcl`, robot_localization (EKF fusion), AprilTag fiducials. **Breaks:** particle deprivation — all particles cluster in the wrong aisle and resampling never recovers. Monitor effective sample size (ESS) and scan-match score.

### M4 · Mapping (≈ CS 8–9)

Topics: occupancy grid mapping; SLAM; feature-based vs grid-based SLAM; GraphSLAM; FastSLAM; mobile robot visual SLAM based on neural networks.

| Concept | One-line definition | Analogy |
|---|---|---|
| Occupancy grid | A grid where each cell holds the probability it is blocked | A heatmap of where errors happen |
| Log-odds update | Store each cell as log(p/(1−p)) so updates become simple additions | Adding up votes instead of multiplying percentages |
| Inverse sensor model | Given a reading, how likely each cell along the beam is occupied or free | Reverse lookup: from symptom to likely cause |
| SLAM | Build the map and locate yourself in it at the same time | Writing the API docs while still discovering the endpoints |
| FastSLAM | Particle filter for the path; each particle keeps its own small Kalman filter per landmark | Each worker thread keeps its own local cache |
| GraphSLAM | Poses and landmarks as graph nodes, measurements as edges; solve all at once offline | Batch reconciliation of a ledger at end of day |
| Loop closure | Recognising a place seen before and correcting the whole map | Detecting a duplicate record and merging histories |
| Visual SLAM (CNN-based) | SLAM driven by camera images, with a CNN extracting features or depth | Replacing hand-written parsers with a learned extractor |

Diagram ideas:
- 2×2 log-odds grid updated by three rays, step by step (matches the midsem question).
- FastSLAM: particle boxes, each holding landmark mean/variance mini-tables.
- GraphSLAM pose graph with a loop-closure edge snapping the drifted path into place.

Scenario step: pallets moved overnight; Shelfie must update its map while working, and the fleet merges maps at shift end.
Notebook idea: log-odds occupancy grid from simulated LiDAR on a 50×50 warehouse grid (numpy + matplotlib); then a 1-D FastSLAM step with 2 particles matching the endsem simplified model. Laptop. Lab 5 (CNN visual SLAM) needs GPU/Colab.
Production angle: Cartographer, slam_toolbox, ORB-SLAM3, RTAB-Map. **Breaks:** false loop closure in a warehouse with identical aisles bends the whole map. Monitor map consistency and relocalization rate.

### M5 · Path Planning (≈ CS 10–13)

Topics: graph-based vs sampling-based planning; A*, D*; RRT, RRT*, PRM; swarm intelligence: cobots, ant colony optimization, particle swarm optimization, genetic algorithm, firefly algorithm; deep reinforcement learning for path planning.

| Concept | One-line definition | Analogy |
|---|---|---|
| A* | Graph search that expands the node with lowest cost-so-far + estimated cost-to-go | Google Maps routing with a straight-line hint |
| D* | A* variant that repairs the plan cheaply when the map changes | Incremental build instead of full rebuild |
| RRT / RRT* | Grow a random tree from start toward samples; RRT* also rewires for shorter paths | Exploring a codebase by random jumps, then refactoring the route |
| PRM | Sample free points once, connect neighbours into a roadmap, then query it many times | Building an index once, querying it many times |
| Probabilistic completeness | If a path exists, the chance of finding it goes to 1 as samples grow; no time bound | "Retries will eventually succeed" — but not by when |
| Ant colony optimization | Simulated ants leave pheromone on good routes; pheromone evaporates; others follow strong trails | Popularity ranking with time decay |
| Genetic algorithm | Evolve a population of candidate routes by selection, crossover and mutation | Feature-flag experiments: keep and combine the winners |
| DRL for planning | An agent learns a policy from reward (reach goal, avoid obstacles) by trial and error | Training a load balancer policy from latency feedback |

Diagram ideas:
- A* vs RRT* on the same warehouse grid: frontier expansion vs random tree growth.
- One ACO iteration: 5 routes, pheromone before/after evaporation and deposit as bar chart.
- DRL loop: state [dx, dy, dist-to-goal, dist-to-obstacle] → policy → action → reward.

Scenario step: Shelfie must get tote 14 from rack R12 to station B through an aisle that was just blocked.
Notebook idea: A* and RRT* on a numpy occupancy grid from M4; one hand-checked ACO iteration (the endsem template: 5 ants, costs, evaporation); optional PPO agent with Stable-Baselines3 on a tiny Gymnasium grid env (CPU fine for small env). Laptop.
Production angle: Nav2 planners (NavFn, Smac), OMPL, SB3. **Breaks:** RL policy trained in sim hits a real shelf (sim-to-real gap); planner oscillates when costmap updates faster than replanning. Monitor path length, replans per minute, near-miss count.

### M6 · Human–Robot Interaction (≈ CS 14–16)

Topics: HRI introduction, modalities, applications, ethical considerations; visual bot: hand/body detection, pose estimation, gesture recognition (static vs dynamic), gesture classification agent; chat bot: LLMs, retrieval-augmented generation, conversational agent; ethics in AI and review.

| Concept | One-line definition | Analogy |
|---|---|---|
| HRI modality | A channel humans use to command a robot: gesture, voice, touch screen | Different API clients: REST, gRPC, CLI |
| Pose estimation | Finding body or hand keypoints (wrist, elbow, fingertips) in an image | Parsing a form into named fields |
| Static vs dynamic gesture | A held hand shape vs a movement over time (wave) | A single request vs a stream of events |
| Gesture classification agent | Classifies a gesture and maps it to a robot action | Router mapping URL to handler |
| RAG | Retrieve relevant documents, then let an LLM answer using them | Search + summarise over internal docs |
| Robot ethics | Privacy, safety and social impact of robots around people | Security and privacy review before launch |

Diagram ideas:
- Gesture pipeline: camera → keypoints → classifier → action → safety check → motor.
- Voice/chat pipeline: speech → text → RAG over warehouse SOPs → command → confirmation.

Scenario step: a worker raises a palm ("stop") or asks "where is tote 14?"; Shelfie obeys safely and answers.
Notebook idea: static gesture classifier on hand keypoints (MediaPipe output or a small synthetic keypoint dataset) with sklearn; then a tiny RAG answering from 10 warehouse SOP snippets with TF-IDF retrieval. Laptop; MediaPipe optional.
Production angle: MediaPipe, OpenPose, LLM APIs with tool calling. **Breaks:** gesture misread as "go" near a person; LLM invents a location. Guardrail: whitelist of allowed commands + confirmation step.

---

## 5. Codebase plan

`codebase/` — **shelfie-sim**: a pure-Python 2D warehouse robot simulator that grows module by module. numpy, matplotlib, scipy, sklearn; optional gymnasium + stable-baselines3. No ROS needed (ROS2 is noted as the production equivalent).

```
codebase/
├── README.md                     how to run, module → file map                 (M1)
├── shelfie/
│   ├── world.py                  grid map, obstacles, robot pose, drift sim     (M1)
│   ├── motion_model.py           odometry + velocity models, noise sampling     (M2)
│   ├── sensor_model.py           LiDAR ray-cast, beam model, likelihood field   (M2)
│   ├── learned_motion.py         MLP that predicts state delta (Lab 3 idea)     (M2)
│   ├── particle_filter.py        MCL + resampling + random-particle injection   (M3)
│   ├── occupancy_grid.py         log-odds mapping with inverse sensor model     (M4)
│   ├── fastslam_1d.py            1-D FastSLAM teaching version                  (M4)
│   ├── planners.py               A*, RRT*, PRM                                  (M5)
│   ├── swarm.py                  ACO + GA route optimisers                      (M5)
│   ├── rl_env.py                 Gymnasium env (state = dx, dy, dist, obstacle) (M5)
│   └── hri.py                    gesture → command router + safety whitelist    (M6)
├── scripts/run_shift.py          one simulated shift end to end                 (M6)
└── tests/
    ├── test_models.py            beam model sums to 1, motion noise stats       (M2)
    ├── test_localization.py      PF converges; recovers after kidnap            (M3)
    └── test_planning.py          A* optimal on toy grid; RRT* path collision-free (M5)
```

---

## 6. Practice topics plan

01 Robot loop and drift — M1, M2 — 4 h
02 Motion and sensor models (beam model, likelihood field, learned motion model) — M2 — 6 h
03 Markov and Monte Carlo localization, kidnapped robot, AMCL idea — M3 — 7 h
04 Occupancy grid mapping with log-odds — M4 — 5 h
05 SLAM: FastSLAM vs GraphSLAM (hand numericals + 1-D code) — M4 — 6 h
06 Graph and sampling planners: A*, D*, RRT*, PRM — M5 — 6 h
07 Swarm and evolutionary planning: ACO, PSO, GA, firefly — M5 — 5 h
08 Deep RL for path planning — M5 — 5 h
09 Human–robot interaction: gestures, RAG chat bot, ethics — M6 — 4 h

---

## 7. Exam signal

Past papers exist for 2025-26 Sem 2 (midsem + endsem, 2 sets each). Pattern:
- **One long story scenario per paper**, reused in every question ("airport service robot" midsem; "earthquake rescue robot" / "symmetric office floor" endsem). Answers must be tied to the scenario; "vague answers will be penalized".
- **Midsem (closed book, 2 h, 30%)**: 4 questions, 9 + 6 + 7 + 8 marks. Roughly half numerical, half justification in ≤ 2–3 sentences.
- **Endsem (open book, 2 h, 35%)**: 4 questions printed as 10 + 10 + 10 + 6 marks. Each long question = one hand-worked numerical (6 marks) + two "modify the scenario so X becomes better than Y" parts.

Repeating themes:
1. **Log-odds occupancy grid update** from a table of ray hits, and **beam model p(z | x)** from z_hit / z_short / z_max / z_rand weights.
2. **Particle filter step**: normalise posterior weights, say which hypothesis dominates, explain why standard PF fails after kidnapping and how augmented MCL fixes it.
3. **FastSLAM one iteration** (1-D corridor, 2 particles, simplified Kalman update, weights before resampling) + "when is GraphSLAM better" + "when is plain occupancy mapping enough".
4. **ACO one iteration** (5 ants, route costs, evaporation) + GA chromosome/fitness design + DRL multi-objective reward design.
5. **RRT\* hand trace** (Manhattan distance, step size, r(n) = min(γ(ln n / n)^(1/d), η), parent choice, rewiring) + probabilistic completeness.
6. **"Pick the better technique for this scenario" pairs**: feature vs correlation sensor model; MCL vs Markov; location vs feature map; velocity vs odometry motion model; beam vs likelihood-field; MCL vs augmented MCL; Bayesian log-odds vs binary grid.

---

## 8. Interview angle

1. **Why is localization probabilistic?** — Sensors are noisy and wheels slip, so a single pose would be confidently wrong; a belief spread can be corrected.
2. **Kalman filter vs particle filter?** — Kalman assumes one Gaussian belief and is cheap; particle filters handle many-peaked beliefs (identical aisles) at higher compute cost.
3. **What is the kidnapped robot problem and how do you handle it?** — Robot moved without knowing; inject random particles or trigger global relocalization when sensor fit drops.
4. **What is particle deprivation and how do you monitor it?** — All particles collapse near a wrong pose; watch effective sample size and scan-match score.
5. **Why log-odds for occupancy grids?** — Bayesian updates become additions, avoid numerical underflow, and are easy to clamp.
6. **FastSLAM vs GraphSLAM?** — FastSLAM is online and per-particle; GraphSLAM optimises the whole trajectory at once, better with loop closures and offline processing.
7. **A\* vs RRT\*?** — A* is optimal on a discrete grid with a good heuristic; RRT* scales to continuous, high-dimensional spaces and is asymptotically optimal.
8. **What breaks when you deploy an RL policy from simulation?** — Sim-to-real gap: friction, sensor noise and latency differ; use domain randomisation and safety layers.
9. **How would you fuse wheel odometry, IMU and GPS?** — An (extended) Kalman filter weighting each by its noise; GPS corrects drift, IMU covers short gaps.
10. **Where does ML add value in a classic robotics stack?** — Learned perception (CNN features, denoising), learned motion models, adaptive filter parameters, and policies where hand-tuning fails.

---

## 9. Repetition plan

| Concept | First met | Revisited in |
|---|---|---|
| Uncertainty / belief | M1 | M2, M3, M4, M5 |
| Motion model | M2 | M3 (predict step), M4 (FastSLAM), M5 (RL dynamics) |
| Measurement model (beam / likelihood field) | M2 | M3 (correct step), M4 (inverse sensor model) |
| Bayes filter predict–correct | M3 | M4 (SLAM), M6 (gesture smoothing) |
| Particles + resampling | M3 | M4 (FastSLAM), M5 (swarm populations, GA) |
| Occupancy grid | M2 (maps) | M4, M5 (planner costmap) |
| Data association | M3 | M4 (loop closure), M6 (which person is commanding) |
| Reward / cost function | M5 (A* cost) | M5 (ACO, GA fitness, DRL reward), M6 (safety) |

---

## 10. Overlap with my other courses

- [../../artificial-and-computational-intelligence/](../../artificial-and-computational-intelligence/) — A* (`revision/ch03-informed-search-astar.md`), local search, GA and ACO (`revision/ch05-genetic-aco-neuroevolution.md`), Bayesian reasoning and HMMs (`revision/ch10-probabilistic-reasoning.md`, `revision/ch11-markov-hmm-viterbi.md`): Bayes filters are HMM forward filtering in disguise.
- [../../deep-reinforcement-learning/](../../deep-reinforcement-learning/) — MDPs, value iteration, policy gradients/PPO behind Lab 3 (PPO) and Lab 7 (DRL path planning).
- [../../llm-engineering/](../../llm-engineering/) and [../../nlp-applications/](../../nlp-applications/) — RAG and conversational agents in M6.
- [../../machine-learning-on-the-edge/](../../machine-learning-on-the-edge/) — running perception models on-robot under compute and power limits.

---

## 11. Build checklist

- [ ] SPEC reviewed
- [ ] cards.json (M1, M2, M3, M4, M5, M6)
- [ ] practice/01 Robot loop and drift
- [ ] practice/02 Motion and sensor models
- [ ] practice/03 Markov and Monte Carlo localization
- [ ] practice/04 Occupancy grid mapping
- [ ] practice/05 SLAM - FastSLAM vs GraphSLAM
- [ ] practice/06 Graph and sampling planners
- [ ] practice/07 Swarm and evolutionary planning
- [ ] practice/08 Deep RL for path planning
- [ ] practice/09 Human-robot interaction
- [ ] codebase/ runs + tests

**Total estimated study hours: ≈ 60 h** (48 h practice topics + 8 h codebase + 4 h past-paper drills).
