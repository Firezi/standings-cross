from datetime import datetime
from pydantic import BaseModel, SecretStr, root_validator, Field

from src.models import GameInfo


class UserCredentials(BaseModel):
    username: str
    password: SecretStr


class UserTokenResponse(BaseModel):
    access_token: str


class HintForUser(BaseModel):
    hint_text: str
    is_used: bool = False

    @root_validator(pre=True)
    def hide_hint_if_not_used(cls, values) -> str:
        if not values["is_used"]:
            values["hint_text"] = ""
        return values


class TaskForUser(BaseModel):
    id: int
    name: str
    coords: str
    statement: str
    is_resolved: bool = False
    is_tried: bool = False
    hints: dict[str, HintForUser]


class TasksResponse(BaseModel):
    tasks: list[TaskForUser] = []

    @staticmethod
    def configure(raw_tasks: list) -> "TasksResponse":
        result_tasks: list[TaskForUser] = []

        for task in raw_tasks:
            user_task = None
            if len(task.users) != 0:
                user_task = task.users[0]
            hints = {
                i: HintForUser(
                    hint_text=getattr(task, f"hint_{i}"),
                    is_used=bool(user_task and getattr(user_task, f"hint_{i}_used")),
                )
                for i in ["1", "2", "3"]
            }

            result_tasks.append(
                TaskForUser(
                    id=int(task.id),
                    name=task.name,
                    coords=task.coords,
                    statement=task.statement,
                    is_resolved=bool(user_task and user_task.is_resolved),
                    is_tried=bool(
                        user_task and (user_task.wrong_attempts_count > 0 or user_task.is_resolved)
                    ),
                    hints=hints,
                )
            )

        return TasksResponse(tasks=result_tasks)


class HintParams(BaseModel):
    task_id: int
    hint_id: int = Field(qe=1, le=3)


class AnswerStatusResponse(BaseModel):
    is_answer_right: bool
    wrong_answers_count: int


class AnswerParams(BaseModel):
    task_id: int
    answer: str


class TaskInStandings(BaseModel):
    task_id: int
    is_resolved: bool = False
    wrong_attempts_count = 0
    penalty: int = 0


class UserInStandings(BaseModel):
    username: str
    total_resolved: int = 0
    total_penalty: int = 0
    place: int = 0
    tasks: list[TaskInStandings] = []


class StandingsResponse(BaseModel):
    game_start_dt: datetime
    game_end_dt: datetime
    users_table: list[UserInStandings] = []

    @staticmethod
    def configure(
        raw_users: list, all_task_ids: tuple[int], game_info: GameInfo
    ) -> "StandingsResponse":
        users_table: list[UserInStandings] = []

        for user in raw_users:
            recorded_task_ids = []
            total_resolved = 0
            total_penalty = 0
            tasks: list[TaskInStandings] = []

            for t in user.tasks:
                recorded_task_ids.append(t.task_id)
                total_resolved += t.is_resolved
                total_penalty += t.resolving_penalty
                tasks.append(
                    TaskInStandings(
                        task_id=t.task_id,
                        is_resolved=t.is_resolved,
                        wrong_attempts_count=t.wrong_attempts_count,
                        penalty=t.resolving_penalty,
                    )
                )
            for task_id in all_task_ids:
                if task_id not in recorded_task_ids:
                    tasks.append(TaskInStandings(task_id=task_id))

            tasks.sort(key=lambda x: x.task_id)
            users_table.append(
                UserInStandings(
                    username=user.username,
                    total_resolved=total_resolved,
                    total_penalty=total_penalty,
                    tasks=tasks,
                )
            )

        users_table.sort(key=lambda x: (-x.total_resolved, x.total_penalty))
        for i in range(len(users_table)):
            if (
                i > 0
                and users_table[i - 1].total_resolved == users_table[i].total_resolved
                and users_table[i - 1].total_penalty == users_table[i].total_penalty
            ):
                users_table[i].place = users_table[i - 1].place
            else:
                users_table[i].place = i + 1

        return StandingsResponse(
            game_start_dt=game_info.start_dt,
            game_end_dt=game_info.end_dt,
            users_table=users_table,
        )
