"""
Model: Profile — Mapping ke tabel `profiles` yang sudah ada di TiDB.

Struktur tabel:
    CREATE TABLE profiles (
        id              INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        user_id         INT NOT NULL,
        nama_lengkap    VARCHAR(100),
        nama_panggilan  VARCHAR(50),
        tempat_lahir    VARCHAR(50),
        tanggal_lahir   DATE,
        email           VARCHAR(100),
        telepon         VARCHAR(20),
        universitas     VARCHAR(100),
        fakultas        VARCHAR(100),
        prodi           VARCHAR(100),
        semester        VARCHAR(20),
        alamat          VARCHAR(4000),
        foto_url        VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
"""
from app.extensions import db


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    nama_lengkap = db.Column(db.String(100), nullable=True)
    nama_panggilan = db.Column(db.String(50), nullable=True)
    tempat_lahir = db.Column(db.String(50), nullable=True)
    tanggal_lahir = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    telepon = db.Column(db.String(20), nullable=True)
    universitas = db.Column(db.String(100), nullable=True)
    fakultas = db.Column(db.String(100), nullable=True)
    prodi = db.Column(db.String(100), nullable=True)
    semester = db.Column(db.String(20), nullable=True)
    alamat = db.Column(db.String(4000), nullable=True)
    foto_url = db.Column(db.String(255), nullable=True)
    foto_tentang_url = db.Column(db.String(255), nullable=True)
    deskripsi = db.Column(db.Text, nullable=True)

    # ── Relationship ──────────────────────────────────────────
    user = db.relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<Profile id={self.id} nama={self.nama_lengkap!r}>"
