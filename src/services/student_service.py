from src.models.student_model import ValidationError, StudentNotFoundError
from src.repositories.student_repository import StudentRepository


class StudentService:
    def __init__(self, repository: StudentRepository):
        self._repo = repository

    # -------------------------------------------------------------------------
    # Helper methods
    # -------------------------------------------------------------------------

    def _calculate_nilai_akhir(self, tugas, uts, uas) -> float:
        """Hitung nilai akhir dengan bobot 30/30/40 dan bulatkan 2 desimal."""
        return round((0.3 * tugas) + (0.3 * uts) + (0.4 * uas), 2)

    def _determine_grade(self, nilai_akhir: float) -> str:
        """Tentukan grade berdasarkan nilai akhir."""
        if nilai_akhir >= 85:
            return "A"
        elif nilai_akhir >= 70:
            return "B"
        elif nilai_akhir >= 60:
            return "C"
        elif nilai_akhir >= 50:
            return "D"
        else:
            return "E"

    # -------------------------------------------------------------------------
    # Validasi input
    # -------------------------------------------------------------------------

    def _validate(self, data: dict) -> None:
        """Validasi data input mahasiswa. Raise ValidationError jika tidak valid."""
        required_fields = ["name", "nilai_tugas", "nilai_uts", "nilai_uas"]
        numeric_fields = ["nilai_tugas", "nilai_uts", "nilai_uas"]

        # 1. Cek field wajib ada
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"{field} tidak boleh kosong")

        # 2. Cek name bertipe str
        if not isinstance(data["name"], str):
            raise ValidationError("name harus bertipe string")

        # 3. Cek name tidak kosong/whitespace
        if not data["name"].strip():
            raise ValidationError("name tidak boleh kosong")

        # 4. Cek nilai bertipe int atau float (bukan bool)
        for field in numeric_fields:
            value = data[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValidationError(f"{field} harus bertipe numerik (int atau float)")

        # 5. Cek nilai dalam rentang 0–100
        for field in numeric_fields:
            value = data[field]
            if value < 0 or value > 100:
                raise ValidationError("nilai harus antara 0 sampai 100")

    # -------------------------------------------------------------------------
    # CRUD operations
    # -------------------------------------------------------------------------

    def create_student(self, data: dict) -> dict:
        """Validasi, kalkulasi, simpan, dan kembalikan dict mahasiswa baru."""
        self._validate(data)
        nilai_akhir = self._calculate_nilai_akhir(
            data["nilai_tugas"], data["nilai_uts"], data["nilai_uas"]
        )
        grade = self._determine_grade(nilai_akhir)
        student_data = {
            "name": data["name"],
            "nilai_tugas": data["nilai_tugas"],
            "nilai_uts": data["nilai_uts"],
            "nilai_uas": data["nilai_uas"],
            "nilai_akhir": nilai_akhir,
            "grade": grade,
        }
        return self._repo.save(student_data)

    def get_all_students(self) -> list:
        """Kembalikan semua mahasiswa dari repository."""
        return self._repo.find_all()

    def get_student_by_id(self, student_id: int) -> dict:
        """Cari mahasiswa berdasarkan id. Raise StudentNotFoundError jika tidak ada."""
        student = self._repo.find_by_id(student_id)
        if student is None:
            raise StudentNotFoundError("Student dengan id tersebut tidak ditemukan")
        return student

    def update_student(self, student_id: int, data: dict) -> dict:
        """Validasi, kalkulasi ulang, update, dan kembalikan dict mahasiswa yang diperbarui."""
        self._validate(data)
        nilai_akhir = self._calculate_nilai_akhir(
            data["nilai_tugas"], data["nilai_uts"], data["nilai_uas"]
        )
        grade = self._determine_grade(nilai_akhir)
        student_data = {
            "name": data["name"],
            "nilai_tugas": data["nilai_tugas"],
            "nilai_uts": data["nilai_uts"],
            "nilai_uas": data["nilai_uas"],
            "nilai_akhir": nilai_akhir,
            "grade": grade,
        }
        result = self._repo.update(student_id, student_data)
        if result is None:
            raise StudentNotFoundError("Student dengan id tersebut tidak ditemukan")
        return result

    def delete_student(self, student_id: int) -> dict:
        """Hapus mahasiswa berdasarkan id. Raise StudentNotFoundError jika tidak ada."""
        success = self._repo.delete(student_id)
        if not success:
            raise StudentNotFoundError("Student dengan id tersebut tidak ditemukan")
        return {"message": "Student berhasil dihapus"}
