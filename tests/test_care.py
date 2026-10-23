#!/usr/bin/env python3
"""照護功能的離線測試：家庭事實表、喪親固定回答、撤回聲音、家人通知。

跟 test_guards.py 一樣不需要模型、不需要金鑰，每次 push 都在 CI 跑。

用法：
    venv\\Scripts\\python.exe -m pytest tests\\test_care.py -v
"""
import asyncio
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_guards import ROOT, load  # noqa: E402  （共用同一套載入與 faster_whisper 空殼）

EXAMPLE = os.path.join(ROOT, "family.example.yaml")


@pytest.fixture
def cw():
    m = load("zh-TW")
    saved = dict(m.family)
    yield m
    m.family = saved


def test_example_family_file_is_valid(cw):
    # 家人第一次打開管理台看到的就是這份範本，它本身一定要能存
    with open(EXAMPLE, encoding="utf-8") as f:
        d, err = cw.parse_family(f.read())
    assert err is None, err
    assert d["people"] and d["bereavement"]
    for b in d["bereavement"]:
        # 範本裡的固定回答不能自己踩到護欄
        assert cw.guard_reply(b["reply"]) == (b["reply"], False)


@pytest.mark.parametrize("text,why", [
    ("people: 阿明", "分類底下要是清單"),
    ("bereavement:\n  - triggers: [阿嬤]\n    reply: 她在忙", "沒寫是誰決定的"),
    ("bereavement:\n  - triggers: []\n    reply: 她在忙\n    approved_by: 阿明", "沒有稱呼"),
    ("people: [", "YAML 壞掉"),
    ("- 只是一個清單", "最外層不是分類"),
])
def test_bad_family_file_is_rejected(cw, text, why):
    _, err = cw.parse_family(text)
    assert err, f"應該擋下（{why}）"


def _set_family(cw, text):
    d, err = cw.parse_family(text)
    assert err is None, err
    cw.family = d


BEREAVEMENT = """
people:
  - 大兒子阿明住台北
bereavement:
  - about: 奶奶
    triggers: [阿嬤, 我太太]
    reply: 阿嬤在忙，我們先坐一下
    approved_by: 阿明
"""


@pytest.mark.parametrize("text", ["阿嬤呢？", "我太太去哪了", "我要找阿嬤", "阿嬤怎麼沒來"])
def test_asking_for_deceased_gets_the_approved_reply(cw, text):
    _set_family(cw, BEREAVEMENT)
    assert cw.bereavement_reply(text) == "阿嬤在忙，我們先坐一下"


@pytest.mark.parametrize("text", ["阿嬤以前煮的菜很好吃", "今天幾號", "阿明呢"])
def test_other_talk_goes_to_the_model(cw, text):
    # 只是聊到她、或問的是別人，就照常交給模型
    _set_family(cw, BEREAVEMENT)
    assert cw.bereavement_reply(text) is None


def test_facts_reach_the_prompt_but_only_what_is_written(cw):
    _set_family(cw, BEREAVEMENT)
    p = cw.get_system_prompt()
    assert "大兒子阿明住台北" in p
    assert "不可以自己編" in p
    cw.family = {}
    assert "大兒子阿明住台北" not in cw.get_system_prompt()


def test_english_cues_find_a_deceased_relative():
    en = load("en")
    d, err = en.parse_family(
        "bereavement:\n  - triggers: [Margaret, my wife]\n"
        "    reply: Margaret is busy just now. Sit with me a while?\n    approved_by: Tom\n")
    assert err is None, err
    saved, en.family = en.family, d
    try:
        assert en.bereavement_reply("Where is my wife?")
        assert en.bereavement_reply("I'm looking for Margaret")
        assert en.bereavement_reply("Margaret made lovely bread") is None
    finally:
        en.family = saved


def test_revoking_the_voice_deletes_it_and_logs_only_a_fingerprint(cw, tmp_path, monkeypatch):
    vdir = tmp_path / "voices"
    vdir.mkdir()
    (vdir / "active_reference.wav").write_bytes(b"RIFF....")
    (vdir / "active_reference.txt").write_text("我同意用我的聲音陪伴家人", encoding="utf-8")
    (vdir / "active_reference.consent.json").write_text(
        json.dumps({"ref_sha256": "abc123"}), encoding="utf-8")
    (vdir / "other_voice.wav").write_bytes(b"keep")
    monkeypatch.setattr(cw, "SCRIPT_DIR", str(tmp_path))
    monkeypatch.setattr(cw.requests, "post", lambda *a, **k: None)
    cw.tts_cache["舊的"] = (b"x", "audio/wav")

    out = asyncio.run(cw.setup_revoke_voice())

    assert sorted(out["removed"]) == ["active_reference.consent.json",
                                      "active_reference.txt", "active_reference.wav"]
    assert (vdir / "other_voice.wav").exists()
    assert not cw.tts_cache
    log = (vdir / "revocations.log").read_text(encoding="utf-8")
    assert "abc123" in log and "同意" not in log   # 只留指紋，不留內容


def test_line_push_is_silent_unless_urgent(cw, monkeypatch):
    calls = []

    class Ok:
        status_code = 200
        text = ""

    def fake_post(url, json=None, **k):
        calls.append((url, json))
        return Ok()

    monkeypatch.setattr(cw, "LINE_TOKEN", "t")
    monkeypatch.setattr(cw, "LINE_TO", "U123")
    monkeypatch.setattr(cw, "TELEGRAM_TOKEN", "")
    monkeypatch.setattr(cw.requests, "post", fake_post)

    asyncio.run(cw.notify_family("爺爺說他跌倒了", "urgent"))
    asyncio.run(cw.notify_family("爺爺提到轉帳", "notice"))

    (u1, b1), (u2, b2) = calls
    assert u1.startswith("https://api.line.me/") and b1["to"] == "U123"
    assert b1["notificationDisabled"] is False
    assert b2["notificationDisabled"] is True


def test_last_heard_comes_from_saved_patterns(cw, monkeypatch):
    monkeypatch.setattr(cw, "patterns", [{"key": "a", "times": [100, 300]},
                                         {"key": "b", "times": [200]}])
    assert cw.last_heard_ts() == 300
    monkeypatch.setattr(cw, "patterns", [])
    assert cw.last_heard_ts() is None
