"""
app/__init__.py — Application Factory.

Inisialisasi Flask app, load config, register extensions & blueprints.
"""
from flask import Flask, session
from app.extensions import db, login_manager

# ── Import Blueprints di Top-Level agar dideteksi Vercel AST Parser ──
from app.routes.health import health_bp
from app.routes.frontend.profile import profile_bp
from app.routes.frontend.skill import skill_bp
from app.routes.frontend.experience import experience_bp
from app.routes.frontend.project import project_bp
from app.routes.frontend.contact import contact_bp
from app.routes.frontend.certificate import certificate_bp
from app.routes.admin import admin_bp


def create_app():
    """Factory function untuk membuat instance Flask app."""
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
    )

    # ── Load configuration ────────────────────────────────────
    app.config.from_object("config.Config")

    # ── Initialize Cloudinary ─────────────────────────────────
    from app.services.cloudinary_service import init_cloudinary
    init_cloudinary(app)

    # ── Initialize extensions ─────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)

    # ── Session timeout (sliding window 10 menit) ─────────────
    @app.before_request
    def make_session_permanent():
        """
        Setiap request me-refresh session timer.

        Flask "permanent session" = session pakai PERMANENT_SESSION_LIFETIME
        sebagai batas waktu. Dengan me-set session.permanent = True di setiap
        request, timer di-reset (sliding window), sehingga session hanya
        expire jika user IDLE selama 10 menit tanpa aktivitas apapun.
        """
        session.permanent = True

    # ── Register blueprints ───────────────────────────────────
    _register_blueprints(app)

    # ── Import models agar SQLAlchemy tahu semua tabel ────────
    with app.app_context():
        import app.models  # noqa: F401

    return app


def _register_blueprints(app: Flask):
    """Register semua blueprint ke app."""
    # --- Health check ---
    app.register_blueprint(health_bp)

    # --- Public routes ---
    app.register_blueprint(profile_bp)
    app.register_blueprint(skill_bp)
    app.register_blueprint(experience_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(certificate_bp)

    # --- Admin routes ---
    app.register_blueprint(admin_bp)
