import socket
import sys

PORT = 3490             
MAXDATASIZE = 512        
MAXLEN = 256          


def main():
    host, flag, message = sys.argv[1], sys.argv[2].lower(), sys.argv[3]
    port = PORT
    
    # Check for valid port
    if len(sys.argv) == 5:
        if not sys.argv[4].isdigit() or not 1 <= int(sys.argv[4]) <= 65535:
            print("client: port must be a number from 1 to 65535",
                  file=sys.stderr)
            return 1
        port = int(sys.argv[4])

    # Check valid encode/decode mode
    if flag not in ("-e", "-d"):
        print("client: flag must be -e (encode) or -d (decode), not %r" % flag,
              file=sys.stderr)
        return 1
    
    # Check for valid length of message
    if len(message) > MAXLEN:
        print("client: message is %d characters, limit is %d"
              % (len(message), MAXLEN), file=sys.stderr)
        return 1

    # Check that the message is valid ASCII
    try:
        request = ("E" if flag == "-e" else "D") + message
        request = request.encode("ascii")
    except UnicodeEncodeError:
        print("client: message must be printable ASCII", file=sys.stderr)
        return 1

    # Connect to server
    try:
        sockfd = socket.create_connection((host, port))
    except OSError as err:
        print("client: connect: %s" % err, file=sys.stderr)
        return 1

    try:
        sockfd.sendall(request)
        sockfd.shutdown(socket.SHUT_WR)  

        data = b""
        while len(data) < MAXDATASIZE:
            chunk = sockfd.recv(MAXDATASIZE - len(data))
            if not chunk:
                break
            data += chunk
    except OSError as err:
        print("client: %s" % err, file=sys.stderr)
        return 1
    finally:
        sockfd.close()

    reply = data.decode("ascii", "replace")
    if not reply:
        print("client: server closed the connection without replying", file=sys.stderr)
        return 1
    if reply.startswith("ERROR:"):
        print("client: %s" % reply, file=sys.stderr)
        return 1

    print(reply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
