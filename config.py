"""
config.py — Konfigurasi aplikasi Flask.

Membaca semua variabel dari file .env via os.getenv().
"""
import os
import ssl
from datetime import timedelta
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Muat .env dari root project
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Config:
    """Base configuration — dipakai di semua environment."""

    # ── Flask Core ────────────────────────────────────────────
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")

    # ── Session ───────────────────────────────────────────────
    # Session berlaku 10 menit sejak aktivitas terakhir (sliding window).
    # Setiap request akan me-refresh timer ini.
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)
    SESSION_COOKIE_HTTPONLY = True      # cookie tidak bisa diakses JS
    SESSION_COOKIE_SAMESITE = "Lax"     # proteksi CSRF dasar

    # ── Database (TiDB / MySQL via PyMySQL) ───────────────────
    _TIDB_HOST = os.getenv("TIDB_HOST", "localhost")
    _TIDB_PORT = os.getenv("TIDB_PORT", "4000")
    _TIDB_USER = os.getenv("TIDB_USER", "root")
    _TIDB_PASSWORD = os.getenv("TIDB_PASSWORD", "")
    _TIDB_DATABASE = os.getenv("TIDB_DATABASE", "portfolio")
    _TIDB_SSL_CA = os.getenv("TIDB_SSL_CA", "")

    # URI dasar (tanpa SSL query string — SSL dikonfigurasi via connect_args)
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{_TIDB_USER}:{_TIDB_PASSWORD}"
        f"@{_TIDB_HOST}:{_TIDB_PORT}/{_TIDB_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SSL connect_args untuk TiDB Cloud
    # PyMySQL memerlukan ssl context object, bukan hanya path string
    # SSL + connection pool settings untuk TiDB Cloud
    # - pool_recycle: daur ulang koneksi tiap 300 detik (TiDB Cloud tutup idle ~5 menit)
    # - pool_pre_ping: cek koneksi masih hidup sebelum dipakai
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    if _TIDB_SSL_CA:
        cert_path = os.path.join(BASE_DIR, _TIDB_SSL_CA) if not os.path.isabs(_TIDB_SSL_CA) else _TIDB_SSL_CA
        if os.path.exists(cert_path):
            _ssl_ctx = ssl.create_default_context(cafile=cert_path)
            SQLALCHEMY_ENGINE_OPTIONS["connect_args"] = {"ssl": _ssl_ctx}
        else:
            print(f"WARNING: SSL CA file not found at {cert_path}")

    # ── Cloudinary ────────────────────────────────────────────
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

    # ── Resend (Email) ────────────────────────────────────────
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
    RESEND_SENDER = os.getenv("RESEND_SENDER") or "onboarding@resend.dev"
    RESEND_SENDER_NAME = os.getenv("RESEND_SENDER_NAME") or "Portfolio"

    # ── Misc ──────────────────────────────────────────────────
    OWNER_EMAIL = os.getenv("OWNER_EMAIL", "")

    # ── Admin Seed (untuk script seed_admin.py) ───────────────
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
