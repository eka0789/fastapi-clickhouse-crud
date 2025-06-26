# 📰 Artikel API with FastAPI & ClickHouse

API sederhana untuk membuat, membaca, memperbarui, dan menghapus artikel menggunakan **FastAPI** dan **ClickHouse** sebagai database. Mendukung visualisasi dokumentasi via Swagger UI.


## 🚀 Fitur

- ✅ CRUD Artikel (`GET`, `POST`, `PUT`, `DELETE`)
- ✅ Tabel `articles` disiapkan otomatis
- ✅ Generate 100 data dummy saat start
- ✅ Swagger UI tersedia
- ✅ Terhubung ke ClickHouse
- ✅ Struktur modular & clean


## ⚙️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [ClickHouse](https://clickhouse.com/)
- [clickhouse-connect](https://pypi.org/project/clickhouse-connect/)
- [Faker](https://faker.readthedocs.io/en/master/) untuk dummy data


## 🧑‍💻 Instalasi Lokal

### 1. Clone Repo

```bash
git clone https://github.com/eka0789/fastapi-clickhouse-crud.git
cd fastapi-clickhouse-crud
````

### 2. Siapkan Virtual Environment

```bash
python -m venv env
env\Scripts\activate      # CMD
# atau
env\Scripts\Activate.ps1  # PowerShell
```

### 3. Install Dependency

```bash
pip install -r requirements.txt
```

> Jika `requirements.txt` belum ada, install manual:

```bash
pip install fastapi uvicorn clickhouse-connect faker
```


## 🐳 Jalankan ClickHouse (dengan Docker)

```bash
docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 yandex/clickhouse-server
```


## 🚦 Menjalankan Server

```bash
uvicorn main:app --reload
```

Buka Swagger UI di:
📄 [http://localhost:8000/docs](http://localhost:8000/docs)


## 🧪 Contoh Request

### `POST /articles`

```json
{
  "title": "Judul Artikel",
  "content": "Isi artikel yang sangat menarik."
}
```

### `GET /articles`

Mendapatkan semua artikel.


## 📁 Struktur Proyek

```
fastapi-clickhouse-crud/
├── main.py
├── README.md
└── env/                # virtual environment (ignore saat commit)
```


## ✨ Rencana Pengembangan (Opsional)

* 🔐 Auth JWT
* 📦 Export data ke CSV
* 🗃️ Pagination & Search
* 📈 Visualisasi data di Grafana


## 📄 Lisensi

MIT License © 2025 [Eka0789](https://github.com/eka0789)

