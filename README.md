# Program Transkripsi Arsip Dokumen Gambar

Program ini menggunakan Google Gemini API untuk mentranskripsi teks dari gambar-gambar dokumen.

## Fitur

-   Menerima direktori input berisi gambar dokumen (PNG, JPG, JPEG).
-   Membuat direktori output (`output_transkripsi/nama_input_hasil_transkripsi/`) untuk menyimpan hasil.
-   Menyimpan hasil transkripsi setiap gambar dalam format JSON dan TXT.
-   Nama file JSON dan TXT sama dengan nama file gambar aslinya.
-   Format JSON: `{"nama_file": "...", "teks_transkripsi": "..."}`.
-   Menggunakan model `gemini-1.5-flash-latest` untuk OCR.
-   API key Google disimpan dengan aman menggunakan file `.env`.
-   System prompt untuk model bahasa dapat dikonfigurasi melalui file `prompt.txt`.
-   Dependensi proyek dikelola dengan Poetry.
-   **Baru**: Menampilkan progress bar selama proses transkripsi.
-   **Baru**: Membuat file log (`transcription_log.txt`) yang merekam detail proses (waktu mulai/selesai, total waktu, total file diproses/dilewati, estimasi token).
-   **Baru**: Tidak akan mentranskripsi ulang dokumen jika file outputnya (JSON dan TXT) sudah ada.

## Struktur Proyek

```
transkripsiArsip/
├── pyproject.toml
├── README.md
├── .env
├── .env.example
├── prompt.txt             # (Opsional) Kustomisasi system prompt
├── prompt.txt.example
├── .gitignore
├── transcription_log.txt  # File log (dibuat otomatis)
├── src/
│   └── transkripsi_arsip/
│       ├── __init__.py
│       ├── main.py
│       ├── ocr.py
│       └── utils.py
├── data/                    # (Contoh) Direktori untuk input gambar Anda
│   └── input_contoh/
└── output_transkripsi/      # Direktori output utama (dibuat otomatis)
    └── nama_direktori_input_hasil_transkripsi/
        └── (hasil .json dan .txt disimpan di sini)
```

## Persiapan

1.  **Install Python & Poetry**: Seperti sebelumnya.
2.  **Clone & Install Dependensi**:
    ```bash
    # git clone ... (jika perlu)
    # cd transkripsiArsip
    poetry install 
    ```
    Perintah `poetry install` akan menginstal `tqdm` yang baru ditambahkan.
3.  **Siapkan API Key & Prompt**: Seperti sebelumnya (`.env` dan `prompt.txt` opsional).

## Cara Menjalankan

Sama seperti sebelumnya. Jalankan dari root direktori proyek:
```bash
poetry run transkripsi path/ke/direktori_input_anda
```
Anda akan melihat progress bar di terminal. Setelah selesai, periksa `transcription_log.txt` di root proyek dan hasil transkripsi di direktori `output_transkripsi`.

## Catatan Mengenai Token
Informasi jumlah token yang digunakan diambil dari `usage_metadata` respons API Gemini. Untuk input gambar, metrik ini mungkin tidak selalu tersedia atau mungkin tidak secara langsung mencerminkan "token" gambar seperti pada input teks. Log akan menampilkan "N/A" jika tidak tersedia.

## Menangani Dokumen Panjang

Model AI memiliki batasan pada ukuran input. Jika Anda memiliki gambar dokumen yang sangat besar atau dengan teks yang sangat padat sehingga melebihi batasan model:

-   **Kualitas Hasil**: Transkripsi mungkin tidak lengkap atau tidak akurat.
-   **Error**: API mungkin mengembalikan error.

**Strategi yang Mungkin (Tidak Diimplementasikan Secara Otomatis di Versi Ini):**

-   **Pemecahan Gambar (Image Tiling)**: Untuk gambar tunggal yang sangat besar, Anda mungkin perlu memecahnya menjadi beberapa bagian yang lebih kecil, mentranskripsi setiap bagian, lalu menggabungkan hasilnya. Ini memerlukan logika pemrosesan gambar tambahan.
-   **Penyesuaian Kualitas Gambar**: Mengurangi resolusi gambar jika terlalu tinggi, namun tetap menjaga keterbacaan teks.

Fungsi `ocr.py` saat ini mengirimkan gambar apa adanya. Jika Anda sering menghadapi masalah dengan dokumen panjang, pertimbangkan untuk mengimplementasikan strategi di atas.

## Troubleshooting

-   **`ValueError: GOOGLE_API_KEY tidak ditemukan`**: Pastikan file `.env` ada di root proyek dan berisi `GOOGLE_API_KEY="KUNCI_ANDA"` dan Anda menjalankan `poetry run ...` dari root proyek.
-   **Error dari API Gemini**: Periksa pesan error. Mungkin terkait dengan format gambar, ukuran, konten yang diblokir karena alasan keamanan, atau masalah koneksi.
-   **Tidak ada file gambar ditemukan**: Pastikan path ke direktori input benar dan direktori tersebut berisi file `.png`, `.jpg`, atau `.jpeg`.
-   **Prompt tidak sesuai**: Jika hasil transkripsi kurang memuaskan, coba sesuaikan isi `prompt.txt` untuk memberikan instruksi yang lebih spesifik kepada model. Jika `prompt.txt` tidak ada, buatlah dari `prompt.txt.example`.
