"""
Model: Certificate — Mapping ke tabel `certificates`
"""
from app.extensions import db

class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    judul = db.Column(db.String(100), nullable=False)
    penerbit = db.Column(db.String(100), nullable=False)
    tanggal_terbit = db.Column(db.Date, nullable=True)
    link_kredensial = db.Column(db.String(255), nullable=True)
    gambar_url = db.Column(db.String(255), nullable=True)
    icon_penerbit_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    # ── Relationship ──────────────────────────────────────────
    user = db.relationship("User", backref=db.backref("certificates", lazy="dynamic"))

    def __repr__(self):
        return f"<Certificate id={self.id} judul={self.judul!r}>"
