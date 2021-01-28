from fastapi.testclient import TestClient
from main import get_application

api = get_application()

test_client = TestClient(api)


def test_status_route_root():
    response = test_client.get("/status")
    assert response.status_code == 200
