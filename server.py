import socket
import threading
import json
from game import Player, start_game

HOST = "localhost"
PORT = 5000
MAX_PLAYERS = 4

rooms = {}
room_counter = 1
lock = threading.Lock()

def find_or_create_room():
    global room_counter
    for room_id, room in rooms.items():
        if not room["game_started"] and len(room["players"]) < MAX_PLAYERS:
            return room_id
    # Brak dostępnego pokoju – tworzymy nowy
    new_id = room_counter
    rooms[new_id] = {"players": [], "sockets": [], "game_started": False}
    room_counter += 1
    return new_id

def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode()
        player_data = json.loads(data)
        name = player_data.get("name")
        avatar = player_data.get("avatar", "warrior")

        print(f"[INFO] {name} połączył się z {addr} z avatarem {avatar}")

        with lock:
            room_id = find_or_create_room()
            room = rooms[room_id]

            player = Player(name, avatar)
            room["players"].append(player)
            room["sockets"].append(conn)

            if len(room["players"]) == MAX_PLAYERS:
                room["game_started"] = True
                print(f"[ROOM {room_id}] Wystarczająca liczba graczy. Start gry.")

                for sock in room["sockets"]:
                    sock.sendall(json.dumps({
                        "type": "start",
                        "msg": f"Your team has entered the dungeon. Good luck..."
                    }).encode())

                threading.Thread(
                    target=start_game,
                    args=(room["players"], room["sockets"]),
                    daemon=True
                ).start()
            else:
                # Powiadom klienta że oczekuje na graczy
                conn.sendall(json.dumps({
                    "type": "waiting",
                    "msg": f"Waiting for other players in room {room_id}..."
                }).encode())

    except Exception as e:
        print(f"[ERROR] {e}")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER] Serwer nasłuchuje na {HOST}:{PORT}...")

    while True:
        try:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
        except Exception as e:
            print(f"[SERVER ERROR] {e}")
            break

    server.close()

if __name__ == "__main__":
    start_server()
