import pytz
from datetime import datetime
from passlib.context import CryptContext

from src.models import User, Task, UserTask


def test_user_password_verification():
    password = "TestPassword1234"
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    hashed_password = pwd_context.hash(password)
    u = User(username="test-user", hashed_password=hashed_password)

    assert u.verify_password("another-password") is False
    assert u.verify_password(password) is True


def test_task_check_answer():
    right_answer = "Ireland"
    t = Task(
        name="Task",
        coords="coords",
        statement="Text",
        right_answer=right_answer,
        hint_1="Ir",
        hint_2="el",
        hint_3="and",
    )
    assert t.check_answer("Ireland") is True
    assert t.check_answer("irelaND") is True
    assert t.check_answer("Iceland") is False


def test_user_task_resolving():
    start_dt = datetime(2022, 1, 1, 9, tzinfo=pytz.utc)
    resolving_dt = datetime(2022, 1, 1, 10, 5, 40, tzinfo=pytz.utc)

    ut = UserTask(user_id="1", task_id="1")
    ut.handle_task_resolving(resolving_dt, start_dt)
    assert ut.is_resolved is True
    assert ut.resolving_penalty == 65

    ut = UserTask(
        user_id="1",
        task_id="1",
        hint_1_used=True,
        hint_2_used=True,
        hint_3_used=True,
        wrong_attempts_count=4,
    )
    ut.handle_task_resolving(resolving_dt, start_dt)
    assert ut.is_resolved is True
    assert ut.resolving_penalty == 65 + 15 * 3 + 30 * 4
