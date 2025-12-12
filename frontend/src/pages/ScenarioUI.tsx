import ScenarioForm from "../components/generator/ScenarioForm";

function ScenarioUI() {
  return (
    <div className="page">
      <h1>UI сценарий</h1>
      <p className="page-subtitle">
        Генерация тест-кейсов и автотестов для пользовательского интерфейса, например калькулятора
        стоимости.
      </p>
      <ScenarioForm scenarioType="ui" />
    </div>
  );
}

export default ScenarioUI;
