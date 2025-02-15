import socket

class OrderClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port

    def send_request(self, request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            client_socket.sendall(request.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            return response

    def start(self):
        print("Order Management Client")
        print("Commands: PLACE <order>, GET <order_id>, EDIT <order_id> <new_order>, EXIT")
        while True:
            command = input("Enter command: ").strip()
            if command.upper() == "EXIT":
                break
            response = self.send_request(command)
            print(response)


client = OrderClient()
client.start()
