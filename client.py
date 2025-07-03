import socket
import threading
import pygame
import sys
import json
from ui import start_screen, combat_screen, end_screen

# === Konfiguracja klienta ===
HOST = "localhost"
PORT = 5000

# === Stan gry ===
messages = []
name = ""
your_turn = False
player_hp = 100
enemy = None
players_info = []
game_over_result = None

def receive_data(sock):
    """Nasłuchuje na dane przychodzące z serwera i aktualizuje stan gry."""
    global messages, your_turn, player_hp, enemy, players_info, game_over_result
    buffer = ""

    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break
            buffer += data

            while True:
                try:
                    msg, index = json.JSONDecoder().raw_decode(buffer)
                    buffer = buffer[index:].lstrip()

                    if msg["type"] == "start":
                        messages.append(msg["msg"])
                    elif msg["type"] == "your_turn":
                        your_turn = True
                        player_hp = msg["player_hp"]
                        enemy = msg["enemy"]
                    elif msg["type"] == "enemy_update":
                        enemy = msg["enemy"]
                    elif msg["type"] == "update":
                        messages.append(msg["msg"])
                    elif msg["type"] == "players_update":
                        players_info = msg["players"]
                        for p in players_info:
                            if p["name"] == name:
                                player_hp = p["hp"]
                    elif msg["type"] == "end":
                        game_over_result = msg["result"].upper()

                except json.JSONDecodeError:
                    break

        except Exception as e:
            print(f"[ERROR] {e}")
            break

def send_action(sock, action):
    """Wysyła akcję gracza do serwera."""
    data = {"action": action}
    sock.sendall(json.dumps(data).encode())

def main():
    """Główna pętla gry klienta. Obsługuje 3 główne ekrany i zakończenie gry."""
    global name, your_turn

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Dawnfall of Eldara")
    clock = pygame.time.Clock()

    # === Ekran startowy ===
    name_avatar = start_screen(screen)
    if not name_avatar:
        pygame.quit()
        sys.exit()

    name, avatar_class = name_avatar

    # === Połączenie z serwerem ===
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    data = json.dumps({"name": name, "avatar": avatar_class})
    sock.sendall(data.encode())

    threading.Thread(target=receive_data, args=(sock,), daemon=True).start()

    # === Pętla gry ===
    running = True
    while running:
        clock.tick(30)

        # === Ekran walki ===
        combat_screen(screen, messages, enemy, players_info, your_turn)

        # === Sprawdzenie końca gry ===
        if game_over_result:
            end_screen(screen, game_over_result)
            pygame.quit()
            sys.exit()

        # === Obsługa zdarzeń ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sock.close()
                pygame.quit()
                sys.exit()

            if your_turn and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    send_action(sock, "attack")
                    your_turn = False
                elif event.key == pygame.K_2:
                    send_action(sock, "heal")
                    your_turn = False
                elif event.key == pygame.K_3:
                    send_action(sock, "pass")
                    your_turn = False

    sock.close()

if __name__ == "__main__":
    main()
