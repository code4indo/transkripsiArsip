# src/transkripsi_arsip/ocr.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image

# Muat environment variables dari .env
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / '.env')

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY tidak ditemukan. Pastikan file .env ada dan berisi API key.")

genai.configure(api_key=API_KEY)

# Menggunakan model gemini-1.5-flash karena gemini-2.0-flash mungkin belum ada atau nama alias
# Sesuaikan dengan nama model yang tersedia dan sesuai untuk tugas OCR.
# Untuk tugas OCR gambar, model yang mendukung input multimodal (gambar) diperlukan.
# 'gemini-1.5-flash-latest' atau 'gemini-pro-vision' (jika masih ada) adalah pilihan yang baik.
# Kita akan menggunakan 'gemini-1.5-flash-latest' sebagai contoh yang lebih modern.
MODEL_NAME = "gemini-1.5-flash-latest" # Pastikan model ini mendukung input gambar

DEFAULT_SYSTEM_PROMPT = "Transkripsikan semua teks yang ada dalam gambar ini secara akurat. Fokus hanya pada teks yang terlihat jelas. Abaikan elemen grafis atau noise pada gambar."

def dapatkan_system_prompt() -> str:
    """Membaca system prompt dari prompt.txt jika ada, jika tidak gunakan default."""
    path_prompt_file = Path(__file__).resolve().parents[2] / "prompt.txt"
    if path_prompt_file.is_file():
        try:
            with open(path_prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
                if prompt:
                    print(f"Menggunakan system prompt kustom dari: {path_prompt_file}")
                    return prompt
                else:
                    print(f"File prompt.txt kosong, menggunakan prompt default.")
                    return DEFAULT_SYSTEM_PROMPT
        except Exception as e:
            print(f"Error membaca file prompt.txt: {e}. Menggunakan prompt default.")
            return DEFAULT_SYSTEM_PROMPT
    else:
        print("File prompt.txt tidak ditemukan. Menggunakan prompt default.")
        return DEFAULT_SYSTEM_PROMPT

def transkripsi_gambar(path_gambar: Path) -> str:
    """
    Mentranskripsi teks dari sebuah gambar menggunakan Gemini API.
    """
    print(f"Mentranskripsi gambar: {path_gambar.name}...")
    try:
        img = Image.open(path_gambar)
        # Model Gemini yang mendukung multimodal input (seperti gambar)
        # biasanya menerima list dari parts, di mana part bisa berupa teks atau data gambar.
        model = genai.GenerativeModel(MODEL_NAME)

        # Prompt untuk mengarahkan model melakukan OCR
        # prompt_ocr = "Transkripsikan teks yang ada dalam gambar ini. Fokus hanya pada teks yang terlihat jelas."
        prompt_ocr = dapatkan_system_prompt() # Menggunakan prompt yang bisa dikonfigurasi

        # Mengirim gambar dan prompt ke model
        # Pastikan format gambar didukung dan cara mengirimkannya sesuai dokumentasi API.
        # Untuk 'gemini-1.5-flash-latest', kita bisa mengirimkan objek PIL Image secara langsung.
        response = model.generate_content([prompt_ocr, img])

        # Menangani respons dari API
        # Periksa apakah ada teks yang dihasilkan dan apakah ada error
        if response and hasattr(response, 'text') and response.text:
            print(f"Transkripsi berhasil untuk {path_gambar.name}.")
            return response.text
        elif response and hasattr(response, 'parts'): # Beberapa model mungkin mengembalikan 'parts'
            all_text = "".join(part.text for part in response.parts if hasattr(part, 'text'))
            if all_text:
                print(f"Transkripsi berhasil untuk {path_gambar.name}.")
                return all_text
            else:
                print(f"Tidak ada teks yang terdeteksi atau respons tidak mengandung teks untuk {path_gambar.name}.")
                return ""
        else:
            # Log detail respons jika tidak sesuai harapan untuk debugging
            print(f"Respons tidak terduga dari API untuk {path_gambar.name}: {response}")
            # Coba akses prompt_feedback jika ada untuk melihat alasan blokir
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                print(f"Prompt feedback: {response.prompt_feedback}")
            return "Error: Respons tidak valid dari API atau tidak ada teks yang dihasilkan."

    except Exception as e:
        print(f"Terjadi error saat mentranskripsi {path_gambar.name}: {e}")
        # Periksa apakah error terkait dengan safety settings
        if "SAFETY" in str(e).upper():
            return "Error: Konten diblokir karena pengaturan keamanan. Coba gambar lain atau sesuaikan pengaturan (jika memungkinkan)."
        return f"Error: {str(e)}"

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
