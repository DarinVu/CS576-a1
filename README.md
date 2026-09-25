# CS 576 — Assignment 1: TCP Server and Client

A TCP server and client written in Python 3.

The client sends a message and a flag to the server over a TCP connection. The
server converts the message and sends it back, and the client prints it.

* `-e` **encode** — replace each character with the next one in the ASCII
  sequence: `Hello World` → `Ifmmp!Xpsme`
* `-d` **decode** — the inverse: `Ifmmp!Xpsme` → `Hello World`


## Files

* `server.py` — listens for connections, converts messages, sends them back
* `client.py` — sends a message and a flag, prints the reply

## User Instructions

You need two terminal windows, both in this directory.

**Terminal 1 - Server:** 

The server runs until you stop it with `Ctrl-C`:

```
python3 server.py
```

**Terminal 2 - Client:**

```
python3 client.py localhost -e "Hello World"
Ifmmp!Xpsme

$ python3 client.py localhost -d 'Ifmmp!Xpsme'
Hello World
```

The command line is:

```
python3 client.py hostname -e|-d message
```

Use `localhost` for the hostname when both programs are on the same machine,
or the server machine's IP address when they are not.

