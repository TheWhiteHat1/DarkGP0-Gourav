from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "message": "Enter Instagram username to get info 🚀"
    })

@app.route('/lookup', methods=['GET'])
def lookup():
    username = request.args.get('iginfo', '').strip()

    # Validate Instagram username (letters, numbers, dots, underscores)
    if not re.fullmatch(r'[A-Za-z0-9._]{1,30}', username):
        return jsonify({"error": "Please provide a valid Instagram username"}), 400

    upstream_url = f"https://info.taitanx.workers.dev/?iginfo={username}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; InstaInfoProxy/1.0)",
            "Accept": "application/json"
        }

        # Request to upstream
        resp = requests.get(upstream_url, headers=headers, timeout=15, verify=True)

        # Forward the response as-is
        return (resp.text, resp.status_code, {"Content-Type": "application/json"})

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to connect to upstream API",
            "details": str(e)
        }), 502


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
