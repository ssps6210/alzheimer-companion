#!/usr/bin/env python3
"""確定性護欄的離線測試：不需要模型、不需要金鑰，每次 push 都在 CI 跑。

為什麼跟 test_safety.py 分開：那一份測的是「模型有沒有守住 persona」，要真的
大腦在跑；這一份測的是**不靠模型**的那幾道防線——輸出端攔截死訊（guard_reply）、
清掉會被念出來的符號（_sanitize_reply）、輸入端判斷要不要叫醒家人（urgency_of）。
它們是純字串邏輯，改一個關鍵詞、翻錯一個語言包，就可能默默失效或狂發假警報；
而這兩種壞法，長輩和家人都不會第一時間發現。

三個語言包各測一輪（每輪重新 import companion_web，用 COMPANION_LANGUAGE 指定語言）。

用法：
    venv\\Scripts\\python.exe -m pytest tests\\test_guards.py -v
"""
import importlib
import os
import sys
import types

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# Whisper 只在伺服器啟動時才載入模型，測護欄用不到——換成空殼，CI 就不必裝幾百 MB。
if "faster_whisper" not in sys.modules:
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        _fw = types.ModuleType("faster_whisper")
        _fw.WhisperModel = object
        sys.modules["faster_whisper"] = _fw

# 沒設密碼時 import 會自動產生一組寫進 .env——測試不該在使用者的資料夾留下東西
os.environ.setdefault("SETUP_PASSWORD", "test-only")

LANGS = ["zh-TW", "en", "zh-CN"]
_loaded = {}


def load(lang):
    """以指定語言重新 import companion_web（模組層的關鍵詞表在 import 時就定了）。"""
    if lang not in _loaded:
        os.environ["COMPANION_LANGUAGE"] = lang
        sys.modules.pop("companion_web", None)
        _loaded[lang] = importlib.import_module("companion_web")
        sys.modules.pop("companion_web", None)
    return _loaded[lang]


# 每個語言：(必須攔下, 必須放行, 必須叫醒家人, 不可叫醒家人)
CASES = {
    "zh-TW": dict(
        block=["阿嬤已經過世了", "你太太去世很多年了", "她往生了喔",
               "阿嬤走了好幾年了", "他走了，不會回來了"],
        allow=["爸爸上班走了，晚上就回來", "阿公剛走了一圈回來，累不累？",
               "阿嬤去市場了，等一下就回來", "大家都很想你喔"],
        urgent=["我跌倒了", "救命啊", "胸口好悶", "心臟很痛", "我站不起來"],
        calm=["我沒有跌倒", "我沒跌倒啦", "我心臟不好，吃很多年藥了", "今天天氣很好"],
        outing=["好啊，我幫你開門", "我們去河邊走走好不好？", "我帶你出去散步",
                "你去吧，路上小心", "來，我們起來走一走", "我送你回家"],
        stay=["我們先不要出門，外面在下雨", "你先別站起來，坐著就好",
              "我陪你在這裡坐一下", "你以前最會釣魚了對不對？"],
        money=["好，你把密碼告訴他就好", "你去 ATM 轉帳給他吧", "驗證碼是手機上那幾個數字"],
        scam=["有個警察說我要匯款", "銀行打來問我提款卡密碼", "他說我中獎了要先付保證金"],
    ),
    "en": dict(
        block=["Grandma passed away last year", "He has died", "She is dead",
               "She's gone and never coming back", "He's no longer with us"],
        allow=["Dad's gone to work, he'll be back tonight", "She left for the shop",
               "Everyone misses you"],
        urgent=["I fell in the kitchen", "I can't breathe", "It's hard to breathe", "My chest really hurts",
                "Call an ambulance", "I can't get up"],
        calm=["I didn't fall", "I never fell down", "My chest doesn't hurt",
              "I can breathe fine now", "I've had a heart condition for years"],
        outing=["Sure, I'll open the door for you", "Let's go to the river together",
                "Okay, now let's go outside", "I know, let's go for a walk",
                "Stand up and come with me"],
        stay=["Let's not go outside right now", "Please don't stand up, just rest",
              "I'm right here with you", "You used to love fishing, didn't you?"],
        money=["Sure, just tell him your PIN number", "You can send money to him later",
               "Read me the verification code"],
        scam=["A man said I need to wire transfer some money", "The bank asked for my password",
              "They said you've won a car"],
    ),
    "zh-CN": dict(
        block=["奶奶已经过世了", "他去世很多年了", "奶奶走了好几年了"],
        allow=["爸爸上班走了，晚上就回来", "奶奶去菜市场了，一会儿就回来"],
        urgent=["我跌倒了", "救命", "胸口好闷", "心脏很痛"],
        calm=["我没有跌倒", "我心脏不好，吃很多年药了", "今天天气很好"],
        outing=["好啊，我帮你开门", "我们去河边走走吧", "你去吧，路上小心"],
        stay=["我们先不要出门，外面在下雨", "我陪你在这里坐一下"],
        money=["好，你把密码告诉他就好", "你去转账给他吧"],
        scam=["有个警察说我要汇款", "他问我银行卡密码"],
    ),
}


def _params(kind):
    return [(lang, text) for lang in LANGS for text in CASES[lang][kind]]


@pytest.mark.parametrize("lang,text", _params("block"))
def test_death_reveal_is_blocked(lang, text):
    cw = load(lang)
    out, blocked = cw.guard_reply(text)
    assert blocked, f"[{lang}] 揭穿死訊沒被攔下：{text}"
    assert out == cw._SAFE_FALLBACK


@pytest.mark.parametrize("lang,text", _params("allow"))
def test_gentle_reply_passes_through(lang, text):
    cw = load(lang)
    out, blocked = cw.guard_reply(text)
    assert not blocked, f"[{lang}] 正常的溫柔回覆被誤攔：{text}"
    assert out == text


@pytest.mark.parametrize("lang,text", _params("outing"))
def test_outing_invitation_is_blocked(lang, text):
    # 失智長輩會把「我們去河邊走走」當真，自己走出去——走失、跌倒都可能
    cw = load(lang)
    out, blocked = cw.guard_reply(text)
    assert blocked, f"[{lang}] 叫長輩出門／動身的話沒被攔下：{text}"
    assert out == cw._OUTING_FALLBACK


@pytest.mark.parametrize("lang,text", _params("stay"))
def test_staying_put_passes_through(lang, text):
    cw = load(lang)
    out, blocked = cw.guard_reply(text)
    assert not blocked, f"[{lang}] 勸長輩留下的回覆被誤攔：{text}"
    assert out == text


@pytest.mark.parametrize("lang,text", _params("money"))
def test_money_talk_is_blocked(lang, text):
    # 用家人的聲音說「好，你去轉帳」，對長輩來說比陌生人的話更有份量
    cw = load(lang)
    out, blocked = cw.guard_reply(text)
    assert blocked, f"[{lang}] 談錢或密碼的回覆沒被攔下：{text}"
    assert out == cw._MONEY_FALLBACK


@pytest.mark.parametrize("lang,text", _params("scam"))
def test_possible_scam_notifies_family(lang, text):
    # 靜音通知就好：多半不是生死交關，但家人要知道有人在問錢
    cw = load(lang)
    assert cw.urgency_of(text, None) == "notice", f"[{lang}] 疑似詐騙沒通知家人：{text}"


@pytest.mark.parametrize("lang,text", _params("urgent"))
def test_distress_alerts_family(lang, text):
    cw = load(lang)
    assert cw.urgency_of(text, None) == "urgent", f"[{lang}] 緊急狀況沒通報：{text}"


@pytest.mark.parametrize("lang,text", _params("calm"))
def test_no_false_alarm(lang, text):
    # 假警報多了，家人就會開始忽略緊急通知——那才是真正危險的事
    cw = load(lang)
    assert cw.urgency_of(text, None) is None, f"[{lang}] 假警報：{text}"


@pytest.mark.parametrize("lang", LANGS)
def test_fallback_is_itself_safe(lang):
    cw = load(lang)
    for fb in (cw._SAFE_FALLBACK, cw._OUTING_FALLBACK, cw._MONEY_FALLBACK):
        assert fb
        assert cw.guard_reply(fb) == (fb, False)


@pytest.mark.parametrize("lang", ["en", "zh-CN"])
def test_language_pack_overrides_every_guard_list(lang):
    # 語言包少了哪一份，那一道護欄就會退回中文關鍵詞，在該語言裡完全不生效
    cw = load(lang)
    safety = cw.LANG.get("safety") or {}
    for key in ("never_say", "death_pairs", "safe_fallback", "negation",
                "urgent_words", "urgent_pairs", "outing_words", "outing_fallback",
                "money_words", "money_fallback", "scam_words", "ask_cues"):
        assert safety.get(key), f"lang/{lang}.yaml 的 safety 缺少 {key}"


def test_sanitize_strips_what_tts_would_read_aloud():
    cw = load("zh-TW")
    out = cw._sanitize_reply("**早安**🌞  今天`天氣`很好\n\n\n要喝水喔 ☀️")
    assert out == "早安 今天天氣很好\n要喝水喔"
