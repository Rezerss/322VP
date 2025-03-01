import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Ключ шифрования (должен быть одинаковым на клиенте и сервере)
KEY = b"erik322xyesos"

def encrypt(data):
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))

def decrypt(data):
    cipher = AES.new(KEY, AES.MODE_ECB)
    return unpad(cipher.decrypt(data), AES.block_size)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(1)
    print("Сервер запущен. Ожидание подключения...")

    client_socket, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # Расшифровываем данные
        decrypted_data = decrypt(data)
        print(f"Получено: {decrypted_data.decode()}")

        # Шифруем ответ
        response = encrypt(b"Hello from server!")
        client_socket.send(response)

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()
