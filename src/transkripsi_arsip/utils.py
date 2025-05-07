# src/transkripsi_arsip/utils.py
import os
import json
from pathlib import Path
import datetime

LOG_FILE_NAME = "transcription_log.txt"

def pastikan_direktori_ada(path_direktori: Path):
    """Memastikan direktori ada, jika tidak maka akan dibuat."""
    path_direktori.mkdir(parents=True, exist_ok=True)

def dapatkan_file_gambar(path_direktori_input: Path) -> list[Path]:
    """Mendapatkan daftar file gambar (png, jpg, jpeg) dari direktori input."""
    ekstensi_didukung = [".png", ".jpg", ".jpeg"]
    return [
        file for file in path_direktori_input.iterdir()
        if file.is_file() and file.suffix.lower() in ekstensi_didukung
    ]

def simpan_hasil_json(path_output: Path, nama_file: str, teks_transkripsi: str):
    """Menyimpan hasil transkripsi ke file JSON."""
    cleaned_transkripsi = teks_transkripsi
    
    prefixes_to_remove = [
        "Baik, berikut transkripsi dari teks yang terlihat jelas pada gambar:\\n\\n",
        "Baik, berikut transkripsi dari teks yang terlihat jelas pada gambar:\\n",
        "Berikut transkripsi teks yang terlihat jelas pada gambar, menggunakan ejaan lama:\\n\\n",
        "Berikut transkripsi teks yang terlihat jelas pada gambar, menggunakan ejaan lama:\\n"
    ]

    for prefix in prefixes_to_remove:
        if cleaned_transkripsi.startswith(prefix):
            cleaned_transkripsi = cleaned_transkripsi[len(prefix):]
            break # Hapus hanya prefiks pertama yang cocok

    data = {
        "nama_file": nama_file,
        "teks_transkripsi": cleaned_transkripsi
    }
    with open(path_output, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def simpan_hasil_txt(path_output_txt: Path, teks_transkripsi: str):
    """Menyimpan hasil transkripsi mentah ke file TXT, mengabaikan struktur paragraf."""
    cleaned_text = teks_transkripsi
    
    prefixes_to_remove = [
        "Baik, berikut transkripsi dari teks yang terlihat jelas pada gambar:\\n\\n",
        "Baik, berikut transkripsi dari teks yang terlihat jelas pada gambar:\\n",
        "Berikut transkripsi teks yang terlihat jelas pada gambar, menggunakan ejaan lama:\\n\\n",
        "Berikut transkripsi teks yang terlihat jelas pada gambar, menggunakan ejaan lama:\\n"
    ]

    for prefix in prefixes_to_remove:
        if cleaned_text.startswith(prefix):
            cleaned_text = cleaned_text[len(prefix):]
            break # Hapus hanya prefiks pertama yang cocok
    
    with open(path_output_txt, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

# Logging functions
log_data = {
    "start_time": None,
    "end_time": None,
    "total_time_seconds": None,
    "total_documents_processed": 0,
    "total_documents_skipped": 0,
    "total_tokens_used": 0, # Akan diakumulasi jika API menyediakan info token
    "actual_tokens_used": 0, # Untuk token nyata yang digunakan
    "log_messages": []
}

def init_log():
    log_data["start_time"] = datetime.datetime.now()
    log_data["log_messages"].append(f"Logging dimulai pada: {log_data['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")

def log_event(message: str):
    print(message) # Juga tampilkan di konsol
    log_data["log_messages"].append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}")

def increment_processed_count():
    log_data["total_documents_processed"] += 1

def increment_skipped_count():
    log_data["total_documents_skipped"] += 1

def add_tokens(tokens: int | None):
    if tokens is not None and isinstance(tokens, int):
        log_data["total_tokens_used"] += tokens

def add_actual_tokens(tokens: int | None):
    """Menambahkan jumlah token nyata yang digunakan."""
    if tokens is not None and isinstance(tokens, int):
        log_data["actual_tokens_used"] += tokens

def finalize_log(project_root_path: Path):
    global log_data # Moved global declaration to the top of the function
    log_data["end_time"] = datetime.datetime.now()
    if log_data["start_time"]:
        log_data["total_time_seconds"] = (log_data["end_time"] - log_data["start_time"]).total_seconds()
    
    log_file_path = project_root_path / LOG_FILE_NAME
    
    summary = (
        f"--- Ringkasan Transkripsi ---\n"
        f"Waktu Mulai: {log_data['start_time'].strftime('%Y-%m-%d %H:%M:%S') if log_data['start_time'] else 'N/A'}\n"
        f"Waktu Selesai: {log_data['end_time'].strftime('%Y-%m-%d %H:%M:%S') if log_data['end_time'] else 'N/A'}\n"
        f"Total Waktu Transkripsi: {log_data['total_time_seconds']:.2f} detik (sekitar {log_data['total_time_seconds']/60:.2f} menit) jika tersedia\n"
        f"Total Dokumen Diproses: {log_data['total_documents_processed']}\n"
        f"Total Dokumen Dilewati (sudah ada): {log_data['total_documents_skipped']}\n"
        f"Total Token Estimasi (dari API): {log_data['total_tokens_used'] if log_data['total_tokens_used'] > 0 else 'N/A (API mungkin tidak menyediakan info ini atau tidak ada yang diproses)'}\n"
        f"Total Token Nyata Digunakan: {log_data['actual_tokens_used'] if log_data['actual_tokens_used'] > 0 else 'N/A (Tidak ada data token nyata)'}\n"
        f"--- Detail Log ---\n"
    )

    with open(log_file_path, 'w', encoding='utf-8') as f:
        f.write(summary)
        for msg in log_data["log_messages"]:
            f.write(msg + "\n")
    print(f"Log lengkap disimpan di: {log_file_path}")
    # Reset log_data untuk potensi run berikutnya dalam sesi yang sama (jika aplikasi interaktif)
    log_data = {
        "start_time": None,
        "end_time": None,
        "total_time_seconds": None,
        "total_documents_processed": 0,
        "total_documents_skipped": 0,
        "total_tokens_used": 0,
        "actual_tokens_used": 0, # Reset juga token nyata
        "log_messages": []
    }

