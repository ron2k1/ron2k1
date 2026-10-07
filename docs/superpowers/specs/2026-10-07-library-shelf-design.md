# Library shelf README design

Date: 2026-10-07. Replaces the 2026-09-18 Shelf design (`2026-09-18-shelf-readme-design.md` and its plan,
removed in the same change and kept in git history).

## The ask

RON2K, 2026-10-07: "make the github readme more aesthetically pleasing ... adjust the readme to be
professional and artsy", in the same request that added HazardCam (NVIDIA x Dell hackathon, October
2026) to ron2k1.github.io.

The 2026-09-18 page sat its six spines in a 230 px block at the top left of an 846 px column, so on
desktop most of the first screen was empty, and the snake under it was the only full-width element.
The bookshelf idea stays, because it is the part of the page nobody else has and it shares nothing
with the portfolio's comic identity. This design takes it further, to a real library.

## The page

1. Two sentences. The plain fact RON2K kept on 2026-09-19 (Rutgers data science and statistics, class
   of 2027), then what he does now, in the wording already public on ron2k1.github.io: research in the
   Rutgers statistics department, grading model outputs for a frontier AI lab through Mercor (never the
   lab's name), and AI engineering at CodePath. The second sentence is the professional half of the ask
   and the easiest line to cut.
2. The shelf, full column width: seven cloth-bound books, each its own linked image, then one unlinked
   image with a bookend and two textbooks lying flat (Statistics, Data Science).
3. The catalog: one line per book, in shelf order. A call number in inline code, padded to one width so
   the links form a column, then the repo link, a middle dot, and what it does. Every line fits on one
   line at the desktop column.
4. The hackathon paragraph in the team "we", now ending with HazardCam at the NVIDIA x Dell hackathon.
   No placement is on record for that event, so none is claimed.
5. The snake, last. It is still the page's moving part (RON2K's 2026-09-18 ask), but it no longer sits
   between the books and their catalog.

No header, rule or contact line: RON2K removed those on 2026-09-19 and the profile sidebar links both
LinkedIn and ron2k1.github.io.

## Call numbers

Each book carries the real Dewey Decimal class for its subject and the Cutter BAS, and the shelf is in
call-number order, which is why HazardCam sits second rather than first. Every class was checked
against library catalog records on 2026-10-07:

| Book | Class | Heading |
| --- | --- | --- |
| structured-concurrency | 005.43 | Operating systems |
| HazardCam | 363.11 | Occupational and industrial safety |
| marginalia | 371.30281 | Study skills, including note-taking |
| crash-app | 381.142 | Electronic commerce |
| Cluely | 658.456 | Conducting meetings |
| spotify-cleaner | 780.285 | Computer applications in music |
| courtside-showcase | 796.323 | Basketball |

## Drawing

`scripts/shelf.py` writes `assets/shelf/<key>.svg` for each book and `assets/shelf/end.svg`. Widths are
in thousandths of the README column and the README sets `width="<units / 10>%"` (GitHub keeps percent
widths), so every file renders at the same height and the row scales as one piece: 271 px tall in the
846 px desktop column, 99 px on a 390 px phone, 76 px on a 320 px phone. The widths add up to 996, so
rounding never pushes the end piece onto a second line.

Each file is 320 units tall with the walnut plank across its bottom 14 units (top face `#a07a55`,
4.88:1 on GitHub's dark background, front `#765236`, 6.93:1 on white). A book is a cloth rectangle under
a left-to-right gradient that darkens both edges, two foil head bands, a tail band, the title, a sticker
and a thin outline. HazardCam's head bands are amber and charcoal hazard tape, after its own camera
wall. Titles are Libre Baskerville Bold turned 90 degrees clockwise, the way an English-language spine
reads, at the largest size up to 24 units that fits across the spine and along it with 2 % spare for
overhanging letters. Stickers are Courier Prime Bold, like a typed library label. Both fonts are
outlined to paths, so the files hold only `svg`, `defs`, `linearGradient`, `stop`, `clipPath`, `rect`
and `path`, and no reference outside the file.

| Book | Width | Height | Cloth | Foil |
| --- | --- | --- | --- | --- |
| CONCURRENCY | 82 | 280 | #2f5d42 forest | #e6c77f gold |
| HAZARDCAM | 92 | 292 | #2a2c31 charcoal | #f2a93b amber |
| MARGINALIA | 84 | 262 | #a466d9 avatar purple | #1f0d36 ink |
| CRASH | 70 | 236 | #7c2832 oxblood | #ecd08f gold |
| CLUELY | 74 | 270 | #253c63 navy | #dfe5ee silver |
| SPOTIFY | 78 | 248 | #c9993f ochre | #2b1e06 ink |
| COURTSIDE | 82 | 284 | #b65a2f burnt orange | #fbecd4 cream |

Every foil clears 4:1 on its cloth (lowest Courtside at 4.02, the test's floor is WCAG's 3:1 for large text) and the sticker ink is 12.76:1 on the sticker. The
purple is the avatar's and still the snake's colour. On the phone the titles shrink with the shelf, so
the catalog under it carries the names in full.

## Tests

`tests/test_shelf.py`: the committed files equal the generator's output byte for byte. Each file has
the right viewBox, only the allowed elements, no text, style, script, image, font or outside URL, and
only `url(#...)` references. Title ink stays inside the spine and between the bands, sticker ink inside
the sticker, contrast floors as above, books in call-number order with the BAS Cutter, widths between
990 and 997, and the plank edge to edge in every file.

`tests/test_readme.py`: every local image exists. The shelf line equals `python scripts/shelf.py
--readme` and carries the generator's widths. The catalog lists the books in shelf order with matching
call numbers, padded to one width, every line but the last ending in `<br>`. The snake sources match
snake.yml and its colour is the Marginalia cloth. Actions are pinned to SHAs. No banned chrome, now
including any `align=` attribute, and no dashes, semicolons or bold in the prose or alt text. Only the
two fonts the generator reads are kept.

## Verification

GitHub's renderer (`gh api markdown`, mode markdown) with github-markdown-css in Playwright at 838, 308
and 238 px in light and dark: one shelf row, no broken images, equal pill widths, every catalog line on
one line at 838. Then the branch on github.com, its rendered README put into the real profile page at
1280, 390 and 320 px viewports in light and dark. There the column measured 846, 308 and 238 px (846 at
every desktop width from 1280 up, 578 at 1012), with one shelf row 271, 99 and 76 px tall and no broken
images.
