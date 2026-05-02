import pytest
from src.services.student_service import StudentService
from src.repositories.student_repository import StudentRepository
from src.models.student_model import ValidationError, StudentNotFoundError


@pytest.fixture
def service():
    return StudentService(StudentRepository())


def valid_data(**overrides):
    data = {"name": "Budi", "nilai_tugas": 80, "nilai_uts": 75, "nilai_uas": 90}
    data.update(overrides)
    return data


# ─── Kalkulasi Nilai Akhir ────────────────────────────────────────────────────

def test_calculate_all_zero(service):
    assert service._calculate_nilai_akhir(0, 0, 0) == 0.0


def test_calculate_all_hundred(service):
    assert service._calculate_nilai_akhir(100, 100, 100) == 100.0


def test_calculate_formula(service):
    # 0.3*80 + 0.3*75 + 0.4*90 = 24 + 22.5 + 36 = 82.5
    assert service._calculate_nilai_akhir(80, 75, 90) == 82.5


def test_calculate_rounds_to_2_decimal(service):
    # 0.3*70 + 0.3*70 + 0.4*70 = 70.0 (exact)
    result = service._calculate_nilai_akhir(70, 70, 70)
    assert result == round(result, 2)


# ─── Penentuan Grade ──────────────────────────────────────────────────────────

def test_grade_A(service):
    assert service._determine_grade(85.0) == "A"
    assert service._determine_grade(100.0) == "A"


def test_grade_B(service):
    assert service._determine_grade(70.0) == "B"
    assert service._determine_grade(84.0) == "B"


def test_grade_C(service):
    assert service._determine_grade(60.0) == "C"
    assert service._determine_grade(69.0) == "C"


def test_grade_D(service):
    assert service._determine_grade(50.0) == "D"
    assert service._determine_grade(59.0) == "D"


def test_grade_E(service):
    assert service._determine_grade(0.0) == "E"
    assert service._determine_grade(49.0) == "E"


def test_grade_boundary_85(service):
    assert service._determine_grade(85.0) == "A"
    assert service._determine_grade(84.99) == "B"


def test_grade_boundary_70(service):
    assert service._determine_grade(70.0) == "B"
    assert service._determine_grade(69.99) == "C"


def test_grade_boundary_60(service):
    assert service._determine_grade(60.0) == "C"
    assert service._determine_grade(59.99) == "D"


def test_grade_boundary_50(service):
    assert service._determine_grade(50.0) == "D"
    assert service._determine_grade(49.99) == "E"


# ─── Validasi Input ───────────────────────────────────────────────────────────

def test_validate_name_kosong(service):
    with pytest.raises(ValidationError, match="name tidak boleh kosong"):
        service._validate(valid_data(name=""))


def test_validate_name_whitespace(service):
    with pytest.raises(ValidationError, match="name tidak boleh kosong"):
        service._validate(valid_data(name="   "))


def test_validate_name_tidak_ada(service):
    data = {"nilai_tugas": 80, "nilai_uts": 75, "nilai_uas": 90}
    with pytest.raises(ValidationError, match="name tidak boleh kosong"):
        service._validate(data)


def test_validate_name_bukan_string(service):
    with pytest.raises(ValidationError, match="name harus bertipe string"):
        service._validate(valid_data(name=123))


def test_validate_nilai_tugas_tidak_ada(service):
    data = {"name": "Budi", "nilai_uts": 75, "nilai_uas": 90}
    with pytest.raises(ValidationError, match="nilai_tugas tidak boleh kosong"):
        service._validate(data)


def test_validate_nilai_di_luar_rentang_negatif(service):
    with pytest.raises(ValidationError, match="nilai harus antara 0 sampai 100"):
        service._validate(valid_data(nilai_tugas=-1))


def test_validate_nilai_di_luar_rentang_lebih_100(service):
    with pytest.raises(ValidationError, match="nilai harus antara 0 sampai 100"):
        service._validate(valid_data(nilai_uts=101))


def test_validate_nilai_bukan_numerik(service):
    with pytest.raises(ValidationError):
        service._validate(valid_data(nilai_uas="sembilan puluh"))


def test_validate_nilai_bool_ditolak(service):
    with pytest.raises(ValidationError):
        service._validate(valid_data(nilai_tugas=True))


# ─── CRUD Operations ─────────────────────────────────────────────────────────

def test_create_student_valid(service):
    result = service.create_student(valid_data())
    assert result["id"] == 1
    assert result["name"] == "Budi"
    assert result["nilai_akhir"] == 82.5
    assert result["grade"] == "B"
    assert all(k in result for k in ["id", "name", "nilai_tugas", "nilai_uts", "nilai_uas", "nilai_akhir", "grade"])


def test_get_all_students_kosong(service):
    assert service.get_all_students() == []


def test_get_all_students_berisi(service):
    service.create_student(valid_data())
    service.create_student(valid_data(name="Ani"))
    assert len(service.get_all_students()) == 2


def test_get_student_by_id_valid(service):
    created = service.create_student(valid_data())
    result = service.get_student_by_id(created["id"])
    assert result["name"] == "Budi"


def test_get_student_by_id_not_found(service):
    with pytest.raises(StudentNotFoundError):
        service.get_student_by_id(999)


def test_update_student_valid(service):
    created = service.create_student(valid_data())
    updated = service.update_student(created["id"], valid_data(name="Ani", nilai_uas=100))
    assert updated["name"] == "Ani"
    assert updated["nilai_akhir"] != created["nilai_akhir"]


def test_update_student_not_found(service):
    with pytest.raises(StudentNotFoundError):
        service.update_student(999, valid_data())


def test_delete_student_valid(service):
    created = service.create_student(valid_data())
    result = service.delete_student(created["id"])
    assert result == {"message": "Student berhasil dihapus"}


def test_delete_student_not_found(service):
    with pytest.raises(StudentNotFoundError):
        service.delete_student(999)
