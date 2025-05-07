# src/transkripsi_arsip/main.py
import argparse
from pathlib import Path
from . import utils
from . import ocr
import time

def jalankan_transkripsi(path_direktori_input_str: str):
    """
    Fungsi utama untuk menjalankan proses transkripsi.
    """
    path_direktori_input = Path(path_direktori_input_str).resolve()

    if not path_direktori_input.is_dir():
        print(f"Error: Direktori input '{path_direktori_input}' tidak ditemukan.")
        return

    # Membuat nama direktori output berdasarkan direktori input
    # Misalnya, jika input adalah 'data/dokumen_penting', output akan menjadi 'data/dokumen_penting_output'
    # atau ditempatkan dalam direktori 'output' dengan nama yang sama.
    # Untuk konsistensi, kita akan buat direktori output di dalam direktori 'data' jika belum ada,
    # dan nama subdirektori output akan sama dengan nama direktori input + '_hasil'.
    
    nama_direktori_output = f"{path_direktori_input.name}_hasil_transkripsi"
    path_direktori_output_induk = path_direktori_input.parent / "output" # Menyimpan semua output di 'data/output/'
    path_direktori_output = path_direktori_output_induk / nama_direktori_output
    
    utils.pastikan_direktori_ada(path_direktori_output)
    print(f"Direktori input: {path_direktori_input}")
    print(f"Direktori output akan dibuat di: {path_direktori_output}")

    daftar_gambar = utils.dapatkan_file_gambar(path_direktori_input)

    if not daftar_gambar:
        print(f"Tidak ada file gambar yang ditemukan di '{path_direktori_input}'.")
        return

    print(f"Ditemukan {len(daftar_gambar)} file gambar untuk ditranskripsi.")

    for path_gambar in daftar_gambar:
        print(f"Memproses {path_gambar.name}...")
        try:
            teks_hasil_transkripsi = ocr.transkripsi_gambar(path_gambar)
            
            nama_file_output_base = path_gambar.stem
            path_file_output_json = path_direktori_output / (nama_file_output_base + ".json")
            path_file_output_txt = path_direktori_output / (nama_file_output_base + ".txt") # Path untuk file .txt
            
            utils.simpan_hasil_json(path_file_output_json, path_gambar.name, teks_hasil_transkripsi)
            print(f"Hasil transkripsi JSON untuk {path_gambar.name} disimpan di {path_file_output_json}")

            utils.simpan_hasil_txt(path_file_output_txt, teks_hasil_transkripsi) # Menyimpan hasil ke .txt
            print(f"Hasil transkripsi TXT untuk {path_gambar.name} disimpan di {path_file_output_txt}")
        
        except Exception as e:
            print(f"Gagal memproses {path_gambar.name}: {e}")
        
        # Memberi jeda singkat untuk menghindari rate limit API (jika ada dan sering terjadi)
        # time.sleep(1) # Sesuaikan jika perlu

    print("Proses transkripsi selesai.")
    print(f"Semua hasil disimpan di direktori: {path_direktori_output}")

def run():
    parser = argparse.ArgumentParser(description="Program Transkripsi Arsip Dokumen Gambar.")
    parser.add_argument(
        "direktori_input",
        type=str,
        help="Path ke direktori yang berisi gambar-gambar dokumen yang akan ditranskripsi."
    )
    
    args = parser.parse_args()
    jalankan_transkripsi(args.direktori_input)

if __name__ == "__main__":
    # Contoh penggunaan jika dijalankan langsung (untuk testing internal)
    # Pastikan ada direktori 'data/input_contoh' dengan gambar di dalamnya
    # dan file .env sudah diatur dengan API Key.
    # contoh_input_dir = Path(__file__).resolve().parents[2] / "data" / "input_contoh"
    # utils.pastikan_direktori_ada(contoh_input_dir) # Buat jika belum ada
    # print(f"Untuk pengujian, pastikan ada gambar di: {contoh_input_dir} dan .env sudah benar.")
    # print("Jalankan dengan: poetry run transkripsi path/ke/direktori_input_anda")
    
    # Untuk menjalankan dari CLI setelah instalasi dengan poetry:
    # poetry install
    # poetry run transkripsi nama_direktori_input_anda
    run()
