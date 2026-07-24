"""
Admin routes: Profiles — CRUD API untuk profil.

Endpoints:
    GET    /admin/profiles              → List semua profil
    GET    /admin/profiles/<id>         → Detail profil
    POST   /admin/profiles              → Buat profil baru
    PUT    /admin/profiles/<id>         → Update profil
    DELETE /admin/profiles/<id>         → Hapus profil
"""
from flask import request
from flask_login import login_required, current_user
from . import admin_bp
from app.extensions import db
from app.models import Profile
from app.utils import api_response
from app.services.cloudinary_service import validate_and_upload_image


def _serialize_profile(p):
    """Convert Profile model ke dict."""
    return {
        "id": p.id,
        "user_id": p.user_id,
        "nama_lengkap": p.nama_lengkap,
        "nama_panggilan": p.nama_panggilan,
        "tempat_lahir": p.tempat_lahir,
        "tanggal_lahir": str(p.tanggal_lahir) if p.tanggal_lahir else None,
        "email": p.email,
        "telepon": p.telepon,
        "universitas": p.universitas,
        "fakultas": p.fakultas,
        "prodi": p.prodi,
        "semester": p.semester,
        "alamat": p.alamat,
        "foto_url": p.foto_url,
        "foto_tentang_url": p.foto_tentang_url,
        "deskripsi": p.deskripsi,
    }


@admin_bp.route("/profiles", methods=["GET"])
@login_required
def list_profiles():
    """List semua profil milik user yang login."""
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    data = [_serialize_profile(profile)] if profile else []
    return api_response("success", f"Ditemukan {len(data)} profil.", data=data)


@admin_bp.route("/profiles/<int:profile_id>", methods=["GET"])
@login_required
def get_profile(profile_id):
    """Detail profil berdasarkan ID."""
    profile = Profile.query.get(profile_id)
    if not profile or profile.user_id != current_user.id:
        return api_response("error", "Profil tidak ditemukan.", status_code=404)
    return api_response("success", "Detail profil.", data=_serialize_profile(profile))


@admin_bp.route("/profiles", methods=["POST"])
@login_required
def create_profile():
    """
    Buat profil baru.
    Mendukung JSON atau multipart/form-data.
    Upload gambar: key 'foto'
    """
    # Cek apakah sudah punya profil
    existing = Profile.query.filter_by(user_id=current_user.id).first()
    if existing:
        return api_response("error", "Profil sudah ada. Gunakan PUT untuk update.", status_code=409)

    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    # Validasi field wajib
    nama_lengkap = (data.get("nama_lengkap") or "").strip()
    if not nama_lengkap:
        return api_response("error", "Field 'nama_lengkap' wajib diisi.", status_code=400)

    # Parse tanggal_lahir jika ada
    tanggal_lahir = None
    if data.get("tanggal_lahir"):
        from datetime import date as dt_date
        try:
            tanggal_lahir = dt_date.fromisoformat(data["tanggal_lahir"])
        except ValueError:
            return api_response("error", "Format 'tanggal_lahir' harus YYYY-MM-DD.", status_code=400)

    foto_url = (data.get("foto_url") or "").strip() or None
    foto_tentang_url = (data.get("foto_tentang_url") or "").strip() or None
    
    # Handle image upload if provided
    file = request.files.get("foto")
    if file and file.filename:
        url, err = validate_and_upload_image(file, folder="portfolio/profiles")
        if err:
            return api_response("error", err, status_code=400)
        foto_url = url

    file_tentang = request.files.get("foto_tentang")
    if file_tentang and file_tentang.filename:
        url2, err2 = validate_and_upload_image(file_tentang, folder="portfolio/profiles")
        if err2:
            return api_response("error", err2, status_code=400)
        foto_tentang_url = url2

    profile = Profile(
        user_id=current_user.id,
        nama_lengkap=nama_lengkap,
        nama_panggilan=(data.get("nama_panggilan") or "").strip() or None,
        tempat_lahir=(data.get("tempat_lahir") or "").strip() or None,
        tanggal_lahir=tanggal_lahir,
        email=(data.get("email") or "").strip() or None,
        telepon=(data.get("telepon") or "").strip() or None,
        universitas=(data.get("universitas") or "").strip() or None,
        fakultas=(data.get("fakultas") or "").strip() or None,
        prodi=(data.get("prodi") or "").strip() or None,
        semester=(data.get("semester") or "").strip() or None,
        alamat=(data.get("alamat") or "").strip() or None,
        foto_url=foto_url,
        foto_tentang_url=foto_tentang_url,
        deskripsi=(data.get("deskripsi") or "").strip() or None,
    )

    db.session.add(profile)
    db.session.commit()

    return api_response("success", "Profil berhasil dibuat.",
                        data=_serialize_profile(profile), status_code=201)


@admin_bp.route("/profiles/<int:profile_id>", methods=["PUT"])
@login_required
def update_profile(profile_id):
    """
    Update profil berdasarkan ID. 
    Mendukung JSON atau multipart/form-data.
    Upload gambar: key 'foto'
    """
    profile = Profile.query.get(profile_id)
    if not profile or profile.user_id != current_user.id:
        return api_response("error", "Profil tidak ditemukan.", status_code=404)

    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    # Update field-field yang dikirim (partial update)
    string_fields = [
        "nama_lengkap", "nama_panggilan", "tempat_lahir", "email",
        "telepon", "universitas", "fakultas", "prodi", "semester",
        "alamat", "foto_url", "foto_tentang_url", "deskripsi",
    ]
    for field in string_fields:
        if field in data:
            value = (data[field] or "").strip() or None
            setattr(profile, field, value)

    # Validasi nama_lengkap tidak boleh kosong setelah update
    if profile.nama_lengkap is None:
        return api_response("error", "Field 'nama_lengkap' tidak boleh kosong.", status_code=400)

    # Parse tanggal_lahir
    if "tanggal_lahir" in data:
        if data["tanggal_lahir"]:
            from datetime import date as dt_date
            try:
                profile.tanggal_lahir = dt_date.fromisoformat(data["tanggal_lahir"])
            except ValueError:
                return api_response("error", "Format 'tanggal_lahir' harus YYYY-MM-DD.", status_code=400)
        else:
            profile.tanggal_lahir = None

    # Handle image upload if provided
    file = request.files.get("foto")
    if file and file.filename:
        url, err = validate_and_upload_image(file, folder="portfolio/profiles")
        if err:
            return api_response("error", err, status_code=400)
        profile.foto_url = url

    file_tentang = request.files.get("foto_tentang")
    if file_tentang and file_tentang.filename:
        url2, err2 = validate_and_upload_image(file_tentang, folder="portfolio/profiles")
        if err2:
            return api_response("error", err2, status_code=400)
        profile.foto_tentang_url = url2

    db.session.commit()
    return api_response("success", "Profil berhasil diupdate.", data=_serialize_profile(profile))


@admin_bp.route("/profiles/<int:profile_id>", methods=["DELETE"])
@login_required
def delete_profile(profile_id):
    """Hapus profil berdasarkan ID."""
    profile = Profile.query.get(profile_id)
    if not profile or profile.user_id != current_user.id:
        return api_response("error", "Profil tidak ditemukan.", status_code=404)

    db.session.delete(profile)
    db.session.commit()
    return api_response("success", "Profil berhasil dihapus.")
