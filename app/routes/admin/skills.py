"""
Admin routes: Skills — CRUD API untuk keahlian.

Endpoints:
    GET    /admin/skills              → List semua skill
    GET    /admin/skills/<id>         → Detail skill
    POST   /admin/skills              → Buat skill baru
    PUT    /admin/skills/<id>         → Update skill
    DELETE /admin/skills/<id>         → Hapus skill
"""
from flask import request
from flask_login import login_required, current_user
from . import admin_bp
from app.extensions import db
from app.models import Skill
from app.utils import api_response
from app.services.cloudinary_service import validate_and_upload_image


def _serialize_skill(s):
    """Convert Skill model ke dict."""
    return {
        "id": s.id,
        "user_id": s.user_id,
        "nama_skill": s.nama_skill,
        "icon_class": s.icon_class,
    }


@admin_bp.route("/skills", methods=["GET"])
@login_required
def list_skills():
    """List semua skill milik user yang login."""
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    data = [_serialize_skill(s) for s in skills]
    return api_response("success", f"Ditemukan {len(data)} skill.", data=data)


@admin_bp.route("/skills/<int:skill_id>", methods=["GET"])
@login_required
def get_skill(skill_id):
    """Detail skill berdasarkan ID."""
    skill = Skill.query.get(skill_id)
    if not skill or skill.user_id != current_user.id:
        return api_response("error", "Skill tidak ditemukan.", status_code=404)
    return api_response("success", "Detail skill.", data=_serialize_skill(skill))


@admin_bp.route("/skills", methods=["POST"])
@login_required
def create_skill():
    """
    Buat skill baru.
    Mendukung JSON atau multipart/form-data.
    Upload gambar: key 'icon'
    """
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    nama_skill = (data.get("nama_skill") or "").strip()
    if not nama_skill:
        return api_response("error", "Field 'nama_skill' wajib diisi.", status_code=400)

    if len(nama_skill) > 50:
        return api_response("error", "Field 'nama_skill' maksimal 50 karakter.", status_code=400)

    icon_class = (data.get("icon_class") or "").strip() or None

    # Handle image upload if provided (bisa digunakan untuk icon berupa gambar custom)
    file = request.files.get("icon")
    if file and file.filename:
        url, err = validate_and_upload_image(file, folder="portfolio/skills")
        if err:
            return api_response("error", err, status_code=400)
        icon_class = url

    skill = Skill(
        user_id=current_user.id,
        nama_skill=nama_skill,
        icon_class=icon_class,
    )

    db.session.add(skill)
    db.session.commit()

    return api_response("success", "Skill berhasil ditambahkan.",
                        data=_serialize_skill(skill), status_code=201)


@admin_bp.route("/skills/<int:skill_id>", methods=["PUT"])
@login_required
def update_skill(skill_id):
    """
    Update skill berdasarkan ID.
    Mendukung JSON atau multipart/form-data.
    Upload gambar: key 'icon'
    """
    skill = Skill.query.get(skill_id)
    if not skill or skill.user_id != current_user.id:
        return api_response("error", "Skill tidak ditemukan.", status_code=404)

    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    if "nama_skill" in data:
        nama_skill = (data["nama_skill"] or "").strip()
        if not nama_skill:
            return api_response("error", "Field 'nama_skill' tidak boleh kosong.", status_code=400)
        if len(nama_skill) > 50:
            return api_response("error", "Field 'nama_skill' maksimal 50 karakter.", status_code=400)
        skill.nama_skill = nama_skill

    if "icon_class" in data:
        skill.icon_class = (data["icon_class"] or "").strip() or None

    # Handle image upload if provided
    file = request.files.get("icon")
    if file and file.filename:
        url, err = validate_and_upload_image(file, folder="portfolio/skills")
        if err:
            return api_response("error", err, status_code=400)
        skill.icon_class = url

    db.session.commit()
    return api_response("success", "Skill berhasil diupdate.", data=_serialize_skill(skill))


@admin_bp.route("/skills/<int:skill_id>", methods=["DELETE"])
@login_required
def delete_skill(skill_id):
    """Hapus skill berdasarkan ID."""
    skill = Skill.query.get(skill_id)
    if not skill or skill.user_id != current_user.id:
        return api_response("error", "Skill tidak ditemukan.", status_code=404)

    db.session.delete(skill)
    db.session.commit()
    return api_response("success", f"Skill '{skill.nama_skill}' berhasil dihapus.")
