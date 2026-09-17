import json

from connect4 import game as G


def test_new_state_shape():
    s = G.new_state()
    assert s["board"] == ["......."] * 6 and s["to_play"] == "R" and s["moves"] == []
    assert s["record"] == {"humans": 0, "bot": 0, "draws": 0} and s["revision"] == 0


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
