from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", description="Liveness check.")
def health_status() -> dict[str, str]:
    return {"status": "ok"}
