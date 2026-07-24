"""
Admin routes: Dashboard — Halaman utama admin panel.
"""
from flask import render_template
from flask_login import login_required
from . import admin_bp


@admin_bp.route("/")
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    """Halaman dashboard admin SPA."""
    return render_template("admin/dashboard.html")
