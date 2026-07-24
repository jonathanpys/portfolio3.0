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
    
    original_wsgi_app = app.wsgi_app
    
    class DebugMiddleware:
        def __init__(self, wsgi_app):
            self.wsgi_app = wsgi_app
            
        def __call__(self, environ, start_response):
            try:
                return self.wsgi_app(environ, start_response)
            except Exception as e:
                import traceback
                error_msg = traceback.format_exc()
                status = '500 Internal Server Error'
                headers = [('Content-Type', 'text/html; charset=utf-8')]
                start_response(status, headers)
                return [f"<h1>Runtime Error</h1><pre>{error_msg}</pre>".encode('utf-8')]
                
    app.wsgi_app = DebugMiddleware(original_wsgi_app)
    
except Exception as e:
    import traceback
    error_msg = traceback.format_exc()
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return f"<h1>Failed to initialize Flask App</h1><pre>{error_msg}</pre>", 500

if __name__ == "__main__":
    app.run(debug=True)
