import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from the Container Failure Lab\n"

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port)