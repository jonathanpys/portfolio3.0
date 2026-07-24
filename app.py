"""
app.py — Entry point aplikasi Flask.

Jalankan dengan:
    flask run --debug
atau:
    python app.py
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
