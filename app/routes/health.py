"""
Blueprint: Health Check — Tes koneksi database.

Endpoint:
    GET /health-db  → Cek koneksi ke TiDB + info tabel & jumlah row.
"""
from flask import Blueprint, jsonify
from app.extensions import db
from app.models import User, Profile, Skill, Experience, Project
from sqlalchemy import text

health_bp = Blueprint("health", __name__)


@health_bp.route("/health-db")
def health_db():
    """
    Health check endpoint untuk memastikan koneksi ke TiDB berhasil.

    Response JSON:
        - status: "ok" atau "error"
        - database: nama database
        - tidb_version: versi TiDB server
        - tables: daftar tabel + jumlah row
        - sample_user: contoh data user pertama (jika ada)
    """
    try:
        # 1. Tes koneksi dasar — SELECT 1
        db.session.execute(text("SELECT 1"))

        # 2. Ambil info database
        result = db.session.execute(text("SELECT DATABASE()"))
        db_name = result.scalar()

        # 3. Ambil versi TiDB
        result = db.session.execute(text("SELECT VERSION()"))
        version = result.scalar()

        # 4. Hitung row di setiap tabel yang sudah di-mapping
        user_count = db.session.query(User).count()
        profile_count = db.session.query(Profile).count()
        skill_count = db.session.query(Skill).count()
        experience_count = db.session.query(Experience).count()
        project_count = db.session.query(Project).count()

        # 5. Ambil sample user (tanpa password_hash)
        sample_user = None
        first_user = db.session.query(User).first()
        if first_user:
            sample_user = {
                "id": first_user.id,
                "username": first_user.username,
                "role": first_user.role,
                "created_at": str(first_user.created_at),
            }

        return jsonify({
            "status": "ok",
            "database": db_name,
            "tidb_version": version,
            "tables": {
                "users": {"row_count": user_count},
                "profiles": {"row_count": profile_count},
                "skills": {"row_count": skill_count},
                "experiences": {"row_count": experience_count},
                "projects": {"row_count": project_count},
            },
            "sample_user": sample_user,
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 500
