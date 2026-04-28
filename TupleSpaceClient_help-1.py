import socket
import sys
import os

def main():
    if len(sys.argv) != 4:
        print("Usage: python tuple_space_client.py <server-hostname> <server-port> <input-file>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    input_file_path = sys.argv[3]

    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' does not exist.")
        sys.exit(1)

    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # TASK 1: Create a TCP/IP socket and connect it to the server.
    # Hint: socket.socket(socket.AF_INET, socket.SOCK_STREAM) creates the socket.
    # Then call sock.connect((hostname, port)) to connect.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))


    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ", 2)
            cmd = parts[0]
            message = ""

            # TASK 2: Build the protocol message string to send to the server.
            # Format:  "NNN X key"        for READ / GET
            #          "NNN P key value"   for PUT
            # where NNN is the total message length as a zero-padded 3-digit number,
            # X is "R" for READ and "G" for GET.
            # Hint: for READ/GET, size = 6 + len(key). For PUT, size = 7 + len(key) + len(value).
            # Reject lines with invalid format or key+" "+value > 970 chars.
            try:
                if cmd == "READ":
                    # Extract the key
                    key = parts[1]
                    # content length
                    total_len = 6 + len(key)
                    content = f"R {key}"

                elif cmd == "GET":
                    key = parts[1]
                    total_len = 6 + len(key)
                    content = f"G {key}"

                elif cmd == "PUT":
                    # Read the key and value
                    key = parts[1]
                    val = parts[2]
                    # Check if the length exceeds 970
                    if len(key + " " + val) > 970:
                        print(f"{line}: ERR Line too long")
                        continue
                    total_len = 7 + len(key) + len(val)
                    content = f"P {key} {val}"
                
                else:
                    # Skip unknown commands
                    print(f"{line}: unknown command")
                    continue
                # Splicing the final message
                message = f"{total_len:03d} {content}"
            except Exception:
                # Skip incorrect format
                print(f"{line}: incorrect format")
                continue




            # TASK 3: Send the message to the server, then receive the response.
            # - Send:    sock.sendall(message.encode())
            # - Receive: first read 3 bytes to get the response size (like the server does).
            #            Then read the remaining (size - 3) bytes to get the response body.

            # Send a message
            sock.sendall(message.encode())
            # Read 3 bytes first to obtain the total length of the response
            size_bytes = sock.recv(3)
            resp_size = int(size_bytes.decode())
            # Read the remaining response content
            response_buffer = sock.recv(resp_size - 3)

            response = response_buffer.decode().strip()
            print(f"{line}: {response}")

    except (socket.error, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        # TASK 4: Close the socket when done (already called for you — explain why
        # reason:Ensure that sock. close() will definitely execute
        # finally: is the right place to do this even if an error occurs above).
        sock.close()

if __name__ == "__main__":
    main()