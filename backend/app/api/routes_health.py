from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from app.core.config import settings


class LLMClient:
    """Простая обертка над Cloud.ru Evolution LLM.

    Сейчас реализован stub режим, если не настроены переменные окружения.
    Под реальный API можно будет заменить метод _call_provider.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        token: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.endpoint = endpoint or settings.cloud_llm_endpoint
        self.token = token or settings.cloud_llm_token
        self.model = model or settings.cloud_llm_model

    @property
    def is_configured(self) -> bool:
        return bool(self.endpoint and self.token)

    async def generate(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.2,
    ) -> str:
        """Сгенерировать ответ модели.

        Если провайдер не настроен, возвращает stub текст, чтобы не ломать демо.
        """
        if not self.is_configured:
            return self._stub_response(prompt)

        try:
            return await self._call_provider(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except Exception as exc:
            # На хакатоне лучше вернуть осмысленное сообщение, чем упасть
            return f"[LLM error: {exc!r}] Fallback for prompt: {prompt[:200]}"

    async def _call_provider(
        self,
        *,
        prompt: str,
        system_prompt: Optional[str],
        max_tokens: int,
        temperature: float,
    ) -> str:
        """Вызов реального LLM провайдера.

        Эту часть нужно будет адаптировать под контракт Cloud.ru Evolution.
        Сейчас оставлено как заготовка с пост-запросом.
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {
            "model": self.model,
            "input": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_prompt:
            payload["system"] = system_prompt

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                str(self.endpoint),
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        # Тут нужно подставить реальный ключ из ответа LLM
        text = data.get("output") or data.get("result") or str(data)
        return str(text)

    def _stub_response(self, prompt: str) -> str:
        preview = prompt.replace("\n", " ")[:160]
        return (
            "[LLM not configured] "
            "Backend вернул стабильный stub ответ. "
            f"Часть промпта: {preview}"
        )


llm_client = LLMClient()
