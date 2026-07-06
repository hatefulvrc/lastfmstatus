from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def get_status():
    try:
        with open("status.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Data not available yet"}), 503

if __name__ == '__main__':
    app.run(port=5000)
