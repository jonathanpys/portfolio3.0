"""
app/extensions.py — Inisialisasi extension Flask (lazy init).

Extension dibuat di sini supaya bisa di-import dari mana saja
tanpa circular import.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# ── Database ──────────────────────────────────────────────────
db = SQLAlchemy()

# ── Auth ──────────────────────────────────────────────────────
login_manager = LoginManager()
login_manager.login_view = "admin.login"         # redirect kalau belum login
login_manager.login_message = "Silakan login terlebih dahulu."
login_manager.login_message_category = "warning"
