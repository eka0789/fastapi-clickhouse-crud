import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_token():
    response = client.post("/auth/login", json={"username": "admin", "password": "password"})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_login_success():
    response = client.post("/auth/login", json={"username": "admin", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_article():
    token = get_token()
    response = client.post(
        "/articles",
        json={"title": "Artikel Test", "content": "Konten artikel uji coba"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["title"] == "Artikel Test"
    assert json_data["content"] == "Konten artikel uji coba"
    assert "id" in json_data
    assert "created_at" in json_data


def test_get_article():
    # Ambil salah satu artikel (id=1 as default)
    response = client.get("/articles/1")
    if response.status_code == 404:
        pytest.skip("Data with id=1 does not exist yet")
    assert response.status_code == 200
    json_data = response.json()
    assert "title" in json_data
    assert "content" in json_data


def test_update_article():
    token = get_token()

    # Buat artikel dulu
    post_res = client.post(
        "/articles",
        json={"title": "Sebelum Update", "content": "Konten awal"},
        headers={"Authorization": f"Bearer {token}"}
    )
    article_id = post_res.json()["id"]

    # Update
    put_res = client.put(
        f"/articles/{article_id}",
        json={"title": "Setelah Update", "content": "Konten sudah diubah"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert put_res.status_code == 200
    assert put_res.json()["title"] == "Setelah Update"


def test_delete_article():
    token = get_token()

    # Buat artikel baru
    res = client.post(
        "/articles",
        json={"title": "To Be Deleted", "content": "Delete me"},
        headers={"Authorization": f"Bearer {token}"}
    )
    article_id = res.json()["id"]

    # Hapus
    del_res = client.delete(f"/articles/{article_id}", headers={"Authorization": f"Bearer {token}"})
    assert del_res.status_code == 200
    assert del_res.json()["message"] == f"Article {article_id} deleted"

    # Pastikan sudah terhapus
    get_res = client.get(f"/articles/{article_id}")
    assert get_res.status_code == 404
