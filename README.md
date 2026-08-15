**Data Science major, Statistics minor -- Rutgers University, New Brunswick.**

I build systems where models meet infrastructure. Python for the modeling, Rust for the hot path,
local LLMs for the reasoning layer. Most of what is below runs on my own hardware with no paid API in
the loop.

[ron2k1.github.io](https://ron2k1.github.io) · [LinkedIn](https://www.linkedin.com/in/ronil-basu)

---

## Selected work

### [claude-code-structured-concurrency](https://github.com/ron2k1/claude-code-structured-concurrency)

Cross-platform reaper for orphan Claude Code process trees. Kernel-enforced cleanup on wrapper exit
rather than a best-effort kill loop.

Windows uses a Win32 Job Object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Linux uses
`systemd-run --user --scope` with `cgroup.kill` on kernel 5.14+, falling back to `setpgid` plus a
bash trap on older kernels and WSL1. macOS is supported at a documented ceiling -- `setpgid` and a
disowned out-of-process watchdog -- pinned by a negative test that proves the failure mode instead of
hiding it.

- **Windows** -- Win32 Job Object, STRONG, 3-9 ms reap latency
- **Linux** -- systemd scope + `cgroup.kill` on 5.14+, `setpgid` fallback for no-systemd and WSL1
- **macOS** -- `setpgid` + disowned watchdog, MEDIUM, honest ceiling pinned by a negative test
- **Shape** -- diagnose orphans, reap with a config-driven predicate, or wrap Claude Code in a
  kernel-enforced job

78 tests across PowerShell and bash, CI matrix on all three platforms.

`PowerShell` `bash` `Win32` `cgroups` `systemd`

### [marginalia](https://github.com/ron2k1/marginalia)

Local-first PDF-to-notes app where every note is pinned to the sentence it came from.

Reads a PDF section by section and streams structured notes over SSE from a local Ollama model, so
there is no API key and nothing leaves the machine. Every note carries an anchor chip: click the card
and the PDF scrolls to the matched passage and flashes it. The resolver tries an exact text match,
falls back to fuzzy matching when the wording drifts, and degrades honestly to page-level anchoring
with the chip telling you which happened. Notes export to wide-margin or Cornell print layouts for
copying out longhand.

- **Anchoring** -- exact, then fuzzy, then page-only. Coordinates normalized to the page, so anchors
  survive zoom and resize
- **Generation** -- local Ollama (`qwen2.5:7b`) streamed over SSE, detail dial from Concise to
  Thorough
- **Testing** -- hermetic Playwright e2e suite that boots its own MockDriver backend on scratch ports

`FastAPI` `SQLModel` `PyMuPDF` `React` `TypeScript` `pdf.js` `Ollama`

### Courtside -- NBA player-prop forecasting engine

Public methodology and validated walk-forward results live in
[courtside-showcase](https://github.com/ron2k1/courtside-showcase). Engine source private.

In paper trading and approaching go-live. Covers projection modeling, a multi-book line sweep,
probability calibration, an 8-layer signal gate, backtesting against 9.1M odds snapshots, and
CLV-tracked paper trading. `FastRust` is a companion Rust compute engine over PyO3 that takes the
hot-path EV math with GIL-releasing batch parallelism, drop-in replaceable with the Python
`compute_ev()`.

- **Calibration** -- temperature scaling + isotonic regression, per stat and per side, walk-forward
  isolated
- **Signal gate** -- 8 independent vetoes: edge floor, CLV gate, stat whitelist, bin blocking,
  confidence floor, sample gate, hit-rate check, real-line requirement
- **Data** -- 877K closing lines, 9.1M NBA snapshots, 3 full seasons
- **Rust layer** -- PyO3 0.22, rayon batch API

`Python` `Rust` `PyO3` `XGBoost` `isotonic regression` `walk-forward backtesting`

### [ClawWorld](https://github.com/ron2k1/ClawWorld)

Tile-based RPG where every NPC is a live AI agent.

Rendering engine written from scratch -- no Phaser, no Pixi -- with `A*` pathfinding, 4-directional
sprite animation, and map transitions. 10 NPCs each route to their own provider (Anthropic, xAI,
Ollama, or a local subprocess). Agents consult each other mid-conversation through tool-call
delegation, so world state is shaped by inter-agent negotiation rather than scripted dialogue trees.

- **Rendering** -- from-scratch canvas engine, `A*` pathfinding, sprite atlas, map transitions
- **Delegation** -- NPCs consult each other mid-stream via `ask_agent()` tool calls
- **Providers** -- Anthropic, xAI, Ollama, subprocess, over an Ed25519-authed WebSocket gateway

`TypeScript` `Canvas` `WebSocket` `Ed25519`

---

## Hackathons

### [Intuit TechWeek SMB Underwriting](https://github.com/ron2k1/intuit-techweek-smb-underwriting)

**2nd place -- Intuit HQ, NY Tech Week 2026**

Explainable-ML underwriting challenge. We turned calibrated PD models (validation AUROC 0.740) into
expected-NPV approval decisions for 13,306 applicants, forecast how the funded book defaults over 13
weeks, and answered 900 causal what-if queries with per-feature guardrails. The dataset was
booby-trapped with selection bias and label leakage on purpose, and finding those traps was most of
the scoring. I owned the shared feature pipeline and the approval-policy deliverable.

`scikit-learn` `probability calibration` `causal inference` `survival analysis`

### [StormLink](https://github.com/Purabhh/stormlink)

**Best Use of ElevenLabs -- HackUSF 2026**

Multi-agent disaster response dashboard. We routed live NOAA and FEMA feeds through Google ADK agents
over the A2A protocol, with ElevenLabs voice alerts surfacing material weather events in real time. I
wrote the AgentPanel component that visualizes the routing pipeline with animated data packets and
elapsed timers.

`Google ADK` `A2A protocol` `Gemini 2.5 Flash` `ElevenLabs` `Next.js` `FastAPI` `Leaflet`

---

## Open source

### [spotify-cleaner](https://github.com/ron2k1/spotify-cleaner)

CLI and local web UI that finds and removes your least-listened Spotify tracks. Scoring reads your
GDPR data export rather than the Web API, because the API does not expose real per-track play counts.
Dry run is the default, and applying a cut requires typing DELETE.

`Python` `spotipy` `FastAPI` `React` · MIT

### [Cluely](https://github.com/ron2k1/Ronils-Cluely-OPENSOURCE)

Capture-invisible AI meeting overlay for Windows. Live transcription through faster-whisper, answers
from the local Claude CLI, and the window is excluded from screen capture, so it does not appear in a
shared screen or a recording.

`Python` `PySide6` `faster-whisper` `Win32` · Apache-2.0

### [Crash](https://github.com/ron2k1/crash-app)

Desktop agent marketplace where humans and AI agents buy, sell, and bid in one live shared room.
Agents pay for their own tool calls over a real x402 USDC micropayment rail.

`Tauri 2` `React 19` `react-three-fiber` `Rust` `x402` · MIT

---

## Building in private

**InternPilot** -- pipeline that scrapes 13 job sources, scores postings against a resume profile,
auto-fills ATS forms via Playwright across Greenhouse, Workday, Lever, Ashby, iCIMS, and
SmartRecruiters, and drafts cover letters through a local LLM. Currently tracking 127 target firms.
`Python` `Playwright` `Ollama` `FastAPI` `APScheduler`

**nemotron-reasoning-challenge** -- daemon that loops through 10 stages: Claude-powered math CoT
generation, QLoRA SFT via Axolotl, GRPO reinforcement learning, vLLM eval, failure diagnosis, and
Kaggle submission. Deadline-aware strategy that shifted from exploration to exploitation as the June
2026 deadline approached.
`PyTorch` `Axolotl` `trl GRPOTrainer` `vLLM` `Claude API`

---

## Stack

- **Languages** -- Python, Rust, TypeScript, R, SQL, Bash, LaTeX
- **ML / quant** -- XGBoost, LightGBM, scikit-learn, NumPy, SciPy, pandas, isotonic and temperature
  calibration
- **Web** -- React, Next.js, FastAPI, Flask, Vite, Alpine.js
- **Infra / AI** -- PyO3, PostgreSQL, SQLite, Playwright, Ollama, Claude API, Google ADK, Railway
