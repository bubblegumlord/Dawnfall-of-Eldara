import random
import json
from .enemy import ENEMY_POOL
from collections import deque

def broadcast(sock_list, message_dict):
    """Wysyła wiadomość JSON do wszystkich podanych socketów."""
    msg = json.dumps(message_dict).encode()
    for sock in sock_list:
        try:
            sock.sendall(msg)
        except Exception as e:
            print(f"[ERROR] broadcast: {e}")

def broadcast_states(sock_list, players, enemy):
    """Wysyła aktualny stan graczy i przeciwnika do klientów."""
    # Stan graczy
    states = [
        {
            "name": p.name,
            "hp": p.hp,
            "alive": p.is_alive(),
            "avatar": getattr(p, "avatar", "warrior")  # domyślnie "warrior"
        }
        for p in players
    ]
    broadcast(sock_list, {"type": "players_update", "players": states})

    # Stan przeciwnika
    if enemy:
        enemy_state = {
            "name": enemy.name,
            "hp": enemy.hp,
            "max_hp": enemy.max_hp,
            "image_path": enemy.image_path
        }
        broadcast(sock_list, {"type": "enemy_update", "enemy": enemy_state})

def start_game(players, player_sockets):
    """Główna pętla gry — obsługuje kolejność tur i przebieg walki."""
    # Przygotowanie kolejki przeciwników
    enemy_queue = deque(random.sample(ENEMY_POOL, 4))
    current_enemy = enemy_queue.popleft()

    broadcast_states(player_sockets, players, current_enemy)

    while True:
        # Sprawdzenie czy gracze żyją
        alive_players = [p for p in players if p.is_alive()]
        if not alive_players:
            broadcast(player_sockets, {"type": "end", "result": "defeat"})
            break

        # === Tura graczy ===
        for i, player in enumerate(players):
            if not player.is_alive():
                continue

            try:
                # Dane o aktualnym przeciwniku
                enemy_state = {
                    "name": current_enemy.name,
                    "hp": current_enemy.hp,
                    "max_hp": current_enemy.max_hp,
                    "image_path": current_enemy.image_path
                }

                # Wyślij informację o turze gracza
                player_sockets[i].sendall(json.dumps({
                    "type": "your_turn",
                    "player_hp": player.hp,
                    "enemy": enemy_state
                }).encode())

                # Odbiór i przetwarzanie akcji
                data = player_sockets[i].recv(1024).decode()
                action_data = json.loads(data)
                action = action_data.get("action")

                if action == "attack":
                    dmg_val = random.randint(15, 25)
                    current_enemy.take_damage(dmg_val)
                    msg = f"{player.name} attacks {current_enemy.name} for {dmg_val} damage."
                elif action == "heal":
                    heal_val = random.randint(10, 20)
                    player.heal(heal_val)
                    msg = f"{player.name} heals for {heal_val} HP."
                elif action == "pass":
                    msg = f"{player.name} skips the turn."
                else:
                    msg = f"{player.name} performed an unknown action."

                broadcast(player_sockets, {"type": "update", "msg": msg})

                # Pokonanie wroga i pojawienie się następnego
                if not current_enemy.is_alive():
                    if enemy_queue:
                        current_enemy = enemy_queue.popleft()
                        broadcast(player_sockets, {
                            "type": "update",
                            "msg": f"{player.name} defeated the enemy! A new enemy appears: {current_enemy.name}!"
                        })
                        broadcast_states(player_sockets, players, current_enemy)
                    else:
                        broadcast(player_sockets, {"type": "end", "result": "victory"})
                        return
                else:
                    broadcast_states(player_sockets, players, current_enemy)

            except Exception as e:
                print(f"[ERROR] Player turn ({player.name}): {e}")

                # === Oznacz gracza jako martwego ===
                player.hp = 0

                broadcast(player_sockets, {
                    "type": "update",
                    "msg": f"{player.name} has disconnected and is now considered defeated."
                })

                broadcast_states(player_sockets, players, current_enemy)

        # === Tura przeciwnika ===
        if current_enemy.is_alive():
            result = current_enemy.attack(players)
            if result:
                broadcast(player_sockets, {"type": "update", "msg": f"{result}"})
                broadcast_states(player_sockets, players, current_enemy)
