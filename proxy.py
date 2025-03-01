from flask import Flask, request, Response
import requests

app = Flask(__name__)

# Основной маршрут для прокси
@app.route('/', defaults={'path': ''}, methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
@app.route('/<path:path>', methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def proxy(path):
    # Целевой сайт, на который будут перенаправляться запросы
    target_url = f"https://{path}" if path else "https://three22vp.onrender.com/"  # Замените example.com на нужный сайт

    # Перенаправляем запрос на целевой сайт
    try:
        # Получаем данные от клиента
        headers = {key: value for (key, value) in request.headers if key != 'Host'}
        data = request.get_data()
        params = request.args

        # Отправляем запрос на целевой сайт
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=data,
            params=params,
            stream=True
        )

        # Возвращаем ответ клиенту
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    except Exception as e:
        return str(e), 500

# Запуск сервера
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
