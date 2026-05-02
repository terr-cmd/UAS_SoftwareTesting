# Student Grading System API

![CI](https://github.com/terr-cmd/UAS_SoftwareTesting/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/terr-cmd/UAS_SoftwareTesting/branch/main/graph/badge.svg)](https://codecov.io/gh/terr-cmd/REPO_NAME)

Aplikasi ini adalah REST API sederhana berbasis Python Flask yang digunakan untuk mengelola data mahasiswa sekaligus menghitung nilai akhir dan menentukan grade secara otomatis.

---

## Deskripsi Aplikasi

Aplikasi ini memiliki beberapa fitur utama:
- Menambahkan data mahasiswa
- Melihat data mahasiswa
- Mengupdate data mahasiswa
- Menghapus data mahasiswa

Selain itu, sistem juga secara otomatis:
- Menghitung nilai akhir berdasarkan bobot
- Menentukan grade (A–E)
- Melakukan validasi input agar data tetap valid

---

## Instalasi

Pastikan Python sudah terinstall, lalu jalankan:

```bash
pip install -r requirements.txt
▶️ Menjalankan Aplikasi
cd project
python -m src.app

Aplikasi akan berjalan di:

http://localhost:5000
🔗 Endpoint API
Method	Endpoint	Deskripsi
POST	/students	Menambahkan mahasiswa baru
GET	/students	Mengambil semua data
GET	/students/{id}	Mengambil data berdasarkan ID
PUT	/students/{id}	Mengupdate data mahasiswa
DELETE	/students/{id}	Menghapus data mahasiswa
📥 Contoh Request
POST /students
{
  "name": "Budi",
  "nilai_tugas": 80,
  "nilai_uts": 75,
  "nilai_uas": 90
}
📤 Contoh Response
✅ Sukses
{
  "id": 1,
  "name": "Budi",
  "nilai_tugas": 80,
  "nilai_uts": 75,
  "nilai_uas": 90,
  "nilai_akhir": 82.5,
  "grade": "B"
}
❌ Error
{
  "error": "name tidak boleh kosong"
}
🧮 Perhitungan Nilai

Nilai akhir dihitung dengan rumus:

nilai_akhir = (0.3 × nilai_tugas) + (0.3 × nilai_uts) + (0.4 × nilai_uas)
🏆 Kriteria Grade
Nilai Akhir	Grade
≥ 85	A
70 – 84.99	B
60 – 69.99	C
50 – 59.99	D
< 50	E
🧪 Menjalankan Testing
Semua Test
pytest tests/
Dengan Coverage
pytest --cov=src --cov-report=term-missing tests/
Unit Test Saja
pytest tests/unit/
Integration Test Saja
pytest tests/integration/
🧪 Strategi Pengujian

Pengujian pada aplikasi ini menggunakan dua pendekatan:

1. Unit Testing

Unit test digunakan untuk menguji bagian kecil dari sistem secara terpisah, terutama pada layer service dan repository.

Yang diuji antara lain:

Perhitungan nilai akhir
Penentuan grade
Validasi input
Operasi CRUD

Tujuannya agar setiap fungsi berjalan dengan benar secara independen.

2. Integration Testing

Integration test digunakan untuk menguji sistem secara keseluruhan melalui endpoint API.

Yang diuji antara lain:

POST /students
GET /students
PUT /students/{id}
DELETE /students/{id}

Pengujian ini memastikan semua bagian sistem dapat bekerja dengan baik secara terintegrasi.

📊 Test Coverage

Aplikasi ini memiliki test coverage sekitar 99%, yang menunjukkan bahwa hampir seluruh kode telah diuji.

🔄 Continuous Integration (CI)

Proyek ini menggunakan GitHub Actions untuk menjalankan testing secara otomatis.

Setiap kali terjadi:

push
pull request

Pipeline akan:

Menginstall dependency
Menjalankan seluruh test
Menghitung coverage

Jika test gagal atau coverage di bawah batas minimal, maka pipeline akan gagal.

📁 Struktur Project
project/
│
├── src/
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   └── models/
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── requirements.txt
├── README.md
└── .github/workflows/ci.yml
📝 Catatan
Sistem login masih sederhana dan hanya digunakan untuk simulasi (menggunakan localStorage)
Data disimpan sementara (in-memory), tidak menggunakan database
Project ini dibuat untuk keperluan pembelajaran software testing dan REST API

---

#  HASIL AKHIR

Dengan ini kamu sudah:
- memenuhi semua requirement tugas  
- terlihat profesional  
- mudah dipahami  
- siap dikumpulkan  

