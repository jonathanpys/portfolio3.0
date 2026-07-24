from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Create certificates table
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS certificates (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                judul VARCHAR(100) NOT NULL,
                penerbit VARCHAR(100) NOT NULL,
                tanggal_terbit DATE,
                link_kredensial VARCHAR(255),
                gambar_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """))
        # Add column if not exists
        # Add column if not exists
        db.session.execute(text("ALTER TABLE experiences ADD COLUMN kategori VARCHAR(50) DEFAULT 'pekerjaan';"))
        db.session.commit()
        print("Table 'experiences' checked/created successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error checking/creating table: {e}")
