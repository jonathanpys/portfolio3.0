"""
app.py — Entry point aplikasi Flask.

Jalankan dengan:
    flask run --debug
atau:
    python app.py
"""
from flask import Flask

# Dummy app untuk mengelabui Vercel AST Parser dan menangkap error
app = Flask(__name__)

try:
    from app import create_app
    app = create_app()
except Exception as e:
    import traceback
    error_msg = traceback.format_exc()
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return f"<h1>Failed to initialize Flask App</h1><pre>{error_msg}</pre>", 500

if __name__ == "__main__":
    app.run(debug=True)
