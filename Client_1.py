# # First we need to import necessary packages
# import socket
# import threading
#
# # ANSI escape codes for colors
# COLORS = {
#     'green': '\033[92m',  # Green color for client's messages
#     'orange': '\033[93m',  # Orange color for client's messages (Yellow close to orange)
#     'red': '\033[91m',  # Red color
#     'reset': '\033[0m'    # Reset color
# }
#
# def receive_messages(client_socket, stop_event):
#     while not stop_event.is_set():
#         try:
#             response = client_socket.recv(1024).decode('utf-8')
#             if response:
#                 print(f"{COLORS['orange']}\nOpponent: {COLORS['reset']}{response}\n {COLORS['red']}Reply:")
#             else:
#                 break
#         except OSError:  # Handle socket closure gracefully
#             break
#         except Exception as e:
#             print(f"Error receiving message: {e}")
#             break
#
# def main():
#     server_address = 'https://messengerusingsocketspython.onrender.com'
#     server_port = 80
#     stop_event = threading.Event()
#
#     try:
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         print(f"Connecting to server at {server_address}:{server_port}...")
#         client_socket.connect((server_address, server_port))
#         print("Connected successfully.")
#
#         # Start the receiver thread
#         threading.Thread(target=receive_messages, args=(client_socket, stop_event), daemon=True).start()
#
#         while True:
#             message = input(f"{COLORS['green']}You: {COLORS['reset']}")
#             if message.lower() == 'exit':
#                 print("Exiting chat...")
#                 stop_event.set()  # Signal the receiving thread to stop
#                 break
#             client_socket.sendall(message.encode('utf-8'))
#
#         client_socket.close()
#         print("Connection closed.")
#
#     except ConnectionRefusedError:
#         print(f"Error: Could not connect to the server at {server_address}:{server_port}.")
#     except socket.error as e:
#         print(f"Socket error: {e}")
#
# if __name__ == "__main__":
#     main()
#



import websocket
import threading

# ANSI escape codes for colors
COLORS = {
    'green': '\033[92m',  # Green color for client's messages
    'orange': '\033[93m',  # Orange color for client's messages (Yellow close to orange)
    'red': '\033[91m',  # Red color
    'reset': '\033[0m'    # Reset color
}

# Function to handle incoming messages from the server (other client)
def on_message(ws, message):
    print(f"{COLORS['orange']}\nOpponent: {COLORS['reset']}{message}\n {COLORS['red']}Reply:")

# Function to handle errors
def on_error(ws, error):
    print(f"Error: {error}")

# Function to handle WebSocket closure
def on_close(ws, close_status_code, close_msg):
    print("Connection closed.")

# Function to send messages to the server (other client)
def on_open(ws):
    print("Connected to server.")
    while True:
        message = input(f"{COLORS['green']}You: {COLORS['reset']}")
        if message.lower() == 'exit':
            print("Exiting chat...")
            break
        ws.send(message)

# Main function to initialize WebSocket client
def main():
    server_url = "wss://messengerusingsocketspython.onrender.com"  # WebSocket URL for Render
    # Create a WebSocket client
    ws = websocket.WebSocketApp(server_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    main()
