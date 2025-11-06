from flask import Flask, request, jsonify, Response
import requests
import re
import os

app = Flask(__name__)

# helper: forward to upstream and return response
def forward_iginfo(username):
    upstream_url = f"https://info.taitanx.workers.dev/?iginfo={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; InstaInfoProxy/1.0)",
        "Accept": "application/json"
    }
    try:
        resp = requests.get(upstream_url, headers=headers, timeout=15, verify=True)
        # forward body and status code and content-type
        content_type = resp.headers.get("Content-Type", "application/json")
        return Response(resp.content, status=resp.status_code, content_type=content_type)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to connect to upstream API", "details": str(e)}), 502

@app.route('/', methods=['GET'])
def home():
    # If iginfo param present at root, forward it
    username = request.args.get('iginfo', '').strip()
    if username:
        # validate instagram username
        if not re.fullmatch(r'[A-Za-z0-9._]{1,30}', username):
            return jsonify({"error": "Please provide a valid Instagram username"}), 400
        return forward_iginfo(username)

    # otherwise show the normal message
    return jsonify({
        "status": "ok",
        "message": "Enter Instagram username to get info 🚀\nUse /lookup?iginfo=<username> or /?iginfo=<username>"
    })

@app.route('/lookup', methods=['GET'])
def lookup():
    username = request.args.get('iginfo', '').strip()
    if not username:
        return jsonify({"error": "Please provide iginfo query parameter, e.g. ?iginfo=gouravparajapt"}), 400

    # Validate Instagram username (letters, numbers, dots, underscores, upto 30 chars)
    if not re.fullmatch(r'[A-Za-z0-9._]{1,30}', username):
        return jsonify({"error": "Please provide a valid Instagram username"}), 400

    return forward_iginfo(username)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
