import pytz
from datetime import datetime
from fastapi import Depends, APIRouter
from tortoise.query_utils import Prefetch

from src.models import User, Task, UserTask, GameInfo
from .auth import get_authorized_user
from .schemas import (
    TasksResponse,
    HintForUser,
    HintParams,
    AnswerParams,
    AnswerStatusResponse,
    StandingsResponse,
)
from src.utils import is_competition_running
from src.exceptions import GameIsNotActive, TaskAlreadyResolved, TaskNotFound


router = APIRouter()


@router.get("/tasks", response_model=TasksResponse)
async def get_all_tasks(user: User = Depends(get_authorized_user)):
    tasks = (
        await Task.all()
        .prefetch_related(Prefetch("users", queryset=UserTask.filter(user_id=user.id)))
        .order_by("id")
    )
    return TasksResponse.configure(tasks)


async def get_task_and_user_task(user, params, raise_if_resolved=True) -> tuple[Task, UserTask]:
    user_task = await UserTask.get_or_none(user_id=user.id, task_id=params.task_id).select_related(
        "task"
    )
    if user_task is not None:
        task = user_task.task
    else:
        user_task = UserTask(user_id=user.id, task_id=params.task_id)
        task = await Task.get_or_none(id=params.task_id)
        if task is None:
            raise TaskNotFound
    if raise_if_resolved and user_task.is_resolved:
        raise TaskAlreadyResolved
    return task, user_task


@router.post("/open-hint", response_model=HintForUser)
async def open_hint(user: User = Depends(get_authorized_user), params: HintParams = Depends()):
    now_dt = datetime.now(pytz.utc)
    if not await is_competition_running(now_dt):
        raise GameIsNotActive

    task, user_task = await get_task_and_user_task(user, params)

    hint_name = f"hint_{params.hint_id}"
    setattr(user_task, f"{hint_name}_used", True)
    await user_task.save()

    return HintForUser(hint_text=getattr(task, hint_name), is_used=True)


@router.post("/send-answer", response_model=AnswerStatusResponse)
async def send_answer(user: User = Depends(get_authorized_user), params: AnswerParams = Depends()):
    now_dt = datetime.now(pytz.utc)
    if not await is_competition_running(now_dt):
        raise GameIsNotActive

    task, user_task = await get_task_and_user_task(user, params)

    if task.check_answer(params.answer):
        game_info = await GameInfo.all().first()
        user_task.handle_task_resolving(now_dt, game_info.start_dt)
    else:
        if user_task.last_wrong_answer != params.answer:
            user_task.last_wrong_answer = params.answer
            user_task.wrong_attempts_count += 1

    await user_task.save()

    return AnswerStatusResponse(
        is_answer_right=user_task.is_resolved, wrong_answers_count=user_task.wrong_attempts_count
    )


@router.get("/standings", response_model=StandingsResponse)
async def get_standings():
    all_users = await User.all().prefetch_related("tasks")
    all_tasks = await Task.all()
    task_ids = tuple(x.id for x in all_tasks)
    game_info = await GameInfo.all().first()
    return StandingsResponse.configure(all_users, task_ids, game_info)
