# McEasy External Sale Invoice

Project ini terdiri dari Odoo 17 dan backend service eksternal yang saling terhubung menggunakan token untuk menampilkan data Sale Order dan Invoice.

---

## 🚀 Cara Menjalankan Project

### 1. Salin File Environment

Salin file `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

### 2. Build dan Jalankan Container Docker

```bash
docker-compose up --build
```

---

## 📄 Dokumentasi API

Buka di browser:

```
http://localhost:8000/docs/
```
Setelah halaman dokumentasi Swagger terbuka:
- Buka file `.env`, salin nilai dari `API_KEY`
- Klik salah satu endpoint, lalu klik tombol **"Try it out"**
- Di kolom `x-api-key`, masukkan API key yang sudah disalin
- Klik **Execute** untuk menjalankan request


---

## ⚙️ Setup Odoo

1. Akses Odoo di:\
   `http://localhost:8069`
   
2. Buat database baru:

   - **Nama**: `odoo17`
   - **Email**: `admin`
   - **Password**: `admin`
   - ✅ Centang **Load demo data**
   - Klik **Create database**

3. Login ke Odoo dan install module berikut:

   - `Sales`
   - `external_sale_invoice` (custom module)

---

## 🔐 Generate External Token

1. Masuk ke menu **Sales > Orders > Customers**
2. Pilih customer
3. Klik action **"Generate External Token"**

---

## 📦 Buat dan Konfirmasi Sale Order

1. Buat Sale Order (melalui UI Odoo atau via API)
2. Klik **Confirm**
3. Update kolom **Delivered Quantity** untuk merubah invoice status menjadi To Invoice

---

## 🌐 Akses Web Eksternal Sale Invoice

Gunakan token yang telah di-generate sebagai URL parameter:

```
http://localhost:8069/external/sale-invoice?token=<external_token>
```

Contoh:

```
http://localhost:8069/external/sale-invoice?token=775d57817e1dc3ac52af2c575771ba820ee9f012f281ea107ada452dbf31a3a5
```

---

## 🔧 Struktur

- `odoo/`: Source kode Odoo & custom module
- `external_service/`: Backend FastAPI client untuk komunikasi dengan Odoo
- `docker-compose.yml`: Orkestrasi service Odoo, PostgreSQL, dan FastAPI

---
