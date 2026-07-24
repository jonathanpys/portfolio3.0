"""
Model: Skill — Mapping ke tabel `skills` yang sudah ada di TiDB.

Struktur tabel:
    CREATE TABLE skills (
        id          INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        user_id     INT NOT NULL,
        nama_skill  VARCHAR(50) NOT NULL,
        icon_class  VARCHAR(50),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
"""
from app.extensions import db


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    nama_skill = db.Column(db.String(50), nullable=False)
    icon_class = db.Column(db.String(255), nullable=True)

    # ── Relationship ──────────────────────────────────────────
    user = db.relationship("User", backref=db.backref("skills", lazy="dynamic"))

    def __repr__(self):
        return f"<Skill id={self.id} nama={self.nama_skill!r}>"
