from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)

@app.route('/')
def home():
    username = request.args.get('iginfo', '').strip()
    if username:
        return lookup_internal(username)

    return jsonify({
        "status": "ok",
        "message": "Enter Instagram username to get info 🚀\nExample: /?iginfo=gouravparajapt"
    })

@app.route('/lookup', methods=['GET'])
def lookup():
    username = request.args.get('iginfo', '').strip()
    if not username:
        return jsonify({"error": "Please provide ?iginfo=<username>"}), 400
    return lookup_internal(username)


def lookup_internal(username):
    # Validate Instagram username
    if not re.fullmatch(r'[A-Za-z0-9._]{1,30}', username):
        return jsonify({"error": "Please provide a valid Instagram username"}), 400

    upstream_url = f"https://info.taitanx.workers.dev/?iginfo={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; InstaInfoProxy/1.0)",
        "Accept": "application/json"
    }

    try:
        resp = requests.get(upstream_url, headers=headers, timeout=15, verify=True)

        # Try to parse JSON from upstream
        try:
            data = resp.json()
        except Exception:
            return jsonify({"error": "Invalid response from upstream"}), 502

        # ✅ Add your credit lines
        data["credit"] = "gourav @darkgp0"
        data["developer"] = "gourav @darkgp0"

        return jsonify(data), resp.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Failed to connect to upstream API",
            "details": str(e)
        }), 502


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
