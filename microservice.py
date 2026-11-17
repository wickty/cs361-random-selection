"""Random Selection microservice. ZeroMQ REQ/REP, JSON, TCP port 5552."""
import json
import secrets
import zmq

PORT = 5552


def handle_request(request):
    if not isinstance(request, dict) or request.get("action") != "select":
        return {"status": "error", "message": "action must be 'select'"}
    items = request.get("items")
    if not isinstance(items, list):
        return {"status": "error", "message": "items must be an array"}
    if not items:
        return {"status": "error", "message": "at least one item is required"}
    return {"status": "ok", "item": secrets.choice(items)}


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.setsockopt(zmq.LINGER, 0)
    socket.bind(f"tcp://127.0.0.1:{PORT}")
    print(f"Random Selection ready on tcp://127.0.0.1:{PORT}", flush=True)
    try:
        while True:
            try:
                request = socket.recv_json()
                print(f"REQUEST: {json.dumps(request, ensure_ascii=False)}", flush=True)
                response = handle_request(request)
            except Exception as exc:
                response = {"status": "error", "message": f"invalid request: {exc}"}
            print(f"RESPONSE: {json.dumps(response, ensure_ascii=False)}", flush=True)
            socket.send_json(response)
    except KeyboardInterrupt:
        print("Service stopped.")
    finally:
        socket.close()
        context.term()


if __name__ == "__main__":
    main()
