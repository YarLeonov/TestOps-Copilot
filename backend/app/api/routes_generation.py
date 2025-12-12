from fastapi import APIRouter

from app.schemas.generation import (
    AutomationGenerationRequest,
    GenerationResponse,
    ManualGenerationRequest,
    ValidationRequest,
)
from app.services.testcases_service import TestCasesService

router = APIRouter()

service = TestCasesService()


@router.post("/manual", response_model=GenerationResponse)
async def generate_manual(request: ManualGenerationRequest) -> GenerationResponse:
    return await service.generate_manual(request)


@router.post("/automation", response_model=GenerationResponse)
async def generate_automation(request: AutomationGenerationRequest) -> GenerationResponse:
    return await service.generate_automation(request)


@router.post("/validate", response_model=GenerationResponse)
async def validate_tests(request: ValidationRequest) -> GenerationResponse:
    return await service.validate_tests(request)
