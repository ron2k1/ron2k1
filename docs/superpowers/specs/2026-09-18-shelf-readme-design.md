# Shelf README design

Date: 2026-09-18. Replaces the comic-issue README and its Connect Four game
(`2026-09-17-profile-readme-connect4-design.md`, removed in the same change; it stays in git history).

## The ask

RON2K, 2026-09-18: "the readme game should work instantaneously if it is too much we will just re
put the snake game, i dont like how it matches the github io, find better about me github examples
from 5-10 industry leaders who are creatives and copy those".

- A README cannot run JavaScript, so every Connect Four move was a GitHub Action round trip of about a
  minute. Instant play is not possible in a README, so the game becomes the Platane/snk contribution
  snake, which is a pre-rendered SVG animation and plays the moment the page loads.
- The old README reused ron2k1.github.io's comic identity (Bangers, red/blue/yellow halftone panels,
  "THE INCREDIBLE RONIL BASU, ISSUE #27"). The new page shares none of it.
- The snake was on the 2026-08-15 banned-chrome list. RON2K's 2026-09-18 request overrides that one
  item. The rest of the list stands: no shields.io walls, capsule-render, komarev counters,
  github-readme-stats cards, `<div align="center">`, or raw `<table>` rows.

## Research

`gh api repos/<u>/<u>/readme` over about 85 designers, creative coders, data-viz people and founders
found 44 profile READMEs. Many creative leaders keep none (Bruno Simon, Josh Comeau, Mike Bostock,
Mr.doob). Each README was screenshotted as github.com renders it at 1280 and 390 px, scored by four
analysts, and narrowed to eight exemplars:

| Handle | What we copy |
| --- | --- |
| tholman (Tim Holman) | Projects drawn as a bookshelf, every spine a link, a plain index under it |
| lynnandtonic (Lynn Fisher) | One identity line with one self-aware word, a flush-left column of project lines, a rule, one footer line |
| orta (Orta Therox) | One generated image made from GitHub's own contribution data, nothing competing with it |
| simonw (Simon Willison) | Proof by shipped things, dated or linked, never adjectives |
| chiphuyen (Chip Huyen) | Each project link carries the reason it exists |
| MaggieAppleton (Maggie Appleton) | A voice in very few words, links as the sentence's own nouns |
| chriscoyier (Chris Coyier) | Every link sits inside a sentence that explains it |
| antfu (Anthony Fu) | The README routes, the repos do the showing |

Three directions were drafted (Shelf, Logbook, Exhibit) and judged. Shelf won on likeness to the
exemplars, distance from the portfolio, and truth. Logbook failed truth (hardware claims from outside
the repo's sources). Exhibit put a 70 px tall snake first on a phone.

## The page

1. One sentence: Rutgers data science and statistics, class of 2027, "slightly overbuilt things that run
   on my own hardware".
2. The shelf: six spine images on one source line with no whitespace between anchors, each wrapped in a
   link to its repo. Inline images share a baseline, so the spines stand on one plank.
3. The snake in a `<picture>` with dark and light sources from the `output` branch.
4. A flush-left index, one line per spine: repo link, a middle dot, what it does. Lines end in `<br>`.
5. One paragraph on the two hackathons, in the team "we".
6. A `----` rule and the contact line: "LinkedIn is fastest. The longer story is at ron2k1.github.io."

Every factual line comes from the previous README or `gh repo view`. All seven linked repos are public
(checked 2026-09-18).

## The spines

`scripts/shelf.py` writes `assets/shelf/<key>.svg` from `fonts/Inter-Bold-caps.ttf` (Inter 4.1 Bold,
OFL 1.1, subset to A to Z with the name table kept). Letters are outlined to `<path>` with fontTools,
so the files carry no `<text>`, `<style>`, script, embedded font, or external reference and render the
same on every OS.

Per file: canvas `(W + 4) x 171`, spine body at x 2 to W + 2, n letters, `H = 12n + 36`, top
`T = 168 - H`. Body rect inset 0.75 with rx 2, fill F, stroke S 1.5. Bands of height 2 at `T + 6` and
`T + H - 8`, fill S. Letters Inter Bold 11 px, advance box centred on the spine, baselines
`T + 28 + 12i`. Plank rect `x 0, y 168, width W + 4, height 3`, fill #8c959f (3.0:1 on white, 6.2:1 on
#0d1117), so adjacent files join into one plank.

| Key | Label | W | Fill | Stroke and bands | Letters | Links to |
| --- | --- | --- | --- | --- | --- | --- |
| marginalia | MARGINALIA | 52 | #a466d9 | #6f3fa6 | #1a0b2e | marginalia |
| concurrency | CONCURRENCY | 46 | #216e39 | #0e4429 | #ffffff | claude-code-structured-concurrency |
| crash | CRASH | 42 | #9be9a8 | #30a14e | #04260f | crash-app |
| cluely | CLUELY | 46 | #40c463 | #216e39 | #04260f | Ronils-Cluely-OPENSOURCE |
| spotify | SPOTIFY | 52 | #30a14e | #216e39 | #04260f | spotify-cleaner |
| courtside | COURTSIDE | 42 | #9be9a8 | #30a14e | #04260f | courtside-showcase |

The greens are GitHub's contribution levels and the purple is the avatar's, which is also the snake's
colour, so the shelf and the grid under it read as one piece. Row width is 304 px, under the roughly
324 px content column on a 390 px phone. Every letter colour clears 4.5:1 on its fill.

## The snake

`.github/workflows/snake.yml`: daily cron, `workflow_dispatch`, and a push trigger on `main` limited to
the workflow file. `Platane/snk/svg-only@v3` writes `github-snake.svg` (palette github-light) and
`github-snake-dark.svg` (palette github-dark), both with `color_snake=%23a466d9`, and
`crazy-max/ghaction-github-pages@v5` pushes them to the `output` branch. The job asks for
`contents: write` because the repo default token is read-only. The `output` branch was deleted with the
old snake, so the workflow must run once before the README can show it.

## Removed

Connect Four (`connect4/`, `game/`, `.github/workflows/connect4.yml`), the comic renderer (`comic/`,
`assets/masthead.svg`, `assets/toolbelt.svg`, `assets/stats.svg`), the nightly stats job
(`.github/workflows/stats.yml`, `data/`), Bangers and JetBrains Mono with their licences, their tests,
and the Connect Four spec and plan. Nothing on the new page reads any of it. `tests.yml` stays for the
new tests.

## Tests

`tests/test_shelf.py`: committed spines equal the generator's output byte for byte and there are
exactly six; each file parses, has viewBox `0 0 W+4 171`, one path per letter, and no text, style,
script, foreignObject or href; letter contrast is at least 4.5:1; the row is at most 308 px wide.

`tests/test_readme.py`: every relative image exists; the six spines appear in order on one line, each
linked to its repo; the snake sources match what snake.yml writes; no banned chrome; no em or en dashes
and no semicolons in the prose; snake.yml carries the palettes, colour, branch and permission above.

## Verification

GitHub's renderer (`gh api markdown`) plus Playwright at 1280 and 390 px in light and dark, the live
branch page on github.com, a green snake run with the `output` branch present, and ZeroGPT on the prose.
