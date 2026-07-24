"""
Admin routes: Certificates — CRUD API untuk sertifikasi.
"""
from flask import request
from flask_login import login_required, current_user
from . import admin_bp
from app.extensions import db
from app.models import Certificate
from app.utils import api_response
from app.services.cloudinary_service import validate_and_upload_image


def _serialize_certificate(c):
    return {
        "id": c.id,
        "user_id": c.user_id,
        "judul": c.judul,
        "penerbit": c.penerbit,
        "tanggal_terbit": str(c.tanggal_terbit) if c.tanggal_terbit else None,
        "link_kredensial": c.link_kredensial,
        "gambar_url": c.gambar_url,
        "icon_penerbit_url": c.icon_penerbit_url,
        "created_at": str(c.created_at) if c.created_at else None,
    }


@admin_bp.route("/certificates", methods=["GET"])
@login_required
def list_certificates():
    certificates = Certificate.query.filter_by(user_id=current_user.id) \
        .order_by(Certificate.created_at.desc()).all()
    data = [_serialize_certificate(c) for c in certificates]
    return api_response("success", f"Ditemukan {len(data)} sertifikat.", data=data)


@admin_bp.route("/certificates/<int:cert_id>", methods=["GET"])
@login_required
def get_certificate(cert_id):
    c = Certificate.query.get(cert_id)
    if not c or c.user_id != current_user.id:
        return api_response("error", "Sertifikat tidak ditemukan.", status_code=404)
    return api_response("success", "Detail sertifikat.", data=_serialize_certificate(c))


@admin_bp.route("/certificates", methods=["POST"])
@login_required
def create_certificate():
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    judul = (data.get("judul") or "").strip()
    penerbit = (data.get("penerbit") or "").strip()
    if not judul or not penerbit:
        return api_response("error", "Field 'judul' dan 'penerbit' wajib diisi.", status_code=400)

    tanggal_terbit = None
    if data.get("tanggal_terbit"):
        from datetime import date as dt_date
        try:
            tanggal_terbit = dt_date.fromisoformat(data["tanggal_terbit"])
        except ValueError:
            return api_response("error", "Format 'tanggal_terbit' harus YYYY-MM-DD.", status_code=400)

    gambar_url = (data.get("gambar_url") or "").strip() or None
    file = request.files.get("gambar")
    if file and file.filename:
        url, err = validate_and_upload_image(file, folder="portfolio/certificates")
        if err:
            return api_response("error", err, status_code=400)
        gambar_url = url

    icon_penerbit_url = (data.get("icon_penerbit_url") or "").strip() or None
    icon_file = request.files.get("icon_penerbit")
    if icon_file and icon_file.filename:
        url, err = validate_and_upload_image(icon_file, folder="portfolio/certificates_icons")
        if err:
            return api_response("error", err, status_code=400)
        icon_penerbit_url = url

    c = Certificate(
        user_id=current_user.id,
        judul=judul,
        penerbit=penerbit,
        tanggal_terbit=tanggal_terbit,
        link_kredensial=(data.get("link_kredensial") or "").strip() or None,
        gambar_url=gambar_url,
        icon_penerbit_url=icon_penerbit_url
    )
    db.session.add(c)
    db.session.commit()

    return api_response("success", "Sertifikat berhasil dibuat.", data=_serialize_certificate(c), status_code=201)


@admin_bp.route("/certificates/<int:cert_id>", methods=["PUT"])
@login_required
def update_certificate(cert_id):
    c = Certificate.query.get(cert_id)
    if not c or c.user_id != current_user.id:
        return api_response("error", "Sertifikat tidak ditemukan.", status_code=404)

    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    if "judul" in data:
        val = (data["judul"] or "").strip()
        if not val:
            return api_response("error", "Field 'judul' tidak boleh kosong.", status_code=400)
        c.judul = val

    if "penerbit" in data:
        val = (data["penerbit"] or "").strip()
        if not val:
            return api_response("error", "Field 'penerbit' tidak boleh kosong.", status_code=400)
        c.penerbit = val

    if "tanggal_terbit" in data:
        if data["tanggal_terbit"]:
            from datetime import date as dt_date
            try:
                c.tanggal_terbit = dt_date.fromisoformat(data["tanggal_terbit"])
            except ValueError:
                return api_response("error", "Format 'tanggal_terbit' harus YYYY-MM-DD.", status_code=400)
        else:
            c.tanggal_terbit = None

    if "link_kredensial" in data:
        c.link_kredensial = (data["link_kredensial"] or "").strip() or None

    file = request.files.get("gambar")
    if file and file.filename:
        url, err = validate_and_upload_image(file, folder="portfolio/certificates")
        if err:
            return api_response("error", err, status_code=400)
        c.gambar_url = url
        
    icon_file = request.files.get("icon_penerbit")
    if icon_file and icon_file.filename:
        url, err = validate_and_upload_image(icon_file, folder="portfolio/certificates_icons")
        if err:
            return api_response("error", err, status_code=400)
        c.icon_penerbit_url = url

    db.session.commit()
    return api_response("success", "Sertifikat berhasil diupdate.", data=_serialize_certificate(c))


@admin_bp.route("/certificates/<int:cert_id>", methods=["DELETE"])
@login_required
def delete_certificate(cert_id):
    c = Certificate.query.get(cert_id)
    if not c or c.user_id != current_user.id:
        return api_response("error", "Sertifikat tidak ditemukan.", status_code=404)

    db.session.delete(c)
    db.session.commit()
    return api_response("success", "Sertifikat berhasil dihapus.")
