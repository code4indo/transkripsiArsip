# src/transkripsi_arsip/ocr.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
from typing import Tuple, Optional

# Muat environment variables dari .env
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY tidak ditemukan. Pastikan file .env ada dan berisi API key.")

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash-latest"
DEFAULT_SYSTEM_PROMPT = "Transkripsikan semua teks yang ada dalam gambar ini secara akurat. Fokus hanya pada teks yang terlihat jelas. Abaikan elemen grafis atau noise pada gambar."

def dapatkan_system_prompt() -> str:
    """Membaca system prompt dari prompt.txt jika ada, jika tidak gunakan default."""
    path_prompt_file = Path(__file__).resolve().parents[2] / "prompt.txt"
    if path_prompt_file.is_file():
        try:
            with open(path_prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
                if prompt:
                    # print(f"Menggunakan system prompt kustom dari: {path_prompt_file}") # Dihilangkan agar tidak spam console
                    return prompt
                else:
                    # print(f"File prompt.txt kosong, menggunakan prompt default.")
                    return DEFAULT_SYSTEM_PROMPT
        except Exception as e:
            print(f"Error membaca file prompt.txt: {e}. Menggunakan prompt default.")
            return DEFAULT_SYSTEM_PROMPT
    else:
        # print("File prompt.txt tidak ditemukan. Menggunakan prompt default.")
        return DEFAULT_SYSTEM_PROMPT

def transkripsi_gambar(path_gambar: Path) -> Tuple[str, Optional[int]]:
    """
    Mentranskripsi teks dari sebuah gambar menggunakan Gemini API.
    Mengembalikan tuple (teks_transkripsi, total_token_digunakan).
    total_token_digunakan bisa None jika API tidak menyediakannya.
    """
    # print(f"Mentranskripsi gambar: {path_gambar.name}...") # Akan dihandle oleh logger
    try:
        img = Image.open(path_gambar)
        model = genai.GenerativeModel(MODEL_NAME)
        prompt_ocr = dapatkan_system_prompt()
        response = model.generate_content([prompt_ocr, img])

        teks_hasil = ""
        if response and hasattr(response, 'text') and response.text:
            teks_hasil = response.text
        elif response and hasattr(response, 'parts'):
            teks_hasil = "".join(part.text for part in response.parts if hasattr(part, 'text'))
        
        token_count = None
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            if hasattr(response.usage_metadata, 'total_token_count'):
                token_count = response.usage_metadata.total_token_count
            elif hasattr(response.usage_metadata, 'prompt_token_count') and hasattr(response.usage_metadata, 'candidates_token_count'):
                token_count = response.usage_metadata.prompt_token_count + response.usage_metadata.candidates_token_count

        if not teks_hasil:
            # print(f"Tidak ada teks yang terdeteksi atau respons tidak mengandung teks untuk {path_gambar.name}.")
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                # print(f"Prompt feedback: {response.prompt_feedback}")
                return f"Error: Konten mungkin diblokir. Feedback: {response.prompt_feedback}", token_count
            return "Error: Respons tidak valid dari API atau tidak ada teks yang dihasilkan.", token_count
        
        # print(f"Transkripsi berhasil untuk {path_gambar.name}.") # Akan dihandle oleh logger
        return teks_hasil, token_count

    except Exception as e:
        # print(f"Terjadi error saat mentranskripsi {path_gambar.name}: {e}") # Akan dihandle oleh logger
        if "SAFETY" in str(e).upper():
            return "Error: Konten diblokir karena pengaturan keamanan.", None
        return f"Error: {str(e)}", None

# Catatan mengenai dokumen panjang:
# Model Gemini memiliki batasan token input. Untuk dokumen yang sangat panjang (misalnya, gambar buku dengan banyak halaman
# atau gambar poster yang sangat besar dengan teks kecil yang banyak), pendekatan berikut mungkin diperlukan:
# 1. Pemecahan Gambar (Image Tiling): Jika satu gambar terlalu besar atau terlalu padat teksnya,
#    gambar bisa dipecah menjadi beberapa bagian yang lebih kecil. Setiap bagian ditranskripsi secara terpisah,
#    kemudian hasilnya digabungkan. Ini memerlukan logika tambahan untuk memotong gambar dan menggabungkan teks.
# 2. Pemrosesan Bertahap: Jika dokumen terdiri dari banyak file gambar (misalnya, setiap halaman adalah file terpisah),
#    skrip ini sudah memprosesnya satu per satu.
# 3. Optimasi Prompt: Untuk dokumen yang kompleks, prompt bisa disesuaikan untuk meminta model fokus pada area tertentu
#    atau jenis informasi tertentu jika relevan.
# 4. Pengecekan Batasan Model: Selalu periksa dokumentasi model Gemini terbaru untuk batasan ukuran input
#    (misalnya, resolusi gambar, ukuran file) dan batasan token output.
# Saat ini, fungsi `transkripsi_gambar` memproses satu gambar utuh. Jika gambar terlalu besar atau kompleks
# sehingga melebihi batas input model, error akan terjadi atau hasilnya mungkin tidak optimal.
