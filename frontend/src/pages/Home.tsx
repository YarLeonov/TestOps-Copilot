import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="page page-home">
      <h1>TestOps Copilot</h1>
      <p className="page-subtitle">
        AI ассистент, который берет на себя рутину по генерации тест-кейсов и автотестов.
      </p>

      <div className="cards-grid">
        <div className="card">
          <h2>UI сценарий</h2>
          <p>
            Вставьте требования к интерфейсу, выберите количество кейсов и получите набор ручных
            тестов и автотестов.
          </p>
          <Link to="/ui" className="btn btn-primary">
            Перейти к UI сценарию
          </Link>
        </div>

        <div className="card">
          <h2>API сценарий</h2>
          <p>
            Используйте требования к API или выдержку из OpenAPI, чтобы быстро собрать тестовый
            набор для backend.
          </p>
          <Link to="/api" className="btn btn-primary">
            Перейти к API сценарию
          </Link>
        </div>
      </div>

      <section className="section">
        <h2>Как это работает</h2>
        <ol className="steps-list">
          <li>Вставляете текст требований для UI или API.</li>
          <li>Генерируете ручные тест-кейсы.</li>
          <li>Получаете код автотестов на pytest.</li>
          <li>Проверяете код по базовым стандартам AAA.</li>
        </ol>
      </section>
    </div>
  );
}

export default Home;
