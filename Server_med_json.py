#!/usr/bin/env python3
import asyncio
import json
from socket import IPPROTO_TCP, TCP_NODELAY

HOST = ""      # Lyssna på alla nätverksgränssnitt
PORT = 5000
clients = {}   # writer -> username

def make_json(data: dict) -> bytes:
    """Konvertera dict till JSON-sträng med radslut, som bytes."""
    return (json.dumps(data) + "\n").encode("utf-8")

async def send(writer, data: dict):
    """Skicka ett JSON-meddelande till en specifik klient."""
    try:
        writer.write(make_json(data))
        await writer.drain()
    except:
        pass

async def broadcast(data: dict, exclude=None):
    """Skicka ett JSON-meddelande till alla klienter."""
    dead = []
    for w in clients:
        if exclude and w == exclude:
            continue
        try:
            w.write(make_json(data))
        except:
            dead.append(w)
    await asyncio.gather(*(w.drain() for w in clients if not w.is_closing()), return_exceptions=True)
    for w in dead:
        clients.pop(w, None)
        try:
            w.close()
        except:
            pass

async def send_userlist():
    """Skicka uppdaterad användarlista till alla klienter."""
    userlist_data = {
        "type": "userlist",
        "users": sorted(clients.values())
    }
    await broadcast(userlist_data)

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    try:
        sock = writer.get_extra_info("socket")
        if sock:
            sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    except:
        pass

    peer = writer.get_extra_info("peername")
    writer.write(b"ENTER_USERNAME\n")
    await writer.drain()

    name_bytes = await reader.readline()
    if not name_bytes:
        writer.close()
        await writer.wait_closed()
        return

    username = name_bytes.decode("utf-8", "ignore").strip() or f"user_{peer[1]}"
    existing = set(clients.values())
    base = username
    i = 2
    while username in existing:
        username = f"{base}{i}"
        i += 1

    clients[writer] = username
    print(f"[+] {username} connected from {peer}", flush=True)

    # Skicka välkomstmeddelande till användaren
    await send(writer, {"type": "info", "message": f"Welcome, {username}!"})
    # Meddela andra
    await broadcast({"type": "info", "message": f"*** {username} joined ***"}, exclude=writer)
    await send_userlist()

    try:
        while True:
            line = await reader.readline()
            if not line:
                break
            try:
                data = json.loads(line.decode("utf-8", "ignore"))
            except json.JSONDecodeError:
                await send(writer, {"type": "error", "message": "Invalid JSON"})
                continue

            msg_type = data.get("type")
            sender = clients.get(writer, "unknown")

            if msg_type == "quit":
                await send(writer, {"type": "info", "message": "Goodbye!"})
                break

            elif msg_type == "list":
                await send_userlist()

            elif msg_type == "message":
                to = data.get("to", "all")
                msg = data.get("message", "").strip()
                if not msg:
                    continue

                msg_data = {
                    "type": "message",
                    "from": sender,
                    "message": msg
                }

                if to == "all":
                    await broadcast(msg_data)
                else:
                    # Riktat meddelande
                    target_writer = None
                    for w, name in clients.items():
                        if name == to:
                            target_writer = w
                            break
                    if target_writer:
                        await send(target_writer, msg_data)
                    else:
                        await send(writer, {"type": "error", "message": f"User '{to}' not found."})
            else:
                await send(writer, {"type": "error", "message": f"Unknown type: {msg_type}"})

    except Exception as e:
        print(f"[!] Error with {username}: {e}")
    finally:
        uname = clients.pop(writer, None)
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass
        if uname:
            print(f"[-] {uname} disconnected", flush=True)
            await broadcast({"type": "info", "message": f"*** {uname} left ***"})
            await send_userlist()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    try:
        sock = server.sockets[0]
        sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    except:
        pass

    addr = ", ".join(str(s.getsockname()) for s in server.sockets)
    print(f"Chat server listening on {addr}", flush=True)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[server stopped]", flush=True)
