from src.api.schemas import HintForUser


def test_hint_hiding():
    assert HintForUser(hint_text="text", is_used=False).hint_text == ""
    assert HintForUser(hint_text="text", is_used=True).hint_text == "text"
