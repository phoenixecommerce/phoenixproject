from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_list_products():
    response = client.get("/api/products")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_product_found():
    assert client.get("/api/products/1").json()["id"] == 1


def test_get_product_missing():
    assert client.get("/api/products/9999").status_code == 404


def test_info_has_version():
    assert "version" in client.get("/api/info").json()
