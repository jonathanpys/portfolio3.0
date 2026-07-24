"""
app.py — Entry point aplikasi Flask.

Jalankan dengan:
    flask run --debug
atau:
    python app.py
"""
import sys
import traceback

try:
    from app import create_app
    app = create_app()
except Exception as e:
    from flask import Flask
    app = Flask(__name__)
    error_msg = traceback.format_exc()
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return f"<h1>Failed to initialize Flask App</h1><pre>{error_msg}</pre>", 500

if __name__ == "__main__":
    app.run(debug=True)
