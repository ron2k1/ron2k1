import json
from types import SimpleNamespace

from connect4 import issues as I


def test_parse_title():
    assert I.parse_title("c4|drop|1") == 0
    assert I.parse_title("  c4|drop|7 ") == 6
    for bad in ("c4|drop|8", "c4|drop|0", "c4|drop|3 extra", "drop|3", "", None, "c4|drop|33"):
        assert I.parse_title(bad) is None


def test_list_open_moves_filters_sorts_and_records_command():
    calls = []
    payload = [
        {"number": 12, "title": "c4|drop|4", "author": {"login": "hubot"}},
        {"number": 9, "title": "Bug: something", "author": {"login": "x"}},
        {"number": 11, "title": "c4|drop|1", "author": {"login": "octocat"}},
        {"number": 13, "title": "c4|drop|9", "author": {"login": "y"}},
        {"number": 14, "title": "c4|drop|2", "author": None},
    ]

    def fake_run(cmd, **kw):
        calls.append(cmd)
        return SimpleNamespace(stdout=json.dumps(payload))

    moves = I.list_open_moves("ron2k1/ron2k1", run=fake_run)
    assert moves == [{"number": 11, "col": 0, "actor": "octocat"}, {"number": 12, "col": 3, "actor": "hubot"},
                     {"number": 14, "col": 1, "actor": "someone"}]
    assert calls[0][:3] == ["gh", "issue", "list"] and "--repo" in calls[0] and "--state" in calls[0]


def test_close_issue_appends_profile_link():
    calls = []
    I.close_issue("ron2k1/ron2k1", 12, "@hubot dropped in column 4.", run=lambda cmd, **kw: calls.append(cmd))
    assert calls[0][:4] == ["gh", "issue", "close", "12"]
    assert calls[0][-1].endswith("See the board at https://github.com/ron2k1.")
