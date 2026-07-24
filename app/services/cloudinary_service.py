"""
app/services/cloudinary_service.py — Helper upload gambar ke Cloudinary.
"""
import cloudinary
import cloudinary.uploader

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def init_cloudinary(app):
    """Konfigurasi Cloudinary dari app.config."""
    cloud_name = app.config.get("CLOUDINARY_CLOUD_NAME")
    api_key = app.config.get("CLOUDINARY_API_KEY")
    api_secret = app.config.get("CLOUDINARY_API_SECRET")
    
    if not cloud_name or not api_key or not api_secret:
        # Warning: Jika belum diset di .env, upload akan gagal saat runtime
        # tapi aplikasi tetap bisa berjalan (untuk endpoint non-upload).
        pass

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
        secure=True,
    )


def allowed_file(filename):
    """Cek ekstensi file yang diizinkan."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_and_upload_image(file, folder="portfolio"):
    """
    Validasi file dan upload ke Cloudinary.
    Return tuple (url, error_message).
    """
    if not file or not file.filename:
        return None, "File tidak ditemukan."
    
    if not allowed_file(file.filename):
        return None, "Tipe file tidak diizinkan. Hanya JPG, PNG, WEBP."
    
    # Cek ukuran (seek ke end, dapat posisi, kembali ke 0)
    file.seek(0, 2)
    file_length = file.tell()
    file.seek(0)
    
    if file_length > MAX_FILE_SIZE:
        return None, f"Ukuran file maksimal 5MB. Ukuran saat ini: {file_length / (1024*1024):.2f}MB"
        
    try:
        result = cloudinary.uploader.upload(file, folder=folder)
        return result["secure_url"], None
    except Exception as e:
        return None, f"Gagal upload ke Cloudinary: {str(e)}"


def delete_image(public_id):
    """Hapus image dari Cloudinary berdasarkan public_id."""
    try:
        return cloudinary.uploader.destroy(public_id)
    except Exception:
        return None
