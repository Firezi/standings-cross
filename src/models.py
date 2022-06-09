import pytz
from datetime import datetime
from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class GameInfo(models.Model):
    id = fields.IntField(pk=True)
    start_dt = fields.DatetimeField()
    end_dt = fields.DatetimeField(null=True, default=None)

    class Meta:
        table = "game_info"


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=32, unique=True)
    hashed_password = fields.CharField(max_length=64)

    def verify_password(self, check_password: str) -> bool:
        return pwd_context.verify(check_password, self.hashed_password)

    class PydanticMeta:
        exclude = ["hashed_password"]


class Task(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    coords = fields.CharField(max_length=64)
    statement = fields.CharField(max_length=300)
    right_answer = fields.CharField(max_length=64)
    hint_1 = fields.CharField(max_length=300)
    hint_2 = fields.CharField(max_length=300)
    hint_3 = fields.CharField(max_length=300)

    def check_answer(self, answer: str):
        return self.right_answer.lower() == answer.lower()


class UserTask(models.Model):
    user = fields.ForeignKeyField("models.User", on_delete="CASCADE", related_name="tasks")
    task = fields.ForeignKeyField("models.Task", on_delete="CASCADE", related_name="users")

    is_resolved = fields.BooleanField(default=False)
    wrong_attempts_count = fields.IntField(default=0)
    last_wrong_answer = fields.CharField(max_length=64, default=None, null=True)
    hint_1_used = fields.BooleanField(default=False)
    hint_2_used = fields.BooleanField(default=False)
    hint_3_used = fields.BooleanField(default=False)
    resolving_dt = fields.DatetimeField(null=True, default=None)
    resolving_penalty = fields.IntField(default=0)

    def handle_task_resolving(self, now_dt: datetime, start_dt: datetime) -> None:
        self.is_resolved = True
        self.resolving_dt = now_dt

        time_penalty = (now_dt - start_dt).total_seconds() // 60
        hints_penalty = (self.hint_1_used + self.hint_2_used + self.hint_3_used) * 15
        wrong_attempts_penalty = self.wrong_attempts_count * 30
        self.resolving_penalty = time_penalty + hints_penalty + wrong_attempts_penalty

    class Meta:
        table = "user_task"
        unique_together = ("user_id", "task_id")


Tortoise.init_models(["src.models"], "models")

UserSchema = pydantic_model_creator(User, name="User")
