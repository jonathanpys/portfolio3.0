"""
Blueprint: Certificate — Endpoint publik untuk data sertifikasi (read-only).
"""
from flask import Blueprint
from app.models import Certificate
from app.utils import api_response

certificate_bp = Blueprint("certificate", __name__)


@certificate_bp.route("/api/certificates")
def get_certificates():
    """API publik: Ambil semua sertifikasi."""
    certificates = Certificate.query.order_by(Certificate.tanggal_terbit.desc()).all()
    data = [{
        "id": c.id,
        "judul": c.judul,
        "penerbit": c.penerbit,
        "tanggal_terbit": str(c.tanggal_terbit) if c.tanggal_terbit else None,
        "link_kredensial": c.link_kredensial,
        "gambar_url": c.gambar_url,
        "icon_penerbit_url": c.icon_penerbit_url,
    } for c in certificates]
    return api_response("success", f"Ditemukan {len(data)} sertifikasi.", data=data)
