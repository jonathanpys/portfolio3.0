"""
app.py — Entry point aplikasi Flask.

Jalankan dengan:
    flask run --debug
atau:
    python app.py
"""
import sys
import traceback

def initialize_app():
    try:
        from app import create_app
        return create_app()
    except Exception as e:
        from flask import Flask
        dummy_app = Flask(__name__)
        error_msg = traceback.format_exc()
        
        @dummy_app.route('/', defaults={'path': ''})
        @dummy_app.route('/<path:path>')
        def catch_all(path):
            return f"<h1>Failed to initialize Flask App</h1><pre>{error_msg}</pre>", 500
        return dummy_app

app = initialize_app()

if __name__ == "__main__":
    app.run(debug=True)
