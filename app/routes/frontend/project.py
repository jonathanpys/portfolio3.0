"""
Blueprint: Project — Endpoint publik untuk data proyek (read-only).

Endpoints:
    GET /api/projects  → List semua proyek
"""
from flask import Blueprint
from app.models import Project
from app.utils import api_response

project_bp = Blueprint("project", __name__)


@project_bp.route("/api/projects")
def get_projects():
    """API publik: Ambil semua proyek."""
    projects = Project.query.order_by(Project.created_at.desc()).all()
    data = [{
        "id": p.id,
        "judul": p.judul,
        "deskripsi": p.deskripsi,
        "gambar_url": p.gambar_url,
        "link_project": p.link_project,
        "link_youtube": p.link_youtube,
    } for p in projects]
    return api_response("success", f"Ditemukan {len(data)} proyek.", data=data)
