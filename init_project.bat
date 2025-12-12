@echo off
set ROOT=testops-copilot

mkdir %ROOT%
cd %ROOT%

echo TestOps Copilot > README.md
type nul > .gitignore
type nul > docker-compose.yml
type nul > .env.example
type nul > .gitlab-ci.yml

rem backend
mkdir backend
mkdir backend\app
mkdir backend\app\core
mkdir backend\app\api
mkdir backend\app\agents
mkdir backend\app\schemas
mkdir backend\app\models
mkdir backend\app\services
mkdir backend\app\tests

type nul > backend\Dockerfile
type nul > backend\requirements.txt

echo # backend package > backend\app\__init__.py
echo from fastapi import FastAPI> backend\app\main.py
echo app = FastAPI()>> backend\app\main.py

echo # core package > backend\app\core\__init__.py
type nul > backend\app\core\config.py
type nul > backend\app\core\llm_client.py

echo # api package > backend\app\api\__init__.py
type nul > backend\app\api\routes_health.py
type nul > backend\app\api\routes_projects.py
type nul > backend\app\api\routes_generation.py

echo # agents package > backend\app\agents\__init__.py
type nul > backend\app\agents\req_parser.py
type nul > backend\app\agents\manual_test_generator.py
type nul > backend\app\agents\automation_generator.py
type nul > backend\app\agents\standards_checker.py
type nul > backend\app\agents\optimizer.py

echo # schemas package > backend\app\schemas\__init__.py
type nul > backend\app\schemas\generation.py
type nul > backend\app\schemas\project.py

echo # models package > backend\app\models\__init__.py
type nul > backend\app\models\requirements.py
type nul > backend\app\models\test_cases.py
type nul > backend\app\models\testsuite.py

echo # services package > backend\app\services\__init__.py
type nul > backend\app\services\requirements_service.py
type nul > backend\app\services\testcases_service.py
type nul > backend\app\services\gitlab_service.py

echo # tests package > backend\app\tests\__init__.py
type nul > backend\app\tests\test_llm_client.py
type nul > backend\app\tests\test_agents.py
type nul > backend\app\tests\test_api.py

rem frontend
mkdir frontend
mkdir frontend\public
mkdir frontend\src
mkdir frontend\src\api
mkdir frontend\src\components
mkdir frontend\src\components\layout
mkdir frontend\src\components\generator
mkdir frontend\src\pages
mkdir frontend\src\styles

type nul > frontend\Dockerfile
type nul > frontend\package.json
type nul > frontend\tsconfig.json
type nul > frontend\vite.config.ts

echo placeholder > frontend\public\index.html

echo // entry point > frontend\src\main.tsx
echo // root component > frontend\src\App.tsx

echo // api client > frontend\src\api\client.ts
echo // generation api > frontend\src\api\generation.ts

echo // layout component > frontend\src\components\layout\Layout.tsx
echo // scenario form > frontend\src\components\generator\ScenarioForm.tsx
echo // result table > frontend\src\components\generator\ResultTable.tsx
echo // code preview > frontend\src\components\generator\CodePreview.tsx

echo // home page > frontend\src\pages\Home.tsx
echo // UI scenario page > frontend\src\pages\ScenarioUI.tsx
echo // API scenario page > frontend\src\pages\ScenarioAPI.tsx

echo /* global styles */ > frontend\src\styles\index.css

echo Project scaffold created.
