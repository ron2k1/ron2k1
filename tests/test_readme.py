"""The profile README: the shelf, the snake under it, the index, and the few sentences around them."""
import pathlib
import re

from scripts import shelf as SH

ROOT = pathlib.Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
SNAKE = (ROOT / ".github" / "workflows" / "snake.yml").read_text(encoding="utf-8")
OUTPUT = "https://raw.githubusercontent.com/ron2k1/ron2k1/output/"
REPO_URL = "https://github.com/ron2k1/"


def prose():
    """README text a reader sees: tags and link targets removed."""
    text = re.sub(r"<[^>]+>", " ", README)
    return re.sub(r"\]\([^)]*\)", "]", text)


def test_every_local_image_exists():
    srcs = re.findall(r'src(?:set)?="([^"]+)"', README)
    local = [s for s in srcs if not s.startswith("https://")]
    assert len(local) == len(SH.SPINES)
    for s in local:
        assert (ROOT / s).is_file(), s


def test_spines_stand_on_one_line_each_linked_to_its_repo():
    lines = [ln for ln in README.splitlines() if "assets/shelf/" in ln]
    assert len(lines) == 1, "the spines must share one source line or GitHub breaks the row"
    anchors = re.findall(r'<a href="([^"]+)"><img src="(assets/shelf/[^"]+)" alt="([^"]+)"></a>', lines[0])
    assert [(href, src) for href, src, _ in anchors] == [
        (REPO_URL + s.repo, f"assets/shelf/{s.key}.svg") for s in SH.SPINES]
    glued = "".join(f'<a href="{h}"><img src="{s}" alt="{a}"></a>' for h, s, a in anchors)
    assert glued in lines[0], "no whitespace between the anchors, or the spines drift apart"


def test_index_names_every_spine_in_shelf_order():
    index = re.findall(r"^\[([^\]]+)\]\((https://github\.com/ron2k1/[^)]+)\) · \S.*$", README, flags=re.M)
    assert [url for _, url in index] == [REPO_URL + s.repo for s in SH.SPINES]
    lines = re.findall(r"^\[[^\]]+\]\(https://github\.com/ron2k1/[^)]+\) · .*$", README, flags=re.M)
    # GitHub joins soft line breaks into one paragraph, so every line but the last needs its <br>.
    assert [ln.endswith("<br>") for ln in lines] == [True] * (len(SH.SPINES) - 1) + [False]


def test_snake_sources_match_what_the_workflow_writes():
    assert f'<source media="(prefers-color-scheme: dark)" srcset="{OUTPUT}github-snake-dark.svg">' in README
    assert f'<source media="(prefers-color-scheme: light)" srcset="{OUTPUT}github-snake.svg">' in README
    assert f'src="{OUTPUT}github-snake.svg"' in README
    marginalia = next(s for s in SH.SPINES if s.key == "marginalia")
    snake = "%23" + marginalia.fill[1:]          # the snake is the marginalia spine's purple
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
    assert not re.search(r"align\s*=\s*[\"']?center", README, flags=re.I)
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
