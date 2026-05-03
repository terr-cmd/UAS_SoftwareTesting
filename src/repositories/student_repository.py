class StudentRepository:
    def __init__(self):
        self._storage: dict[int, dict] = {}
        self._next_id: int = 1

    def save(self, student_data: dict) -> dict:
        """Assign auto-increment id, simpan ke storage, kembalikan dict lengkap."""
        student_data = dict(student_data)
        student_data["id"] = self._next_id
        self._storage[self._next_id] = student_data
        self._next_id += 1

        print("ISI STORAGE:", self._storage)
        
        return student_data

    def find_all(self) -> list[dict]:
        """Kembalikan list semua value dari storage."""
        return list(self._storage.values())

    def find_by_id(self, student_id: int) -> dict | None:
        """Kembalikan dict jika ada, None jika tidak ditemukan."""
        return self._storage.get(student_id)

    def update(self, student_id: int, student_data: dict) -> dict | None:
        """Update storage jika id ada, kembalikan dict yang diupdate atau None."""
        if student_id not in self._storage:
            return None
        student_data = dict(student_data)
        student_data["id"] = student_id
        self._storage[student_id] = student_data
        return student_data

    def delete(self, student_id: int) -> bool:
        """Hapus dari storage jika ada. Kembalikan True jika berhasil, False jika tidak ditemukan."""
        if student_id not in self._storage:
            return False
        del self._storage[student_id]
        return True
