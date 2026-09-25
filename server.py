import socket
import sys

PORT = 3490
BACKLOG = 10        
MAXDATASIZE = 512       
MAXLEN = 256   
FIRST_CH = 32           
LAST_CH = 126     

# Helper function to shift each character forward for encoding or backward for decoding
def convert(message, flag):
    step = 1 if flag == "E" else -1
    return "".join(chr(FIRST_CH + (ord(ch) - FIRST_CH + step) % (LAST_CH - FIRST_CH + 1)) for ch in message)

# Validate before converting message
def handle(data):

    # Check for valid data
    if not data:
        return "ERROR: empty request"
    
    # Check for that message is valid ASCII
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError:
        return "ERROR: request must be plain ASCII"

    # Extract flag from message
    flag = text[0].upper() 
    message = text[1:]

    # Check for valid encode/decode flag
    if flag not in ("E", "D"):
        return "ERROR: unknown flag %r (expected E or D)" % text[0]
    
    # Check that message is valid length
    if len(message) > MAXLEN:
        return "ERROR: message is %d characters, limit is %d" % (
            len(message), MAXLEN)
    
    # Check that each character is valid
    for ch in message:
        if not FIRST_CH <= ord(ch) <= LAST_CH:
            return "ERROR: message has a non-printable character (code %d)" % ord(ch)

    return convert(message, flag)


def main():
    port = PORT
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sockfd.bind(("", port))
        sockfd.listen(BACKLOG)
    except OSError as err:
        print("server: bind: %s" % err, file=sys.stderr)
        return 1

    print("server: waiting for connections on port %d..." % port)

    while True:
        try:
            conn, addr = sockfd.accept()
        except KeyboardInterrupt:
            print("\nserver: shutting down")
            break
        except OSError as err:
            print("server: accept: %s" % err, file=sys.stderr)
            continue

        print("server: got connection from %s" % addr[0])
        try:
            # Read until the client half-closes, or until we hit our limit.
            data = b""
            while len(data) < MAXDATASIZE:
                chunk = conn.recv(MAXDATASIZE - len(data))
                if not chunk:
                    break
                data += chunk

            reply = handle(data)
            print("server: sending '%s'" % reply)
            conn.sendall(reply.encode("ascii"))
        except OSError as err:
            print("server: %s" % err, file=sys.stderr)
        finally:
            conn.close()

    sockfd.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
