<img src="assets/masthead.svg" alt="The Incredible Ronil Basu, Issue 27. Data science and AI, Rutgers 2027. Now with a game." width="880">

Data science and statistics at Rutgers, class of 2027. I build things that run on my own hardware,
mostly local models and tools I actually use.

[ron2k1.github.io](https://ron2k1.github.io) · [LinkedIn](https://www.linkedin.com/in/ronil-basu)

## Play me

<!-- c4:start -->
Red is you. Tap a column to drop.

<a href="https://github.com/ron2k1/ron2k1/issues/new?title=c4%7Cdrop%7C1&body=Press%20Submit%20new%20issue.%20The%20bot%20answers%20here%20within%20a%20minute."><img src="assets/drop-1.svg" width="14%" alt="Drop in column 1"></a><a href="https://github.com/ron2k1/ron2k1/issues/new?title=c4%7Cdrop%7C2&body=Press%20Submit%20new%20issue.%20The%20bot%20answers%20here%20within%20a%20minute."><img src="assets/drop-2.svg" width="14%" alt="Drop in column 2"></a><a href="https://github.com/ron2k1/ron2k1/issues/new?title=c4%7Cdrop%7C3&body=Press%20Submit%20new%20issue.%20The%20bot%20answers%20here%20within%20a%20minute."><img src="assets/drop-3.svg" width="14%" alt="Drop in column 3"></a><a href="https://github.com/ron2k1/ron2k1/issues/new?title=c4%7Cdrop%7C4&body=Press%20Submit%20new%20issue.%20The%20bot%20answers%20here%20within%20a%20minute."><img src="assets/drop-4.svg" width="14%" alt="Drop in column 4"></a><a href="https://github.com/ron2k1/ron2k1/issues/new?title=c4%7Cdrop%7C5&body=Press%20Submit%20new%20issue.%20The%20bot%20answers%20here%20within%20a%20minute."><img src="assets/drop-5.svg" width="14%" alt="Drop in column 5"></a><a href="https://github.com/ron2k1/ron2k1/issues/new?title=c4%7Cdrop%7C6&body=Press%20Submit%20new%20issue.%20The%20bot%20answers%20here%20within%20a%20minute."><img src="assets/drop-6.svg" width="14%" alt="Drop in column 6"></a><a href="https://github.com/ron2k1/ron2k1/issues/new?title=c4%7Cdrop%7C7&body=Press%20Submit%20new%20issue.%20The%20bot%20answers%20here%20within%20a%20minute."><img src="assets/drop-7.svg" width="14%" alt="Drop in column 7"></a>
<img src="game/board-1.svg" alt="Connect Four, game 1, move 2, red to play" width="100%">

Red to play · Last move by @ron2k1 · Humans 0, bot 0, draws 0 · Most moves: @ron2k1 (1)

<img src="game/hall-1.svg" alt="Beat the bot: nobody yet. No game finished yet." width="100%">
<!-- c4:end -->

Tap a column and press Submit on the issue it opens. Give it a minute, then refresh. I cap the bot
at two seconds a move. The engine is in [connect4/](connect4/).

## Hot off the press

### [claude-code-structured-concurrency](https://github.com/ron2k1/claude-code-structured-concurrency)

Kills orphan Claude Code process trees at the kernel level on Windows and Linux, with a watchdog
on macOS, so a dead session never leaves forty node processes behind.

`PowerShell` `bash` `Win32 Job Objects` `cgroups`

### [marginalia](https://github.com/ron2k1/marginalia)

Turns a PDF into notes pinned to the exact sentence they came from. Click a note and the page
scrolls to it. Runs fully offline on a local model.

`FastAPI` `React` `PyMuPDF` `Ollama`

### Courtside

NBA player-prop forecasting engine, in paper trading. Methodology and walk-forward results are in
[courtside-showcase](https://github.com/ron2k1/courtside-showcase). The engine is private.

`Python` `XGBoost` `probability calibration`

## Hackathons

### [Intuit TechWeek SMB Underwriting](https://github.com/ron2k1/intuit-techweek-smb-underwriting)

**2nd place · Intuit HQ, NY Tech Week 2026**

An AI that decides which small-business loans are safe to fund, on a loan book seeded with
selection bias and label leakage. I owned the feature pipeline and the approval policy.

`scikit-learn` `probability calibration` `causal inference` `survival analysis`

### StormLink

**Best Use of ElevenLabs · HackUSF 2026**

We routed live storm data through Google ADK agents into voice alerts for people in the path. I
built the panel that shows the agents working.

`Google ADK` `ElevenLabs` `Next.js` `FastAPI` `Leaflet`

## Open source

### [spotify-cleaner](https://github.com/ron2k1/spotify-cleaner)

Finds the songs you never play and clears them out of your Spotify library. Dry run by default,
and deleting anything means typing DELETE first.

`Python` `spotipy` `FastAPI` `React` · MIT

### [Cluely](https://github.com/ron2k1/Ronils-Cluely-OPENSOURCE)

A meeting overlay for Windows that transcribes live and answers from a local Claude CLI, invisible
to screen share.

`Python` `PySide6` `faster-whisper` `Win32` · Apache-2.0

### [Crash](https://github.com/ron2k1/crash-app)

A desktop marketplace where humans and AI agents buy, sell, and bid in one live room. Agents pay
for their own tool calls over a real x402 USDC rail.

`Tauri 2` `React 19` `react-three-fiber` `Rust` `x402` · MIT

## The toolbelt

<img src="assets/toolbelt.svg" alt="Languages: Python, Java, C++, TypeScript, JavaScript, Go, SQL, R, Rust, Bash, PowerShell. Frameworks and libraries: FastAPI, React, Next.js, Node.js, PyTorch, scikit-learn, XGBoost, LightGBM, pandas, NumPy, SciPy, statsmodels, LangChain, Hugging Face Transformers, Sentence Transformers. Developer tools and cloud: Git, GitHub Actions, CI/CD, Docker, Linux, AWS, Google Cloud, Railway, PostgreSQL, pgvector, SQLite, Redis, Supabase, pytest, REST APIs. Machine learning and data: RAG, semantic search, vector databases, agentic AI, multiagent systems, Google ADK, A2A, MCP, LLM finetuning, LoRA and PEFT, vLLM, TRL, bitsandbytes, prompt engineering, LLM evaluation, ETL, data pipelines, feature engineering, model calibration, time series validation." width="880">

<img src="assets/stats.svg" alt="Four counters: public repos, contributions in the past year, hackathon awards, AI roles. Refreshed nightly from the GitHub API." width="880">

SIE certified, FINRA, Sep 2025.

## Building in private

### InternPilot

Scrapes 13 job sources, scores postings against my resume, fills ATS forms with Playwright, and
drafts cover letters on a local LLM.

### nemotron-reasoning-challenge

A daemon that generates math reasoning data, fine-tunes with QLoRA and GRPO, evaluates on vLLM,
and submits to Kaggle on its own.

## Say hi

[LinkedIn](https://www.linkedin.com/in/ronil-basu) is fastest. The longer story is at
[ron2k1.github.io](https://ron2k1.github.io).
