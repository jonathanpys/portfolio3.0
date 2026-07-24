"""
app.py — Entry point aplikasi Flask.

Jalankan dengan:
    flask run --debug
atau:
    python app.py
"""
from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
