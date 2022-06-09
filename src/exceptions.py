from fastapi import HTTPException, status


class AuthException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Not authenticated"}
        )


class GameIsNotActive(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Game is not active"}
        )


class TaskAlreadyResolved(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"message": "Task already resolved"}
        )


class TaskNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Task with task_id not found"},
        )
