# Random Selection Microservice

## What it does

Picks one random item from a list. This could be used to pick a recipe, player, assignment, or anything else.

## How to run it

You need Python and `pyzmq` installed. Open a terminal in this folder:

```bash
python -m pip install -r requirements.txt
python microservice.py
```

Leave that running. Open another terminal in the same folder and run:

```bash
python test_client.py
```

## Communication contract

This service uses **ZeroMQ REQ/REP with JSON** on `tcp://127.0.0.1:5552`. The client sends one request and then waits for one reply. Run the server before running the client.

### Requesting data

Use `action` set to `select` and `items` with at least one item. The item returned can change each time.

Example JSON request:

```json
{
  "action": "select",
  "items": [
    "A",
    "B",
    "C"
  ]
}
```

Example Python code that **sends the request and receives the reply**:

```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5552")

request = {'action': 'select', 'items': ['A', 'B', 'C']}
socket.send_json(request)

reply = socket.recv_json()
print(reply)

socket.close()
context.term()
```

The client uses `socket.send_json(request)` to send the request. It does not import or call the microservice's functions directly.

### Receiving data

Use `socket.recv_json()` to receive the reply. A successful reply contains `"status": "ok"`. If something is wrong with the request, the reply contains `"status": "error"` and a `"message"` explaining why.

Example successful response:

```json
{
  "status": "ok",
  "item": "B"
}
```

To check the response in Python:

```python
reply = socket.recv_json()
if reply["status"] == "ok":
    print(reply)
else:
    print(reply["message"])
```

The example above shows the receive step separately; in a real client, use it **once per request**, as shown in the full example earlier.

## UML sequence diagram

```mermaid
sequenceDiagram
    participant Client as Test Program
    participant Service as Random Selection Service
    Client->>Service: send_json(request) over ZeroMQ
    activate Service
    Service->>Service: handle_request(request)
    Service-->>Client: send_json(response) over ZeroMQ
    deactivate Service
    Client->>Client: recv_json() and display response
```

## Files

- `microservice.py`: Runs the server and handles requests.
- `test_client.py`: Sends example requests and prints the replies.
- `requirements.txt`: Lists the Python dependency.
- `sample_requests.json`: Extra example requests.

The server and test client run as separate programs.
