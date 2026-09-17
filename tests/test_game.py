import json

from connect4 import game as G


def test_new_state_shape():
    s = G.new_state()
    assert s["board"] == ["......."] * 6 and s["to_play"] == "R" and s["moves"] == []
    assert s["record"] == {"humans": 0, "bot": 0, "draws": 0} and s["revision"] == 0 and s["hall"] == []


def test_human_move_then_bot_reply():
    s, out = G.apply_human_move(G.new_state(), 3, "octocat", 12, budget=0.3)
    assert out.accepted
    assert s["board"][-1][3] == "R"
    assert sum(row.count("B") for row in s["board"]) == 1
    assert s["to_play"] == "R" and len(s["moves"]) == 2
    assert s["moves"][0] == {"col": 3, "by": "octocat", "issue": 12, "actor": "R"}
    assert s["last_bot"]["depth"] >= 1 and s["revision"] == 1 and s["movers"] == {"octocat": 1}
    assert "column 4" in out.message and "octocat" in out.subject


def test_full_column_rejected_without_change():
    s = G.new_state()
    s["board"] = ["R......", "B......", "R......", "B......", "R......", "B......"]
    s["moves"] = [{}] * 6
    before = json.loads(json.dumps(s))
    s2, out = G.apply_human_move(s, 0, "octocat", 13, budget=0.2)
    assert not out.accepted and s2 == before


def test_human_win_updates_record_and_finishes():
    s = G.new_state()
    s["board"] = ["......." , "......." , "......." , "......." , "......." , "RRR.BBB"]
    s["moves"] = [{}] * 6
    s2, out = G.apply_human_move(s, 3, "octocat", 14, budget=0.2)
    assert s2["finished"] and s2["result"] == "R" and s2["record"]["humans"] == 1
    assert "won" in out.message.lower()


def test_next_move_after_finish_starts_new_game():
    s = G.new_state()
    s.update(finished=True, result="R", game_no=4, record={"humans": 1, "bot": 0, "draws": 0},
             board=["......." , "......." , "......." , "......." , "......." , "RRRRBBB"],
             moves=[{"col": 0, "by": "x", "issue": 1, "actor": "R"}] * 7)
    s2, out = G.apply_human_move(s, 0, "hubot", 15, budget=0.2)
    assert s2["game_no"] == 5 and not s2["finished"] and s2["record"]["humans"] == 1
    assert s2["last_game"] == {"game_no": 4, "result": "R", "moves": 7, "winning_move_by": "x"}
    assert sum(row.count("R") for row in s2["board"]) == 1


def test_bad_column_rejected():
    s, out = G.apply_human_move(G.new_state(), 9, "x", 1, budget=0.1)
    assert not out.accepted


def test_apply_issues_in_order_with_one_outcome_each():
    issues = [{"number": 5, "col": 3, "actor": "octocat"}, {"number": 6, "col": 3, "actor": "hubot"},
              {"number": 7, "col": 3, "actor": "hubot"}]
    s, outcomes = G.apply_issues(G.new_state(), issues, budget=0.2)
    assert [o["number"] for o in outcomes] == [5, 6, 7]
    assert all(o["accepted"] for o in outcomes)
    assert s["revision"] == 3 and len(s["moves"]) == 6 and s["movers"] == {"octocat": 1, "hubot": 2}
    assert [m["issue"] for m in s["moves"] if m["actor"] == "R"] == [5, 6, 7]
    assert G.commit_subject(outcomes) == "c4: 3 moves by @octocat, @hubot"
    assert G.commit_subject(outcomes[:1]) == "c4: game 1 move 1 by @octocat"


def test_apply_issues_full_column_rejected_but_later_issue_still_played():
    s = G.new_state()
    s["board"] = ["R......", "B......", "R......", "B......", "R......", "B......"]
    s["moves"] = [{}] * 6
    s, outcomes = G.apply_issues(s, [{"number": 1, "col": 0, "actor": "a"}, {"number": 2, "col": 1, "actor": "b"}], budget=0.2)
    assert [o["accepted"] for o in outcomes] == [False, True]
    assert "full" in outcomes[0]["message"] and s["revision"] == 1


def test_human_win_appends_hall_entry_and_wall_line():
    s = G.new_state()
    s["board"] = ["......." , "......." , "......." , "......." , "......." , "RRR.BBB"]
    s["moves"] = [{}] * 6
    s2, out = G.apply_human_move(s, 3, "octocat", 14, budget=0.2)
    assert s2["hall"] == [{"game_no": 1, "by": "octocat", "moves": 7}]
    assert out.message == ("@octocat dropped in column 4 and won game 1. You're on the wall now. "
                           "The next drop starts game 2.")


def test_bot_win_and_draw_leave_hall_alone():
    s = G.new_state()
    s["board"] = ["......." , "......." , "......." , "......." , "R......" , "RR.BBB."]
    s["moves"] = [{}] * 6
    s2, out = G.apply_human_move(s, 0, "octocat", 1, budget=0.3)
    assert s2["finished"] and s2["result"] == "B" and s2["hall"] == []
    s = G.new_state()
    s["board"] = ["..RBRBR", "RBRBRBR", "BRBRBRB", "BRBRBRB", "RBRBRBR", "RBRBRBR"]
    s["moves"] = [{}] * 40
    s2, out = G.apply_human_move(s, 0, "octocat", 2, budget=0.3)
    assert s2["finished"] and s2["result"] == "draw" and s2["record"]["draws"] == 1 and s2["hall"] == []


def test_load_migrates_missing_hall_and_rollover_carries_it(tmp_path):
    old = G.new_state()
    del old["hall"]
    (tmp_path / "state.json").write_text(json.dumps(old), encoding="utf-8")
    assert G.load(tmp_path / "state.json")["hall"] == []
    s = G.new_state()
    s.update(finished=True, result="R", game_no=4, hall=[{"game_no": 4, "by": "x", "moves": 7}],
             board=["......." , "......." , "......." , "......." , "......." , "RRRRBBB"],
             moves=[{"col": 0, "by": "x", "issue": 1, "actor": "R"}] * 7)
    s2, _ = G.apply_human_move(s, 0, "hubot", 15, budget=0.2)
    assert s2["game_no"] == 5 and s2["hall"] == [{"game_no": 4, "by": "x", "moves": 7}]
