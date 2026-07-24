from flask import Flask
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return "<h1>Hello from Vercel!</h1><p>If you see this, the Vercel runtime is working correctly.</p>"

if __name__ == "__main__":
    app.run(debug=True)
