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
    print("FAILED TO INITIALIZE FLASK APP:")
    traceback.print_exc(file=sys.stdout)
    raise e

if __name__ == "__main__":
    app.run(debug=True)
