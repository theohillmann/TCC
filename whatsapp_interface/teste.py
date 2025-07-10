from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    process_message(data)
    return jsonify({"status": "OK"}), 200


def process_message(message):
    print(message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
