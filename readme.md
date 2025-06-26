# 📰 Artikel API with FastAPI & ClickHouse

API lengkap untuk membuat, membaca, memperbarui, dan menghapus artikel menggunakan **FastAPI** dan **ClickHouse** sebagai database utama. API ini mendukung otentikasi JWT, dokumentasi Swagger UI, ekspor data ke CSV, pagination, serta visualisasi melalui **Grafana**.


## 🚀 Fitur Lengkap

- ✅ CRUD Artikel (`GET`, `POST`, `PUT`, `DELETE`)
- 🔐 Login dengan Auth JWT
- 📄 Swagger UI otomatis
- 🔁 Pagination & Search
- 📦 Export data ke CSV
- 🧪 Unit Test dengan `pytest`
- 📊 Visualisasi data di Grafana
- 🔧 Struktur proyek modular dan terorganisir
- 🐳 Siap deploy dengan Docker Compose


## ⚙️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [ClickHouse](https://clickhouse.com/)
- [clickhouse-connect](https://pypi.org/project/clickhouse-connect/)
- [Faker](https://faker.readthedocs.io/en/master/) untuk dummy data
- [Grafana](https://grafana.com/) untuk dashboard
- [Docker](https://www.docker.com/) untuk containerisasi
- [pytest](https://docs.pytest.org/) untuk pengujian


## 📁 Struktur Proyek

```
fastapi-clickhouse-crud/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   └── article.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── articles.py
│   └── services/
│       └── clickhouse_client.py
├── tests/
│   └── test_articles.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```


## 🧑‍💻 Instalasi Lokal (Non-Docker)

### 1. Clone Repo

```bash
git clone https://github.com/eka0789/fastapi-clickhouse-crud.git
cd fastapi-clickhouse-crud
```

### 2. Siapkan Virtual Environment

```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

### 3. Install Dependency

```bash
pip install -r requirements.txt
```

### 4. Jalankan ClickHouse (Manual)

```bash
docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server
```

### 5. Jalankan Server FastAPI

```bash
uvicorn app.main:app --reload
```


## 🐳 Deploy dengan Docker Compose (Direkomendasikan)

```bash
docker compose up --build -d
```

Akses:
- API: http://localhost:8000/docs
- Grafana: http://localhost:3000
- ClickHouse: http://localhost:8123

Login Grafana: `admin / admin`


## 🧪 Contoh Request API

### 🔐 `POST /auth/login`
```json
{
  "username": "admin",
  "password": "password"
}
```

### `POST /articles` (dengan JWT)
```json
{
  "title": "Judul Artikel",
  "content": "Isi artikel yang sangat menarik."
}
```

### `GET /articles`
Mendapatkan semua artikel (support `?skip=0&limit=10&q=keyword`)

### `GET /articles/export`
Mengunduh artikel dalam bentuk file CSV.


## 🧪 Pengujian (Testing)

```bash
pytest tests/test_articles.py
```


## 📈 Visualisasi Data

1. Akses Grafana `http://localhost:3000`
2. Tambah **ClickHouse** sebagai Data Source (host: `http://clickhouse:8123`)
3. Buat Dashboard → Panel → Query: 
   ```sql
   SELECT count() FROM articles
   ```
4. Simpan & sesuaikan visualisasinya.


## ✨ Rencana Lanjutan

- 🔐 Manajemen user & roles (admin/user)
- ⏱ Scheduled job & data analytics
- 📦 Export ke Excel/JSON
- 🔒 Rate limiting & throttling
- ☁️ CI/CD deployment pipeline


## 📄 Lisensi

MIT License © 2025 [Eka Prasetyo (Aktif Koding)](https://github.com/eka0789)
