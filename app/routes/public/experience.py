"""
Blueprint: Experience — Endpoint publik untuk data pengalaman (read-only).

Endpoints:
    GET /api/experiences  → List semua pengalaman
"""
from flask import Blueprint
from app.models import Experience
from app.utils import api_response

experience_bp = Blueprint("experience", __name__)


@experience_bp.route("/api/experiences")
def get_experiences():
    """API publik: Ambil semua pengalaman."""
    experiences = Experience.query.order_by(Experience.durasi.asc()).all()
    data = [{
        "id": e.id,
        "posisi": e.posisi,
        "perusahaan": e.perusahaan,
        "durasi": e.durasi,
        "deskripsi": e.deskripsi,
        "kategori": e.kategori,
    } for e in experiences]
    return api_response("success", f"Ditemukan {len(data)} pengalaman.", data=data)
