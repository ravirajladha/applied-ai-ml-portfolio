# 7. Setup

Every command here was run and verified on the development machine, not copied
from a vendor's documentation. Where something failed the first time, the note
says so — those are the parts most likely to bite you too.

The reasoning behind these choices is in
[ADR-0007](06-decisions.md#adr-0007--development-environment-on-windows-arm64)
and [ADR-0008](06-decisions.md#adr-0008--split-the-repository-across-three-locations).

---

## What you need

- **Disk:** roughly 6 GB for the environment, plus 2–3 GB for the dataset and
  the offline store. They do not have to be on the same drive.
- **A Linux environment.** On Windows that means WSL2. Everything below assumes
  Ubuntu 24.04 LTS.

> **If you are on Windows ARM64, read this first.** Several core packages —
> `pyarrow`, `lightgbm`, `confluent-kafka`, `mlflow`, `fastparquet` — publish no
> wheels for native ARM64 Windows Python. They fall back to a source build and
> fail. This is not a version-pinning problem and cannot be worked around with
> flags. WSL2 is the fix, because linux-aarch64 wheels do exist for all of them.

---

## 1. WSL2 and Ubuntu

```powershell
wsl --version                          # confirm WSL is present
wsl --install -d Ubuntu-24.04 --no-launch
```

`--no-launch` skips the interactive account prompt, which is what you want when
scripting. Create the account afterwards:

```bash
wsl -d Ubuntu-24.04 -u root -- bash -lc '
  useradd -m -s /bin/bash YOURNAME
  usermod -aG sudo YOURNAME
  printf "[user]\ndefault=YOURNAME\n\n[boot]\nsystemd=true\n" > /etc/wsl.conf
'
wsl --shutdown        # required for /etc/wsl.conf to take effect
```

`systemd=true` matters — Redis and Redpanda are managed as systemd services
below, and without it neither will start.

Set a password when convenient, since `sudo` will ask for one:

```bash
wsl -d Ubuntu-24.04 -u root -- passwd YOURNAME
```

## 2. System packages

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  git curl ca-certificates redis-server libgomp1
```

`libgomp1` is not optional and is easy to miss. LightGBM's wheel links against
the OpenMP runtime, and without it `import lightgbm` fails at load time with
`OSError: libgomp.so.1: cannot open shared object file` — which looks like a
broken install rather than a missing system library.

## 3. Redpanda

```bash
curl -sS "https://dl.redpanda.com/nzc4ZYQK3WRGd9sy/redpanda/cfg/setup/bash.deb.sh" -o ~/rp.sh
sudo bash ~/rp.sh
sudo apt-get install -y redpanda
```

Configure it as a single-node development cluster on port 19092, matching the
port used in `docker-compose.yml` so client configuration is identical either
way:

```bash
sudo rpk redpanda mode development
sudo rpk redpanda config set redpanda.kafka_api            "[{address: 0.0.0.0, port: 19092}]" --format yaml
sudo rpk redpanda config set redpanda.advertised_kafka_api "[{address: localhost, port: 19092}]" --format yaml
sudo systemctl enable --now redpanda
sudo systemctl restart redpanda
```

**The restart is not redundant.** Installing the package starts Redpanda
immediately with its default configuration, so it is already listening on 9092
before you change anything. `systemctl enable --now` on a running service does
nothing, and you are left with a healthy-looking service on the wrong port and a
client that cannot connect. Restart, or the config change never takes effect.

Verify:

```bash
sudo systemctl start redis-server
redis-cli ping                              # PONG
rpk cluster health -X brokers=localhost:19092   # Healthy: true
```

Note `-X brokers=...`, not `--brokers`; the flag was renamed.

## 4. Python environment

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

Keep the virtual environment on the Linux filesystem even though the code lives
on the Windows drive — a venv is thousands of small files, which is the slowest
possible case for the WSL translation layer:

```bash
export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/rtfd"
cd /mnt/c/dev/ai-ml/software-engineering-for-machine-learning/projects/realtime-fraud-detection
uv sync --all-extras --dev
```

Add both exports to `~/.bashrc` so they survive a new shell.

## 5. Where the data goes

The dataset and the offline store need a few gigabytes. If your system drive is
short of space, point them elsewhere — in this setup, a second partition:

```bash
cp .env.example .env
```

```ini
RTFD_DATA_DIR=/mnt/a/rtfd-data
```

`raw_dir` and `offline_dir` follow `RTFD_DATA_DIR` automatically. Setting
`RTFD_DATA_DIR` alone is enough.

## 6. Kaggle credentials

Needed once, to download the dataset:

1. Sign in at kaggle.com → Settings → API → **Create New Token**
2. Save the downloaded `kaggle.json` to `~/.kaggle/kaggle.json` **inside WSL**
3. `chmod 600 ~/.kaggle/kaggle.json`

## 7. Check it works

```bash
uv run pytest -q                # 27 passing
uv run ruff check src tests
uv run mypy
uv run rtfd-download            # ~470 MB
uv run rtfd-profile             # writes reports/dataset-profile.md
```

---

## Gotchas found the hard way

**Git Bash mangles Unix paths passed to `wsl.exe`.** Running
`wsl.exe -d Ubuntu-24.04 -- bash -lc 'curl -o /tmp/x ...'` from Git Bash on
Windows silently rewrites `/tmp/x` into a Windows path, and the command fails
with a confusing "No such file or directory". Prefix the call with
`MSYS_NO_PATHCONV=1`, or use PowerShell.

**Two Python environments will diverge.** An earlier Windows-side virtual
environment had a different `ruff` version to the WSL one, and the two disagreed
about formatting — so `ruff format --check` passed in one and failed in the
other. The Windows environment was deleted. There is one environment, and
`uv.lock` pins the tool versions.

**Line endings.** Git on Windows converts to CRLF, git in WSL does not. Without
`.gitattributes` enforcing LF, files rewritten from one side appear as
whole-file diffs on the other.

**`0.0.0.0` in listener config.** Redpanda's `advertised_kafka_api` must be an
address a client can actually resolve. Advertising `0.0.0.0` produces a broker
that accepts the connection, hands back an unusable address, and then appears to
hang — the single most common Kafka setup failure.

---

Back to: [README](../README.md)
