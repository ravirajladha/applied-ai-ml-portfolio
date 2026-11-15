"""
labkit.py — ONE portable bootstrap for every LLM lab notebook.

WHY THIS EXISTS
    The labs must run unchanged on Colab and Kubeflow. Each puts persistent
    storage, the GPU, and the pre-installed packages in a *different* place.
    When every notebook detects all that on its own, they drift apart (which is
    exactly what happened). Here it is decided once; notebooks just read the
    answers back.

STANDARD FIRST CELL (identical in every notebook)
    import labkit
    L = labkit.setup()                 # env + HF cache + device + dtype + paths
    labkit.ensure({"trl": "trl==0.12.1"})   # install ONLY if missing (never upgrades)

    # then use:  L.DEVICE  L.DTYPE  L.CACHE_ROOT  L.WORK_DIR  L.IS_GPU  L.GPU_MEM_GB

STANDARD MODEL LOAD (identical in every notebook)
    tokenizer, model = labkit.load_model("Qwen/Qwen2.5-0.5B-Instruct")
    # cache-first: loads from L.CACHE_ROOT, downloads only on a cache miss

STANDARD GENERATE CALL
    output_ids = model.generate(**inputs, **labkit.gen_kwargs(tokenizer, 250, temperature))
    # greedy when temperature == 0, without the "temperature is set" warnings

ORDER MATTERS
    setup() sets HF_HOME, which Hugging Face reads only at import time. So call
    setup() BEFORE importing transformers/datasets/trl. Put it in cell 1.

UNITS
    All sizes are reported in GiB (2**30 bytes), so an "80 GB" A100 shows ~79.3,
    not 85.0. VRAM and disk figures are therefore directly comparable.
"""

from __future__ import annotations
import os, sys, shutil, subprocess, importlib.util
from types import SimpleNamespace

_STATE: SimpleNamespace | None = None   # filled by setup(), reused by helpers
_GiB = 2 ** 30


# --------------------------------------------------------------------------
# 1. Where are we running? Signals, most specific first.
# --------------------------------------------------------------------------
# Only two backends are supported: Colab and Kubeflow. `local` is a bare
# safety fallback so setup() never crashes if run somewhere unexpected.
def detect_env() -> str:
    if importlib.util.find_spec("google.colab") is not None:
        return "colab"
    if "NB_PREFIX" in os.environ or "KUBERNETES_SERVICE_HOST" in os.environ \
       or os.path.isdir("/home/jovyan/data"):
        return "kubeflow"
    return "local"


# Per-env PERSISTENT root — the volume that survives a restart. Big caches and
# training outputs go here. Order in each list = preference; first writable one
# wins, else we fall back to cwd.
_PERSIST_ROOTS = {
    "colab":    ["/content"],                                    # ephemeral — wiped each session; models re-download (no Drive space used)
    "kubeflow": ["/home/jovyan/data"],                           # NFS volume — persists across pod restarts
    "local":    [os.path.expanduser("~/lab-data"), os.getcwd()], # bare fallback only
}


def _first_writable(paths) -> str:
    for p in paths:
        try:
            os.makedirs(p, exist_ok=True)
            t = os.path.join(p, ".labkit_write_test")
            open(t, "w").close(); os.remove(t)
            return p
        except Exception:
            continue
    return os.getcwd()   # last resort: always writable


# --------------------------------------------------------------------------
# 2. setup() — the one call every notebook makes.
# --------------------------------------------------------------------------
def setup(quiet_logs: bool = True) -> SimpleNamespace:
    """Detect env (Colab or Kubeflow), point the HF cache at the right place,
    resolve device/dtype.

    On Colab the cache is the ephemeral /content disk on purpose: models
    re-download each session and use NO Google Drive space. (Mount Drive in the
    notebook's first cell only so `import labkit` can find labkit.py — not for
    the cache.) On Kubeflow the cache lives on the persistent ~/data volume.
    """
    global _STATE
    env = detect_env()
    root = _first_writable(_PERSIST_ROOTS[env])

    # HF cache -> <root>/hf-cache. Set BEFORE any transformers import.
    cache_root = os.path.join(root, "hf-cache")
    os.environ["HF_HOME"]           = cache_root
    os.environ["HF_DATASETS_CACHE"] = os.path.join(cache_root, "datasets")
    os.makedirs(os.environ["HF_DATASETS_CACHE"], exist_ok=True)

    if quiet_logs:
        os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
        os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
        os.environ.setdefault("HF_HUB_VERBOSITY", "error")
        os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

    # Device + dtype. Import torch lazily so `import labkit` stays cheap.
    device, dtype, gpu_name, gpu_mem = "cpu", "float32", None, 0.0
    try:
        import torch
        if torch.cuda.is_available():
            device = "cuda"
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = round(torch.cuda.get_device_properties(0).total_memory / _GiB, 1)
            # bf16 is numerically safer than fp16 for Qwen/Llama; use it when supported.
            dtype = "bfloat16" if torch.cuda.is_bf16_supported() else "float16"
        elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            device, dtype = "mps", "float16"   # Apple Silicon
    except Exception:
        pass

    _STATE = SimpleNamespace(
        ENV=env, PERSIST_ROOT=root, CACHE_ROOT=cache_root,
        WORK_DIR=os.path.join(root, "lab-work"),
        DEVICE=device, DTYPE=dtype, IS_GPU=(device == "cuda"),
        GPU_NAME=gpu_name, GPU_MEM_GB=gpu_mem,
    )
    os.makedirs(_STATE.WORK_DIR, exist_ok=True)

    gpu_str = f"{gpu_name} ({gpu_mem} GiB)" if gpu_name else "none"
    print(f"env={env}  device={device}  dtype={dtype}  gpu={gpu_str}")
    print(f"persistent root : {root}" + ("   (ephemeral on Colab)" if env == "colab" else ""))
    print(f"HF cache        : {cache_root}")
    return _STATE


def _require_setup() -> SimpleNamespace:
    if _STATE is None:
        raise RuntimeError("Call labkit.setup() first (in cell 1).")
    return _STATE


# --------------------------------------------------------------------------
# 3. ensure() — install ONLY what's missing; never upgrade.
#    Unifies the three different install cells. On Kubeflow (setup_env.sh
#    already ran) every package is present, so this is a no-op — which respects
#    the "additive installs OK, upgrades not" rule of the pinned venv.
# --------------------------------------------------------------------------
def ensure(packages: dict[str, str]) -> None:
    """packages: {importable_module_name: pip_spec}, e.g. {"faiss": "faiss-cpu==1.9.0"}."""
    missing = [spec for mod, spec in packages.items()
               if importlib.util.find_spec(mod) is None]
    if not missing:
        print("deps: all present (no install needed)")
        return
    print("deps: installing", ", ".join(missing))
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", *missing], check=True)


# --------------------------------------------------------------------------
# 4. Model loading + generation helpers (shared by every notebook).
# --------------------------------------------------------------------------
def load_model(name: str, token: str | None = None, **model_kwargs):
    """Cache-first load of a causal LM + its tokenizer.

    1. Try local_files_only=True against L.CACHE_ROOT — no network, instant on
       Kubeflow once the model is cached on ~/data.
    2. On a cache miss, download once into the same cache.

    dtype/device come from setup() (L.DTYPE, device_map="auto"); anything in
    model_kwargs overrides them (e.g. quantization_config=... for QLoRA).
    Returns (tokenizer, model) with model already in eval() mode.
    """
    s = _require_setup()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    kw = dict(torch_dtype=getattr(torch, s.DTYPE), device_map="auto")
    kw.update(model_kwargs)

    try:
        tok = AutoTokenizer.from_pretrained(name, token=token, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(name, token=token, local_files_only=True, **kw)
        source = "cache"
    except (OSError, ValueError):
        print(f"{name}: not in cache — downloading to {s.CACHE_ROOT} (first run only"
              + (", every session on Colab" if s.ENV == "colab" else "") + ") ...")
        tok = AutoTokenizer.from_pretrained(name, token=token)
        model = AutoModelForCausalLM.from_pretrained(name, token=token, **kw)
        source = "download"

    model.eval()
    print(f"{name}: loaded from {source} on {model.device} ({s.DTYPE})")
    return tok, model


def gen_kwargs(tokenizer, max_new_tokens: int = 250, temperature: float = 0.0, **extra) -> dict:
    """Generation kwargs that behave correctly for both greedy and sampled decoding.

    Many instruct checkpoints (Qwen, Llama) ship a generation_config with
    temperature/top_p/top_k preset. With do_sample=False those trigger
    "`do_sample` is set to `False`. However, `temperature` is set..." warnings.
    For greedy decoding we explicitly null them out, which silences the warnings
    without changing the output.
    """
    do_sample = temperature > 0
    kw = dict(max_new_tokens=max_new_tokens, do_sample=do_sample,
              pad_token_id=tokenizer.eos_token_id)
    if do_sample:
        kw["temperature"] = temperature
    else:
        kw.update(temperature=None, top_p=None, top_k=None)
    kw.update(extra)
    return kw


# --------------------------------------------------------------------------
# 5. Small helpers notebooks were hardcoding.
# --------------------------------------------------------------------------
def by_hardware(gpu_choice, cpu_choice):
    """Pick a model (or anything) by available hardware. Replaces the scattered
    `"...-3B" if DEVICE=="cuda" else "...-0.5B"` lines."""
    return gpu_choice if _require_setup().IS_GPU else cpu_choice


def training_dir(name: str) -> str:
    """A per-lab output_dir on persistent storage. Pair with save_total_limit=1
    in your TrainingArguments/DPOConfig so optimizer-state checkpoints can't pile
    up (that pile-up is what filled 13 GB)."""
    d = os.path.join(_require_setup().WORK_DIR, name)
    os.makedirs(d, exist_ok=True)
    return d


# --------------------------------------------------------------------------
# 6. Disk hygiene — the 15 GB student budget lives or dies here.
# --------------------------------------------------------------------------
def _dir_bytes(path: str) -> int:
    if not os.path.isdir(path):
        return 0
    total = 0
    for dp, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(dp, f)
            try:
                if not os.path.islink(fp):      # HF hub snapshots symlink to blobs; count blobs once
                    total += os.path.getsize(fp)
            except OSError:
                pass
    return total


def _dir_gb(path: str) -> float:
    return round(_dir_bytes(path) / _GiB, 2)


def _cached_models(cache_root: str) -> list[tuple[str, float]]:
    """[(repo_id, GiB)] for every model in the HF hub cache, largest first."""
    hub = os.path.join(cache_root, "hub")
    out = []
    if os.path.isdir(hub):
        for d in os.listdir(hub):
            if d.startswith(("models--", "datasets--")):
                kind, _, rest = d.partition("--")
                repo = rest.replace("--", "/")
                if kind == "datasets":
                    repo = f"[dataset] {repo}"
                out.append((repo, _dir_gb(os.path.join(hub, d))))
    return sorted(out, key=lambda x: -x[1])


def disk_report(budget_gb: float = 15.0) -> None:
    """Read-only: how much of YOUR budget the labs are using.

    The budget is measured as HF cache + lab-work — the two folders labkit
    writes to — NOT the whole volume. On Kubeflow ~/data is a shared NFS mount,
    so shutil.disk_usage reports the entire filesystem (thousands of GB) and is
    meaningless against a 15 GB per-student budget. It is shown for info only.
    """
    s = _require_setup()
    cache_gb = _dir_gb(s.CACHE_ROOT)
    work_gb  = _dir_gb(s.WORK_DIR)
    venv_gb  = _dir_gb(os.path.join(s.PERSIST_ROOT, "venv")) if s.ENV == "kubeflow" else 0.0
    mine     = cache_gb + work_gb + venv_gb

    print(f"labs usage vs {budget_gb:.0f} GB budget: {mine:.2f} GiB  ({100*mine/budget_gb:.0f}%)")
    print(f"  HF cache : {cache_gb:.2f} GiB   ({s.CACHE_ROOT})")
    for repo, gb in _cached_models(s.CACHE_ROOT):
        print(f"      {gb:6.2f}  {repo}")
    print(f"  lab work : {work_gb:.2f} GiB   ({s.WORK_DIR})")
    if s.ENV == "kubeflow":
        print(f"  venv     : {venv_gb:.2f} GiB")

    try:
        fs = shutil.disk_usage(s.PERSIST_ROOT)
        note = "shared volume, info only" if s.ENV == "kubeflow" else "info only"
        print(f"  (filesystem free: {fs.free/_GiB:.1f} GiB — {note})")
    except OSError:
        pass

    if mine > 0.9 * budget_gb:
        print(f"  ⚠ over 90% of your {budget_gb:.0f} GB budget.")
        if work_gb >= cache_gb:
            print("    Training output is the bulk -> run labkit.cleanup().")
        else:
            print("    Model cache is the bulk -> remove models you no longer need with")
            print("    labkit.remove_model('<repo_id>')  (e.g. one listed above).")


def cleanup() -> None:
    """Free this lab's TRAINING output — the checkpoint/optimizer-state folders that
    a run writes fresh each time (this is what overflows a 15 GB volume).

    The model cache is deliberately NOT touched: load_model() is cache-first
    (local_files_only=True, download only on a miss), so the cache is a re-usable
    asset, not garbage. To drop a specific model, use remove_model()."""
    s = _require_setup()
    freed = _dir_gb(s.WORK_DIR)
    shutil.rmtree(s.WORK_DIR, ignore_errors=True)
    os.makedirs(s.WORK_DIR, exist_ok=True)
    print(f"cleaned training output at {s.WORK_DIR}  (~{freed:.2f} GiB freed; model cache kept)")


def remove_model(repo_id: str) -> None:
    """Delete ONE model from the HF cache (it re-downloads if a lab needs it again)."""
    s = _require_setup()
    d = os.path.join(s.CACHE_ROOT, "hub", "models--" + repo_id.replace("/", "--"))
    if not os.path.isdir(d):
        print(f"{repo_id}: not in cache ({d})")
        return
    freed = _dir_gb(d)
    shutil.rmtree(d, ignore_errors=True)
    print(f"removed {repo_id} from cache (~{freed:.2f} GiB freed)")
