import socket

def main():
    # Create a UDP socket
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    peer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    peer_socket.bind(('127.0.0.1', 12346))
    addr = ('127.0.0.1', 12345)
    print("Peer 2 is listening for connection.")
    
    # Send connection request to Peer 1
    peer_socket.sendto(b'connect', ('127.0.0.1', 12345))
    print("Connection request sent to Peer 1.")
    
    # Prompt the user to choose whether to send or receive a file
    choice = input("Do you want to send or receive a file? (send/receive): ").lower()
    
    if choice == 'send':
        # Prompt the user to enter the file they want to share
        file_path = input("Enter the path of the file you want to share: ")
        
        # Read the content of the file
        try:
            with open(file_path, "rb") as file:
                while True:
                    file_chunk = file.read(4096)  
                    if not file_chunk:
                        peer_socket.sendto(b'', addr)  # Send an empty message to indicate end of file
                        break  
                    peer_socket.sendto(file_chunk, addr)
        except FileNotFoundError:
            print("File not found.")
            return
        print("File sent successfully.")

    elif choice == 'receive':
        # Receive file content from Peer 1
        with open("received_file_from_peer1.bin", "wb") as file:
            while True:
                try:
                    file_chunk, addr = peer_socket.recvfrom(4096)
                except socket.error as e:
                    print(f"Error receiving data: {e}")
                    break  
                if not file_chunk:
                    break  
                if file_chunk== b'':
                    break  # Exit the loop when an empty message is received
                file.write(file_chunk)
                print("Receiving file...")
            
        print("File received successfully.")

if __name__ == '__main__':
    main()

