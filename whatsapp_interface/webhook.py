from flask import Flask, request, jsonify
from processors import MessageProcessor

app = Flask(__name__)

message_processor = MessageProcessor()


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message_processor.process(data)
    return jsonify({"status": "OK"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
