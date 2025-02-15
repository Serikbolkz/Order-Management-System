import socket
import threading

class OrderServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.orders = {}  # Dictionary to store orders
        self.lock = threading.Lock()  # Thread safety for shared resources

    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                
                response = self.process_request(data)
                client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()

    def process_request(self, request):
        try:
            parts = request.split(' ', 1)
            command = parts[0].upper()
            data = parts[1] if len(parts) > 1 else ""

            if command == "PLACE":
                return self.place_order(data)
            elif command == "GET":
                return self.get_order(data)
            elif command == "EDIT":
                return self.edit_order(data)
            else:
                return "ERROR: Unknown command"
        except Exception as e:
            return f"ERROR: {str(e)}"

    def place_order(self, data):
        with self.lock:
            order_id = len(self.orders) + 1
            self.orders[order_id] = data
            return f"SUCCESS: Order placed with ID {order_id}"

    def get_order(self, data):
        try:
            order_id = int(data)
            with self.lock:
                if order_id in self.orders:
                    return f"SUCCESS: Order {order_id}: {self.orders[order_id]}"
                else:
                    return "ERROR: Order ID not found"
        except ValueError:
            return "ERROR: Invalid order ID"

    def edit_order(self, data):
        try:
            order_id, new_order = data.split(' ', 1)
            order_id = int(order_id)
            with self.lock:
                if order_id in self.orders:
                    self.orders[order_id] = new_order
                    return f"SUCCESS: Order {order_id} updated"
                else:
                    return "ERROR: Order ID not found"
        except ValueError:
            return "ERROR: Invalid input format"

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()



server = OrderServer()
server.start()