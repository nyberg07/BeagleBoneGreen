#!/usr/bin/env python3
import asyncio, sys, json
from socket import IPPROTO_TCP, TCP_NODELAY

# Serveradress och port
SERVER_HOST = "10.0.0.100"
SERVER_PORT = 5000
PROMPT = "> "

# Lista över kända mottagare (uppdateras under körning)
recipients = ["all"]

async def recv_task(reader: asyncio.StreamReader):
    """Tar emot JSON-meddelanden från servern och skriver ut dem."""
    global recipients
    try:
        while True:
            line = await reader.readline()
            if not line:
                print("\n[server closed]", flush=True)
                break

            decoded = line.decode("utf-8", "ignore").strip()

            try:
                data = json.loads(decoded)
                msg_type = data.get("type")

                if msg_type == "userlist":
                    recipients = data.get("users", ["all"])
                    print(f"\n[Användarlista uppdaterad: {', '.join(recipients)}]")
                elif msg_type == "message":
                    sender = data.get("from", "okänd")
                    msg = data.get("message", "")
                    print(f"\n{sender}: {msg}")
                elif msg_type == "info":
                    print(f"\n[Info] {data.get('message', '')}")
                elif msg_type == "error":
                    print(f"\n[Fel] {data.get('message', '')}")
                else:
                    print(f"\n[Okänt meddelande]: {decoded}")
            except json.JSONDecodeError:
                # Föll tillbaka till vanlig text (ej JSON)
                print(f"\n{decoded}")

            sys.stdout.write(PROMPT)
            sys.stdout.flush()
    except Exception as e:
        print(f"\n[Fel i mottagning: {e}]")

async def input_task(writer: asyncio.StreamWriter, my_username: str):
    """Meny för att välja mottagare och skicka meddelanden som JSON."""
    try:
        while True:
            print("\nVälj mottagare:")
            for i, user in enumerate(recipients):
                print(f"{i + 1}. {user}")
            print(f"{len(recipients) + 1}. Uppdatera användarlista")
            print(f"{len(recipients) + 2}. Avsluta (/quit)")

            choice = await asyncio.to_thread(input, "Val: ")
            choice = choice.strip()

            if choice == str(len(recipients) + 2) or choice.lower() == "/quit":
                quit_data = {
                    "from": my_username,
                    "to": "server",
                    "type": "quit"
                }
                writer.write((json.dumps(quit_data) + "\n").encode("utf-8"))
                await writer.drain()
                break
            elif choice == str(len(recipients) + 1):
                list_request = {
                    "from": my_username,
                    "to": "server",
                    "type": "list"
                }
                writer.write((json.dumps(list_request) + "\n").encode("utf-8"))
                await writer.drain()
                continue

            try:
                recipient_index = int(choice) - 1
                if 0 <= recipient_index < len(recipients):
                    recipient = recipients[recipient_index]
                else:
                    print("Ogiltigt val.")
                    continue
            except ValueError:
                print("Välj ett nummer.")
                continue

            msg = await asyncio.to_thread(input, f"Skriv meddelande till {recipient}: ")
            if not msg:
                continue

            message_data = {
                "from": my_username,
                "to": recipient,
                "type": "message",
                "message": msg.strip()
            }
            writer.write((json.dumps(message_data) + "\n").encode("utf-8"))
            await writer.drain()

    except (EOFError, KeyboardInterrupt):
        quit_data = {
            "from": my_username,
            "to": "server",
            "type": "quit"
        }
        try:
            writer.write((json.dumps(quit_data) + "\n").encode("utf-8"))
            await writer.drain()
        except:
            pass

async def main():
    username = (await asyncio.to_thread(lambda: input("Välj användarnamn: ").strip())) or "user"

    try:
        reader, writer = await asyncio.open_connection(SERVER_HOST, SERVER_PORT)
    except Exception as e:
        print(f"[Kunde inte ansluta till servern: {e}]")
        return

    try:
        sock = writer.get_extra_info("socket")
        if sock is not None:
            sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    except Exception:
        pass

    # Vänta på "ENTER_USERNAME" från servern
    banner = await reader.readline()
    if b"ENTER_USERNAME" not in banner:
        print("[Oväntat svar från servern]")
        return

    writer.write((username + "\n").encode("utf-8"))
    await writer.drain()

    print(f"Välkommen, {username}! Skriv meddelanden till en användare eller alla. Avsluta med /quit.")

    tasks = [
        asyncio.create_task(recv_task(reader)),
        asyncio.create_task(input_task(writer, username)),
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for t in pending:
        t.cancel()

    try:
        writer.close()
        await writer.wait_closed()
    except:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[Klienten avslutad]", flush=True)
