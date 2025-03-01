from flask import Flask, jsonify
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)

@app.route("/status", methods=["GET"])
def status():
    logging.debug("Получен запрос на проверку статуса сервера")
    return jsonify({"status": "ok", "message": "Сервер работает"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
