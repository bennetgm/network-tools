from flask import Flask, render_template, jsonify
from monitor import poll_all
import threading, time

app = Flask(__name__)
cache = []

def background_poll():
    global cache
    while True:
        cache = poll_all()
        time.sleep(5)   # poll every 5 seconds

@app.route("/")
def dashboard():
    return render_template("dashboard.html", devices=cache)

@app.route("/data")
def data():
    return jsonify(cache)

if __name__ == "__main__":
    t = threading.Thread(target=background_poll, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5050, debug=True)