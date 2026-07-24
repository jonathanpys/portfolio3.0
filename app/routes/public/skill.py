"""
Blueprint: Skill — Endpoint publik untuk data keahlian (read-only).

Endpoints:
    GET /api/skills  → List semua skill
"""
from flask import Blueprint
from app.models import Skill
from app.utils import api_response

skill_bp = Blueprint("skill", __name__)


@skill_bp.route("/api/skills")
def get_skills():
    """API publik: Ambil semua skill."""
    skills = Skill.query.all()
    data = [{
        "id": s.id,
        "nama_skill": s.nama_skill,
        "icon_class": s.icon_class,
    } for s in skills]
    return api_response("success", f"Ditemukan {len(data)} skill.", data=data)
