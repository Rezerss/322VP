from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Подключение к SQLite
conn = sqlite3.connect('chat.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы для сообщений
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    channel TEXT NOT NULL,
    user TEXT NOT NULL,
    text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/messages/<channel>')
def get_messages(channel):
    cursor.execute('SELECT user, text, timestamp FROM messages WHERE channel = ? ORDER BY timestamp', (channel,))
    messages = cursor.fetchall()
    return jsonify(messages)

@socketio.on('sendMessage')
def handle_send_message(data):
    channel = data['channel']
    user = data['user']
    text = data['text']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Сохраняем сообщение в базу данных
    cursor.execute('INSERT INTO messages (channel, user, text) VALUES (?, ?, ?)', (channel, user, text))
    conn.commit()

    # Отправляем сообщение всем подключённым клиентам
    send({
        'channel': channel,
        'user': user,
        'text': text,
        'timestamp': timestamp
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
