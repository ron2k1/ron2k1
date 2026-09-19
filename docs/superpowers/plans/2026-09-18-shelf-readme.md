# Shelf README implementation plan

Spec: `docs/superpowers/specs/2026-09-18-shelf-readme-design.md`. Branch `feat/readme-creative` from
`main`. Every commit keeps `pytest` green. Merge is RON2K's call.

## Global constraints

- Real data only: README lines come from the previous README or `gh repo view`.
- No em or en dashes, no semicolons, no bold in prose. No banned chrome except the requested snake.
- No attribution trailers in commits or the PR.

### Task 1: snake workflow

- Create `.github/workflows/snake.yml` as the spec says, plus a temporary push trigger on
  `feat/readme-creative` so the `output` branch exists before review.
- Push, watch the run go green, confirm `output` holds both SVGs.

### Task 2: the spines

- Add `fonts/Inter-Bold-caps.ttf`, `fonts/OFL-Inter.txt`, and a fonts note.
- Write `tests/test_shelf.py` first (red: no generator yet).
- Write `scripts/shelf.py`, run it, commit `assets/shelf/*.svg` (green).
- Add `fonttools` to `requirements-dev.txt`.

### Task 3: swap the page

- Write the new `tests/test_readme.py` checks (red against the old README).
- Replace `README.md` with the shelf page (green).
- Delete Connect Four, the comic renderer, stats, their tests, fonts, data, workflows, and the old spec
  and plan in the same commit, since the old page is what used them.

### Task 4: verify

- Render with the harness at 1280 and 390, light and dark. Check the spines stay on one row, the plank
  joins, no image is broken, no horizontal scroll.
- Open the branch page on github.com. Run ZeroGPT on the prose.

### Task 5: review and ship

- Review Workflow (rendering, workflow safety, tests and copy), fix confirmed findings test first.
- Drop the temporary trigger, push, open the PR to `main`.
