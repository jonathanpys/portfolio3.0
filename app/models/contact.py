"""
Model: Contact — Mapping ke tabel `contacts`.
"""
from app.extensions import db

class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subjek = db.Column(db.String(150), nullable=False)
    pesan = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="unread")
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Contact id={self.id} nama={self.nama!r}>"
