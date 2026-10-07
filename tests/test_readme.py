"""The profile README: the shelf, the catalog under it, the hackathon paragraph, and the snake at the end."""
import pathlib
import re

from scripts import shelf as SH

ROOT = pathlib.Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
SNAKE = (ROOT / ".github" / "workflows" / "snake.yml").read_text(encoding="utf-8")
OUTPUT = "https://raw.githubusercontent.com/ron2k1/ron2k1/output/"
CATALOG = re.compile(r"^`([\d.]+)( *)` \[([^\]]+)\]\((https://github\.com/ron2k1/[^)]+)\) · \S.*$", flags=re.M)


def prose():
    """README text a reader sees: tags and link targets removed."""
    text = re.sub(r"<[^>]+>", " ", README)
    return re.sub(r"\]\([^)]*\)", "]", text)


def test_every_local_image_exists():
    srcs = re.findall(r'src(?:set)?="([^"]+)"', README)
    local = [s for s in srcs if not s.startswith("https://")]
    assert len(local) == len(SH.BOOKS) + 1
    for s in local:
        assert (ROOT / s).is_file(), s


def test_shelf_is_the_generators_line_on_one_source_line():
    lines = [ln for ln in README.splitlines() if "assets/shelf/" in ln]
    assert lines == [SH.readme_line()], "regenerate it with python scripts/shelf.py --readme"
    widths = re.findall(r'width="([\d.]+)%"', lines[0])
    assert [float(w) for w in widths] == [b.width / 10 for b in SH.BOOKS] + [SH.END_WIDTH / 10]


def test_catalog_lists_every_book_in_shelf_order_with_its_call_number():
    rows = CATALOG.findall(README)
    assert [url for *_, url in rows] == [SH.REPO_URL + b.repo for b in SH.BOOKS]
    assert [num for num, *_ in rows] == ["".join(b.call[:-1]) for b in SH.BOOKS]
    # Padded to one width so the links line up in a column.
    assert len({len(num + pad) for num, pad, *_ in rows}) == 1
    lines = [m.group(0) for m in CATALOG.finditer(README)]
    # GitHub joins soft line breaks into one paragraph, so every line but the last needs its <br>.
    assert [ln.endswith("<br>") for ln in lines] == [True] * (len(SH.BOOKS) - 1) + [False]


def test_snake_sources_match_what_the_workflow_writes():
    assert f'<source media="(prefers-color-scheme: dark)" srcset="{OUTPUT}github-snake-dark.svg">' in README
    assert f'<source media="(prefers-color-scheme: light)" srcset="{OUTPUT}github-snake.svg">' in README
    assert f'src="{OUTPUT}github-snake.svg"' in README
    marginalia = next(b for b in SH.BOOKS if b.key == "marginalia")
    snake = "%23" + marginalia.cloth[1:]          # the snake is the marginalia book's purple
    assert f"dist/github-snake.svg?palette=github-light&color_snake={snake}" in SNAKE
    assert f"dist/github-snake-dark.svg?palette=github-dark&color_snake={snake}" in SNAKE
    assert "target_branch: output" in SNAKE and "contents: write" in SNAKE


def test_snake_actions_are_pinned_to_commit_shas():
    uses = re.findall(r"uses: (\S+)", SNAKE)
    assert uses and all(re.fullmatch(r"[\w.-]+/[\w./-]+@[0-9a-f]{40}", u) for u in uses), uses


def test_no_template_chrome():
    for banned in ("shields.io", "capsule-render", "komarev", "github-readme-stats", "readme-typing-svg",
                   "skillicons", "<table", "<div"):
        assert banned not in README, banned
    assert not re.search(r"align\s*=", README, flags=re.I)
    assert not re.search(r"^\s*\|.*\|\s*$", README, flags=re.M), "markdown tables are chrome too"


def test_prose_reads_like_a_person_wrote_it():
    alts = re.findall(r'alt="([^"]*)"', README)
    for text in (prose(), *alts):
        for banned in ("—", "–", "&mdash;", "&ndash;", ";", "**", "__", " -- "):
            assert banned not in text, (banned, text[:60])
    assert not re.search(r"<(b|strong)\b", README, flags=re.I), "no bold in prose"


def test_the_old_game_and_comic_page_are_gone():
    assert not re.search(r"c4:start|connect4|game/|masthead|toolbelt", README)
    workflows = sorted(p.name for p in (ROOT / ".github" / "workflows").glob("*.yml"))
    assert workflows == ["snake.yml", "tests.yml"]
    for gone in ("comic", "connect4", "game", "data"):
        # git leaves ignored __pycache__ folders behind on checkout, so only real files count
        left = [f for f in (ROOT / gone).rglob("*") if f.is_file() and "__pycache__" not in f.parts]
        assert not left, left[:3]


def test_only_the_fonts_the_generator_reads_are_kept():
    fonts = sorted(p.name for p in (ROOT / "fonts").glob("*.ttf"))
    assert fonts == sorted([SH.TITLE_FONT.name, SH.LABEL_FONT.name])
