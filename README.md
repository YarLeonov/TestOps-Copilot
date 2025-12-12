# TestOps Copilot

AI ассистент, который снимает рутину с тестировщиков и помогает быстрее получать качественные тест-кейсы и автотесты на основе требований и OpenAPI.

Проект подготовлен под кейс "TestOps Copilot" (AI DevTools Hack, Cloud.ru).

---

## 1. Что делает этот сервис

TestOps Copilot помогает QA и TestOps командам:

- Принимать текстовые требования для UI или API (в перспективе - OpenAPI спецификацию)
- Генерировать набор ручных тест-кейсов
- Генерировать простой код автотестов на pytest (AAA структура в комментариях)
- Проверять код автотестов на базовые стандарты (AAA и импорт pytest)
- Работать через удобный веб интерфейс: ввод требований, просмотр тестов, просмотр и копирование кода

Это MVP архитектуры, которую можно развивать:
- заменить stub генерацию на реальный вызов Cloud.ru Evolution Foundation Model
- усилить логику агентов
- добавить Allure TestOps as Code, GitLab интеграцию и т.д.

---

## 2. Стек технологий

**Backend**

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic / pydantic-settings
- httpx (для вызовов LLM и GitLab)
- pytest (тесты)

**Frontend**

- React 18
- TypeScript
- Vite
- react-router-dom

**Инфраструктура**

- Docker
- docker-compose
- (опционально) PostgreSQL как основная БД, SQLite как упрощенный вариант

---

## 3. Структура проекта

Сокращенная структура, важные части:

```text
testops-copilot/
  README.md
  .gitignore
  docker-compose.yml
  .env.example
  .gitlab-ci.yml

  backend/
    Dockerfile
    requirements.txt
    app/
      main.py
      core/
        config.py
        llm_client.py
      api/
        routes_health.py
        routes_projects.py
        routes_generation.py
      agents/
        req_parser.py
        manual_test_generator.py
        automation_generator.py
        standards_checker.py
        optimizer.py
      schemas/
        generation.py
        project.py
      models/
        requirements.py
        test_cases.py
        testsuite.py
      services/
        requirements_service.py
        testcases_service.py
        gitlab_service.py
      tests/
        test_llm_client.py
        test_agents.py
        test_api.py

  frontend/
    Dockerfile
    package.json
    tsconfig.json
    vite.config.ts
    public/
      index.html
    src/
      main.tsx
      App.tsx
      api/
        client.ts
        generation.ts
      components/
        layout/Layout.tsx
        generator/ScenarioForm.tsx
        generator/ResultTable.tsx
        generator/CodePreview.tsx
      pages/
        Home.tsx
        ScenarioUI.tsx
        ScenarioAPI.tsx
      styles/
        index.css
```

**4\. Архитектура**

**4.1 Backend**

Backend - это FastAPI приложение, которое предоставляет:

- GET /health - статус сервиса
- GET /projects и POST /projects - простое in memory управление проектами
- POST /generation/manual - генерация ручных тест-кейсов из требований
- POST /generation/automation - генерация кода pytest автотестов из ручных кейсов
- POST /generation/validate - проверка кода автотестов на базовые стандарты

Главные слои:

- **core**
    - config.py - загрузка настроек из .env
    - llm_client.py - обертка над LLM Cloud.ru, сейчас с режимом stub (если нет токена и endpoint)
- **agents**
    - ReqParserAgent - разбивает текст требований на сущности Requirement
    - ManualTestGeneratorAgent - по Requirement генерирует TestCase с шагами
    - AutomationGeneratorAgent - по TestCase генерирует простой файл pytest с AAA комментариями
    - StandardsCheckerAgent - проверяет наличие Arrange, Act, Assert и импорта pytest
    - OptimizationAgent - пример анализа дублей (пока не подключен в API)
- **services**
    - RequirementsService - фасад над ReqParserAgent
    - TestCasesService - главная точка для API: координирует агентов и формирует ответы
    - GitLabService - заглушка для будущей интеграции с GitLab
- **schemas** - Pydantic модели запросов и ответов для API
- **models** - внутренние dataclass модели домена

**4.2 Frontend**

Frontend - это SPA на React:

- Страница Home - обзор проекта и переходы к сценариям
- Страница ScenarioUI - сценарий генерации для UI
- Страница ScenarioAPI - сценарий генерации для API

Компоненты:

- Layout - общая рамка приложения (шапка, меню, подвал)
- ScenarioForm - основной рабочий экран: ввод требований, кнопки генерации, отображение результата
- ResultTable - таблица ручных тест-кейсов
- CodePreview - просмотр и копирование сгенерированного кода

Frontend ходит в backend по адресу из VITE_BACKEND_URL.

**5\. Переменные окружения**

Пример настроек в .env.example:

\# Общие настройки

APP_ENV=dev

LOG_LEVEL=info

\# Backend

BACKEND_HOST=0.0.0.0

BACKEND_PORT=8000

\# База данных

\# Для docker-compose:

DATABASE_URL=postgresql+asyncpg://testops:testops@db:5432/testops

\# Для локального запуска можно использовать SQLite:

\# DATABASE_URL=sqlite+aiosqlite:///./testops.db

\# Интеграция с LLM Cloud.ru Evolution

CLOUD_LLM_ENDPOINT=https://api.cloudru.example/evolution/v1/chat

CLOUD_LLM_TOKEN=replace_with_real_token

CLOUD_LLM_MODEL=evolution-foundation-testops

\# Интеграция с GitLab (опционально)

GITLAB_BASE_URL=https://gitlab.example.com

GITLAB_TOKEN=replace_with_gitlab_token

GITLAB_PROJECT_ID=123

\# Токены для API тестового стенда (опционально)

EVOLUTION_API_BASE_URL=https://api.evolution.example.com

EVOLUTION_API_TOKEN=replace_with_evolution_token

\# Frontend

FRONTEND_PORT=5173

VITE_BACKEND_URL=http://localhost:8000

Минимально для запуска нужны:

- BACKEND_HOST, BACKEND_PORT - можно оставить по умолчанию
- DATABASE_URL - можно оставить PostgreSQL от docker-compose или сменить на SQLite
- VITE_BACKEND_URL - адрес backend для фронта (для Docker обычно http://backend:8000, для локального - http://localhost:8000)

Если не задать CLOUD_LLM_\*, backend будет отвечать stub строкой от LLM, но не упадет.

**6\. Запуск проекта**

**Вариант 1: через Docker Compose**

Предпочтительный способ для быстрой демонстрации.

1.  Скопировать env файл

cp .env.example .env

1.  При необходимости поправить параметры в .env

- Если используем docker-compose как есть, DATABASE_URL уже настроен на сервис db
- VITE_BACKEND_URL в дев режиме с docker-compose можно оставить http://localhost:8000

1.  Поднять все сервисы

docker compose up --build

docker-compose поднимет:

- db - PostgreSQL (порт 5433 на хосте)
- backend - FastAPI (порт 8000)
- frontend - React приложение (порт 5173)

1.  Открыть в браузере

- Frontend: http://localhost:5173
- Backend Swagger: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Чтобы остановить:

docker compose down

**Вариант 2: запуск backend локально, frontend локально**

Подходит для разработки и отладки.

**6.1 Backend**

Требуется Python 3.11.

1.  Установить зависимости

cd backend

python -m venv venv

\# Linux или macOS

source venv/bin/activate

\# Windows

\# venv\\Scripts\\activate

pip install -r requirements.txt

1.  Скопировать .env

cd ..

cp .env.example .env

Можно для локальной разработки заменить DATABASE_URL на SQLite:

DATABASE_URL=sqlite+aiosqlite:///./testops.db

1.  Запустить backend

cd backend

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Backend будет доступен по адресу:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

**6.2 Frontend**

Требуется Node 18+.

1.  Установить зависимости

cd frontend

npm install

1.  Убедиться, что VITE_BACKEND_URL указывает на backend

В .env или .env.local:

VITE_BACKEND_URL=http://localhost:8000

1.  Запустить dev сервер

npm run dev -- --host 0.0.0.0 --port 5173

Frontend будет доступен по адресу: http://localhost:5173

**7\. Как пользоваться приложением**

1.  Открыть frontend (http://localhost:5173)
2.  На главной странице выбрать сценарий:
    - "UI сценарий"
    - "API сценарий"
3.  На странице сценария:
    - Вставить в большое поле текст требований, например:
        - "Пользователь открывает калькулятор стоимости, выбирает виртуальную машину и диск, видит итоговую цену"
    - Выбрать количество тест-кейсов (например 10)
    - Нажать "Сгенерировать тест-кейсы"
4.  В левой колонке появится список ручных кейсов в формате:
    - TC-001: UI - Проверка калькулятора стоимости
    - TC-002: UI - ...
5.  Нажать кнопку "Сгенерировать автотесты"
    - В правой колонке появится файл test_ui_generated.py с функциями test_tc_auto_001_... и комментариями AAA блоков
6.  Нажать "Проверить по стандартам"
    - Backend проверит, есть ли в коде Arrange, Act, Assert и импорт pytest
    - Внизу появится блок "Замечания" или сообщение о том, что нарушений не найдено
7.  Кнопка "Копировать" рядом с кодом скопирует содержимое файла в буфер обмена для вставки в репозиторий.

**8\. Backend API для интеграции**

Ниже базовые примеры запросов.

**8.1 Генерация ручных тест-кейсов**

POST /generation/manual

Пример запроса:

{

"project_id": "demo-project",

"scenario_type": "ui",

"source_type": "text",

"content": "Пользователь открывает калькулятор стоимости и считает цену\\nПользователь меняет конфигурацию машины",

"max_tests": 5

}

Пример ответа:

{

"project_id": "demo-project",

"summary": "Сгенерировано 2 ручных тест-кейсов",

"manual_test_cases": \[

"TC-001: UI - Пользователь открывает калькулятор стоимости и считает цену",

"TC-002: UI - Пользователь меняет конфигурацию машины"

\],

"code_bundles": \[\],

"warnings": \[\]

}

**8.2 Генерация кода автотестов**

POST /generation/automation

Пример запроса:

{

"project_id": "demo-project",

"target": "ui",

"manual_test_cases": \[

"TC-001: UI - Пользователь открывает калькулятор стоимости и считает цену"

\]

}

Ответ содержит массив code_bundles с файлом:

- name - например test_ui_generated.py
- content - текст python файла

**8.3 Валидация кода**

POST /generation/validate

{

"project_id": "demo-project",

"code": "import pytest\\n\\n# Arrange...\\n",

"rules": \[\]

}

Ответ:

{

"project_id": "demo-project",

"summary": "Проверка завершена. ...",

"manual_test_cases": \[\],

"code_bundles": \[\],

"warnings": \["..."\]

}

**9\. Тестирование и качество**

**9.1 Backend тесты**

Выполнить:

cd backend

pytest

Включены:

- test_llm_client.py - проверка stub режима LLM клиента
- test_agents.py - проверка основных агентов разбора и генерации
- test_api.py - проверка основных HTTP эндпоинтов

**9.2 Frontend**

Базовый lint и сборка:

cd frontend

npm run build

**10\. Дальнейшее развитие**

Идеи, как расширять MVP:

- Подключить реальный Cloud.ru Evolution Foundation Model в LLMClient вместо stub логики
- Переделать генерацию автотестов на полноценный Allure TestOps as Code формат
- Добавить поддержку OpenAPI файла как источника требований для сценария API
- Реализовать GitLab MR создание через GitLabService
- Расширить StandardsCheckerAgent: проверка Allure тегов, приоритетов, именования
- Добавить хранение проектов и тестов в БД вместо in memory