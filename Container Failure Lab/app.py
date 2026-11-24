import os
import sys
from flask import Flask

#Scanerio 1

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from the Container Failure Lab\n"

#Scanerio 2
# In this (DB_URL) setup, there isn't a separate database server running yet—DB_URL is just an environment variable your Flask app.py checks at startup to decide whether to exit with code 1 or start normally.

# db_url = os.environ.get("DB_URL")
# if not db_url:
#     print("ERROR: DB_URL environment variable is not set.", file=sys.stderr)
#     sys.exit(1)


if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "5000"))
    app.run(host=host, port=port)