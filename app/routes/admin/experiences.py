"""
Admin routes: Experiences — CRUD API untuk pengalaman.

Endpoints:
    GET    /admin/experiences              → List semua pengalaman
    GET    /admin/experiences/<id>         → Detail pengalaman
    POST   /admin/experiences              → Buat pengalaman baru
    PUT    /admin/experiences/<id>         → Update pengalaman
    DELETE /admin/experiences/<id>         → Hapus pengalaman
"""
from flask import request
from flask_login import login_required, current_user
from . import admin_bp
from app.extensions import db
from app.models import Experience
from app.utils import api_response


def _serialize_experience(e):
    """Convert Experience model ke dict."""
    return {
        "id": e.id,
        "user_id": e.user_id,
        "posisi": e.posisi,
        "perusahaan": e.perusahaan,
        "durasi": e.durasi,
        "deskripsi": e.deskripsi,
        "kategori": e.kategori,
        "created_at": str(e.created_at) if e.created_at else None,
    }


@admin_bp.route("/experiences", methods=["GET"])
@login_required
def list_experiences():
    """List semua pengalaman milik user yang login."""
    experiences = Experience.query.filter_by(user_id=current_user.id) \
        .order_by(Experience.created_at.desc()).all()
    data = [_serialize_experience(e) for e in experiences]
    return api_response("success", f"Ditemukan {len(data)} pengalaman.", data=data)


@admin_bp.route("/experiences/<int:exp_id>", methods=["GET"])
@login_required
def get_experience(exp_id):
    """Detail pengalaman berdasarkan ID."""
    exp = Experience.query.get(exp_id)
    if not exp or exp.user_id != current_user.id:
        return api_response("error", "Pengalaman tidak ditemukan.", status_code=404)
    return api_response("success", "Detail pengalaman.", data=_serialize_experience(exp))


@admin_bp.route("/experiences", methods=["POST"])
@login_required
def create_experience():
    """
    Buat pengalaman baru.

    Request body (JSON):
        {
            "posisi": "wajib",
            "perusahaan": "wajib",
            "durasi": "opsional",
            "deskripsi": "opsional"
        }
    """
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    if not data:
        return api_response("error", "Data tidak boleh kosong.", status_code=400)

    # Validasi field wajib
    posisi = (data.get("posisi") or "").strip()
    perusahaan = (data.get("perusahaan") or "").strip()
    kategori = (data.get("kategori") or "pekerjaan").strip()

    errors = []
    if not posisi:
        errors.append("'posisi' wajib diisi")
    if not perusahaan:
        errors.append("'perusahaan' wajib diisi")
    if kategori not in ["pekerjaan", "organisasi", "prestasi"]:
        errors.append("kategori tidak valid")
    if len(posisi) > 100:
        errors.append("'posisi' maksimal 100 karakter")
    if len(perusahaan) > 100:
        errors.append("'perusahaan' maksimal 100 karakter")

    if errors:
        return api_response("error", "Validasi gagal: " + "; ".join(errors) + ".", status_code=400)

    tanggal_mulai = (data.get("tanggal_mulai") or "").strip()
    tanggal_selesai = (data.get("tanggal_selesai") or "").strip()
    durasi = (data.get("durasi") or "").strip()
    if not durasi and (tanggal_mulai or tanggal_selesai):
        durasi = f"{tanggal_mulai} — {tanggal_selesai or 'Sekarang'}"

    deskripsi = (data.get("deskripsi_pekerjaan") or data.get("deskripsi") or "").strip()

    exp = Experience(
        user_id=current_user.id,
        posisi=posisi,
        perusahaan=perusahaan,
        durasi=durasi or None,
        deskripsi=deskripsi or None,
        kategori=kategori
    )

    db.session.add(exp)
    db.session.commit()

    return api_response("success", "Pengalaman berhasil ditambahkan.",
                        data=_serialize_experience(exp), status_code=201)


@admin_bp.route("/experiences/<int:exp_id>", methods=["PUT"])
@login_required
def update_experience(exp_id):
    """Update pengalaman berdasarkan ID."""
    exp = Experience.query.get(exp_id)
    if not exp or exp.user_id != current_user.id:
        return api_response("error", "Pengalaman tidak ditemukan.", status_code=404)

    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    if not data:
        return api_response("error", "Data tidak boleh kosong.", status_code=400)

    if "posisi" in data:
        posisi = (data["posisi"] or "").strip()
        if not posisi:
            return api_response("error", "Field 'posisi' tidak boleh kosong.", status_code=400)
        if len(posisi) > 100:
            return api_response("error", "Field 'posisi' maksimal 100 karakter.", status_code=400)
        exp.posisi = posisi

    if "perusahaan" in data:
        perusahaan = (data["perusahaan"] or "").strip()
        if not perusahaan:
            return api_response("error", "Field 'perusahaan' tidak boleh kosong.", status_code=400)
        if len(perusahaan) > 100:
            return api_response("error", "Field 'perusahaan' maksimal 100 karakter.", status_code=400)
        exp.perusahaan = perusahaan

    if "kategori" in data:
        kategori = (data.get("kategori") or "").strip()
        if kategori in ["pekerjaan", "organisasi", "prestasi"]:
            exp.kategori = kategori

    if "durasi" in data or "tanggal_mulai" in data or "tanggal_selesai" in data:
        tanggal_mulai = (data.get("tanggal_mulai") or "").strip()
        tanggal_selesai = (data.get("tanggal_selesai") or "").strip()
        durasi = (data.get("durasi") or "").strip()
        
        if not durasi and (tanggal_mulai or tanggal_selesai):
            durasi = f"{tanggal_mulai} — {tanggal_selesai or 'Sekarang'}"
            
        exp.durasi = durasi or None

    if "deskripsi" in data or "deskripsi_pekerjaan" in data:
        exp.deskripsi = (data.get("deskripsi_pekerjaan") or data.get("deskripsi") or "").strip() or None

    db.session.commit()
    return api_response("success", "Pengalaman berhasil diupdate.", data=_serialize_experience(exp))


@admin_bp.route("/experiences/<int:exp_id>", methods=["DELETE"])
@login_required
def delete_experience(exp_id):
    """Hapus pengalaman berdasarkan ID."""
    exp = Experience.query.get(exp_id)
    if not exp or exp.user_id != current_user.id:
        return api_response("error", "Pengalaman tidak ditemukan.", status_code=404)

    db.session.delete(exp)
    db.session.commit()
    return api_response("success", f"Pengalaman '{exp.posisi}' berhasil dihapus.")
