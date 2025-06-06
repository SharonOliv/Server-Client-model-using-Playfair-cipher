import socket
import threading
import sys

HOST = '10.1.160.202'
PORT = 12345
KEY = "SECURITY"  # Playfair cipher key

def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    seen = set()

    for char in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, letter):
    for r, row in enumerate(matrix):
        if letter in row:
            return r, row.index(letter)
    return None, None

def playfair_encrypt(plain_text, matrix):
    plain_text = plain_text.upper().replace("J", "I").replace(" ", "")
    if len(plain_text) % 2 != 0:
        plain_text += 'X'

    encrypted_text = ""
    for i in range(0, len(plain_text), 2):
        a, b = plain_text[i], plain_text[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            encrypted_text += matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            encrypted_text += matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            encrypted_text += matrix[row_a][col_b] + matrix[row_b][col_a]

    return encrypted_text

def playfair_decrypt(cipher_text, matrix):
    decrypted_text = ""
    for i in range(0, len(cipher_text), 2):
        a, b = cipher_text[i], cipher_text[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        if row_a == row_b:
            decrypted_text += matrix[row_a][(col_a - 1) % 5] + matrix[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            decrypted_text += matrix[(row_a - 1) % 5][col_a] + matrix[(row_b - 1) % 5][col_b]
        else:
            decrypted_text += matrix[row_a][col_b] + matrix[row_b][col_a]
    return decrypted_text

def send_messages(client_socket, matrix):
    try:
        while True:
            sys.stdout.write("Client: ")
            sys.stdout.flush()
            
            message = input()
            if message.lower() == "exit":
                print("Closing connection...")
                client_socket.sendall("exit".encode('utf-8'))
                break

            encrypted_message = playfair_encrypt(message, matrix)
            print(f"Encrypted Sent: {encrypted_message}")
            client_socket.sendall(encrypted_message.encode('utf-8'))
    except:
        print("Connection closed by client.")

def receive_messages(client_socket, matrix):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data or data.lower() == "exit":
                print("\nServer disconnected.")
                break

            decrypted_data = playfair_decrypt(data, matrix)
            print(f"\nEncrypted Received: {data}")
            print(f"Server (Decrypted): {decrypted_data}")

            sys.stdout.write("Client: ")
            sys.stdout.flush()
    except:
        print("Connection closed by server.")

matrix = generate_playfair_matrix(KEY)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to server at {HOST}:{PORT}")

try:
    send_thread = threading.Thread(target=send_messages, args=(client_socket, matrix))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, matrix))
    send_thread.start()
    receive_thread.start()
    send_thread.join()
    receive_thread.join()
except:
    print("Error occurred.")
finally:
    client_socket.close()
    print("Client closed.")