# Beat the Bot Wall Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A drawn panel under the Connect Four board that lists every GitHub login whose red drop beat the bot, and says NOBODY YET. until one does.

**Architecture:** One new module `connect4/hall.py` derives everything from `game/state.json` at render time and draws `game/hall-<rev>.svg` with the primitives in `comic/draw.py`. `game.py` records a win in a new `hall` list, `readme.py` emits one more image line, `__main__.py` writes and prunes the file next to the board. No workflow edit.

**Tech Stack:** Python 3.12 stdlib, pytest, fontTools (dev only, for two font-measurement tests).

**Spec:** `docs/superpowers/specs/2026-09-17-beat-the-bot-wall-design.md` (all geometry, strings, and test assertions live there; this plan sequences them).

## Global Constraints

- No em-dash, en-dash, semicolon, or bullet glyph in any drawn or README string (only latin glyphs exist in the embedded font subsets).
- Every string enters an SVG through `D.esc`; logins are re-validated against `^[A-Za-z0-9-]{1,39}$` and fall back to `someone`.
- One hall file per revision in `game/`, like the board. The Action runtime stays stdlib.
- Commits: imperative subject under 70 characters, a why body, no attribution trailers. Run `python -m pytest -q -p no:asyncio` before each commit.
- The c4 region is written only by `connect4/readme.py`; regenerate with `python -m connect4 render` after any change to hall.py.

---

### Task 1: Wall module: strings, login fit, derived state, alt text, and the drawing

**Files:**
- Create: `connect4/hall.py`
- Test: `tests/test_hall.py` (spec tests 1 to 10)

**Interfaces:**
- Consumes: `comic.draw` (`panel`, `chip`, `chip_width`, `shadowed_text`, `star`, `svg`, palette), `state` dicts from `connect4.game.new_state` (reads `state.get("hall", [])` so it works before Task 2 lands).
- Produces: `TITLE, EMPTY_TEXT, INVITE, CHIP_NONE, CHIP_HUMAN, ON_THE_WALL, LOGIN, ADV, LOGIN_X, LABEL_X, AVAIL`, `width(text, size) -> float`, `login_size(login) -> (int, bool)`, `finished_games(state) -> int`, `unbeaten(state) -> int`, `chip_text(state) -> str`, `entries(state) -> list[(rank, by, game_no, moves)]`, `label(state) -> str`, `render_hall(state) -> str`.

- [ ] **Step 1: Write tests 1 to 10 from the spec in `tests/test_hall.py`** (helpers `_texts(svg)` via ElementTree, `_state(hall, game_no, finished, result)`, `_entry(by, game_no, moves)`).
- [ ] **Step 2: Run `python -m pytest -q -p no:asyncio tests/test_hall.py`.** Expected: collection error, `connect4.hall` does not exist.
- [ ] **Step 3: Write `connect4/hall.py`** per spec section 2 and 3. `ADV` is the fontTools extraction (63 login characters plus `@`). `render_hall` draws the empty state when `entries()` is empty, else one row per entry with the rank-1 star drawn before its disc and a rule after every row but the last.
- [ ] **Step 4: Run the file again.** Expected: 10 tests pass (tests 7 and 8 skip if fontTools is missing).
- [ ] **Step 5: Commit** `connect4/hall.py tests/test_hall.py docs/superpowers/specs/2026-09-17-beat-the-bot-wall-design.md docs/superpowers/plans/2026-09-17-beat-the-bot-wall.md` as "Draw the beat-the-bot wall from game state".

### Task 2: Record human wins in the state

**Files:**
- Modify: `connect4/game.py` (`new_state`, `load`, `_finish`, the rollover in `apply_human_move`, the human-win message)
- Test: `tests/test_game.py` (spec tests 13 to 16)

**Interfaces:**
- Consumes: `hall.ON_THE_WALL`.
- Produces: `state["hall"]` list of `{"game_no", "by", "moves"}`; `load()` migrates a state without the key.

- [ ] **Step 1: Add the assert to `test_new_state_shape` and write tests 14 to 16.**
- [ ] **Step 2: Run `tests/test_game.py`.** Expected: 4 failures (KeyError on `hall`, message mismatch).
- [ ] **Step 3: Implement:** `new_state(..., hall=None, ...)` writes `"hall": hall or []`; `load()` calls `state.setdefault("hall", [])`; `_finish` appends the entry when `w == E.RED`; the rollover passes `hall=st["hall"]`; the win message inserts `ON_THE_WALL`.
- [ ] **Step 4: Run the whole suite.** Expected: green.
- [ ] **Step 5: Commit** as "Record every human win in the game state".

### Task 3: Wire the wall into the README region and the file writer

**Files:**
- Modify: `connect4/readme.py` (`hall_path`, `region`), `connect4/__main__.py` (`_write_all`)
- Test: `tests/test_readme.py` (spec test 17), `tests/test_hall.py` (spec test 11)

**Interfaces:**
- Consumes: `hall.label`, `hall.render_hall`.
- Produces: `readme.hall_path(state) -> "game/hall-<rev>.svg"`; the region ends with the wall image line; `_write_all` leaves exactly one `hall-*.svg`.

- [ ] **Step 1: Write tests 17 and 11.**
- [ ] **Step 2: Run them.** Expected: fail (no `hall_path`, no hall file written).
- [ ] **Step 3: Implement** per spec section 3: region appends `\n<img src="{hall_path}" alt="{label}" width="100%">\n`; `_write_all` writes `render_hall(state)` and unlinks other `game/hall*.svg`.
- [ ] **Step 4: Run the suite.** Expected: green except test 12 (not yet written).
- [ ] **Step 5: Commit** as "Show the wall under the board in the README".

### Task 4: Migrate the live state, the slack sentence, and the page-wide lint

**Files:**
- Modify: `README.md` (one sentence), `requirements-dev.txt`, `docs/superpowers/specs/2026-09-17-profile-readme-connect4-design.md`
- Generate: `game/state.json` (+`hall`), `game/hall-1.svg`, README region (via `python -m connect4 render`)
- Test: `tests/test_hall.py` (spec test 12), `tests/test_readme.py` (spec tests 18, 19)

- [ ] **Step 1: Write tests 12, 18, 19.**
- [ ] **Step 2: Run them.** Expected: 12 fails (no hall-1.svg), 18 fails (sentence missing), 19 passes or fails depending on existing assets (fix any real hit, never weaken the test).
- [ ] **Step 3: Edit the README sentence** to "Tap a column and press Submit on the issue it opens. Give it a minute, then refresh. I cap the bot at two seconds a move. The engine is in [connect4/](connect4/)." Add `fonttools[woff]>=4.62` to `requirements-dev.txt`. Update the connect4 design spec (state example, region example, "### The wall" subsection, repo layout).
- [ ] **Step 4: Run `python -m connect4 render`,** then the full suite. Expected: 64 pass (62 if fontTools is absent).
- [ ] **Step 5: Commit** as "Put the wall on the live page" (state, hall-1.svg, README, requirements, spec).

### Task 5: Browser verification, review, ship

- [ ] **Step 1: Harness render** (`scratchpad/render/render_readme.py`) at 1280 light and dark: twelve images, zero broken, zero `[align="center"]`; wall edges line up with the board's. Playwright at 390 px: NOBODY YET. and the caption legible.
- [ ] **Step 2: Populated fixture** in the scratchpad (five entries with rank 1, a 39 character hyphenated login, an all-m login): screenshot `render_hall` output, confirm the star sits behind the first disc, no login reaches GAME · MOVES, the squeezed login reads, no rule crosses the star. Delete the fixture.
- [ ] **Step 3: Win path smoke:** `python -m connect4 move --title 'c4|drop|4' --actor octocat --issue 1 --root <tmp>` against a hand-built RRR.BBB state prints the win message and writes a one-row hall with the star.
- [ ] **Step 4: Review Workflow** (three lenses, two refuters per finding), fix on merit, re-run the suite and the harness.
- [ ] **Step 5: Push `feat/beat-the-bot-wall`, open the PR** (base `feat/readme-special` until that PR merges, then main). Merge is RON2K's call.
- [ ] **Step 6: After merge:** play one real move, confirm the Action commit adds `game/hall-2.svg` and removes `hall-1.svg`, and the profile page shows the wall.
