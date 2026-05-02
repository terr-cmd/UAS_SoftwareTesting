import pytest
from src.repositories.student_repository import StudentRepository


@pytest.fixture
def repo():
    return StudentRepository()


# --- save() ---

def test_save_assigns_id(repo):
    result = repo.save({"name": "Budi", "nilai_tugas": 80, "nilai_uts": 75, "nilai_uas": 90})
    assert result["id"] == 1


def test_save_increments_id(repo):
    repo.save({"name": "Budi"})
    result = repo.save({"name": "Ani"})
    assert result["id"] == 2


def test_save_returns_full_dict(repo):
    data = {"name": "Budi", "nilai_tugas": 80, "nilai_uts": 75, "nilai_uas": 90}
    result = repo.save(data)
    assert result["name"] == "Budi"
    assert result["nilai_tugas"] == 80
    assert "id" in result


def test_save_does_not_mutate_original(repo):
    data = {"name": "Budi"}
    repo.save(data)
    assert "id" not in data


# --- find_all() ---

def test_find_all_empty(repo):
    assert repo.find_all() == []


def test_find_all_returns_all(repo):
    repo.save({"name": "Budi"})
    repo.save({"name": "Ani"})
    result = repo.find_all()
    assert len(result) == 2


# --- find_by_id() ---

def test_find_by_id_existing(repo):
    saved = repo.save({"name": "Budi"})
    result = repo.find_by_id(saved["id"])
    assert result["name"] == "Budi"


def test_find_by_id_not_found(repo):
    assert repo.find_by_id(999) is None


# --- update() ---

def test_update_existing(repo):
    saved = repo.save({"name": "Budi", "nilai_tugas": 80})
    result = repo.update(saved["id"], {"name": "Budi Updated", "nilai_tugas": 90})
    assert result["name"] == "Budi Updated"
    assert result["nilai_tugas"] == 90
    assert result["id"] == saved["id"]


def test_update_not_found(repo):
    result = repo.update(999, {"name": "Ghost"})
    assert result is None


def test_update_persists_in_storage(repo):
    saved = repo.save({"name": "Budi"})
    repo.update(saved["id"], {"name": "Budi Updated"})
    found = repo.find_by_id(saved["id"])
    assert found["name"] == "Budi Updated"


# --- delete() ---

def test_delete_existing(repo):
    saved = repo.save({"name": "Budi"})
    result = repo.delete(saved["id"])
    assert result is True


def test_delete_removes_from_storage(repo):
    saved = repo.save({"name": "Budi"})
    repo.delete(saved["id"])
    assert repo.find_by_id(saved["id"]) is None


def test_delete_not_found(repo):
    result = repo.delete(999)
    assert result is False
