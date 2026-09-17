# Beat the bot wall

Date: 2026-09-17. Repo: `ron2k1/ron2k1`. Branch `feat/beat-the-bot-wall`, on top of
`feat/readme-special` (tappable columns, 45 tests green).

Origin: RON2K asked for "something special for the readme on github as well humanized". A panel
of four proposals (editor's note, this wall, a weekly strip, a credits box) was scored by three
judges on memorable, human, real data, buildable and comic fit. All three chose the wall. It is
the one proposal where a visitor's own action changes the page, its empty state is true today
(record 0-0-0), and it rides the existing drain, write, commit path with no workflow edit. Merge of
the PR is the approval gate.

One addition: a drawn panel under the board that lists every GitHub login whose red drop won a
game, by all-time rank, and says NOBODY YET. until one does.

## 1. What visitors see

### 1a. README.md, inside the c4 region (written by `connect4/readme.py`)

One line after the status line. Everything else in the region is unchanged.

```
Red is you. Tap a column to drop.

<a href="…"><img src="assets/drop-1.svg" width="14%" alt="Drop in column 1"></a>…<a href="…"><img src="assets/drop-7.svg" width="14%" alt="Drop in column 7"></a>
<img src="game/board-1.svg" alt="Connect Four, game 1, move 2, red to play" width="100%">

Red to play · Last move by @ron2k1 · Humans 0, bot 0, draws 0 · Most moves: @ron2k1 (1)

<img src="game/hall-1.svg" alt="Beat the bot: nobody yet. No game finished yet." width="100%">
```

The wall is `width="100%"` like the board, and both are drawn in a 720 px viewBox, so they scale
together and their edges line up at every viewport width. No new Markdown sentence inside the
region.

### 1b. README.md, the static paragraph after `<!-- c4:end -->` (edited by hand)

Before:

```
Tap a column and press Submit on the issue it opens. Give it a minute, then refresh. The engine is
in [connect4/](connect4/).
```

After:

```
Tap a column and press Submit on the issue it opens. Give it a minute, then refresh. I cap the bot
at two seconds a move. The engine is in [connect4/](connect4/).
```

That sentence is the one line of slack. A test pins it to the bot's budget (section 5, test 18).

### 1c. `game/hall-<rev>.svg`, empty wall (today's state)

Title band BEAT THE BOT, chip NO GAME FINISHED YET, body NOBODY YET., caption WIN ONE AND YOUR
HANDLE GOES HERE.

### 1d. `game/hall-<rev>.svg`, once humans have won

Chip is one of BOT UNBEATEN · 1 GAME, BOT UNBEATEN · {n} GAMES, A HUMAN WON THE LAST GAME. Rows
are the latest five hall entries, oldest of those first, each keeping its all-time rank: a red
disc, #{rank}, @{login}, GAME {game_no} · {moves} MOVES. Rank 1 gets a yellow star behind its
disc, the only yellow on the wall.

### 1e. Alt text (README img alt and the SVG aria-label are the same string)

Empty: `Beat the bot: nobody yet. No game finished yet.`
Populated: `Beat the bot: 1 octocat, game 3 in 9 moves. 2 hubot, game 5 in 12 moves. Bot unbeaten, 2 games.`

### 1f. Issue close comment on a red win

`@octocat dropped in column 4 and won game 3. You're on the wall now. The next drop starts game 4. See the board at https://github.com/ron2k1.`

Only "You're on the wall now." is new. `connect4/issues.py` `close_issue` already appends the last
sentence. Bot-win, draw and rejection messages are untouched.

## 2. Design

File `game/hall-<revision>.svg`, 720 px wide like the board (the 880 rule covers page-level assets
in `assets/`; `game/` holds the 720 board). Drawn by `connect4/hall.py` using `comic/draw.py`
only: panel, chip, chip_width, shadowed_text, star, svg, esc, the dots and dotsp patterns, both
embedded fonts. Palette from draw.py, no new font, only latin glyphs.

Every number below was measured with fontTools 4.62.1 against `fonts/Bangers-Regular.woff2` and
`fonts/JetBrainsMono.woff2` (unitsPerEm 1000 for both). The panel is 704 wide to match the
board's panel after the tappable-columns change, so the two right edges and shadows coincide.

- Empty: viewBox `0 0 720 200`, `D.panel(8, 8, 704, 184)`. With n rows (1 to 5): viewBox
  `0 0 720 H`, H = 100 + 46 n, `D.panel(8, 8, 704, H - 16)`.
- Title band: rect x 8 y 8 w 704 h 64 fill BLUE stroke INK 3, then the same rect filled
  `url(#dotsp)`. Blue is the bot's color, the thing to beat, and it leaves yellow for one element.
  Text BEAT THE BOT class d, x 30 y 55, size 40, fill PAPER, letter-spacing .03em (188.5 px, ends
  at x 219).
- Chip: `D.chip(x, 24, text, D.PAPER2, D.INK, size=12, pad=12, sh=3)`, right-aligned with
  `x = 692 - D.chip_width(text, 12, 12)` (the board's chip also ends at 692). Chip widths: NO GAME
  FINISHED YET 172 (x 520, the board chip's x), BOT UNBEATEN · 1 GAME 180, BOT UNBEATEN · 999
  GAMES 202 (x 490), A HUMAN WON THE LAST GAME 210 (x 482). None reaches the title's end at 219.
- Empty body: `D.shadowed_text(360, 136, "NOBODY YET.", 44, D.RED, [(3, 3, D.INK, 1)],
  anchor="middle")` (184 px, centred on the panel). Caption WIN ONE AND YOUR HANDLE GOES HERE
  class d, size 24, fill INK, letter-spacing .04em, text-anchor middle at x 360, y 172 (331 px).
  Bangers 24 is about 12 px once GitHub mobile scales 720 to roughly 350, still legible. A 13 px
  mono line would be 6 px there, which is why the caption is display type and why no Markdown
  duplicate is needed.
- Row i (0-based), centre cy = 103 + 46 i:
  - Disc: shadow circle (47, cy + 3) r 16 INK, disc (44, cy) r 16 RED stroke INK 3, glint
    (39, cy - 5) r 4 PAPER opacity .55. The board's disc recipe at half size.
  - Rank 1 only, drawn before the disc: `polygon points=D.star(47, cy + 3, 26, 17)` INK, then
    `D.star(44, cy, 26, 17)` YELLOW stroke INK 2.
  - Rank: `#{rank}` class d size 26 INK, x 80, y cy + 9. #999 is 54 px and ends at 134.
  - Login: `D.shadowed_text(140, cy + 10, "@" + login, size, D.RED, [(2, 2, D.INK, 1)],
    extra=...)`, size from `login_size()`.
  - Label: `GAME {game_no} · {moves} MOVES` class m size 12 weight 500 letter-spacing .14em
    INKSOFT text-anchor end, x 700 (the board's right status label x). GAME 999 · 42 MOVES is 167
    px and starts at 533. A game has at most 42 moves.
  - Rule between rows, never after the last: line x 80 to 690 at y cy + 23, INKSOFT, stroke 1.5,
    opacity .25. It starts at 80 so a star tip (max x 70) never crosses it.
- Login fit. `LOGIN_X = 140`, `LABEL_X = 700`, `AVAIL = 353` (140 to 493, 40 px clear of the
  widest label at 533). `ADV` is a dict of Bangers advance widths in units per 1000 em for "@" and
  the 63 login characters `[A-Za-z0-9-]`, extracted once with fontTools (widest m and M 619,
  narrowest I 200, @ 987). `width(text, size) = sum(ADV[c] for c in text) / 1000 * size`.
  `login_size(login)` returns `(size, squeeze)`: 28 if it fits, else the largest integer size down
  to 16 that fits, else 16 with `textLength='353' lengthAdjust='spacingAndGlyphs'` passed through
  shadowed_text's `extra` so every layer squeezes together. Measured: @octocat 28 px at 111 px,
  @claude-code-structured-concurrency-xyz 21 px at 345 px, @ plus 39 m 16 px squeezed from 402 to
  353.

## 3. Data flow

`game/state.json` gains one key, `"hall"`: a list of `{"game_no", "by", "moves"}` in the order the
wins happened.

- `connect4/game.py`: `new_state(..., hall: list | None = None, revision=0)` writes
  `"hall": hall or []`. `load()` does `state.setdefault("hall", [])` so the committed state
  migrates on first read. `_finish()` appends `{"game_no": state["game_no"], "by":
  state["moves"][-1]["by"], "moves": len(state["moves"])}` when the winner is RED (`moves[-1]` is
  the red drop `_drop` just appended, so `by` is the issue author gh returned). The rollover inside
  `apply_human_move` passes `hall=st["hall"]` into `new_state`. The human-win branch's message
  becomes `f"@{actor} dropped in column {col + 1} and won game {g}. {ON_THE_WALL} The next drop
  starts game {g + 1}."`. The draw branch keeps its current text.
- `connect4/hall.py` (new) derives everything else from state at render time. `finished_games =
  game_no if finished else game_no - 1`. `unbeaten = finished_games - (hall[-1]["game_no"] if hall
  else 0)`. Draws count as unbeaten. `chip_text`: CHIP_NONE when finished_games == 0, CHIP_HUMAN
  when unbeaten == 0, `BOT UNBEATEN · 1 GAME`, else `BOT UNBEATEN · {n} GAMES`. `entries(state)`
  returns the last five hall items as `(rank, by, game_no, moves)` with rank = index + 1 in the
  full list, replacing any `by` that fails `LOGIN = ^[A-Za-z0-9-]{1,39}$` with "someone" (the
  fallback issues.py already uses). `label(state)` builds the alt text: the chip lowercased with
  " · " turned into ", " and its first letter capitalised. `render_hall(state)` draws it.
  Constants exported: `TITLE`, `EMPTY_TEXT`, `INVITE`, `CHIP_NONE`, `CHIP_HUMAN`, `ON_THE_WALL =
  "You're on the wall now."`, `LOGIN`, `ADV`, `LOGIN_X`, `LABEL_X`, `AVAIL`.
- `connect4/readme.py`: `from . import hall as HL`; `hall_path(state) =
  f"game/hall-{state['revision']}.svg"`; `region()` returns its current string plus
  `f'\n<img src="{hall_path(state)}" alt="{HL.label(state)}" width="100%">\n'` after the status
  line. `rewrite()` is untouched.
- `connect4/__main__.py` `_write_all`: after writing the board, write `root / R.hall_path(state)`
  with `render_hall(state)` and unlink every other `game/hall*.svg`, the same one-file-per-revision
  rule as the board. connect4.yml already stages with `git add -A game README.md`, so the new file
  and the deletion ride the existing commit. No workflow file changes.
- Migration: run `python -m connect4 render` once locally. It writes `"hall": []` into
  `game/state.json`, creates `game/hall-1.svg` and rewrites the README region. Commit those with
  the code.

## 4. Files

New:
- `connect4/hall.py` (about 120 LOC)
- `game/hall-1.svg` (generated by `python -m connect4 render`, committed)
- `tests/test_hall.py`

Edited:
- `connect4/game.py` (new_state hall param, load migration, _finish append, win message, rollover
  carries hall)
- `connect4/readme.py` (hall_path, region emits the img line)
- `connect4/__main__.py` (_write_all writes and prunes hall-<rev>.svg)
- `game/state.json` (gains `"hall": []` via render)
- `README.md` (region via render, plus the one static sentence by hand)
- `tests/test_game.py` (one added assert, three new tests)
- `tests/test_readme.py` (three new tests)
- `requirements-dev.txt` (add `fonttools[woff]>=4.62`, test-only, the Action runtime stays stdlib)
- `docs/superpowers/specs/2026-09-17-profile-readme-connect4-design.md` (state.json example gains
  `"hall": []`, a short "### The wall" subsection after "### README region", the region example
  gains the hall img line, repo layout gains connect4/hall.py, game/hall-<rev>.svg,
  tests/test_hall.py)

Untouched: `comic/*`, `assets/*`, `connect4/engine.py`, `connect4/bot.py`, `connect4/render.py`,
`connect4/issues.py`, all three workflows.

## 5. Tests (names and assertions)

`tests/test_hall.py`

1. `test_empty_wall_says_nobody_yet`: `render_hall(G.new_state())` parses with ElementTree, root
   tag ends with `svg`, viewBox is `0 0 720 200`, the text nodes include BEAT THE BOT, NOBODY YET.,
   WIN ONE AND YOUR HANDLE GOES HERE and NO GAME FINISHED YET, no text node contains "@", the
   invitation's text element has font-size >= 22, and `data:font/woff2;base64,` appears exactly
   twice.
2. `test_latest_five_rows_keep_all_time_rank`: seven hall entries (u1..u7, games 1..7) with
   game_no 8 in progress render viewBox `0 0 720 330`, text nodes #3 through #7 and @u3 through
   @u7, no #1, #2, @u1 or @u2, and the label `GAME 7 · 13 MOVES`.
3. `test_rank_one_star_is_the_only_yellow`: one entry renders viewBox `0 0 720 146` and exactly one
   occurrence of `fill='#ffc400'`, on a polygon. Seven entries (rank 1 scrolled off) render zero.
4. `test_unbeaten_count_and_chip_text` (parametrized): new_state -> 0 and NO GAME FINISHED YET.
   game 1 finished by the bot, hall empty -> 1 and BOT UNBEATEN · 1 GAME. game 2 in progress, hall
   empty -> 1. game 2 finished R with hall [{game 2}] -> 0 and A HUMAN WON THE LAST GAME. game 3
   finished draw with hall [{game 2}] -> 1 (a draw counts). game 6 in progress with hall
   [{game 2}] -> 3 and BOT UNBEATEN · 3 GAMES.
5. `test_bad_login_draws_as_someone_and_is_escaped`: entries with by `<script>alert(1)</script>`
   and `a'b` render as @someone, the SVG contains neither `<script` nor `alert`, and `label()` says
   someone. An entry by octocat is unchanged.
6. `test_login_never_reaches_the_game_label`: `login_size("octocat") == (28, False)`,
   `login_size("claude-code-structured-concurrency-xyz") == (21, False)` with
   `width("@claude-code-structured-concurrency-xyz", 21) <= AVAIL`, `login_size("m" * 39) ==
   (16, True)`, the rendered all-m row carries `textLength='353' lengthAdjust='spacingAndGlyphs'`
   on every layer of that login, and the octocat render carries no textLength.
7. `test_bangers_advances_match_the_font`: `pytest.importorskip("fontTools")`, open
   fonts/Bangers-Regular.woff2, assert unitsPerEm == 1000, `set(ADV) == set("@" + ascii_letters +
   digits + "-")`, and every `ADV[c]` equals the font's hmtx advance for that glyph.
8. `test_widest_label_leaves_the_gap`: importorskip fontTools, measure `GAME 999 · 42 MOVES` at 12
   px with .14em tracking from JetBrainsMono.woff2 and assert `LABEL_X - width >= LOGIN_X + AVAIL +
   15`; measure BEAT THE BOT at 40 px .03em and assert `30 + width < 482` (the widest chip's x).
9. `test_label_text`: `label(G.new_state()) == "Beat the bot: nobody yet. No game finished yet."`;
   game 7 finished by the bot with hall [octocat game 3 in 9, hubot game 5 in 12] gives exactly
   `Beat the bot: 1 octocat, game 3 in 9 moves. 2 hubot, game 5 in 12 moves. Bot unbeaten, 2 games.`
10. `test_no_banned_glyphs_in_any_wall_string`: for the empty and populated renders (text nodes
    plus aria-label via ElementTree, so `&#39;` entities do not false-positive), the four chip
    strings, ON_THE_WALL, both labels and the win message from `apply_human_move`, none contains
    U+2014, U+2013, ";" or U+25CF.
11. `test_write_all_leaves_one_hall_file`: write a README with the markers into tmp,
    `main(["init", "--root", tmp])` produces game/hall-0.svg, game/board-0.svg and a state.json
    with `"hall": []`; bump revision to 3, save, `main(["render", "--root", tmp])` leaves exactly
    one hall-*.svg (hall-3.svg), one board-*.svg (board-3.svg), and the README contains
    `src="game/hall-3.svg"`.
12. `test_committed_hall_asset_is_current`: load the repo's game/state.json, assert
    `ROOT / R.hall_path(state)` exists, its text equals `render_hall(state)` byte for byte, and
    game/ holds exactly one hall-*.svg.

`tests/test_game.py`

13. `test_new_state_shape` (existing): add `s["hall"] == []`.
14. `test_human_win_appends_hall_entry_and_wall_line`: the RRR.BBB scenario with octocat dropping
    column 3 gives `hall == [{"game_no": 1, "by": "octocat", "moves": 7}]` and `out.message ==
    "@octocat dropped in column 4 and won game 1. You're on the wall now. The next drop starts game
    2."`.
15. `test_bot_win_and_draw_leave_hall_alone`: board `["......." ,"......." ,"......." ,".......
    ,"R......" ,"RR.BBB."]` with six moves, human drops column 0, the bot takes its immediate win,
    result B, hall []. Board `["..RBRBR","RBRBRBR","BRBRBRB","BRBRBRB","RBRBRBR","RBRBRBR"]` with
    40 moves, human drops column 0, the bot's only move fills column 1, result draw, draws 1,
    hall [].
16. `test_load_migrates_missing_hall_and_rollover_carries_it`: a temp state file without `hall`
    loads with `hall == []`; a finished game 4 whose hall holds one entry rolls into game 5 with
    the same hall.

`tests/test_readme.py`

17. `test_region_has_wall_image_after_status_line`: `region(new_state())` places
    `src="game/hall-0.svg"` after `Humans 0, bot 0, draws 0`, carries `alt="Beat the bot: nobody
    yet. No game finished yet." width="100%"`, `rewrite` stays idempotent, and revision 7 yields
    `hall-7.svg` with no `hall-0` left.
18. `test_live_readme_bot_cap_matches_budget`: whitespace-normalised README text after
    `<!-- c4:end -->` contains `I cap the bot at two seconds a move.`,
    `inspect.signature(bot.choose_move).parameters["budget"].default == 2.0`, and
    `_parser().parse_args(["drain", "--outcomes", "x"]).budget == 2.0`.
19. `test_live_page_has_no_dashes`: README.md contains no U+2014, U+2013 or U+25CF, and every SVG
    under assets/ and game/ has none in its text nodes or aria-label. (Semicolons are not asserted
    page-wide because toolbelt.svg's aria-label joins with them today. The wall's own ban is
    test 10.)

Total after the change: 64 tests (45 today plus 19).

## 6. Action safety

- Input from strangers stays a column and a login. `issues.parse_title` matches
  `^\s*c4\|drop\|([1-7])\s*$` and yields an int. `list_open_moves` requests only
  `number,title,author` from `gh issue list`, never a body. Nothing here changes.
- The wall reads `by` from `state["moves"][-1]["by"]`, the same login the status line already
  prints, re-checks it against `^[A-Za-z0-9-]{1,39}$` (GitHub's login alphabet) and draws
  "someone" otherwise. Every string enters the SVG through `D.esc`. The README alt is built from
  that validated login and integers, so it cannot carry a quote or an angle bracket.
- connect4.yml is byte-identical. Permissions stay `contents: write` and `issues: write`.
  `git add -A game README.md` already stages the new file and the deletion.
- The win comment adds a constant sentence. The `@{actor}` in it is the same interpolation the
  message already had.
- The wall contains no link in Markdown or SVG, so no visitor can plant a URL on the page.
- `hall` is appended only by `_finish` from validated data. A hand-edited state with a bad login
  degrades to "someone" rather than breaking the render.

## 7. Browser and live checks

1. Local: `python -m pytest -q -p no:asyncio` green at 64. `python -m connect4 render`.
   `git status` shows game/state.json (+hall), game/hall-1.svg (new), README.md (region plus the
   one static sentence).
2. Render README.md through the existing `gh api markdown` plus Playwright harness in light and
   dark at 1280 px. Twelve images load (masthead, seven buttons, board-1, hall-1, toolbelt,
   stats). The wall shows Bangers for BEAT THE BOT and NOBODY YET. and JetBrains Mono for the
   chip. The wall's left and right edges line up with the board's. Zero `[align="center"]`.
3. Populated fixture in the scratchpad: five hall entries including rank 1, a 39 character
   hyphenated login and an all-m 39 character login. Render with `hall.render_hall` to a
   scratchpad file and screenshot it. The star sits behind the first disc, the longest logins end
   left of GAME · MOVES, the squeezed login is still readable, no rule crosses the star. Delete
   the fixture, never commit it.
4. Mobile: Playwright viewport 390 px on the rendered README. NOBODY YET. and the caption are
   legible. The chip is small but so is the board's chip above it.
5. After merge to main: open one real move issue, wait for the Action, confirm the commit touches
   game/state.json, game/board-2.svg, game/hall-2.svg (added), game/hall-1.svg (deleted) and
   README.md, the README wall alt still reads "nobody yet", and the close comment is the ordinary
   non-win text.
6. Win path: test 14 plus a local `python -m connect4 move --title 'c4|drop|4' --actor octocat
   --issue 1 --root <tmp>` against a hand-built RRR.BBB state, which prints the win message and
   writes a hall-<rev>.svg with one row and the star.

## 8. Risks

- If someone wins between now and merge, humans reads 1 with an empty wall. Backfill `hall` from
  the git history of game/state.json (`last_game.winning_move_by` and `moves`) before merging.
- One more 75 KB SVG per page load and one more file per move commit. The one-file-per-revision
  rule keeps game/ at one hall file.
- The continuous size rule can put a 28 px login above a 21 px one. Accepted, since a single small
  size would punish the common short handle.
- fontTools plus brotli is a dev dependency only. If a future runner cannot install it, tests 7
  and 8 importorskip out and the other 62 still run, and the ADV table is static data that only
  changes if the font file does.

## 9. Grafts declined

- Rotated rubber-stamp chip: the wall sits flush under the board and mirrors its band, a tilted
  chip breaks that read.
- DRAWS COUNT AS UNBEATEN small print: explaining. Unbeaten already includes draws.
- BOT GETS 2 S A MOVE footer inside the SVG: duplicates the board's status strip. The fact went to
  the Markdown slack line instead, pinned by test 18.
- A Markdown duplicate of the invitation for phones: the caption is 24 px Bangers instead, legible
  at mobile scale, and test 1 pins the size.
