# src/transkripsi_arsip/utils.py
import os
import json
from pathlib import Path

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
    data = {
        "nama_file": nama_file,
        "teks_transkripsi": teks_transkripsi
    }
    with open(path_output, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

