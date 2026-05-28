<div align="center">

<img src="https://capsule-render.vercel.app/api?type=cylinder&color=gradient&customColorList=12,14,16,18,20&height=230&section=header&text=Ronil%20Basu&fontSize=55&fontColor=FFFFFF&fontAlignY=40&desc=Building%20systems%20that%20turn%20data%20into%20edge.&descSize=18&descColor=E0E0E0&descAlignY=62&animation=scaleIn" width="100%" />

[![GitTok — vertical demo videos of finished GitHub projects](https://dev.gittok.net/og/readme-card.svg)](https://dev.gittok.net/feed)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ronil-basu)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1)
[![Profile Views](https://komarev.com/ghpvc/?username=ron2k1&style=for-the-badge&color=00d9ff)](https://github.com/ron2k1)

</div>

<br/>

> **`Data Science | Statistics | @ Rutgers University, New Brunswick`** -- I build systems where models meet infrastructure. Python for modeling, Rust for the hot path, LLMs for reasoning.

<br/>

## What I'm Building

<div align="center">

### Structured Concurrency

**Cross-platform reaper for orphan Claude Code process trees.**

</div>

Kernel-enforced cleanup on wrapper exit. Windows uses a Win32 Job Object with `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, Linux uses `systemd-run --user --scope` with `cgroup.kill` on kernel 5.14+ and falls back to `setpgid` + a bash trap on older kernels and WSL1. macOS is supported at a documented honesty ceiling using `setpgid` + a disowned out-of-process watchdog, pinned by a negative test that proves the failure mode rather than hides it. 78 tests across PowerShell and bash, CI matrix on all three platforms.

<table><tbody>
<tr><td><b>Windows</b></td><td>Win32 Job Object, STRONG, 3-9ms reap latency</td></tr>
<tr><td><b>Linux</b></td><td>systemd-run scope + cgroup.kill on 5.14+ (STRONG), setpgid fallback for no-systemd / WSL1</td></tr>
<tr><td><b>macOS</b></td><td>setpgid + disowned watchdog, MEDIUM (no Job Object, no cgroup.kill), honest ceiling pinned by a negative test</td></tr>
<tr><td><b>Shape</b></td><td>Diagnose orphans, reap with a config-driven predicate, or wrap Claude Code in a kernel-enforced job</td></tr>
</tbody></table>

<div align="center">

[![claude-code-structured-concurrency](https://img.shields.io/badge/claude--code--structured--concurrency-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1/claude-code-structured-concurrency)
![CI](https://img.shields.io/badge/CI-passing-10B981?style=for-the-badge&logo=githubactions&logoColor=white)

---

</div>

<div align="center">

### GitTok

**Vertical-video PWA for sharing build demos.**

<br/>

[![LIVE at dev.gittok.net](https://img.shields.io/badge/LIVE-dev.gittok.net-FF4081?style=for-the-badge&logo=railway&logoColor=white&labelColor=0D1117)](https://dev.gittok.net)

</div>

15-60 second build demos in a TikTok-style vertical feed for shipped GitHub projects. 33 numbered Postgres migrations behind a Codex adversarial-review CI gate that blocks the PR if a reviewer's findings haven't been answered in the diff. GDPR Article-17 erasure is wired into automated PII drift checks that fail the build if personal data leaks into a new column.

<div align="center">

![migrations](https://img.shields.io/badge/migrations-33_numbered-FF4081?style=flat-square&labelColor=0D1117)
![CI gate](https://img.shields.io/badge/CI_gate-Codex_adversarial-FF4081?style=flat-square&labelColor=0D1117)
![compliance](https://img.shields.io/badge/compliance-GDPR_Article_17-FF4081?style=flat-square&labelColor=0D1117)
![PII drift](https://img.shields.io/badge/PII_drift-blocks_PR-FF4081?style=flat-square&labelColor=0D1117)

<br/>

![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Postgres](https://img.shields.io/badge/Postgres-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)

<br/>

![source-private](https://img.shields.io/badge/source-private-21262D?style=for-the-badge&logo=github&logoColor=888888)

---

</div>

<div align="center">

### FullEV-PropAnalyzer + FastRust

**NBA player-prop EV engine in paper trading, approaching GO-LIVE. Core proprietary.**

</div>

Local prop EV engine covering projection modeling, multi-book line sweep, probability calibration with isotonic regression, 8-layer signal gating, historical backtesting against 9M+ odds snapshots, and CLV-tracked paper trading. `FastRust` is a companion Rust compute engine via PyO3 that handles the hot-path EV math with GIL-releasing batch parallelism, drop-in replaceable with the Python `compute_ev()`.

<table><tbody>
<tr><td><b>Calibration</b></td><td>Temperature scaling + isotonic regression, per-stat per-side, walk-forward isolation</td></tr>
<tr><td><b>Signal gate</b></td><td>8 independent veto conditions: edge floor, CLV gate, stat whitelist, bin blocking, confidence floor, sample gate, hit-rate check, real-line requirement</td></tr>
<tr><td><b>Data</b></td><td>877K closing lines, 9.1M NBA snapshots, 3 full seasons</td></tr>
<tr><td><b>Rust layer</b></td><td>PyO3 0.22, rayon batch API, drop-in replacement for Python compute_ev()</td></tr>
</tbody></table>

<div align="center">

![FullEV-PropAnalyzer](https://img.shields.io/badge/FullEV--PropAnalyzer-00D9FF?style=for-the-badge&logo=github&logoColor=0D1117)
![FastRust](https://img.shields.io/badge/FastRust_(Compute)-DEA584?style=for-the-badge&logo=rust&logoColor=0D1117)
![](https://img.shields.io/badge/core_proprietary-21262D?style=for-the-badge&logo=github&logoColor=888888)

---

</div>

<div align="center">

### ClawWorld

**Tile-based RPG where every NPC is a live AI agent.**

</div>

Wrote the rendering engine from scratch (no Phaser or Pixi) with A* pathfinding, 4-directional sprite animation, and map transitions. 10 NPCs each route to their own LLM provider (Anthropic, xAI, Ollama, or local subprocess). Agents consult each other mid-conversation through tool-call delegation, so the world's state is shaped by inter-agent negotiation, not scripted dialogue trees.

<table><tbody>
<tr><td><b>Rendering</b></td><td>From-scratch canvas engine, A* pathfinding, sprite atlas, map transitions</td></tr>
<tr><td><b>Delegation</b></td><td>NPCs consult each other mid-stream via ask_agent() tool calls</td></tr>
<tr><td><b>Providers</b></td><td>Anthropic, xAI, Ollama, subprocess, Ed25519-authed WebSocket gateway</td></tr>
</tbody></table>

<div align="center">

[![ClawWorld](https://img.shields.io/badge/ClawWorld-10B981?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1/ClawWorld)

---

</div>

## Other Public Work

**[RedLine](https://github.com/ron2k1/RedLine)** -- *SEC filing change detection with local LLM analysis*

Watches any SEC-reporting company on EDGAR. When a new 10-K or 10-Q drops, diffs each section against the prior filing at the sentence level using cosine similarity and greedy bipartite matching, flags material changes against 9 red-flag patterns, and runs risk scoring through a local Ollama model. No paid APIs, no cloud dependencies.

`Python` `Ollama` `EDGAR` `cosine similarity` `bipartite matching`

<br/>

## Hackathons

**[StormLink](https://github.com/Purabhh/stormlink)** -- *Multi-agent disaster response dashboard* (HackUSF 2026, **Best Use of ElevenLabs**)

Co-built a multi-agent platform that routes live NOAA and FEMA feeds through Google ADK agents over the A2A protocol, with ElevenLabs voice alerts surfacing material weather events in real time. Wrote the AgentPanel component that visualizes the routing pipeline with animated data packets and elapsed timers.

`Google ADK` `A2A protocol` `Gemini 2.5 Flash` `ElevenLabs` `Next.js 16` `FastAPI` `Leaflet`

<br/>

## Currently Building in Private

**InternPilot** -- *Automated job application pipeline*

Pipeline that scrapes 13 job sources (JSearch, Greenhouse, Lever, Indeed, LinkedIn, Handshake, and more), scores postings against a resume profile, auto-fills ATS forms via Playwright across Greenhouse, Workday, Lever, Ashby, iCIMS, and SmartRecruiters, and drafts cover letters through a local LLM. Currently tracking 127 target firms.

`Python` `Playwright` `Ollama` `FastAPI` `APScheduler`

**nemotron-reasoning-challenge** -- *Autonomous fine-tuning pipeline*

Daemon that loops through 10 stages: Claude-powered math CoT generation, QLoRA SFT via Axolotl, GRPO reinforcement learning, vLLM eval, failure diagnosis, and Kaggle submission. Deadline-aware strategy that shifts from exploration to exploitation as the June 2026 deadline approaches.

`PyTorch` `Axolotl` `trl GRPOTrainer` `vLLM` `Claude API`

<br/>

## Tech Stack

<div align="center">

**`Languages`**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=flat-square&logo=r&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=flat-square&logo=latex&logoColor=white)

**`ML / Quant`**

![XGBoost](https://img.shields.io/badge/XGBoost-189FDD?style=flat-square&logo=xgboost&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-02569B?style=flat-square&logo=lightgbm&logoColor=white)
![scikit--learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

**`Web / Backend`**

![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Alpine.js](https://img.shields.io/badge/Alpine.js-8BC0D0?style=flat-square&logo=alpinedotjs&logoColor=black)

**`Infrastructure & AI`**

![PyO3](https://img.shields.io/badge/PyO3-000000?style=flat-square&logo=rust&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white)
![Claude](https://img.shields.io/badge/Claude_API-D97757?style=flat-square&logo=anthropic&logoColor=white)
![Google ADK](https://img.shields.io/badge/Google_ADK-4285F4?style=flat-square&logo=google&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)

</div>

<br/>

<!-- Contribution snake -->
<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ron2k1/ron2k1/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/ron2k1/ron2k1/output/github-snake.svg" />
  <img alt="github-snake" src="https://raw.githubusercontent.com/ron2k1/ron2k1/output/github-snake-dark.svg" />
</picture>

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00D9FF,50:161B22,100:0D1117&height=120&section=footer" width="100%" />
