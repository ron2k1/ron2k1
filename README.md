<div align="center">

<img src="https://capsule-render.vercel.app/api?type=cylinder&color=gradient&customColorList=12,14,16,18,20&height=230&section=header&text=Ronil%20Basu&fontSize=55&fontColor=FFFFFF&fontAlignY=40&desc=Building%20systems%20that%20turn%20data%20into%20edge.&descSize=18&descColor=E0E0E0&descAlignY=62&animation=scaleIn" width="100%" />

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

<table>
<tr>
<td width="50%" valign="top">

<div align="center">

**DiamondClaws**

*Cognitive distortion engine for equity research*

</div>

Red-team simulator that injects documented cognitive biases (Kahneman, Nickerson, Weinstein) as **deterministic data transformations** before routing to LLM sell-side personas. Every response includes `distortions_applied` citing the source papers. Ships with a consensus attack simulation that models how coordinated desks manufacture artificial buy-side consensus.

<table><tbody>
<tr><td><b>Interface</b></td><td>Bloomberg-dark UI · Lightweight Charts · vanilla JS</td></tr>
<tr><td><b>Agents</b></td><td>Headmaster + 3 roundtable personas via OpenRouter (200+ models)</td></tr>
<tr><td><b>Audit</b></td><td>Full distortion trail per response: what was warped, how, why</td></tr>
</tbody></table>

<div align="center">

[![DiamondClaws](https://img.shields.io/badge/DiamondClaws-8B5CF6?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1/diamondclaws)

</div>

</td>
<td width="50%" valign="top">

<div align="center">

**ClawWorld** *(private)* + **OpenClaw**

*Tile-based RPG where every NPC is a live AI agent*

</div>

Custom Canvas engine (no Phaser/Pixi) with A* pathfinding, 4-directional animation, map transitions, and 10 AI-powered NPCs routed across Anthropic, xAI, Ollama, and subprocess backends. OpenClaw handles gateway routing with security gating and quality checks.

<table><tbody>
<tr><td><b>Delegation</b></td><td>Multi-agent tool calls: NPCs consult each other mid-stream</td></tr>
<tr><td><b>Memory</b></td><td>Errors feed back into CLAUDE.md primer on next invocation</td></tr>
<tr><td><b>Tests</b></td><td>62 frontend (Vitest) + 213 backend (pytest) + CI</td></tr>
</tbody></table>

<div align="center">

[![ClawWorld](https://img.shields.io/badge/ClawWorld-10B981?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1/ClawWorld)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-161B22?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ron2k1/OpenClaw)

</div>

</td>
</tr>
</table>

<div align="center">

---

</div>

## More Projects

**Numina** ![](https://img.shields.io/badge/private-21262D?style=flat-square&logo=github&logoColor=888888) -- *SEC EDGAR claim verifier*

REST API that runs LLM-generated financial text through extraction and normalization, then verdicts each numeric claim against live XBRL ground truth with accession-level citations. Workspace-scoped multi-tenancy, Redis rate limiting, verified claim fixture suite covering 12 financial metrics across multiple SEC filers.

`FastAPI` `edgartools` `PostgreSQL` `React 19`

---

**[RedLine](https://github.com/ron2k1/RedLine)** -- *SEC filing risk intelligence*

Monitors any SEC-reporting company on EDGAR, runs sentence-level semantic diffing across 10-K/10-Q filings using cosine similarity + greedy bipartite matching, flags material changes with 9 red-flag patterns, and surfaces risk insights through local LLM analysis. 172 tests, zero paid APIs.

`Python` `sentence-transformers` `Ollama` `Flask` `SQLite`

---

**InternPilot** ![](https://img.shields.io/badge/private-21262D?style=flat-square&logo=github&logoColor=888888) -- *Automated job applications*

8-stage pipeline (scrape, enrich descriptions, score, enrich contacts, draft, humanize, apply, track). Scrapes 12+ sources including JSearch, Greenhouse, Lever, Indeed, LinkedIn, Handshake, GitHub job listings, Firecrawl, SpeedyApply, and ZapplyJobs. Scores against a resume profile, drafts cover letters via local LLM, and tracks applications across 127 target firms.

`Python` `Playwright` `Ollama` `FastAPI` `APScheduler`

---

**nemotron-reasoning-challenge** ![](https://img.shields.io/badge/private-21262D?style=flat-square&logo=github&logoColor=888888) -- *Autonomous fine-tuning pipeline*

24/7 daemon looping through 10 stages: Claude-powered math CoT generation, QLoRA SFT via Axolotl, GRPO reinforcement learning, vLLM eval, Claude failure diagnosis, Kaggle submission, repeat. Deadline-aware strategy that shifts from explore to exploit to submit_best as June 2026 approaches.

`PyTorch` `Axolotl` `trl GRPOTrainer` `vLLM` `Claude API`

---

**[StormLink](https://github.com/Purabhh/stormlink)** -- *Disaster response dashboard* (HackUSF 2026)

Multi-agent dashboard routing natural language queries through Google ADK/Gemini to surface live NOAA weather alerts and nearby emergency resources on an interactive Leaflet map. AgentPanel visualizes the routing pipeline with animated data packets and live elapsed timers.

`Google ADK` `Gemini 2.5 Flash` `Next.js 16` `FastAPI` `Leaflet`

---

**vulnerability-radar** ![](https://img.shields.io/badge/private-21262D?style=flat-square&logo=github&logoColor=888888) -- *CVE radar*

FastAPI service that ingests CVEs from NVD API v2.0, scores them with a hand-implemented CVSS v3.1 calculator (validated against Log4Shell, BlueKeep vectors), maps to NIST CSF functions via CWE-to-function lookup, and delivers deduped webhook alerts with exponential-backoff retry. 16 test modules, 366 tests.

`Python` `FastAPI` `asyncpg` `Prometheus` `CVSS v3.1`

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
