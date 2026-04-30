<div align="center">

<img src="https://capsule-render.vercel.app/api?type=cylinder&color=gradient&customColorList=12,14,16,18,20&height=230&section=header&text=Ronil%20Basu&fontSize=55&fontColor=FFFFFF&fontAlignY=40&desc=Building%20systems%20that%20turn%20data%20into%20edge.&descSize=18&descColor=E0E0E0&descAlignY=62&animation=scaleIn" width="100%" />

[![GitTok — vertical demo videos of finished GitHub projects](https://dev.gittok.net/og/readme-card.svg)](https://dev.gittok.net/feed)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ronil-basu)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1)
[![Profile Views](https://komarev.com/ghpvc/?username=ron2k1&style=for-the-badge&color=00d9ff)](https://github.com/ron2k1)

</div>

<br/>

> **`Economics | Statistics | Data Science | @ Rutgers University, New Brunswick`** -- I build data-driven systems across sports analytics, ML, and multi-agent infrastructure. Python for modeling, Rust for performance, LLMs for reasoning.

<br/>

## What I'm Working On

<div align="center">

### FullEV-PropAnalyzer + FastRust

**NBA player-prop EV engine in paper trading, approaching GO-LIVE.**

</div>

Local prop EV engine covering projection modeling, multi-book line sweep, probability calibration with isotonic regression, 8-layer signal gating, historical backtesting against 9M+ odds snapshots, and CLV-tracked paper trading. `FastRust` is a companion Rust compute engine via PyO3 that handles the hot-path EV math with GIL-releasing batch parallelism.

<table><tbody>
<tr><td><b>Calibration</b></td><td>Temperature scaling + isotonic regression, per-stat per-side, walk-forward isolation</td></tr>
<tr><td><b>Signal gate</b></td><td>8 independent veto conditions: edge floor, CLV gate, stat whitelist, bin blocking, confidence floor, sample gate, hit-rate check, real-line requirement</td></tr>
<tr><td><b>Data</b></td><td>877K closing lines · 9.1M NBA snapshots · 3 full seasons</td></tr>
<tr><td><b>Rust layer</b></td><td>PyO3 0.22 · rayon batch API · drop-in replacement for Python compute_ev()</td></tr>
</tbody></table>

<div align="center">

![FullEV-PropAnalyzer](https://img.shields.io/badge/FullEV--PropAnalyzer-00D9FF?style=for-the-badge&logo=github&logoColor=0D1117)
![FastRust](https://img.shields.io/badge/FastRust_(Compute)-DEA584?style=for-the-badge&logo=rust&logoColor=0D1117)
![](https://img.shields.io/badge/source-private-21262D?style=for-the-badge&logo=github&logoColor=888888)

---

</div>

<div align="center">

### ClawWorld + OpenClaw

**Tile-based RPG where every NPC is a live AI agent.**

</div>

Built the rendering engine from scratch (no Phaser or Pixi) with A* pathfinding, 4-directional sprite animation, and map transitions. 10 NPCs each route to their own LLM provider (Anthropic, xAI, Ollama, or subprocess). Agents can consult each other mid-conversation through tool-call delegation. [OpenClaw](https://github.com/ron2k1/OpenClaw) sits behind the gateway and handles security gating, quality checks, and an 8-layer validation pipeline.

<table><tbody>
<tr><td><b>Delegation</b></td><td>NPCs consult each other mid-stream via ask_agent() tool calls</td></tr>
<tr><td><b>Providers</b></td><td>Anthropic, xAI, Ollama, subprocess, OpenClaw WebSocket (Ed25519 auth)</td></tr>
<tr><td><b>Tests</b></td><td>62 frontend (Vitest) + 213 backend (pytest)</td></tr>
</tbody></table>

<div align="center">

[![ClawWorld](https://img.shields.io/badge/ClawWorld-10B981?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1/ClawWorld)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-161B22?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1/OpenClaw)
![](https://img.shields.io/badge/private_repo-21262D?style=for-the-badge&logo=github&logoColor=888888)

---

### RedLine

**SEC filing change detection with local LLM analysis.**

</div>

Watches any SEC-reporting company on EDGAR. When a new 10-K or 10-Q drops, it diffs each section against the prior filing at the sentence level using cosine similarity and greedy bipartite matching, flags material changes against 9 red-flag patterns, and runs risk scoring through a local Ollama model. No paid APIs, no cloud dependencies.

<table><tbody>
<tr><td><b>Diffing</b></td><td>Sentence-level cosine similarity + greedy bipartite matching</td></tr>
<tr><td><b>Analysis</b></td><td>9 red-flag patterns + local LLM risk scoring via Ollama</td></tr>
<tr><td><b>Tests</b></td><td>172 tests, all external calls mocked</td></tr>
</tbody></table>

<div align="center">

[![RedLine](https://img.shields.io/badge/RedLine-EF4444?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1/RedLine)

---

</div>

## More Projects

**InternPilot** ![](https://img.shields.io/badge/private-21262D?style=flat-square&logo=github&logoColor=888888) -- *Automated job application pipeline*

8-stage pipeline that scrapes 13 job sources (JSearch, Greenhouse, Lever, Indeed, LinkedIn, Handshake, GitHub listings, and more), scores postings against my resume profile, auto-fills ATS forms via Playwright (Greenhouse, Workday, Lever, Ashby, iCIMS, SmartRecruiters), and drafts cover letters through a local LLM. Currently tracking 127 target firms.

`Python` `Playwright` `Ollama` `FastAPI` `APScheduler`

---

**nemotron-reasoning-challenge** ![](https://img.shields.io/badge/private-21262D?style=flat-square&logo=github&logoColor=888888) -- *Autonomous fine-tuning pipeline*

Daemon that loops through 10 stages: Claude-powered math CoT generation, QLoRA SFT via Axolotl, GRPO reinforcement learning, vLLM eval, failure diagnosis, and Kaggle submission. Deadline-aware strategy that shifts from exploration to exploitation as the June 2026 deadline approaches.

`PyTorch` `Axolotl` `trl GRPOTrainer` `vLLM` `Claude API`

---

## Hackathons

**[StormLink](https://github.com/Purabhh/stormlink)** -- *Disaster response dashboard* (HackUSF 2026)

Multi-agent dashboard that routes natural language queries through Google ADK/Gemini to pull live NOAA weather alerts and nearby emergency resources onto a Leaflet map. Built the AgentPanel component that visualizes the routing pipeline with animated data packets and elapsed timers.

`Google ADK` `Gemini 2.5 Flash` `Next.js 16` `FastAPI` `Leaflet`

---

**[DiamondClaws](https://github.com/ron2k1/diamondclaws)** -- *Adversarial equity research simulator* ([MischiefClaw Hack NY](https://nyc.aitinkerers.org/p/evil-clawhack-ny), AI Tinkerers NYC)

Red-team tool that injects documented cognitive biases (Kahneman, Nickerson, Weinstein) as deterministic data transformations before routing to LLM sell-side personas. Every response ships with a `distortions_applied` field citing the source papers, so you can see exactly what was warped and why. Built for the "build the worst possible OpenClaw instance" challenge.

`Python` `OpenRouter` `Lightweight Charts` `vanilla JS`

<br/>

## Tech Stack

<div align="center">

**`Languages`**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white)

**`ML / Quant`**

![XGBoost](https://img.shields.io/badge/XGBoost-189FDD?style=flat-square&logo=xgboost&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-02569B?style=flat-square&logo=lightgbm&logoColor=white)
![scikit--learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=flat-square&logo=scipy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)

**`Web / Backend`**

![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Alpine.js](https://img.shields.io/badge/Alpine.js-8BC0D0?style=flat-square&logo=alpinedotjs&logoColor=black)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)

**`Infrastructure & AI`**

![PyO3](https://img.shields.io/badge/PyO3-000000?style=flat-square&logo=rust&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat-square&logo=ollama&logoColor=white)
![Claude](https://img.shields.io/badge/Claude_API-D97757?style=flat-square&logo=anthropic&logoColor=white)
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
