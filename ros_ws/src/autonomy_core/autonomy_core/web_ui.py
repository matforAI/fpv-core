from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify({"status":"ok"})

@app.route("/start")
def start():
    return "MISSION START"

@app.route("/rth")
def rth():
    return "RETURN HOME"

app.run(host="0.0.0.0", port=8080)
