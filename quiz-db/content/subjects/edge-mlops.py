from helpers import mcq, tf, out, fill

SUBJECT = "edge-mlops"

TOPICS = [
    ("edge-mlops-arch", "Edge MLOps pipeline and architecture"),
    ("orchestration", "Lightweight deployment orchestration"),
    ("cicd", "CI/CD workflows for edge models"),
    ("registry-versioning", "Model registry and model versioning"),
    ("monitoring-logging", "On-device monitoring and logging"),
    ("drift-psi", "Drift detection with PSI"),
    ("ota-updates", "Over-the-air (OTA) updates"),
    ("shadow-ab", "Shadow deployment and A/B / canary testing"),
    ("feedback-retraining", "Feedback loops and continuous retraining"),
]

QUESTIONS = [
    # ------------------------------------------------------------------ L1
    mcq("What does 'Edge MLOps' add to ordinary MLOps?",
        ["Managing models across a fleet of many, varied, sometimes-offline devices",
         "Training models only on the edge device instead of in the cloud",
         "Replacing monitoring with manual testing",
         "Running the model registry on each device"], 0,
        "Think of where the model runs after training.",
        "MLOps already covers training, versioning, deployment and monitoring. At the edge the same loop must work across thousands of different devices that you cannot log into and that may be offline for days. Training usually still happens in the cloud.",
        topic="edge-mlops-arch", level=1,
        analogy="Like going from deploying one web server to pushing a mobile app update to millions of phones: same code discipline, very different rollout problem."),
    mcq("In a typical edge MLOps architecture, which job usually stays in the cloud?",
        ["Training and retraining the model",
         "Running every inference",
         "Reading the camera or sensor",
         "Switching the actuator on and off"], 0,
        "Which step needs lots of compute and data from many devices?",
        "The cloud is the control plane: it trains, registers and decides what to ship. Devices are the data plane: they read sensors, run inference and act. Retraining needs pooled data and GPUs, so it stays in the cloud.",
        topic="edge-mlops-arch", level=1,
        diagram="""
 cloud (control plane)          devices (data plane)
 train -> registry -> deploy ==> infer -> act
   ^                                 |
   +------ logs, drift stats <-------+
"""),
    tf("In edge MLOps, a 'fleet' means the full set of devices that run your model and are managed together.", True,
       "Same word as a fleet of trucks.",
       "A fleet is every managed device, often split into device groups (by site, hardware or region) so you can ship updates to one group at a time.",
       topic="orchestration", level=1),
    mcq("What does CI/CD stand for?",
        ["Continuous Integration / Continuous Delivery (or Deployment)",
         "Cloud Inference / Cloud Deployment",
         "Code Inspection / Code Documentation",
         "Central Index / Central Database"], 0,
        "Two 'continuous' words.",
        "CI builds and tests every change automatically; CD ships passing builds to staging or production automatically. For models, the build also converts and quantizes the model and the tests include accuracy checks.",
        topic="cicd", level=1),
    mcq("What is a model registry?",
        ["A versioned store of trained models with their metrics and metadata",
         "A list of every device in the fleet",
         "A log of every prediction a device makes",
         "A database of training labels"], 0,
        "Like a package registry, but for models.",
        "A registry (for example MLflow Model Registry) keeps each model version with its metrics, training data snapshot and stage (staging, production, archived). Deployments point at a registry version, not at a file on someone's laptop.",
        topic="registry-versioning", level=1,
        analogy="Like npm or a Docker registry: you install 'model 2.3.1', not 'the file Priya emailed'."),
    fill("A process that sends a new model to devices over the network, without anyone visiting them, is called an ____ update (3-letter abbreviation).", "OTA",
         "Over The ...",
         "OTA = over-the-air. Phones get OS updates this way; edge devices get firmware and model updates the same way.",
         topic="ota-updates", level=1),
    mcq("What is 'drift' for a deployed model?",
        ["The live data (or its relation to the label) moving away from what the model was trained on",
         "The model file slowly getting corrupted on disk",
         "The device clock running fast",
         "The model's weights changing by themselves after deployment"], 0,
        "The model is frozen; what changes?",
        "The weights of a deployed model do not change. The world does: new lighting, a new supplier's parts, seasonal patterns. When live inputs stop looking like the training data, accuracy usually drops.",
        topic="drift-psi", level=1),
    fill("PSI, the drift score used in this course, stands for Population ____ Index.", "Stability",
         "It measures whether the population stays the same.",
         "Population Stability Index: it compares the share of data in each bin now with the share at training time.",
         topic="drift-psi", level=1),
    mcq("In shadow deployment, what happens to the new model's predictions?",
        ["They are logged and compared, but never used to act",
         "They replace the old model's predictions for all users",
         "They are used for half of the devices",
         "They are thrown away without being stored"], 0,
        "A shadow follows you but does nothing.",
        "The new model sees the same real inputs as the live model, but only the live model's output drives the actuator. You compare the two offline. Zero user risk, but extra compute.",
        topic="shadow-ab", level=1,
        diagram="""
 input --+--> live model   --> actuator (acts)
         |
         +--> shadow model --> log only
"""),
    mcq("Which describes A/B testing of two edge models?",
        ["Some devices run model A and others run model B, and their real outcomes are compared",
         "Both models run on every device and only A's output is logged",
         "Model B is tested only in the lab",
         "A and B are averaged into one model"], 0,
        "Both models act on real traffic.",
        "In A/B testing each model really serves part of the fleet or traffic, so you measure real outcomes (defect escapes, false alarms). Unlike shadow, model B can affect users.",
        topic="shadow-ab", level=1),
    tf("A feedback loop in edge MLOps means field results (labels, corrections, outcomes) flow back so the model can be retrained and redeployed.", True,
       "Loop = output goes back to the start.",
       "Devices log what they saw and, where possible, what really happened (an operator corrects a defect call). That data reaches the cloud, retraining happens there, and the new version ships through the same CI/CD path.",
       topic="feedback-retraining", level=1),
    mcq("Which is the most useful thing for a camera-based inspection device to log for monitoring?",
        ["Each prediction's class, confidence score and latency",
         "Every raw video frame at full resolution",
         "Nothing: logs waste storage",
         "Only the device's serial number"], 0,
        "Small, useful, cheap to send.",
        "Prediction, confidence and latency are a few bytes each and are enough for drift and health dashboards. Uploading every raw frame defeats the bandwidth and privacy reasons for running at the edge.",
        topic="monitoring-logging", level=1),
    tf("Once a model is deployed to an edge device, its accuracy stays the same forever because its weights do not change.", False,
       "The weights are frozen; is the data?",
       "Frozen weights mean the model's behaviour on a fixed input is fixed, but the inputs change (seasons, new products, a dirty lens). Accuracy on live data can fall even though the file is unchanged. That is why we monitor.",
       topic="monitoring-logging", level=1),
    mcq("What does 'rollback' mean in an OTA update?",
        ["Returning the device to the previous working version when the new one fails",
         "Deleting all models from the device",
         "Sending the device back to the factory",
         "Undoing the training run in the cloud"], 0,
        "Like undo for a deployment.",
        "If the new firmware or model fails its health check (crashes, will not boot, accuracy collapses), the device goes back to the last good version, ideally automatically.",
        topic="ota-updates", level=1,
        analogy="Like redeploying the previous Docker image tag when a release breaks production."),
    fill("PSI below ____ is read as 'stable, no action' in this course (a decimal).", "0.1",
         "The lowest of the two thresholds.",
         "Course bands: PSI < 0.1 stable; 0.1-0.25 moderate drift, investigate; > 0.25 significant drift, retrain.",
         topic="drift-psi", level=1),
    mcq("Why does an edge model need a version number?",
        ["So you know exactly which model each device runs and can roll back to a known one",
         "Because the device cannot load a file without a number in its name",
         "To make the model run faster",
         "Version numbers are only needed for source code, not models"], 0,
        "Think of debugging a bug report from one device.",
        "When device 4,017 misbehaves you need to know it runs model 2.3.1 built from data snapshot X. Without versions you cannot reproduce, compare or roll back.",
        topic="registry-versioning", level=1),
    mcq("What is a 'canary' release?",
        ["Shipping the new version to a small group first and watching it before going wider",
         "Shipping to every device at midnight",
         "Testing only on a simulator",
         "Releasing a model with a yellow warning label"], 0,
        "Miners took a canary into the mine as an early warning.",
        "A canary group (say 2% of devices) gets the update first. If its metrics stay healthy, the rollout continues in waves; if not, it stops before most devices are affected.",
        topic="shadow-ab", level=1),
    tf("In CI/CD for an edge model, an automated test can block a release if the converted INT8 model loses too much accuracy.", True,
       "That is what a 'gate' is for.",
       "Pipelines add gates such as 'INT8 accuracy within 1 point of FP32' and 'size under 2 MB'. A failing gate stops the build from reaching the registry's production stage.",
       topic="cicd", level=1),
    mcq("What does 'desired state' mean in fleet orchestration?",
        ["The configuration (for example model version 2.4) the cloud wants each device to run",
         "The temperature a device should stay at",
         "The accuracy the model is hoped to reach",
         "The state the device was in at the factory"], 0,
        "Declare what you want; the device works out how to get there.",
        "Like Kubernetes, edge orchestrators are declarative: you set 'group plant-3 should run model 2.4' and each device's agent pulls and installs it, then reports its actual state.",
        topic="orchestration", level=1),
    mcq("A model's confidence is the probability it gives its top prediction. If a deployed model's confidence scores keep getting lower month after month, what is the most likely meaning?",
        ["Inputs are becoming less like the training data (possible drift)",
         "The model is learning on the device",
         "The device is getting faster",
         "Accuracy has definitely improved"], 0,
        "Less sure usually means less familiar.",
        "A model trained on clean parts is usually very confident on clean parts. When confidence slides down, the inputs are probably changing. It is a warning sign that needs no labels, though you still need labels to confirm the accuracy drop.",
        topic="monitoring-logging", level=1,
        diagram="""
 share of predictions per confidence bin
            0.9-1  0.8-0.9  0.7-0.8  <0.7
 training   ####   ###      #        #
 this month ##     ###      ##       ##
"""),

    # ------------------------------------------------------------------ L2
    out("""import numpy as np
expected = np.array([0.5, 0.3, 0.2])   # training shares per bin
actual   = np.array([0.4, 0.3, 0.3])   # this week
psi = np.sum((actual - expected) * np.log(actual / expected))
print(round(float(psi), 3))""",
        ["0.063", "0.0", "-0.018", "0.2"], 0,
        "One bin lost 10 points, one gained 10, one did not move.",
        "Terms: (0.4-0.5)ln(0.8) = 0.022, (0)ln(1) = 0, (0.1)ln(1.5) = 0.041; sum 0.063, stable (< 0.1). Both non-zero terms are positive: a falling share has a negative difference AND a negative log, so they never cancel like a plain difference would (sum of a - e is 0).",
        topic="drift-psi", level=2),
    out("""def band(psi):
    if psi < 0.1:
        return "stable"
    if psi <= 0.25:
        return "moderate"
    return "significant"
print([band(p) for p in [0.05, 0.1, 0.18, 0.25, 0.31]])""",
        ["['stable', 'moderate', 'moderate', 'moderate', 'significant']",
         "['stable', 'stable', 'moderate', 'significant', 'significant']",
         "['stable', 'moderate', 'moderate', 'significant', 'significant']",
         "['stable', 'stable', 'moderate', 'moderate', 'significant']"], 0,
        "Check the two boundary values against < and <=.",
        "With the course bands (< 0.1 stable, 0.1-0.25 moderate, > 0.25 significant) exactly 0.1 and exactly 0.25 both land in 'moderate'. In the exam, state your boundary convention if a value sits on a threshold.",
        topic="drift-psi", level=2),
    mcq("A gateway's PSI on a model's confidence distribution comes out at 0.17. Following the course thresholds, what should the team do?",
        ["Investigate: check recent inputs, devices and sites for the cause, and watch the next reading",
         "Nothing: anything below 0.25 is stable",
         "Retrain and redeploy immediately",
         "Roll the fleet back to the previous model"], 0,
        "0.17 sits between the two thresholds.",
        "0.1-0.25 is moderate drift: a signal to investigate (a camera moved? a new product line?) and to watch the trend. Retraining is the action for > 0.25. Rolling back only helps if a recent model change caused it.",
        topic="drift-psi", level=2,
        diagram="""
 0 ------- 0.1 ---------- 0.25 --------->  PSI
   stable  |   moderate    |  significant
   no action   investigate     retrain
                 ^ 0.17
"""),
    tf("Every term (actual - expected) * ln(actual / expected) in a PSI sum is greater than or equal to zero.", True,
       "Compare the signs of the two factors when actual < expected.",
       "If actual > expected both factors are positive; if actual < expected both are negative; if equal the term is 0. So PSI can only grow as bins move, which is why you can read 'which bin contributes most' straight off the terms.",
       topic="drift-psi", level=2),
    out("""fleet = 2000
cumulative_pct = [1, 5, 25, 100]       # rollout waves
done = 0
new = []
for p in cumulative_pct:
    target = fleet * p // 100
    new.append(target - done)
    done = target
print(new)""",
        ["[20, 80, 400, 1500]", "[20, 100, 500, 2000]", "[20, 80, 400, 2000]", "[1, 5, 25, 100]"], 0,
        "Each wave adds devices up to the new cumulative target.",
        "Cumulative targets are 20, 100, 500, 2000 devices, so each wave adds 20, 80, 400 and 1500. Staged rollouts are defined by cumulative share; only the canary 20 are at risk if the update is bad.",
        topic="ota-updates", level=2,
        diagram="""
wave:     1     2      3       4
share:    1%    5%     25%     100%
devices:  20 -> 100 -> 500 -> 2000
          ^ canary: halt here if health checks fail
"""),
    mcq("Why do edge devices commonly use A/B (dual) partitions for OTA updates?",
        ["The new image is written to the inactive slot, so a failed or interrupted update can boot the old slot",
         "So the device can run model A and model B at the same time for A/B testing",
         "To double the storage available to the model",
         "So the update can be downloaded twice for safety"], 0,
        "What if power fails halfway through writing?",
        "With two slots the running system is never overwritten. The device writes slot B, flips the boot flag, and if B fails its health check it boots slot A again. 'A/B partitions' is about update safety, not the A/B testing of models: a common mix-up.",
        topic="ota-updates", level=2,
        diagram="""
 slot A: v2.3 (running)   slot B: write v2.4
 reboot -> boot B -> health check
     pass: B becomes active
     fail: boot flag back to A (v2.3)
"""),
    mcq("A model is trained in FP32, then converted to INT8 TFLite for Coral devices and to an ONNX file for Jetsons. What should the registry record for each artefact?",
        ["Version, target hardware, precision, runtime version, preprocessing version and its metrics",
         "Only the file name",
         "Only the training accuracy of the FP32 model",
         "Only the date it was uploaded"], 0,
        "Two devices, two files, one logical model.",
        "One trained model yields several artefacts. Each needs its own metadata, and its own measured accuracy after conversion, because INT8 on Coral and FP16 on Jetson do not score the same. Recording only the FP32 accuracy hides conversion losses.",
        topic="registry-versioning", level=2),
    mcq("Which list is a sensible CI pipeline for an edge model, in order?",
        ["Train -> evaluate -> convert/quantize per target -> test accuracy, size and latency -> sign and register",
         "Deploy to all devices -> train -> evaluate",
         "Convert -> train -> quantize -> deploy",
         "Register -> train -> deploy -> test"], 0,
        "You cannot test what you have not built, and you should not ship what you have not tested.",
        "Edge CI adds per-target conversion and quantization, and tests the converted artefact (not just the FP32 model) on accuracy, size and latency. Only passing, signed artefacts reach the registry and then the CD stage.",
        topic="cicd", level=2,
        analogy="Like compile -> unit tests -> integration tests -> publish to the artifact store, where 'compile' now also means 'convert and quantize for each device'."),
    tf("With a device twin (AWS IoT 'shadow' or Azure IoT 'device twin'), a device that is offline when you change the desired model version will pick up the change when it reconnects.", True,
       "The cloud keeps a document for each device.",
       "The twin stores desired and reported properties. An offline device misses nothing: on reconnect it reads 'desired: 2.4', installs it and reports 'reported: 2.4'. Do not confuse this with 'shadow deployment' of a model, which is a testing strategy.",
       topic="orchestration", level=2,
       analogy="Like Kubernetes' spec (desired) and status (actual): a controller keeps closing the gap."),
    fill("In shadow deployment on the device itself, both the live and the shadow model run on every input, so inference compute roughly ____ (one word).", "doubles",
         "Two models, one input.",
         "On-device shadowing about doubles compute, latency (if run serially) and energy. On a battery MCU that is often unacceptable, so teams shadow on a sample of inputs or on the gateway.",
         topic="shadow-ab", level=2),
    out("""inf_per_s = 2
raw = inf_per_s * 86_400 * 32          # one 32-byte log record per inference
summary = 24 * (10 * 4 + 16)           # hourly: 10-bin histogram + 16-byte header
print(round(raw / 1e6, 2), round(summary / 1e3, 2))""",
        ["5.53 1.34", "5.53 0.06", "0.06 1.34", "2.76 1.34"], 0,
        "Seconds in a day, then bytes per record.",
        "Per-inference logs: 2 x 86,400 x 32 B = 5.53 MB a day per device. Hourly histograms: 24 x 56 B = 1.34 KB. On a cellular fleet, ship summaries (enough for PSI) and keep raw records local or sampled.",
        topic="monitoring-logging", level=2),
    mcq("A factory gateway receives only the predictions and confidence scores of its inspection cameras; true labels arrive weeks later, if ever. Which can it monitor TODAY?",
        ["Confidence distribution, prediction class mix, latency and input statistics",
         "Accuracy and F1 score per camera",
         "The exact cause of every misclassification",
         "Nothing useful until labels arrive"], 0,
        "Which metrics need ground truth?",
        "Accuracy and F1 need labels. Confidence histograms, class mix, latency and simple input stats (brightness, mean vibration) need none, and they shift when the data shifts. That is why the papers monitor the confidence distribution.",
        topic="monitoring-logging", level=2),
    tf("A PSI computed on the model's confidence distribution tells you which input feature caused the drift.", False,
       "What was binned?",
       "Confidence PSI is computed on the model's output, so it says 'the model has become less sure' without saying why. To find the cause, compute PSI or other drift statistics per input feature, or inspect samples.",
       topic="drift-psi", level=2),
    mcq("Devices on a bus fleet are online only when parked at depots and sit behind mobile-network NAT. How should they get model updates?",
        ["Pull: each device's agent polls the update service when it is online and downloads its assigned version",
         "Push: the cloud opens a connection to each device and uploads the model",
         "A technician copies the model from a USB stick each month",
         "The cloud waits until every bus is online at the same time"], 0,
        "Who can start a connection through NAT?",
        "Outbound connections from the device work through NAT and firewalls; inbound ones usually do not. Pull-based agents (Greengrass, Azure IoT Edge, Mender) check in when connected, compare desired vs current version and fetch the update.",
        topic="orchestration", level=2,
        analogy="Like a mobile app polling for updates when it opens, instead of the server trying to reach a phone that is switched off."),
    mcq("Your fleet has STM32 microcontrollers and Linux gateways. Where does a lightweight Kubernetes such as K3s or KubeEdge fit?",
        ["On the Linux gateways; the MCUs get their model inside a firmware image through an OTA agent",
         "On the MCUs, one pod per model",
         "Nowhere: Kubernetes needs a data centre",
         "On both, since K3s needs only a few kilobytes of RAM"], 0,
        "K3s still needs Linux and hundreds of MB of RAM.",
        "Container orchestration needs an OS, a container runtime and RAM in the hundreds of MB, which gateways have and MCUs do not. On MCUs the model is compiled into or stored next to the firmware and updated by an OTA bootloader.",
        topic="orchestration", level=2),
    fill("Using semantic versioning (MAJOR.MINOR.PATCH), a new model that needs a different input size, so old preprocessing code will break, gets a ____ version bump (one word).", "major",
         "Breaking change.",
         "Breaking the input contract (shape, normalisation, label set) is a MAJOR change. Retraining on fresh data with the same contract is MINOR or PATCH. Devices running old preprocessing must not receive a new MAJOR model.",
         topic="registry-versioning", level=2,
         analogy="Same rule as an API: a field rename breaks clients, so it is v3, not v2.1."),
    mcq("Which is a valid trigger for automatically retraining an edge model?",
        ["PSI on the monitored distribution exceeds 0.25, or accuracy on a fresh labelled sample falls below the agreed floor",
         "Any single device reports one low-confidence prediction",
         "A new version of Python is released",
         "The model has been in production for one day"], 0,
        "Triggers should be significant and measured.",
        "Common triggers: drift above the significant threshold, a measured accuracy drop, or a schedule (monthly). One low-confidence input is noise; retraining on it would thrash the pipeline.",
        topic="feedback-retraining", level=2),
    tf("Digitally signing an OTA model image encrypts it, so nobody who intercepts it can read the model.", False,
       "Signing and encrypting answer different questions.",
       "A signature proves who built the image and that it was not changed (integrity and authenticity); the device checks it with the vendor's public key before installing. Hiding the content (confidentiality) needs encryption, for example TLS in transit or an encrypted image.",
       topic="ota-updates", level=2,
       analogy="Like a signed git commit or a signed npm package: anyone can read it, but nobody can forge or alter it unnoticed."),
    mcq("Why does an edge CI pipeline run tests on a real device (hardware-in-the-loop), not only on the build server?",
        ["Latency, memory use and operator support can only be trusted when measured on the target hardware",
         "Build servers cannot run Python",
         "Real devices give higher accuracy",
         "It is required by the TFLite licence"], 0,
        "Your laptop is not a Raspberry Pi.",
        "A model can pass on an x86 server and then fall back to slow CPU ops, run out of RAM or miss its latency budget on the device. A small rack of target boards in CI catches this before the fleet does.",
        topic="cicd", level=2),
    mcq("An operator on a packing line can tap 'wrong' on the screen when the defect model makes a mistake. In MLOps terms, what are these taps?",
        ["Field labels that feed the retraining dataset",
         "Model weights",
         "Drift scores",
         "Device telemetry about CPU load"], 0,
        "What does retraining need that monitoring cannot provide?",
        "Corrections from humans are ground-truth labels collected in production. Logged with the input and model version, they let you measure real accuracy and add hard cases to the next training set.",
        topic="feedback-retraining", level=2),
    mcq("Why is the MLOps loop usually slower and less complete at the edge than for a cloud model?",
        ["Devices are often offline, labels rarely come back, and the fleet runs many hardware types and versions at once",
         "Edge models are always more accurate, so they need less monitoring",
         "Edge devices cannot store any logs",
         "CI/CD tools do not exist for edge devices"], 0,
        "Think about what the cloud gets for free: logs, labels, one hardware type.",
        "A cloud model sees every request, can join labels from the database and runs on one server type. An edge fleet reports late (or never), has few labels, and is a mix of hardware and model versions, so monitoring and rollout must be designed for partial information.",
        topic="edge-mlops-arch", level=2),
    tf("Shadow deployment lets you measure the business outcome (for example how many defects escape) that the new model would cause.", False,
       "Does the shadow model ever act?",
       "A shadow model's outputs never drive actions, so you only see how its predictions differ from the live model's. To measure real outcomes caused by the new model you need A/B or canary testing, where it actually acts on part of the fleet.",
       topic="shadow-ab", level=2),
    mcq("In a model registry, what does 'promoting' a version from Staging to Production usually mean?",
        ["Marking it as the version deployments should use, after it passed the gates and review",
         "Retraining it on more data",
         "Copying it onto every device immediately",
         "Deleting the old production version"], 0,
        "Stages are labels with rules.",
        "Promotion changes which version the CD pipeline and device groups point at. The old version stays (Archived) so you can roll back to it. Shipping to devices then happens through the staged rollout, not at promotion time.",
        topic="registry-versioning", level=2),
    out("""desired = "2.4"
reported = ["2.4", "2.3", "2.4", "2.4", "2.2", "2.3", "2.4"]
behind = [v for v in reported if v != desired]
print(len(behind), sorted(set(behind)))""",
        ["3 ['2.2', '2.3']", "2 ['2.2', '2.3']", "3 ['2.3']", "4 ['2.2', '2.3', '2.4']"], 0,
        "Count the reports that differ from the desired version.",
        "Three devices still report an old version (two on 2.3, one on 2.2). Fleets always run a mix; dashboards compare desired vs reported versions so you know who has not updated and why.",
        topic="orchestration", level=2),

    # ------------------------------------------------------------------ L3
    out("""import numpy as np
ref = np.array([50, 25, 15, 10]) / 100   # confidence bins 0.9-1, 0.8-0.9, 0.7-0.8, <0.7
aug = np.array([44, 27, 17, 12]) / 100
sep = np.array([28, 26, 24, 22]) / 100
def psi(e, a):
    return round(float(np.sum((a - e) * np.log(a / e))), 3)
print(psi(ref, aug), psi(ref, sep))""",
        ["0.015 0.265", "0.015 0.128", "0.265 0.015", "0.06 0.453"], 0,
        "Four terms per month; the top bin moves most in September.",
        "A dairy cooperative's milk-sample camera: August PSI 0.015 (stable, no action); September 0.265 (just above 0.25, significant: retrain). The top-bin term alone is (0.28-0.50)ln(0.56) = 0.128. Calling 0.265 'moderate' because it is 'close to 0.25' is the common slip.",
        topic="drift-psi", level=3),
    mcq("A reference confidence bin [0.9-1.0] holds 45% of predictions; this month it holds 30%. What is that bin's PSI term?",
        ["0.061", "-0.061", "0.150", "0.405"], 0,
        "(a - e) times ln(a / e), with a = 0.30 and e = 0.45.",
        "(0.30 - 0.45) x ln(0.30 / 0.45) = (-0.15) x (-0.405) = 0.061. Writing -0.061 forgets that the log is negative too; 0.405 is the log alone; 0.15 is the difference alone. In the exam show each term like this, then add the four.",
        topic="drift-psi", level=3),
    mcq("A textile mill's fabric-defect gateway reports monthly PSI on the confidence distribution: June 0.02, July 0.09, August 0.16, September 0.23. No single month is above 0.25. What should the operations team conclude?",
        ["Drift is progressive and accelerating; plan retraining now (collect and label recent data) before it crosses 0.25",
         "Everything is fine because no month is significant",
         "Retrain only after a month exceeds 0.25, never before",
         "The gateway is broken, since PSI should not change"], 0,
        "Look at the direction, not just the latest value.",
        "Each month is worse than the last. The trend predicts October will cross 0.25, and retraining takes time (data, labels, CI, rollout), so start now. This is the papers' 'what does the progression tell you' point: a trend is an early warning a single reading cannot give.",
        topic="drift-psi", level=3,
        diagram="""
PSI
0.25 |- - - - - - - - - - - - - significant
     |                     *
     |               *
0.10 |- - - - - - *- - - - - - - moderate
     |   *
     +---Jun---Jul---Aug---Sep-->
"""),
    out("""devices = 1200
full_mb, delta_mb = 48, 6
rate = 0.09                              # rupees per MB on the cellular plan
full = round(devices * full_mb * rate, 2)
delta = round(devices * delta_mb * rate, 2)
print(full, delta, round(full / delta, 1))""",
        ["5184.0 648.0 8.0", "5184.0 648.0 0.1", "57600 7200 8.0", "518.4 64.8 8.0"], 0,
        "MB per device x devices x rupees per MB.",
        "Full image: 1,200 x 48 MB x Rs 0.09 = Rs 5,184 per rollout; delta: 1,200 x 6 MB x 0.09 = Rs 648, 8x cheaper. Deltas also shorten the time a device spends downloading over a weak link, which cuts failed updates.",
        topic="ota-updates", level=3),
    mcq("A team shows that the PSI is 0 because 'the shares that went down exactly balance the shares that went up: the differences add to zero'. What is wrong?",
        ["The differences always add to zero for any two distributions; PSI weights each difference by ln(a/e), and every term is non-negative",
         "Nothing: if the differences cancel there is no drift",
         "They should have used percentages, not fractions",
         "PSI must be computed on raw counts, not shares"], 0,
        "Both distributions sum to 1.",
        "Since both sum to 100%, Σ(a - e) is ALWAYS 0, so it cannot measure anything. The log factor gives each term the same sign as its difference, so all terms are positive and add up. This is the classic exam slip.",
        topic="drift-psi", level=3),
    mcq("A model update is going out to 3,000 metro-turnstile face-match devices. The canary is 2% of devices. Which halt rule is best?",
        ["Stop the rollout if canary devices show more crashes, a higher reject rate or a confidence-PSI rise versus non-updated devices over the same 24 h",
         "Stop only if every canary device crashes",
         "Never stop; roll back after the full rollout if complaints arrive",
         "Stop if any single canary device reports one error"], 0,
        "Compare like with like, over a window.",
        "Halt rules compare the canary with a control group (same time, similar sites) on health and model KPIs, over enough time to be meaningful. 'All devices crash' is too late; 'one error' halts on noise. Comparing against last month instead of a same-time control confuses drift with the update.",
        topic="shadow-ab", level=3),
    out("""import numpy as np
ref = np.array([55, 25, 12, 8]) / 100
now = np.array([38, 27, 20, 15]) / 100
terms = (now - ref) * np.log(now / ref)
print(np.round(terms, 3).tolist(), round(float(terms.sum()), 3))""",
        ["[0.063, 0.002, 0.041, 0.044] 0.149",
         "[-0.063, 0.002, 0.041, 0.044] 0.024",
         "[0.063, 0.002, 0.041, 0.044] 0.251",
         "[0.17, 0.02, 0.08, 0.07] 0.34"], 0,
        "Write out the four terms like the exam asks.",
        "Terms 0.063 + 0.002 + 0.041 + 0.044 = 0.149: moderate drift, investigate. The top bin (55% -> 38%) dominates, but the two low-confidence bins together add as much. The last option adds the raw differences (0.17 + 0.02 + 0.08 + 0.07), which is not PSI.",
        topic="drift-psi", level=3),
    fill("A confidence bin 'below 0.7' rises from 10% of predictions to 25%. Its PSI term, to 3 decimal places, is ____.", "0.137",
         "0.15 x ln(2.5).",
         "(0.25 - 0.10) x ln(0.25 / 0.10) = 0.15 x 0.916 = 0.137. A fast-growing low-confidence bin is often the biggest single term after the top bin, and it is the one that says 'the model is unsure about many more inputs'.",
         topic="drift-psi", level=3),
    mcq("After an OTA update boots from the new slot, what should the device check before it 'commits' the update (makes the new slot permanent)?",
        ["The app starts, the model loads, a stored golden input gives the expected output and latency is within budget",
         "Only that the device powered on",
         "That the download finished, before rebooting",
         "Nothing; commit first and check later"], 0,
        "Booting is not the same as working.",
        "A health check proves the new version actually works: process up, model loaded on the right accelerator, known input -> known output, latency OK, cloud reachable. If any check fails or times out, the bootloader reverts to the old slot.",
        topic="ota-updates", level=3,
        diagram="""
 boot new slot -> app up? -> model loads? -> golden
   input OK? -> latency OK? -> COMMIT
 any 'no' or watchdog timeout -> revert to old slot
"""),
    out("""import numpy as np
live   = np.array([1, 0, 0, 1, 1, 0, 1, 0, 0, 1])
shadow = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1])
agree = float(np.mean(live == shadow))
print(agree, np.flatnonzero(live != shadow).tolist())""",
        ["0.7 [2, 4, 8]", "0.3 [2, 4, 8]", "0.7 [3, 5, 9]", "0.8 [2, 4]"], 0,
        "Count matching positions; indexes start at 0.",
        "7 of 10 predictions match, and the disagreements are at indexes 2, 4 and 8. Shadow analysis focuses on those cases: label them, and you learn which model was right without either model having acted on the new prediction.",
        topic="shadow-ab", level=3),
    out("""mj = 40                       # energy per inference, millijoules
per_day = 86_400               # one inference per second
base = mj * per_day / 1000     # joules
full_shadow = 2 * base
sampled = base * (1 + 0.10)    # shadow only 10% of inputs
print(base, full_shadow, round(sampled, 1))""",
        ["3456.0 6912.0 3801.6", "3456.0 6912.0 345.6", "3456 6912 3801.6", "34.56 69.12 38.02"], 0,
        "Shadow runs a second model on the inputs it covers.",
        "Live model: 40 mJ x 86,400 = 3,456 J a day. Full shadow doubles it to 6,912 J; shadowing 10% of inputs adds only 10% (3,801.6 J). On a battery device that difference decides whether you can shadow at all.",
        topic="shadow-ab", level=3),
    mcq("Version 3.0 of a crop-disease model was trained with inputs normalised by (x - mean) / std. It was pushed OTA to farm devices whose app still scales pixels to [0, 1]. Confidence collapses overnight. What process fix prevents this?",
        ["Version the preprocessing with the model (one bundle, or a compatibility field the device checks) and test the bundle on-device in CI",
         "Lower the confidence threshold on the devices",
         "Retrain v3.0 for longer",
         "Ship models only on weekends"], 0,
        "The model was fine; its contract was not.",
        "A model plus the wrong preprocessing is a broken model. Bundle the preprocessing parameters with the artefact (or record a MAJOR input contract and refuse incompatible installs), and run the bundle on a real device in CI. This is the pipeline-mismatch trap from Module 1, now at update time.",
        topic="registry-versioning", level=3),
    out("""metrics = {"acc_drop": 1.4, "size_mb": 3.1, "p95_ms": 38}
limits  = {"acc_drop": 1.0, "size_mb": 4.0, "p95_ms": 40}
failed = [k for k in limits if metrics[k] > limits[k]]
print(failed or "release")""",
        ["['acc_drop']", "release", "['size_mb', 'p95_ms']", "['acc_drop', 'p95_ms']"], 0,
        "Compare each metric with its limit.",
        "Size (3.1 <= 4.0) and p95 latency (38 <= 40) pass, but the INT8 model lost 1.4 accuracy points against a 1.0 limit, so the gate blocks the release. Typical fix: try QAT or better calibration data, then rerun the pipeline.",
        topic="cicd", level=3),
    out("""per_day = 50_000          # inferences per device
kb = 60                   # one compressed image
hard = per_day * 0.01     # lowest-confidence 1%
rand = per_day * 0.002    # uniform random 0.2%
print(hard * kb / 1000, rand * kb / 1000)""",
        ["30.0 6.0", "30 6", "3.0 0.6", "300.0 60.0"], 0,
        "Images per day x KB, then KB to MB.",
        "500 hard images x 60 KB = 30 MB; 100 random images = 6 MB per device per day. The hard cases help the model most; the random sample keeps an unbiased view of the real data and real accuracy. Budget both before you size the data plan.",
        topic="feedback-retraining", level=3,
        diagram="""
 50,000 inferences/day on one device
   lowest-confidence 1%  -> 500 images (hard cases)
   uniform random 0.2%   -> 100 images (unbiased)
   x 60 KB each          -> 30 MB + 6 MB per day
"""),
    out("""import numpy as np
lat = np.array([12, 13, 12, 14, 13, 15, 12, 40, 13, 14])   # ms, from device logs
p50 = float(np.percentile(lat, 50))
p95 = round(float(np.percentile(lat, 95)), 2)
print(p50, p95, p95 < 30)""",
        ["13.0 28.75 True", "13.0 40.0 False", "15.8 28.75 True", "13.5 15.0 True"], 0,
        "np.percentile interpolates linearly between sorted values.",
        "Sorted, the median is 13.0 ms. p95 sits at position 0.95 x 9 = 8.55, between 15 and 40, so 15 + 0.55 x 25 = 28.75 ms. One 40 ms outlier barely moves the median but drags p95 close to the 30 ms budget: monitor tail latency per device, not the mean.",
        topic="monitoring-logging", level=3),
    mcq("A cold-chain truck's device is offline for most of each trip. Which design keeps monitoring working?",
        ["Keep running the last good model, store summaries in a bounded local buffer, and upload them with version IDs when connected",
         "Stop inference whenever the cloud is unreachable",
         "Stream every reading live and drop data when the link fails",
         "Store unlimited raw logs until the disk fills"], 0,
        "Offline-first, bounded storage.",
        "Offline-first means inference never depends on the cloud, and telemetry is buffered (a ring buffer with oldest-first eviction) and sent later, tagged with model version and timestamps so the cloud can rebuild the timeline.",
        topic="edge-mlops-arch", level=3,
        analogy="Like an offline-first mobile app: write to a local queue, sync when the network comes back."),
    mcq("A regulator asks which data trained the model that rejected a batch of tablets at a pharma plant on 3 March. What must your MLOps setup provide?",
        ["The device's logged model version, and registry lineage from that version to its training data snapshot, code commit and pipeline run",
         "The latest model in the registry",
         "The device's CPU temperature log",
         "The accuracy of the FP32 model on the test set"], 0,
        "Trace backwards from the device to the data.",
        "Lineage connects device log -> model version -> registry entry -> data snapshot + code commit + pipeline run. 'The latest model' may not be what that device ran on 3 March; with mixed-version fleets you need the version stamped on every prediction log.",
        topic="registry-versioning", level=3,
        diagram="""
 device log (3 Mar): model 2.3.1, hash 9f2c...
        |
 registry 2.3.1 -> data snapshot 2026-01-15
                -> git commit a41e, pipeline run #812
"""),
    tf("Putting the new model on all devices of a new plant and the old model on all devices of an older plant gives a fair A/B comparison.", False,
       "What else differs between the plants?",
       "Lighting, machines, products and operators differ between plants, so any difference in outcomes mixes the model effect with the site effect. Randomise devices within each site (or alternate by shift) so both models see similar conditions.",
       topic="shadow-ab", level=3,
       analogy="Like running an A/B test where all mobile users get variant B and all desktop users get A: you measure the device, not the variant."),
    mcq("A model update must reach 900 devices: Jetsons at 3 hubs and Raspberry Pis in 40 vans. Which rollout order is best?",
        ["Lab test rig -> a few devices of EACH hardware type at one friendly site -> 5-10% waves per hardware group -> the rest",
         "All Jetsons first, all Pis a week later",
         "Every device at once at night, when traffic is low",
         "One random device, then all 899 others"], 0,
        "A bug may exist on only one hardware type.",
        "Each hardware group runs a different artefact or execution path, so each needs its own canary. Waves within each group limit the blast radius. 'At night' reduces user impact but not the number of broken devices.",
        topic="orchestration", level=3,
        diagram="""
 lab rig -> pilot site (2 Jetson + 3 Pi)
   -> Jetson group: 10% -> 50% -> 100%
   -> Pi group:     10% -> 50% -> 100%
 halt any group on health/KPI regression
"""),
    mcq("A fruit-sorting line changes fruit with the season (mango in summer, apple in winter). Which retraining policy fits best?",
        ["Retrain on drift (PSI above 0.25 or an accuracy drop on audited samples), with a minimum gap between retrains and seasonal data kept in the training set",
         "Retrain every day on yesterday's data only",
         "Never retrain; seasons repeat anyway",
         "Retrain on a fixed monthly schedule, whatever the monitoring says"], 0,
        "Trigger on evidence, but do not forget old seasons.",
        "Drift-triggered retraining spends compute only when the data has moved; a minimum gap stops thrashing. Training only on recent data forgets the previous season, which will return. A fixed schedule either wastes runs or reacts too late.",
        topic="feedback-retraining", level=3),
    tf("If drift is detected after a new model version was rolled out, rolling back to the previous version will always fix it.", False,
       "Where does drift live: in the model or in the data?",
       "Rollback fixes regressions caused by the new version (a bug, a bad conversion). Data drift is in the world: the old model sees the same shifted inputs. Check whether PSI rose at the update time (the model changed) or gradually (the data changed).",
       topic="ota-updates", level=3),
    fill("In Azure IoT Edge, the per-device cloud document holding the desired and the reported properties (for example the model version) is called the device ____.", "twin",
         "AWS calls its version a 'shadow'.",
         "Device twin (Azure) / device shadow (AWS IoT). The cloud writes desired properties, the device writes reported ones, and the gap shows which devices have not converged yet.",
         topic="orchestration", level=3),
    mcq("A fleet-wide dashboard shows confidence PSI 0.04 across 50 sites, so the team relaxes. One site's own PSI is 0.42. What lesson does this teach?",
        ["Compute drift per site or device group as well; a fleet-wide pool dilutes a local problem",
         "The site's PSI must be a computing error, since the fleet is stable",
         "Average the site PSIs instead, and the problem disappears",
         "Only fleet-wide PSI matters for retraining"], 0,
        "One site is 2% of the pool.",
        "Pooling 50 sites means one bad site barely shifts the overall histogram. Local causes (a fogged lens, a new product at one plant) show up only in per-site or per-device monitoring. Alert on the worst groups, not just the total.",
        topic="monitoring-logging", level=3,
        analogy="Like an overall 99.9% API success rate hiding that one customer's region is completely down."),
    tf("The reference distribution for confidence monitoring should come from the deployed artefact (for example the INT8 model) on held-out validation data, not from the FP32 model's confidences on its own training set.", True,
       "Which model and which data will the live numbers come from?",
       "Training-set confidences are inflated (the model has seen those images) and quantization shifts confidences a little. Comparing live INT8 confidences with FP32 training confidences reports 'drift' on day one. Rebuild the reference whenever a new model version ships.",
       topic="monitoring-logging", level=3),

    # ------------------------------------------------------------------ L4
    mcq("Plant X's confidence PSI is 0.002 in January and 0.394 in February. Plant Y's is 0.060 in April and 0.453 in May. Both end above 0.25. What extra does each two-month story tell the team?",
        ["X jumped from flat to significant: look for a discrete event (new supplier, camera moved, firmware change) as well as retraining; Y was already drifting: the cause is gradual and the April reading was an early warning",
         "Nothing extra: both need the same retrain and the history is irrelevant",
         "X is worse because its rise is larger",
         "Y is fine because April was below 0.1"], 0,
        "Shape of the change, not only its size.",
        "A sudden jump points to a step change you can often find and fix at the source, so retraining alone may be the wrong fix. A slow climb points to gradual change (wear, season, product mix) and argues for trend alerts. Both final readings say retrain; the history says why.",
        topic="drift-psi", level=4,
        diagram="""
 PSI      month 1   month 2
 Plant X   0.002 ->  0.394   step: find the event
 Plant Y   0.060 ->  0.453   ramp: early warning missed
 bands: <0.1 stable | 0.1-0.25 moderate | >0.25 retrain
"""),
    mcq("A new model version ships, and the confidence PSI against the old reference immediately jumps to 0.30 although the input data did not change. What is the most likely explanation?",
        ["The new model is calibrated differently, so its confidence distribution differs; the reference must be rebuilt for each model version",
         "The data drifted at exactly the moment of deployment",
         "PSI is always high in the first week",
         "The new model must be worse and should be rolled back"], 0,
        "What does a confidence distribution describe: the data or the model on the data?",
        "Confidence is a property of model + data. A distilled or re-quantized model may be less (or more) confident on the same inputs. Pin each reference to a model version, and compute input-feature drift separately, so a model change is not mistaken for data drift.",
        topic="drift-psi", level=4),
    tf("If the PSI of the confidence distribution stays below 0.1, the model's accuracy cannot have dropped.", False,
       "Can a model be confidently wrong?",
       "Under concept drift (same inputs, new correct labels) or for out-of-distribution inputs, models are often confidently wrong, so confidence stays high while accuracy falls. Confidence PSI is a cheap, label-free alarm, not proof of health: back it with a small labelled audit.",
       topic="monitoring-logging", level=4),
    mcq("An attacker gets hold of an OLD, genuinely signed firmware image that has a known vulnerability and pushes it to devices. Signature checks pass. What stops this?",
        ["Anti-rollback: a monotonic security version counter (in OTP fuses or secure storage) that refuses images older than the minimum allowed",
         "A/B partitions",
         "Delta updates",
         "Signing the image a second time"], 0,
        "The signature is valid; the version is the problem.",
        "Signatures prove origin, not freshness. Anti-rollback stores a minimum security version on the device; images below it are refused. Note the tension with operational rollback: you roll back within the allowed versions, and you raise the minimum only when the old version must be retired.",
        topic="ota-updates", level=4,
        analogy="Like refusing a JWT that is validly signed but expired: authenticity alone is not enough."),
    mcq("A coffee-bean sorter's camera lens slowly fogs. The model keeps calling beans 'grade A' with 0.95 confidence, and confidence PSI stays at 0.03. Which monitoring would have caught it?",
        ["Input-side checks on the device: image sharpness/brightness statistics and their drift, plus a periodic labelled audit sample",
         "Raising the confidence threshold to 0.99",
         "Computing PSI with more confidence bins",
         "Monitoring the CPU temperature"], 0,
        "The output looked normal; the input did not.",
        "Silent failures happen when bad inputs map to confident outputs. Cheap input statistics (Laplacian variance for blur, mean brightness) catch sensor problems the model cannot see, and the audit sample catches accuracy loss. Output monitoring alone is not enough.",
        topic="monitoring-logging", level=4),
    mcq("A company retrains its weld-defect model only on images that operators flagged as mistakes. After three cycles, false alarms on normal welds rise. Why?",
        ["The training data is no longer a representative sample: it over-represents hard and flagged cases, so the class balance and decision boundary drift",
         "Operators are always wrong",
         "Three retrains overflow the model's capacity",
         "Flagged images are lower resolution"], 0,
        "Selection bias in the feedback loop.",
        "Feedback data is selected by the current model and by people's attention, so it is biased. Mix flagged cases with a uniform random sample and the original data, keep a fixed untouched test set, and track accuracy on it across versions.",
        topic="feedback-retraining", level=4,
        analogy="Like a recommender trained only on what users clicked: it never learns about what it never showed them."),
    mcq("An STM32 device has one internal flash bank, enough for only one firmware image, plus a 4 MB external SPI flash. How can it still update safely over the air?",
        ["Download and verify the new image in external flash, then let the bootloader swap it in with a scratch area so an interrupted copy can resume or revert",
         "Erase internal flash first, then download the new image straight into it",
         "Updates are impossible without two internal banks",
         "Run the new image directly from the SPI flash without verifying it"], 0,
        "You need somewhere to stage the image that is not the running copy.",
        "Bootloaders such as MCUboot support swap with a scratch sector (or an overwrite-only mode with a recovery image). The running image is replaced only after the staged copy is fully downloaded and verified, and the swap is resumable after power loss. 'Erase first' is how devices get bricked.",
        topic="ota-updates", level=4,
        diagram="""
 SPI flash: new image (downloaded, signature OK)
        | bootloader swap, sector by sector,
        v progress kept in a scratch area
 internal flash: old <-> new   (power cut: resume)
"""),
    mcq("Your OTA system ships binary deltas from version 2.3 to 2.4. 15% of the fleet is still on 2.1 or 2.2. What happens and what should you do?",
        ["A delta only applies to its exact base image; build deltas per base version or fall back to the full image for those devices",
         "Deltas apply to any older version",
         "Those devices skip 2.4 automatically and are fine",
         "Delete the old versions from the registry"], 0,
        "A diff is computed against one specific file.",
        "A delta is a patch against specific bytes; applied to another base it fails verification (or worse, without a hash check, corrupts the image). Update services either keep deltas for each supported base or send full images to stragglers; the device must check the base hash before patching.",
        topic="ota-updates", level=4,
        analogy="Like a git patch that only applies cleanly to the commit it was generated from."),
    out("""new = [20, 80, 400, 1500]          # devices added per wave
fails = [0, 1, 12, 0]               # failed health checks in that wave
exposed = 0
for w, (n, f) in enumerate(zip(new, fails), start=1):
    exposed += n
    if f / n > 0.02:
        print("halt at wave", w, "exposed", exposed)
        break
else:
    print("complete", exposed)""",
        ["halt at wave 3 exposed 500", "halt at wave 2 exposed 100", "complete 2000", "halt at wave 3 exposed 400"], 0,
        "Failure rate per wave against 2%.",
        "Wave 1: 0%. Wave 2: 1/80 = 1.25%, under 2%. Wave 3: 12/400 = 3%, so the rollout halts with 500 devices updated and 1,500 untouched. The staged rollout contained a bad release that a 1-device or all-at-once rollout would not have.",
        topic="ota-updates", level=4),
    mcq("An A/B test of two traffic-camera models runs for two weeks. No ground-truth labels come back, so the team compares how often each model outputs 'violation'. Model B flags 18% more. What can they conclude?",
        ["Only that B predicts differently; without labels on a sample they cannot tell whether B catches more real violations or makes more false alarms",
         "B is 18% better",
         "B is 18% worse",
         "The test proves both models are equally accurate"], 0,
        "A proxy metric is not an outcome.",
        "Prediction rate is a proxy. To turn the A/B into evidence, label a random sample from each arm (human review), compute precision and recall per arm, and only then promote. The same applies to shadow disagreements.",
        topic="shadow-ab", level=4),
    mcq("Logs from 4,000 devices arrive in the cloud. Which field, added to every log record, makes debugging a mixed-version fleet possible?",
        ["A build identifier: model version + artefact hash, plus runtime and preprocessing versions",
         "The device's local time only",
         "The name of the engineer who trained the model",
         "The file size of the model"], 0,
        "You need to group records by exactly what was running.",
        "During a staged rollout two or three versions run at once. Stamping each record with model version and hash (and runtime/preprocessing versions) lets you split every metric by version, which is how you spot that 2.4 on Raspberry Pis regresses while 2.4 on Jetsons does not.",
        topic="registry-versioning", level=4),
    mcq("Fishing boats are offline about 70% of the time and pay per MB for satellite links. Where should the confidence PSI for each boat be computed?",
        ["On the device: keep a running 4-bin histogram of confidences and send only the counts (a few bytes) when connected; the cloud computes PSI against the reference",
         "In the cloud, from every uploaded raw image",
         "Nowhere; offline boats cannot be monitored",
         "On the device, uploading every prediction record"], 0,
        "What is the smallest thing that still lets you compute PSI?",
        "PSI needs only bin shares. A histogram of counts per period is tiny, survives long offline gaps (just keep counting), and is privacy-friendly. This is 'compute where the data is' applied to monitoring.",
        topic="edge-mlops-arch", level=4,
        diagram="""
 device: conf -> bin counts [412, 260, 180, 148]
          (few bytes, sent when link is up)
 cloud:  shares vs reference -> PSI -> alert
"""),
    fill("With MCUboot's test-swap upgrade, if the new image boots but the application does not mark it as confirmed before the next reset, the bootloader ____ to the old image (one word, past tense).", "reverted",
         "Unconfirmed means 'trial'.",
         "A test swap is a trial run: the app must confirm the image after its own health checks. If it crashes, hangs or a watchdog resets it first, the next boot reverts to the previous image. This makes rollback automatic, not a human decision.",
         topic="ota-updates", level=4),
    mcq("Running the same CI pipeline twice on the same commit and data produces two INT8 models with different accuracy (91.2% vs 90.4%). What is the most likely cause and fix?",
        ["The calibration subset for quantization is sampled without a fixed seed; pin the calibration set (or seed) and record it in the registry",
         "INT8 models are random by nature and nothing can be done",
         "The device clock differs between runs",
         "The test set is too large"], 0,
        "Which step in PTQ reads a sample of data?",
        "Post-training quantization picks scales from a calibration sample. A different sample gives different ranges and accuracy. Reproducible pipelines pin calibration data, seeds and tool versions, so a 'retrained' model differs only for the reasons you changed.",
        topic="cicd", level=4),
    mcq("A factory has 200 tiny sensor MCUs (FreeRTOS) and one Linux gateway per hall running AWS IoT Greengrass. What is the cleanest way to manage models for both tiers?",
        ["The gateway is the local orchestrator: Greengrass components on the gateway, and MCU firmware/model updates relayed through it with FreeRTOS OTA",
         "Install Greengrass on each MCU",
         "Give every MCU its own Kubernetes node",
         "Manage the MCUs by hand and only automate the gateway"], 0,
        "Each tier gets the agent it can run.",
        "Full agents need Linux; MCUs run small OTA clients. A hierarchical design (cloud -> gateway -> MCUs) keeps one control plane, lets the gateway cache images for the whole hall (one download instead of 200) and keeps the MCU footprint tiny.",
        topic="orchestration", level=4),
    mcq("For a battery-powered wildlife camera, the team wants to compare a new model with the live one before switching. Which plan best balances risk and resources?",
        ["Shadow the new model on the base-station gateway using frames the cameras already send, then canary it on a few cameras",
         "Run both models on every camera for every frame",
         "Switch all cameras to the new model and compare with last year's data",
         "Skip testing, since both models passed CI"], 0,
        "Shadow where compute is cheap, canary where risk is small.",
        "Moving the shadow to the gateway keeps camera energy unchanged; a small canary then measures real on-device behaviour (latency, battery, accuracy on audited frames). CI proves the artefact runs; it does not prove it works better in the field.",
        topic="shadow-ab", level=4),
    tf("After drift is confirmed, the safest retraining set is the recent field data only, because old data no longer represents the world.", False,
       "What happens when the old conditions come back?",
       "Training only on recent data forgets earlier conditions (night shift, last season, the old supplier), so the model regresses when they return. Combine recent labelled data with a representative sample of older data, and evaluate on both old and new test slices before promoting.",
       topic="feedback-retraining", level=4),

    # ------------------------------------------------------------------ more practice (mixed levels)
    mcq("Which stage fills the gap in the edge MLOps loop?",
        ["Deploy (ship the artefact to devices, usually over the air)",
         "Delete the old data",
         "Buy new hardware",
         "Write the project report"], 0,
        "What must happen between building a model and watching it in the field?",
        "The loop is data -> train -> optimize -> deploy -> monitor -> retrain. Deploy at the edge means packaging per target and shipping OTA in stages; monitoring then feeds the next round of data.",
        topic="edge-mlops-arch", level=1,
        diagram="""
 data -> train -> optimize -> [ ? ]
  ^                             |
  |                             v
 retrain <------------------ monitor
"""),
    out("""targets = {"jetson": ["fp16", "int8"], "nuc": ["fp32", "int8"],
           "rpi": ["int8"], "coral": ["int8"]}
builds = [(t, p) for t, ps in targets.items() for p in ps]
print(len(builds), builds[-1])""",
        ["6 ('coral', 'int8')", "4 ('coral', 'int8')", "8 ('coral', 'int8')", "6 ('jetson', 'fp16')"], 0,
        "Count every (target, precision) pair.",
        "2 + 2 + 1 + 1 = 6 artefacts from one trained model. Each one is converted, tested and registered separately in the CI build matrix, the same way a web project builds and tests for several browsers or OS versions.",
        topic="cicd", level=2),
    fill("A CI test stage that runs the converted model on a real target board (for example a Raspberry Pi in a test rack) is called hardware-in-the-____ testing.", "loop",
         "Three words: hardware-in-the-...",
         "Hardware-in-the-loop (HIL) testing measures real latency, memory and operator support on the target before release.",
         topic="cicd", level=2,
         analogy="Like running your front-end tests on real phones in a device farm instead of only in desktop Chrome."),
    fill("Sending a device's lowest-confidence samples to humans for labelling, because they teach the model the most, is called ____ learning.", "active",
         "The model actively chooses what to be taught.",
         "Active learning picks the most informative samples (often lowest confidence or highest disagreement) for labelling, so a small labelling budget gives the biggest accuracy gain.",
         topic="feedback-retraining", level=2),
    out("""hard_images = 5_000        # fleet-wide per day
per_hour = 300             # images one labeller handles per hour
rupees_per_label = 2
print(round(hard_images / per_hour, 1), hard_images * rupees_per_label)""",
        ["16.7 10000", "16.6 10000", "1500.0 10000", "16.7 2500"], 0,
        "Images divided by speed, images times price.",
        "5,000 / 300 = 16.7 labeller-hours and 5,000 x Rs 2 = Rs 10,000 a day. Labelling, not compute, is often the real limit on how fast a feedback loop turns, which is why teams select samples carefully.",
        topic="feedback-retraining", level=2),
    out("""def compatible(device_major, versions):
    return [v for v in versions if int(v.split(".")[0]) == device_major]
print(compatible(2, ["2.4.1", "3.0.0", "2.5.0", "1.9.9"]))""",
        ["['2.4.1', '2.5.0']", "['2.4.1', '3.0.0', '2.5.0']", "['3.0.0']", "['2.4.1', '2.5.0', '1.9.9']"], 0,
        "Only the MAJOR number has to match.",
        "Devices whose app speaks input contract 2 may take any 2.x.y model, never 3.0.0 (breaking change) and not 1.9.9 (old contract). An update service that checks this refuses installs that would silently break preprocessing.",
        topic="registry-versioning", level=2),
    out("""devices = 5_000
summ = devices * 24 * 56                  # hourly 56-byte histogram
raw = devices * 2 * 86_400 * 32           # 2 inf/s, 32-byte record each
print(round(summ / 1e6, 2), round(raw / 1e9, 1))""",
        ["6.72 27.6", "6.72 2.8", "0.67 27.6", "6.72 276.5"], 0,
        "Summary MB and raw GB per day for the whole fleet.",
        "Summaries: 5,000 x 24 x 56 B = 6.72 MB a day for the whole fleet. Raw records: 5,000 x 172,800 x 32 B = 27.6 GB a day. Same drift signal, about 4,000x less data: the reduction-ratio idea from Module 3 applied to telemetry.",
        topic="edge-mlops-arch", level=3),
    out("""import numpy as np
counts = np.array([412, 260, 180, 148])     # this week's confidence-bin counts
ref = np.array([0.45, 0.30, 0.15, 0.10])
a = counts / counts.sum()
print(round(float(np.sum((a - ref) * np.log(a / ref))), 3))""",
        ["0.033", "33.2", "0.33", "ValueError"], 0,
        "Turn counts into shares first.",
        "Shares are 0.412, 0.26, 0.18, 0.148, giving PSI 0.033: stable. Plugging raw counts straight into the formula gives nonsense in the hundreds, the usual bug when a device sends counts and the cloud forgets to normalise.",
        topic="drift-psi", level=3),
    out("""psi = [0.03, 0.05, 0.04, 0.07, 0.11, 0.16, 0.14]   # weekly
streak = 0
for w in range(1, len(psi)):
    streak = streak + 1 if psi[w] > psi[w - 1] else 0
    if streak == 3:
        print("trend alert at week", w + 1)
        break""",
        ["trend alert at week 6", "trend alert at week 5", "trend alert at week 7", "trend alert at week 4"], 0,
        "Count consecutive rises; weeks are numbered from 1.",
        "Rises: week 4 (0.04 -> 0.07), week 5, week 6, so the third rise in a row is week 6, while PSI is only 0.16. A trend rule fires during the moderate band, buying time to collect labels before a significant reading forces a rushed retrain.",
        topic="drift-psi", level=3),
    mcq("Where in the pipeline should model artefacts be signed?",
        ["At the end of CI, with a key held in a secured signing service (HSM or KMS), before the artefact enters the registry",
         "On each device, after download",
         "By the engineer on their laptop, with a key in the repository",
         "Signing is not needed if the download uses HTTPS"], 0,
        "Who must never hold the private key?",
        "Signing once in a controlled CI step means every device can verify with the public key. A key on a laptop or in the repo is one leak away from attackers signing their own firmware. HTTPS protects the transfer, not the artefact sitting on a CDN or in a cache.",
        topic="cicd", level=3,
        diagram="""
 CI: build -> test -> SIGN (HSM key)
                        |
 registry (staging -> production)
                        |
 device: download -> VERIFY (public key) -> install
"""),
]
