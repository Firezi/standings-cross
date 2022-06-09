from fastapi import APIRouter

from .auth import router as auth_router
from .tasks import router as tasks_router

router: APIRouter = APIRouter()

router.include_router(auth_router)
router.include_router(tasks_router)
