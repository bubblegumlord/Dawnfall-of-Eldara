import pygame
from .utils import load_font, parse_message, PLAYER_COLORS

def draw_waiting_screen(screen):
    """Wyświetla ekran oczekiwania na innych graczy."""
    screen.fill((0, 0, 0))
    font = load_font(36)

    text = "Waiting for other players..."
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

def combat_screen(screen, messages, enemy, players_info, your_turn):
    """Ekran walki."""
    if len(players_info) < 4:
        draw_waiting_screen(screen)
        return

    # === Wczytanie czcionek i tła ====
    small_font = load_font(20)
    big_font = load_font(26)
    bg_image = pygame.image.load("assets/background/combat.png").convert()
    screen.blit(bg_image, (0, 0))

    # === GÓRA: przeciwnik ===
    if enemy:
        try:
            # Wczytanie obrazka przeciwnika
            enemy_image = pygame.image.load(enemy['image_path']).convert_alpha()
            image_rect = enemy_image.get_rect(center=(screen.get_width() // 2, 120))
            screen.blit(enemy_image, image_rect)

            # Nazwa + HP przeciwnika
            name_surface = big_font.render(enemy['name'], True, (255, 255, 255))
            hp_surface = big_font.render(f"HP: {enemy['hp']}/{enemy['max_hp']}", True, (255, 255, 255))

            screen.blit(name_surface, (30, 30))
            screen.blit(hp_surface, (30, 30 + name_surface.get_height() + 5))

        except Exception as e:
            error_text = small_font.render(f"Image not found: {enemy.get('image_path', '???')}", True, (255, 0, 0))
            screen.blit(error_text, (20, 20))

    # === ŚRODEK: Log walki ===
    log_rect = pygame.Rect(50, 210, screen.get_width() - 160, 150)
    log_lines = messages[-3:]

    for i, line in enumerate(log_lines):
        fragments = parse_message(line, players_info, enemy['name'] if enemy else None)
        x = log_rect.x + 10
        y = log_rect.y + 10 + i * 22

        for part, color in fragments:
            part_surface = small_font.render(part, True, color)
            screen.blit(part_surface, (x, y))
            x += part_surface.get_width()

    if your_turn:
        instruction_text = "1 - ATTACK          2 - HEAL            3 - PASS"
        instruction_surface = small_font.render(instruction_text, True, (255, 255, 255))
        instruction_rect = instruction_surface.get_rect(center=(screen.get_width() // 2, 310))
        screen.blit(instruction_surface, instruction_rect)

    # === DÓŁ: Avatary graczy ===
    avatars_y = 380
    avatar_size = 90

    for i, p in enumerate(players_info):
        # Wybierz avatar zależnie od stanu HP
        if p["hp"] <= 0:
            avatar_path = "assets/portraits/dead.png"
            name_color = (98, 98, 98)
            hp_color = (98, 98, 98)
        else:
            avatar_path = f"assets/portraits/{p.get('avatar', 'warrior')}.png"
            name_color = PLAYER_COLORS[i] if i < len(PLAYER_COLORS) else (255, 255, 255)
            hp_color = (255, 255, 255)

        try:
            avatar_img = pygame.image.load(avatar_path).convert_alpha()
            avatar_img = pygame.transform.scale(avatar_img, (avatar_size, avatar_size))
        except:
            # Jeśli avatar nie wczytany — placeholder
            avatar_img = pygame.Surface((avatar_size, avatar_size))
            avatar_img.fill((98, 98, 98))

        x = 35 + i * (avatar_size + 70)
        screen.blit(avatar_img, (x, avatars_y))

        # Nazwa gracza + HP
        name_surface = small_font.render(p["name"], True, name_color)
        hp_surface = small_font.render(f"HP: {p['hp']}/100", True, hp_color)

        name_rect = name_surface.get_rect(center=(x + avatar_size // 2, avatars_y - 38))
        hp_rect = hp_surface.get_rect(center=(x + avatar_size // 2, avatars_y - 15))

        screen.blit(name_surface, name_rect)
        screen.blit(hp_surface, hp_rect)

    pygame.display.flip()
