# # First we need to import necessary packages
# import socket
# import threading
# import os
#
# # Function to handle communication between two clients
# def handle_client(client_socket, client_address, client_id, other_client_socket):
#     print(f"User {client_id} connected from {client_address}")
#
#     while True:
#         try:
#             # Receive the message from the current client
#             message = client_socket.recv(1024).decode('utf-8')
#             if not message: # If message is empty, break the loop
#                 break
#             print(f"User: {client_id} says: {message}")
#
#             # Send the message to the other client immediately
#             other_client_socket.sendall(message.encode('utf-8'))
#             print(f"Message forwarded to User: {3 - client_id}")
#
#         except Exception as e:
#             print(f"Error: {e}")
#             break
#     # Close the connection when done
#     client_socket.close()
#     print(f"User {client_id} disconnected.")
#
# # Server function to handle connections and start communication between two clients
# def start_server():
#     server_address = '0.0.0.0'
#     server_port = int(os.getenv("PORT", 6000))
#
#     # Create socket object
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((server_address, server_port))
#     server_socket.listen(5)
#     print(f"Server listening on {server_address}:{server_port}...")
#
#     # Accept two clients
#     client_socket_1, client_address_1 = server_socket.accept()
#     print(f"User 1 connected from {client_address_1}")
#     client_socket_2, client_address_2 = server_socket.accept()
#     print(f"User 2 connected from {client_address_2}")
#
#     # Start handling communication between the two clients
#     thread_1 = threading.Thread(target=handle_client, args=(client_socket_1, client_address_1, 1, client_socket_2))
#     thread_2 = threading.Thread(target=handle_client, args=(client_socket_2, client_address_2, 2, client_socket_1))
#
#     thread_1.start()
#     thread_2.start()
#
# if __name__ == "__main__":
#     start_server()
#


import asyncio
import websockets
import os

# Function to handle communication between two clients
connected_clients = []


async def handle_client(websocket, path):
    # Add client to the list of connected clients
    connected_clients.append(websocket)
    client_id = len(connected_clients)
    print(f"User {client_id} connected.")

    try:
        async for message in websocket:
            print(f"User {client_id} says: {message}")

            # Forward the message to the other client (broadcasting)
            # Only forward if there is another client connected
            if len(connected_clients) > 1:
                # Find the other client
                other_client = connected_clients[1] if client_id == 1 else connected_clients[0]
                await other_client.send(message)
                print(f"Message forwarded to User {3 - client_id}")
            else:
                print("Waiting for another client to connect...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Remove the client from the list when disconnected
        connected_clients.remove(websocket)
        print(f"User {client_id} disconnected.")


# Start WebSocket server
async def start_server():
    server_address = '0.0.0.0'
    server_port = int(os.getenv("PORT", 6000))  # Use the PORT environment variable or fallback to 6000
    print(f"Server listening on {server_address}:{server_port}...")

    # Create the WebSocket server
    async with websockets.serve(handle_client, server_address, server_port):
        await asyncio.Future()  # Keep the server running


if __name__ == "__main__":
    asyncio.run(start_server())
