"""
Model: Project — Mapping ke tabel `projects` yang sudah ada di TiDB.

Struktur tabel:
    CREATE TABLE projects (
        id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        user_id       INT NOT NULL,
        judul         VARCHAR(100) NOT NULL,
        deskripsi     VARCHAR(4000),
        gambar_url    VARCHAR(255),
        link_project  VARCHAR(255),
        link_youtube  VARCHAR(255),
        created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
"""
from app.extensions import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    judul = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.String(4000), nullable=True)
    gambar_url = db.Column(db.String(255), nullable=True)
    link_project = db.Column(db.String(255), nullable=True)
    link_youtube = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # ── Relationship ──────────────────────────────────────────
    user = db.relationship("User", backref=db.backref("projects", lazy="dynamic"))

    def __repr__(self):
        return f"<Project id={self.id} judul={self.judul!r}>"
