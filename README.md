# Server-Client Model using Playfair Cipher
This repository contains the implementation of the **Playfair cipher** in a **client-server model**, enabling secure **dual communication** between the server and the client.

## Overview

The repo demonstrates:
- Secure message exchange using the **Playfair cipher** encryption technique.
- Both server and client can send and receive encrypted messages.
- A basic understanding of classical cryptography integrated with network programming.

The **Playfair cipher** is a digraph substitution cipher that encrypts pairs of letters, providing better security than simple monoalphabetic ciphers.

## Features

- Encrypt outgoing messages using the Playfair cipher.
- Decrypt incoming messages using the Playfair cipher.
- Enable secure two-way (dual) communication between server and client.
- Simple socket-based client-server model for encrypted messaging.

## Technologies Used

- Python 3
- Socket programming (TCP Sockets)
- Custom implementation of the Playfair cipher

## How to Run

1. Clone the repository:
   
2. Navigate to the project directory:
   
3. Run the server:
   ```bash
   python playfair_server.py
   ```

4. In a new terminal, run the client:
   ```bash
   python playfair_client.py
   ```

5. Start sending and receiving encrypted messages!

## Notes

- The Playfair cipher is a classical encryption technique, mainly for educational purposes.
- For real-world applications, modern encryption algorithms are recommended.
