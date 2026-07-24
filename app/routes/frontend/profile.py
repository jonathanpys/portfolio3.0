"""
Blueprint: Profile — Endpoint publik untuk data profil (read-only).

Endpoints:
    GET /             → Halaman utama (nanti render template)
    GET /api/profile  → Data profil dalam JSON
"""
from flask import Blueprint, render_template
from app.models import Profile
from app.utils import api_response

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/")
def index():
    """Halaman utama portofolio."""
    return render_template('public/index.html')


@profile_bp.route("/api/profile")
def get_profile():
    """API publik: Ambil data profil (user_id=1 sebagai default)."""
    profile = Profile.query.first()
    if not profile:
        return api_response("success", "Belum ada profil.", data=None)

    return api_response("success", "Data profil.", data={
        "id": profile.id,
        "nama_lengkap": profile.nama_lengkap,
        "nama_panggilan": profile.nama_panggilan,
        "tempat_lahir": profile.tempat_lahir,
        "tanggal_lahir": str(profile.tanggal_lahir) if profile.tanggal_lahir else None,
        "email": profile.email,
        "telepon": profile.telepon,
        "universitas": profile.universitas,
        "fakultas": profile.fakultas,
        "prodi": profile.prodi,
        "semester": profile.semester,
        "alamat": profile.alamat,
        "foto_url": profile.foto_url,
        "foto_tentang_url": profile.foto_tentang_url,
        "deskripsi": profile.deskripsi,
    })
