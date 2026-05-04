import pytest
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def valid_payload(**overrides):
    data = {"name": "Budi", "nilai_tugas": 80, "nilai_uts": 75, "nilai_uas": 90}
    data.update(overrides)
    return data


# ─── POST /students ───────────────────────────────────────────────────────────

def test_post_valid_student(client):
    response = client.post("/students", json=valid_payload())
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 1
    assert data["name"] == "Budi"
    assert data["nilai_akhir"] == 82.5
    assert data["grade"] == "B"
    assert all(k in data for k in ["id", "name", "nilai_tugas", "nilai_uts", "nilai_uas", "nilai_akhir", "grade"])


def test_post_invalid_name_kosong(client):
    response = client.post("/students", json=valid_payload(name=""))
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_post_invalid_nilai_di_luar_rentang(client):
    response = client.post("/students", json=valid_payload(nilai_tugas=150))
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_post_invalid_field_tidak_ada(client):
    response = client.post("/students", json={"name": "Budi", "nilai_tugas": 80})
    assert response.status_code == 400
    assert "error" in response.get_json()


# ─── GET /students ────────────────────────────────────────────────────────────

def test_get_all_students_kosong(client):
    response = client.get("/students")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_all_students_berisi(client):
    client.post("/students", json=valid_payload())
    client.post("/students", json=valid_payload(name="Ani"))
    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.get_json()) == 2


# ─── GET /students/{id} ───────────────────────────────────────────────────────

def test_get_student_by_id_valid(client):
    client.post("/students", json=valid_payload())
    response = client.get("/students/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Budi"


def test_get_student_by_id_not_found(client):
    response = client.get("/students/9999")
    assert response.status_code == 404
    assert "error" in response.get_json()


# ─── PUT /students/{id} ───────────────────────────────────────────────────────

def test_put_student_valid(client):
    client.post("/students", json=valid_payload())
    response = client.put("/students/1", json=valid_payload(name="Ani", nilai_uas=100))
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Ani"
    assert data["nilai_uas"] == 100
    assert data["nilai_akhir"] == 86.5
    assert data["grade"] == "A"


def test_put_student_not_found(client):
    response = client.put("/students/9999", json=valid_payload())
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_put_student_invalid_data(client):
    client.post("/students", json=valid_payload())
    response = client.put("/students/1", json=valid_payload(nilai_tugas=-10))
    assert response.status_code == 400
    assert "error" in response.get_json()


# ─── DELETE /students/{id} ────────────────────────────────────────────────────

def test_delete_student_valid(client):
    client.post("/students", json=valid_payload())
    response = client.delete("/students/1")
    assert response.status_code == 200


def test_delete_student_kemudian_get_not_found(client):
    client.post("/students", json=valid_payload())
    client.delete("/students/1")
    response = client.get("/students/1")
    assert response.status_code == 404


def test_delete_student_not_found(client):
    response = client.delete("/students/9999")
    assert response.status_code == 404
    assert "error" in response.get_json()
