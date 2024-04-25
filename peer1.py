import socket


def main():
    # Create a UDP socket
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    peer_socket.bind(('127.0.0.1', 12345))
    print("Peer 1 is listening for connection.")
    
    # Wait for connection from Peer 2
    while True:
        # Receive message from Peer 2
        message, addr = peer_socket.recvfrom(1024)
        print(f"Received message from Peer 2: {message.decode('utf-8')}")
        
        # Check if the message is a connection request from Peer 2
        if message.decode('utf-8') == 'connect':
            print("Connection established with Peer 2.")
            break
    
    # Prompt the user to choose whether to send or receive a file
    choice = input("Do you want to send or receive a file? (send/receive): ").lower()

    if choice == 'send':
        # Prompt the user to enter the file they want to share
        file_path = input("Enter the path of the file you want to share: ")
        
        # Read the content of the file
        try:
            with open(file_path, "rb") as file:
                count=0
                while True:
                    file_chunk = file.read(4096)  
                    if not file_chunk:
                        peer_socket.sendto(b'', addr)  # Send an empty message to indicate end of file
                        break  # End of file
                    count+=1
                    peer_socket.sendto(file_chunk, addr)
                print(count)
        except FileNotFoundError:
            print("File not found.")
            return
        
        print("File sent successfully.")

 
    elif choice == 'receive':
        # Receive file content from Peer 1
        with open("received_file_from_peer2.bin", "wb") as file:
            while True:
                try:
                    file_chunk, addr = peer_socket.recvfrom(4096)
                except socket.error as e:
                    print(f"Error receiving data: {e}")
                    break 
                if not file_chunk:
                    break 
                if file_chunk == b'':
                    break 
                file.write(file_chunk)
                print("Receiving file...")
            
        print("File received successfully.")


if __name__ == '__main__':
    main()
