from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_manual_generation_endpoint():
    payload = {
        "project_id": "demo",
        "scenario_type": "ui",
        "source_type": "text",
        "content": "Проверка калькулятора стоимости",
        "max_tests": 5,
    }
    response = client.post("/generation/manual", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "manual_test_cases" in data
    assert len(data["manual_test_cases"]) >= 1


def test_projects_crud_in_memory():
    create_resp = client.post(
        "/projects",
        json={"name": "Demo project", "description": "Just for tests"},
    )
    assert create_resp.status_code == 201
    project = create_resp.json()
    project_id = project["id"]

    list_resp = client.get("/projects")
    assert list_resp.status_code == 200
    assert any(p["id"] == project_id for p in list_resp.json())

    get_resp = client.get(f"/projects/{project_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == project_id
