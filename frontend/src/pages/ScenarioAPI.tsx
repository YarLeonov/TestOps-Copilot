import ScenarioForm from "../components/generator/ScenarioForm";

function ScenarioAPI() {
  return (
    <div className="page">
      <h1>API сценарий</h1>
      <p className="page-subtitle">
        Генерация тест-кейсов и автотестов для REST API по текстовым требованиям или OpenAPI
        спецификации.
      </p>
      <ScenarioForm scenarioType="api" />
    </div>
  );
}

export default ScenarioAPI;
