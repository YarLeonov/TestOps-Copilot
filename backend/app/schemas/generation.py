from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ManualGenerationRequest(BaseModel):
    """Запрос на генерацию ручных тест-кейсов."""

    project_id: Optional[str] = Field(default=None)
    scenario_type: str = Field(
        default="ui",
        description="Тип сценария: ui или api",
        examples=["ui", "api"],
    )
    source_type: str = Field(
        default="text",
        description="Тип источника: text или openapi",
    )
    content: str = Field(
        ...,
        description="Текст требований или содержимое OpenAPI",
    )
    max_tests: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Максимальное количество генерируемых тест-кейсов",
    )


class AutomationGenerationRequest(BaseModel):
    """Запрос на генерацию кода автотестов на основе ручных кейсов."""

    project_id: Optional[str] = Field(default=None)
    target: str = Field(
        default="ui",
        description="Цель: ui или api",
    )
    manual_test_cases: List[str] = Field(
        default_factory=list,
        description="Сырые описания ручных тест-кейсов",
    )


class ValidationRequest(BaseModel):
    """Запрос на валидацию тестов по стандартам."""

    project_id: Optional[str] = Field(default=None)
    code: str = Field(..., description="Исходный код автотестов для проверки")
    rules: List[str] = Field(default_factory=list, description="Дополнительные правила валидации")


class CodeBundle(BaseModel):
    """Один файл с кодом автотестов."""

    name: str
    language: str = "python"
    content: str


class GenerationResponse(BaseModel):
    """Общий ответ генерации или валидации."""

    project_id: Optional[str] = None
    summary: str
    manual_test_cases: List[str] = Field(default_factory=list)
    code_bundles: List[CodeBundle] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
