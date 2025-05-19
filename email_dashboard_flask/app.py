from flask import Flask, render_template, request
from mail_agents.email_ingestion import fetch_support_threads  # your working script

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    limit = int(request.args.get("limit", 10))
    threads = fetch_support_threads(limit=limit)
    return render_template("index.html", threads=threads, limit=limit)

if __name__ == "__main__":
    app.run(debug=True)
