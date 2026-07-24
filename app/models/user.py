"""
Model: User — Mapping ke tabel `users` yang sudah ada di TiDB.

Struktur tabel:
    CREATE TABLE users (
        id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        username      VARCHAR(50) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        role          VARCHAR(10) NOT NULL,
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # ── Relationship ──────────────────────────────────────────
    profile = db.relationship("Profile", back_populates="user", uselist=False,
                              cascade="all, delete-orphan")

    # ── Password helpers ──────────────────────────────────────
    def set_password(self, password):
        """Hash password dan simpan ke password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifikasi password terhadap hash yang tersimpan."""
        # Support plain-text password yang sudah ada di DB (legacy)
        if not self.password_hash.startswith(("pbkdf2:", "scrypt:")):
            return self.password_hash == password
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r} role={self.role!r}>"
