import pygame
from .utils import load_font, wrap_text

def end_screen(screen, result_text):
    """Ekran końcowy."""

    # === Czcionka ===
    font = load_font(30)

    # === Wybór tła i tekstu w zależności od wyniku ===
    if result_text.lower() == "victory":
        bg_image = pygame.image.load("assets/background/victory.png").convert()
        description_text = (
            "Congratulations - Your team has endured the dungeon and found the hidden treasure. "
            "Your names will forever echo in legends."
        )
    else:
        bg_image = pygame.image.load("assets/background/defeat.png").convert()
        description_text = (
            "Rest in Peace - Your team has fallen. "
            "Your dead bodies will forever remain in the darkness of the dungeon."
        )

    # === Zawijanie opisu na linie ===
    wrapped_lines = wrap_text(description_text, font, 560)

    running = True
    clock = pygame.time.Clock()

    while running:
        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.blit(bg_image, (0, 0))

        # Opis fabularny
        y = 280
        for line in wrapped_lines:
            line_surface = font.render(line, True, (255, 255, 255))
            line_rect = line_surface.get_rect(center=(screen.get_width() // 2, y))
            screen.blit(line_surface, line_rect)
            y += line_surface.get_height() + 5

        # Instrukcja wyjścia
        instruction_text = "Press ESC to exit"
        instruction_surface = font.render(instruction_text, True, (255, 255, 255))
        instruction_rect = instruction_surface.get_rect(center=(screen.get_width() // 2, 400))
        screen.blit(instruction_surface, instruction_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
