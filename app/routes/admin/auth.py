"""
Admin routes: Auth — Login / Logout via JSON API.

Endpoints:
    GET  /admin/login   → Render Halaman Login HTML
    POST /admin/login   → Login (JSON body: username, password)
    POST /admin/logout  → Logout
"""
from flask import request, render_template, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import admin_bp
from app.extensions import login_manager
from app.models import User
from app.utils import api_response


# ── Flask-Login: user_loader callback ─────────────────────────
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID untuk Flask-Login session."""
    return User.query.get(int(user_id))


# ── Unauthorized handler (return JSON bukan redirect HTML) ────
@login_manager.unauthorized_handler
def unauthorized():
    """
    Jika request expects JSON (API), return 401.
    Jika request browser biasa, redirect ke login.
    """
    if request.headers.get("Accept") == "application/json" or request.path.startswith("/admin/profiles") or request.path.startswith("/admin/skills") or request.path.startswith("/admin/projects") or request.path.startswith("/admin/experiences"):
        return api_response("error", "Login diperlukan untuk mengakses endpoint ini.", status_code=401)
    
    return redirect(url_for("admin.login"))


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    GET: Render HTML Login
    POST: Login admin via JSON
    """
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("admin.dashboard"))
        return render_template("admin/login.html")

    # Jika sudah login
    if current_user.is_authenticated:
        return api_response("success", "Sudah login.", data={
            "user": {"id": current_user.id, "username": current_user.username}
        })

    data = request.get_json(silent=True)
    if not data:
        return api_response("error", "Request body harus JSON.", status_code=400)

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        return api_response("error", "Username dan password wajib diisi.", status_code=400)

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return api_response("error", "Username atau password salah.", status_code=401)

    login_user(user)
    return api_response("success", f"Login berhasil. Selamat datang, {user.username}!", data={
        "user": {"id": user.id, "username": user.username, "role": user.role}
    })


@admin_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Proses logout admin."""
    logout_user()
    return api_response("success", "Berhasil logout.")
