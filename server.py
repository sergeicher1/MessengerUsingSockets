# First we need to import necessary packages
import socket
import threading

# Function to handle communication between two clients
def handle_client(client_socket, client_address, client_id, other_client_socket):
    print(f"User {client_id} connected from {client_address}")

    while True:
        try:
            # Receive the message from the current client
            message = client_socket.recv(1024).decode('utf-8')
            if not message: # If message is empty, break the loop
                break
            print(f"User: {client_id} says: {message}")

            # Send the message to the other client immediately
            other_client_socket.sendall(message.encode('utf-8'))
            print(f"Message forwarded to User: {3 - client_id}")

        except Exception as e:
            print(f"Error: {e}")
            break
    # Close the connection when done
    client_socket.close()
    print(f"User {client_id} disconnected.")

# Server function to handle connections and start communication between two clients
def start_server():
    server_address = '127.0.0.1'
    server_port = 6000

    # Create socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_address}:{server_port}...")

    # Accept two clients
    client_socket_1, client_address_1 = server_socket.accept()
    print(f"User 1 connected from {client_address_1}")
    client_socket_2, client_address_2 = server_socket.accept()
    print(f"User 2 connected from {client_address_2}")

    # Start handling communication between the two clients
    thread_1 = threading.Thread(target=handle_client, args=(client_socket_1, client_address_1, 1, client_socket_2))
    thread_2 = threading.Thread(target=handle_client, args=(client_socket_2, client_address_2, 2, client_socket_1))

    thread_1.start()
    thread_2.start()

if __name__ == "__main__":
    start_server()

