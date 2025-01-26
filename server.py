import socket

with open('keys/server.ip', 'r') as file:
    IP = file.read()

def start_my_server():
    try:
        server = socket.create_server((IP, 8000))
        server.listen(4)
        while True:
            print("Working...")
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode("utf-8")
            print(data)
            content = load_page_from_get_request(data)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
        print("shutdown this shit...")

def load_page_from_get_request(request_data):
    HDRS = 'HTTP/1.1 200 OK\r\rContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\rContent-Type: text/html; charset=utf-8\r\n\r\n'

    path = request_data.split(' ')[1]
    response = ''
    try:
        with open('pages' + path, 'rb') as file:
            response = file.read()
        return HDRS.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Sorry, bro! No page...').encode('utf-8')

    
if __name__ == '__main__':
    start_my_server()