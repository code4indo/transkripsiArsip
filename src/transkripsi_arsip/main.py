# src/transkripsi_arsip/main.py
import argparse
from pathlib import Path
from . import utils
from . import ocr
import time
from tqdm import tqdm # Import tqdm

def jalankan_transkripsi(path_direktori_input_str: str):
    """
    Fungsi utama untuk menjalankan proses transkripsi.
    """
    project_root = Path(__file__).resolve().parents[2]
    utils.init_log()
    utils.log_event(f"Memulai proses transkripsi untuk direktori: {path_direktori_input_str}")

    path_direktori_input = Path(path_direktori_input_str).resolve()

    if not path_direktori_input.is_dir():
        utils.log_event(f"Error: Direktori input '{path_direktori_input}' tidak ditemukan.")
        utils.finalize_log(project_root)
        return

    nama_direktori_output = f"{path_direktori_input.name}_hasil_transkripsi"
    # Menyimpan output log dan hasil transkripsi relatif terhadap struktur proyek
    # Misal output akan ada di /home/project/transkripsiArsip/output_transkripsi/
    path_direktori_output_induk = project_root / "output_transkripsi" 
    path_direktori_output = path_direktori_output_induk / nama_direktori_output
    
    # Membuat subdirektori untuk output JSON dan TXT
    path_direktori_output_json = path_direktori_output / "json"
    path_direktori_output_txt = path_direktori_output / "txt"
    
    utils.pastikan_direktori_ada(path_direktori_output_json)
    utils.pastikan_direktori_ada(path_direktori_output_txt)
    utils.log_event(f"Direktori input: {path_direktori_input}")
    utils.log_event(f"Direktori output utama: {path_direktori_output}")
    utils.log_event(f"Output JSON akan disimpan di: {path_direktori_output_json}")
    utils.log_event(f"Output TXT akan disimpan di: {path_direktori_output_txt}")

    # Dapatkan system prompt sekali saja untuk dicatat di log jika perlu
    # current_system_prompt = ocr.dapatkan_system_prompt() # Bisa dicatat jika ingin tahu prompt yg digunakan
    # utils.log_event(f"Menggunakan system prompt: {current_system_prompt[:100]}...") # Log sebagian prompt

    daftar_gambar = utils.dapatkan_file_gambar(path_direktori_input)

    if not daftar_gambar:
        utils.log_event(f"Tidak ada file gambar yang ditemukan di '{path_direktori_input}'.")
        utils.finalize_log(project_root)
        return

    utils.log_event(f"Ditemukan {len(daftar_gambar)} file gambar untuk diproses.")

    # Menggunakan tqdm untuk progress bar
    for path_gambar in tqdm(daftar_gambar, desc="Mentranskripsi Gambar", unit="file"):
        nama_file_output_base = path_gambar.stem
        # Mengarahkan path output ke subdirektori yang sesuai
        path_file_output_json = path_direktori_output_json / (nama_file_output_base + ".json")
        path_file_output_txt = path_direktori_output_txt / (nama_file_output_base + ".txt")

        # Cek apakah file output sudah ada (misalnya .json dan .txt di lokasi baru)
        if path_file_output_json.is_file() and path_file_output_txt.is_file():
            utils.log_event(f"Output untuk {path_gambar.name} sudah ada, dilewati.")
            utils.increment_skipped_count()
            continue # Lanjut ke gambar berikutnya

        utils.log_event(f"Memproses {path_gambar.name}...")
        try:
            teks_hasil_transkripsi, token_digunakan = ocr.transkripsi_gambar(path_gambar)
            utils.add_tokens(token_digunakan)
            
            utils.simpan_hasil_json(path_file_output_json, path_gambar.name, teks_hasil_transkripsi)
            # utils.log_event(f"Hasil transkripsi JSON untuk {path_gambar.name} disimpan di {path_file_output_json}")

            utils.simpan_hasil_txt(path_file_output_txt, teks_hasil_transkripsi)
            utils.log_event(f"Hasil transkripsi (JSON & TXT) untuk {path_gambar.name} disimpan.")
            utils.increment_processed_count()
        
        except Exception as e:
            utils.log_event(f"Gagal memproses {path_gambar.name}: {e}")
        
        # time.sleep(0.1) # Jeda kecil jika diperlukan, tqdm menangani refresh rate

    utils.log_event("Proses transkripsi selesai.")
    utils.finalize_log(project_root)

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
    run()
