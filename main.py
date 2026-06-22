import socket
from enum import StrEnum

HOST = "127.0.0.1"
PORT = 8080

class Method(StrEnum):
    GET = 'GET'
    POST = 'POST'

def request_about() -> str:
    body = "<!DOCTYPE html><html><body>Привет</body></html>".encode("utf-8")
    headers = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html; charset=utf-8\r\n"
    f"Content-Length: {len(body)}\r\n"
    "\r\n"
).encode("utf-8")
    response = headers + body
    return response

def read_full_body_post_method(data: bytes, conn, headers_end) -> bytes:
    body_start = headers_end + 4
    for header in data[:headers_end].split(b'\r\n'):
        if header.lower().startswith(b'content-length:'):
            content_size = int(header.split(b':', 1)[1].strip())

    while len(data) - body_start < content_size:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)

    print(f"""Старт сервера на {HOST} порт {PORT}\n 
          нажмите ctrl+c, чтобы остановить """)
    
    conn, addr = sock.accept()

    print('Подключено:', addr)

    data = conn.recv(4096)

    while b"\r\n\r\n" not in data:
        data += conn.recv(4096)

    headers_end = data.find(b"\r\n\r\n")
    headers_part = data[:headers_end].split(b'\r\n')
    method = headers_part[0].split(b' ')[0].decode('utf-8')
   
    if (method == Method.POST):
        print(read_full_body_post_method(data, conn, headers_end))
    elif (method == Method.GET):
        end_point = headers_part[0].split(b' ')[1]
        if (end_point == b'/about'):
            conn.sendall(request_about())