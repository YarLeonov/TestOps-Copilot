import { apiRequest } from "./client";

export type ScenarioType = "ui" | "api";

export interface ManualGenerationRequest {
  project_id?: string | null;
  scenario_type: ScenarioType;
  source_type: "text" | "openapi";
  content: string;
  max_tests: number;
}

export interface AutomationGenerationRequest {
  project_id?: string | null;
  target: ScenarioType;
  manual_test_cases: string[];
}

export interface ValidationRequest {
  project_id?: string | null;
  code: string;
  rules: string[];
}

export interface CodeBundle {
  name: string;
  language: string;
  content: string;
}

export interface GenerationResponse {
  project_id?: string | null;
  summary: string;
  manual_test_cases: string[];
  code_bundles: CodeBundle[];
  warnings: string[];
}

export async function generateManual(
  payload: ManualGenerationRequest
): Promise<GenerationResponse> {
  return apiRequest<GenerationResponse>("/generation/manual", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function generateAutomation(
  payload: AutomationGenerationRequest
): Promise<GenerationResponse> {
  return apiRequest<GenerationResponse>("/generation/automation", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function validateTests(
  payload: ValidationRequest
): Promise<GenerationResponse> {
  return apiRequest<GenerationResponse>("/generation/validate", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}
