"""
Blueprint: Contact — Endpoint publik untuk form kontak.

Endpoints:
    POST /api/contact  → Menerima form kontak, simpan ke DB, kirim email via Resend
"""
import re
from flask import Blueprint, request
from app.extensions import db
from app.models import Contact
from app.utils import api_response
from app.services.resend_service import send_contact_email

contact_bp = Blueprint("contact", __name__)

def is_valid_email(email):
    """Basic email format validation."""
    regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(regex, email) is not None

@contact_bp.route("/api/contact", methods=["POST"])
def submit_contact():
    """
    API publik: Submit form kontak.
    Menerima JSON:
    {
        "nama": "...",
        "email": "...",
        "subjek": "...",
        "pesan": "..."
    }
    """
    data = request.get_json(silent=True) or request.form.to_dict()
    
    nama = (data.get("nama") or "").strip()
    email = (data.get("email") or "").strip()
    subjek = (data.get("subjek") or "").strip()
    pesan = (data.get("pesan") or "").strip()

    # 1. Validasi Input
    errors = []
    if not nama: errors.append("Nama wajib diisi")
    if not email: errors.append("Email wajib diisi")
    elif not is_valid_email(email): errors.append("Format email tidak valid")
    if not subjek: errors.append("Subjek wajib diisi")
    if not pesan: errors.append("Pesan wajib diisi")

    if errors:
        return api_response("error", "Validasi gagal: " + ", ".join(errors), status_code=400)

    # 2. Simpan ke Database
    contact_msg = Contact(
        nama=nama,
        email=email,
        subjek=subjek,
        pesan=pesan,
        status="unread"
    )
    db.session.add(contact_msg)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return api_response("error", "Gagal menyimpan pesan ke database.", status_code=500)

    # 3. Kirim Email via Resend
    # Meskipun gagal, data sudah tersimpan di DB
    success, error_msg = send_contact_email(nama, email, subjek, pesan)
    
    if not success:
        return api_response(
            "success", 
            f"Pesan Anda berhasil disimpan di database kami, namun gagal meneruskan ke email admin. Error: {error_msg}", 
            status_code=201
        )

    return api_response("success", "Pesan Anda berhasil dikirim!", status_code=201)
