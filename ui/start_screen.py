import pygame
from .utils import load_font, wrap_text, InputBox, HoverableAvatar

def start_screen(screen):
    """Ekran startowy."""
    selected_avatar = None

    # === Wczytanie czcionek, tła, awatarów ===
    font = load_font(22)
    bg_image = pygame.image.load("assets/background/start.png").convert_alpha()
    avatar_files = ["warrior.png", "mage.png", "hunter.png", "warlock.png"]
    avatar_paths = [f"assets/portraits/{name}" for name in avatar_files]

    avatars = []
    for i, path in enumerate(avatar_paths):
        x = 20 + i * 160
        avatars.append(HoverableAvatar(path, (x, 320), scale=2))

    instructions = (
        "In the shadowed depths of Eldara, Heroes rise to challenge all evils.\n"
        "Assemble your party of four - enter your name and choose your avatar to begin the Quest.\n"
        "Press Enter when you're ready."
    )

    # === Pole do wpisania imienia ===
    input_box = InputBox(170, 235, 310, 36, font, placeholder="enter name")

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.blit(bg_image, (0, 0))

        # === Rysowanie instrukcji ===
        lines = []
        for paragraph in instructions.split('\n'):
            lines.extend(wrap_text(paragraph, font, 560))
        y = 100
        for line in lines:
            line_surf = font.render(line, True, (255, 255, 255))
            line_x = (screen.get_width() - line_surf.get_width()) // 2
            screen.blit(line_surf, (line_x, y))
            y += line_surf.get_height() + 4

        # === Pole tekstowe (imię gracza) ===
        input_box.draw(screen)

        # === Rysowanie awatarów do wyboru ===
        mouse_pos = pygame.mouse.get_pos()
        for avatar in avatars:
            avatar.update(mouse_pos)
            avatar.draw(screen)

        pygame.display.flip()

        # === Obsługa zdarzeń ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            input_box.handle_event(event)

            # Zatwierdzenie wyboru
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_box.is_valid() and selected_avatar is not None:
                        name = input_box.get_text()
                        chosen_avatar = avatar_files[selected_avatar].replace(".png", "")
                        return name, chosen_avatar

            # Wybór awatara
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, avatar in enumerate(avatars):
                    if avatar.handle_event(event):
                        selected_avatar = i
                        for j, a in enumerate(avatars):
                            a.selected = (j == i)

        clock.tick(30)

    return None
