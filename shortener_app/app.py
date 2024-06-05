from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API_URL = "http://localhost:8000"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json['original_url']
    response = requests.post(f"{API_URL}/url", json={"target_url": original_url})
    if response.status_code == 200:
        data = response.json()
        return jsonify({"short_url": data["url"], "admin_url": data["admin_url"]})
    else:
        return jsonify({"error": response.json()['detail']}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
