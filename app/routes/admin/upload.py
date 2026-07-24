"""
Admin routes: Upload — Endpoint upload gambar ke Cloudinary.
"""
from flask_login import login_required
from . import admin_bp


@admin_bp.route("/upload", methods=["POST"])
@login_required
def upload_image():
    """Upload gambar ke Cloudinary dan return URL."""
    # TODO:
    # 1. Ambil file dari request.files
    # 2. Validasi tipe file (hanya gambar)
    # 3. Upload via cloudinary_service.upload_image(file)
    # 4. Return JSON { "url": "...", "public_id": "..." }
    return {"message": "TODO: upload image to Cloudinary"}
