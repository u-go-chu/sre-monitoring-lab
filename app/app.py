from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "status": "healthy",
        "message": "SRE Monitoring Lab API is running"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/api/test")
def test():
    return jsonify({
        "status": "success",
        "message": "API request received"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)