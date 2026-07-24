"""
Model: Experience — Mapping ke tabel `experiences` yang sudah ada di TiDB.

Struktur tabel:
    CREATE TABLE experiences (
        id          INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        user_id     INT NOT NULL,
        posisi      VARCHAR(100) NOT NULL,
        perusahaan  VARCHAR(100) NOT NULL,
        durasi      VARCHAR(50),
        deskripsi   VARCHAR(4000),
        created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
"""
from app.extensions import db


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    posisi = db.Column(db.String(100), nullable=False)
    perusahaan = db.Column(db.String(100), nullable=False)
    durasi = db.Column(db.String(50), nullable=True)
    deskripsi = db.Column(db.String(4000), nullable=True)
    kategori = db.Column(db.String(50), nullable=False, server_default='pekerjaan')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # ── Relationship ──────────────────────────────────────────
    user = db.relationship("User", backref=db.backref("experiences", lazy="dynamic"))

    def __repr__(self):
        return f"<Experience id={self.id} posisi={self.posisi!r}>"
