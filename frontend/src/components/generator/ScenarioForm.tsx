import { FormEvent, useState } from "react";
import {
  AutomationGenerationRequest,
  CodeBundle,
  GenerationResponse,
  ManualGenerationRequest,
  ScenarioType,
  ValidationRequest,
  generateAutomation,
  generateManual,
  validateTests
} from "../../api/generation";
import ResultTable from "./ResultTable";
import CodePreview from "./CodePreview";

interface ScenarioFormProps {
  scenarioType: ScenarioType;
}

function ScenarioForm({ scenarioType }: ScenarioFormProps) {
  const [content, setContent] = useState("");
  const [maxTests, setMaxTests] = useState(10);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [manualTests, setManualTests] = useState<string[]>([]);
  const [bundles, setBundles] = useState<CodeBundle[]>([]);
  const [warnings, setWarnings] = useState<string[]>([]);

  const hasManualTests = manualTests.length > 0;
  const hasBundles = bundles.length > 0;

  async function handleGenerateManual(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSummary(null);
    setBundles([]);
    setWarnings([]);

    if (!content.trim()) {
      setError("Введите требования или описание сценария");
      return;
    }

    const payload: ManualGenerationRequest = {
      project_id: "demo-project",
      scenario_type: scenarioType,
      source_type: "text",
      content,
      max_tests: maxTests
    };

    try {
      setLoading(true);
      const response: GenerationResponse = await generateManual(payload);
      setSummary(response.summary);
      setManualTests(response.manual_test_cases);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Ошибка генерации тест-кейсов");
    } finally {
      setLoading(false);
    }
  }

  async function handleGenerateAutomation() {
    setError(null);
    setSummary(null);
    setBundles([]);
    setWarnings([]);

    if (!hasManualTests) {
      setError("Сначала сгенерируйте ручные тест-кейсы");
      return;
    }

    const payload: AutomationGenerationRequest = {
      project_id: "demo-project",
      target: scenarioType,
      manual_test_cases: manualTests
    };

    try {
      setLoading(true);
      const response = await generateAutomation(payload);
      setSummary(response.summary);
      setBundles(response.code_bundles);
      setWarnings(response.warnings || []);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Ошибка генерации кода автотестов"
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleValidateCode() {
    setError(null);
    setSummary(null);
    setWarnings([]);

    if (!hasBundles) {
      setError("Нет сгенерированного кода для проверки");
      return;
    }

    // Проверяем первый файл, для демо этого достаточно
    const codeToValidate = bundles[0].content;

    const payload: ValidationRequest = {
      project_id: "demo-project",
      code: codeToValidate,
      rules: []
    };

    try {
      setLoading(true);
      const response = await validateTests(payload);
      setSummary(response.summary);
      setWarnings(response.warnings || []);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Ошибка проверки автотестов по стандартам"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="scenario-form">
      <form onSubmit={handleGenerateManual} className="scenario-form-panel">
        <div className="field-group">
          <label className="field-label">
            Требования или описание сценария
            <textarea
              className="field-textarea"
              placeholder={
                scenarioType === "ui"
                  ? "Например: пользователь открывает калькулятор стоимости, выбирает продукт и конфигурацию..."
                  : "Вставьте выдержку требований или описание того, что должно делать API..."
              }
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={8}
            />
          </label>
        </div>

        <div className="field-row">
          <label className="field-label-inline">
            Количество тест-кейсов
            <input
              type="number"
              min={1}
              max={50}
              value={maxTests}
              onChange={(e) => setMaxTests(Number(e.target.value) || 1)}
              className="field-input-number"
            />
          </label>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? "Генерация..." : "Сгенерировать тест-кейсы"}
          </button>
        </div>
      </form>

      {error && <div className="alert alert-error">{error}</div>}

      {summary && <div className="alert alert-info">{summary}</div>}

      <div className="scenario-results">
        <div className="scenario-column">
          <div className="scenario-column-header">
            <h2>Ручные тест-кейсы</h2>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleGenerateAutomation}
              disabled={loading || !hasManualTests}
            >
              Сгенерировать автотесты
            </button>
          </div>

          <ResultTable testCases={manualTests} />
        </div>

        <div className="scenario-column">
          <div className="scenario-column-header">
            <h2>Код автотестов</h2>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleValidateCode}
              disabled={loading || !hasBundles}
            >
              Проверить по стандартам
            </button>
          </div>

          <CodePreview bundles={bundles} />
          {warnings.length > 0 && (
            <div className="alert alert-warning">
              <strong>Замечания:</strong>
              <ul>
                {warnings.map((w, idx) => (
                  <li key={idx}>{w}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default ScenarioForm;
