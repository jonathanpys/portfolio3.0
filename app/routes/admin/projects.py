"""
Admin routes: Projects — CRUD API untuk proyek.

Endpoints:
    GET    /admin/projects              → List semua proyek
    GET    /admin/projects/<id>         → Detail proyek
    POST   /admin/projects              → Buat proyek baru
    PUT    /admin/projects/<id>         → Update proyek
    DELETE /admin/projects/<id>         → Hapus proyek
"""
from flask import request
from flask_login import login_required, current_user
from . import admin_bp
from app.extensions import db
from app.models import Project
from app.utils import api_response
from app.services.cloudinary_service import validate_and_upload_image


def _serialize_project(p):
    """Convert Project model ke dict."""
    return {
        "id": p.id,
        "user_id": p.user_id,
        "judul": p.judul,
        "deskripsi": p.deskripsi,
        "gambar_url": p.gambar_url,
        "link_project": p.link_project,
        "link_youtube": p.link_youtube,
        "created_at": str(p.created_at) if p.created_at else None,
    }


@admin_bp.route("/projects", methods=["GET"])
@login_required
def list_projects():
    """List semua proyek milik user yang login."""
    projects = Project.query.filter_by(user_id=current_user.id) \
        .order_by(Project.created_at.desc()).all()
    data = [_serialize_project(p) for p in projects]
    return api_response("success", f"Ditemukan {len(data)} proyek.", data=data)


@admin_bp.route("/projects/<int:project_id>", methods=["GET"])
@login_required
def get_project(project_id):
    """Detail proyek berdasarkan ID."""
    project = Project.query.get(project_id)
    if not project or project.user_id != current_user.id:
        return api_response("error", "Proyek tidak ditemukan.", status_code=404)
    return api_response("success", "Detail proyek.", data=_serialize_project(project))


@admin_bp.route("/projects", methods=["POST"])
@login_required
def create_project():
    """
    Buat proyek baru.
    Mendukung JSON atau multipart/form-data.
    Upload gambar: key 'gambar'
    """
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    judul = (data.get("judul") or "").strip()
    if not judul:
        return api_response("error", "Field 'judul' wajib diisi.", status_code=400)
    if len(judul) > 100:
        return api_response("error", "Field 'judul' maksimal 100 karakter.", status_code=400)

    gambar_url = (data.get("gambar_url") or "").strip() or None
    
    # Handle image upload if provided
    file = request.files.get("gambar")
    if file and file.filename:
        url, err = validate_and_upload_image(file, folder="portfolio/projects")
        if err:
            return api_response("error", err, status_code=400)
        gambar_url = url

    project = Project(
        user_id=current_user.id,
        judul=judul,
        deskripsi=(data.get("deskripsi") or "").strip() or None,
        gambar_url=gambar_url,
        link_project=(data.get("link_project") or "").strip() or None,
        link_youtube=(data.get("link_youtube") or "").strip() or None,
    )

    db.session.add(project)
    db.session.commit()

    return api_response("success", "Proyek berhasil ditambahkan.",
                        data=_serialize_project(project), status_code=201)


@admin_bp.route("/projects/<int:project_id>", methods=["PUT"])
@login_required
def update_project(project_id):
    """
    Update proyek berdasarkan ID.
    Mendukung JSON atau multipart/form-data.
    Upload gambar: key 'gambar'
    """
    project = Project.query.get(project_id)
    if not project or project.user_id != current_user.id:
        return api_response("error", "Proyek tidak ditemukan.", status_code=404)

    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict()

    if "judul" in data:
        judul = (data["judul"] or "").strip()
        if not judul:
            return api_response("error", "Field 'judul' tidak boleh kosong.", status_code=400)
        if len(judul) > 100:
            return api_response("error", "Field 'judul' maksimal 100 karakter.", status_code=400)
        project.judul = judul

    if "deskripsi" in data:
        project.deskripsi = (data["deskripsi"] or "").strip() or None

    if "link_project" in data:
        project.link_project = (data["link_project"] or "").strip() or None

    if "link_youtube" in data:
        project.link_youtube = (data["link_youtube"] or "").strip() or None

    # Update URL explicitly via JSON/Form text
    if "gambar_url" in data:
        project.gambar_url = (data["gambar_url"] or "").strip() or None

    # Handle image upload if provided
    file = request.files.get("gambar")
    if file and file.filename:
        url, err = validate_and_upload_image(file, folder="portfolio/projects")
        if err:
            return api_response("error", err, status_code=400)
        project.gambar_url = url

    db.session.commit()
    return api_response("success", "Proyek berhasil diupdate.", data=_serialize_project(project))


@admin_bp.route("/projects/<int:project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id):
    """Hapus proyek berdasarkan ID."""
    project = Project.query.get(project_id)
    if not project or project.user_id != current_user.id:
        return api_response("error", "Proyek tidak ditemukan.", status_code=404)

    # TODO: Bisa tambahkan cloudinary_service.delete_image(public_id) jika mau
    
    db.session.delete(project)
    db.session.commit()
    return api_response("success", f"Proyek '{project.judul}' berhasil dihapus.")
