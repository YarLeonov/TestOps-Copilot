from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings
from app.schemas.generation import CodeBundle


class GitLabService:
    """Заготовка под интеграцию с GitLab.

    Сейчас делает только заглушечный вызов, чтобы не ломать демо.
    При необходимости можно реализовать создание ветки и MR.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        project_id: Optional[int] = None,
    ) -> None:
        self.base_url = base_url or settings.gitlab_base_url
        self.token = token or settings.gitlab_token
        self.project_id = project_id or settings.gitlab_project_id

    @property
    def is_configured(self) -> bool:
        return bool(self.base_url and self.token and self.project_id)

    async def create_mr_with_tests(
        self,
        *,
        branch_name: str,
        title: str,
        code_bundles: List[CodeBundle],
        target_branch: str = "main",
    ) -> Dict[str, Any]:
        if not self.is_configured:
            # Заглушка для демо
            return {
                "url": "https://gitlab.example.com/demo/project/merge_requests/1",
                "branch": branch_name,
                "title": title,
                "note": "GitLab не настроен, возвращен stub ответ.",
            }

        # Здесь должен быть реальный вызов GitLab API
        # Оставляем заготовку, чтобы не усложнять хакатон
        async with httpx.AsyncClient(timeout=60) as client:
            _ = client  # чтобы линтер не ругался, пока нет реальной логики

        return {
            "url": f"{self.base_url}/projects/{self.project_id}/merge_requests/dummy",
            "branch": branch_name,
            "title": title,
        }
