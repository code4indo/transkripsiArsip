# Program Transkripsi Arsip Dokumen Gambar

Program ini menggunakan Google Gemini API untuk mentranskripsi teks dari gambar-gambar dokumen.

## Fitur

-   Menerima direktori input berisi gambar dokumen (PNG, JPG, JPEG).
-   Membuat direktori output dengan nama yang sesuai dengan direktori input (misal: `nama_input_hasil_transkripsi`).
-   Menyimpan hasil transkripsi setiap gambar dalam format JSON.
-   Nama file JSON sama dengan nama file gambar aslinya.
-   Format JSON: `{"nama_file": "...", "teks_transkripsi": "..."}`.
-   Menggunakan model `gemini-1.5-flash-latest` (atau model multimodal lain yang sesuai) untuk OCR.
-   API key Google disimpan dengan aman menggunakan file `.env`.
-   Dependensi proyek dikelola dengan Poetry.

## Struktur Proyek

```
transkripsiArsip/
├── pyproject.toml         # Konfigurasi Poetry
├── README.md              # File ini
├── .env                   # (Dibuat manual) Simpan API key di sini
├── .env.example           # Contoh untuk .env
├── src/
│   └── transkripsi_arsip/
│       ├── __init__.py
│       ├── main.py          # Skrip utama
│       ├── ocr.py           # Logika OCR dengan Gemini
│       └── utils.py         # Fungsi utilitas
└── data/                    # (Dibuat manual jika perlu untuk contoh)
    ├── input_contoh/
    │   └── (letakkan gambar di sini)
    └── output/
        └── (hasil akan disimpan di sini)
```

## Persiapan

1.  **Install Python**: Pastikan Python versi 3.9 atau lebih baru terinstal.
2.  **Install Poetry**: Jika belum terinstal, ikuti petunjuk di [situs resmi Poetry](https://python-poetry.org/docs/#installation).
3.  **Clone Proyek (jika dari Git)**:
    ```bash
    git clone <url_repository_anda>
    cd transkripsiArsip
    ```
4.  **Install Dependensi**:
    ```bash
    poetry install
    ```
5.  **Siapkan API Key**:
    *   Dapatkan API Key dari [Google AI Studio](https://aistudio.google.com/app/apikey) atau Google Cloud Console.
    *   Buat file bernama `.env` di root direktori proyek (sejajar dengan `pyproject.toml`).
    *   Salin isi dari `.env.example` ke `.env`.
    *   Masukkan API key Anda ke dalam file `.env`:
        ```
        GOOGLE_API_KEY="API_KEY_ANDA"
        ```

## Cara Menjalankan

1.  **Siapkan Direktori Input**:
    *   Buat sebuah direktori di mana saja (misalnya, `dokumen_untuk_transkripsi`).
    *   Letakkan semua file gambar dokumen (format `.png`, `.jpg`, atau `.jpeg`) yang ingin Anda transkripsi ke dalam direktori tersebut.

2.  **Jalankan Skrip Transkripsi**:
    Gunakan perintah berikut dari terminal, pastikan Anda berada di root direktori proyek (`transkripsiArsip`):
    ```bash
    poetry run transkripsi path/ke/direktori_input_anda
    ```
    Contoh:
    ```bash
    poetry run transkripsi data/input_contoh
    ```
    Atau jika direktori input Anda bernama `arsip_bulan_ini` dan berada di luar folder proyek:
    ```bash
    poetry run transkripsi /path/lengkap/ke/arsip_bulan_ini
    ```

3.  **Lihat Hasil**:
    *   Skrip akan membuat direktori output di dalam `transkripsiArsip/data/output/nama_direktori_input_anda_hasil_transkripsi/`.
    *   Di dalamnya, Anda akan menemukan file-file JSON yang berisi hasil transkripsi untuk setiap gambar.

## Menangani Dokumen Panjang

Model AI memiliki batasan pada ukuran input. Jika Anda memiliki gambar dokumen yang sangat besar atau dengan teks yang sangat padat sehingga melebihi batasan model:

-   **Kualitas Hasil**: Transkripsi mungkin tidak lengkap atau tidak akurat.
-   **Error**: API mungkin mengembalikan error.

**Strategi yang Mungkin (Tidak Diimplementasikan Secara Otomatis di Versi Ini):**

-   **Pemecahan Gambar (Image Tiling)**: Untuk gambar tunggal yang sangat besar, Anda mungkin perlu memecahnya menjadi beberapa bagian yang lebih kecil, mentranskripsi setiap bagian, lalu menggabungkan hasilnya. Ini memerlukan logika pemrosesan gambar tambahan.
-   **Penyesuaian Kualitas Gambar**: Mengurangi resolusi gambar jika terlalu tinggi, namun tetap menjaga keterbacaan teks.

Fungsi `ocr.py` saat ini mengirimkan gambar apa adanya. Jika Anda sering menghadapi masalah dengan dokumen panjang, pertimbangkan untuk mengimplementasikan strategi di atas.

## Troubleshooting

-   **`ValueError: GOOGLE_API_KEY tidak ditemukan`**: Pastikan file `.env` ada di root proyek dan berisi `GOOGLE_API_KEY="KUNCI_ANDA"`.
-   **Error dari API Gemini**: Periksa pesan error. Mungkin terkait dengan format gambar, ukuran, konten yang diblokir karena alasan keamanan, atau masalah koneksi.
-   **Tidak ada file gambar ditemukan**: Pastikan path ke direktori input benar dan direktori tersebut berisi file `.png`, `.jpg`, atau `.jpeg`.
