import pygame

# === Kolory graczy i przeciwnika potrzebne dla parse_message() ===
PLAYER_COLORS = [
    (89, 166, 64),    # green
    (128, 78, 163),   # purple
    (129, 175, 255),  # blue
    (255, 211, 91),   # yellow
]

ENEMY_COLOR = (174, 12, 23)
DEFAULT_COLOR = (255, 255, 255)

def load_font(size):
    return pygame.font.Font("assets/fonts/dpcomic.ttf", size)

class HoverableAvatar:
    def __init__(self, image_path, position, scale=1):
        original_image = pygame.image.load(image_path).convert_alpha()
        base_size = original_image.get_size()
        self.base_image = pygame.transform.scale(original_image, (base_size[0] * scale, base_size[1] * scale))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(topleft=position)
        self.position = position
        self.hovered = False
        self.selected = False
        self.scale = scale

    def update(self, mouse_pos):
        """Sprawdza czy myszka znajduje się nad awatarem."""
        self.hovered = self.rect.collidepoint(mouse_pos) or self.selected

    def draw(self, surface):
        """Rysuje awatar, zmieniając wygląd po najechaniu lub wybraniu."""
        img = self.base_image.copy()
        if self.hovered or self.selected:
            img.set_alpha(255)
            if self.hovered and not self.selected:
                img = pygame.transform.scale(img, (int(img.get_width() * 1.2), int(img.get_height() * 1.2)))
        else:
            img.set_alpha(180)

        rect = img.get_rect(center=self.rect.center)
        surface.blit(img, rect)
        self.rect = rect  # aktualizujemy hitbox po przeskalowaniu

    def handle_event(self, event):
        """Obsługa kliknięcia — zaznaczenie awataru."""
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.selected = True
            return True
        return False

class InputBox:
    def __init__(self, x, y, w, h, font, placeholder="enter your name", max_len=15):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.max_len = max(1, max_len) 
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        """Obsługa kliknięcia lub wpisywania tekstu."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_len and event.unicode.isprintable():
                self.text += event.unicode

    def draw(self, screen):
        """Rysuje pole tekstowe z tekstem lub placeholderem. Walidacja imienia."""
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

        # Kolor ramki
        border_color = (89, 166, 64) if self.is_valid() else (174, 12, 23)
        pygame.draw.rect(screen, border_color, self.rect, 5)

        # Placeholder
        if self.text:
            txt_surface = self.font.render(self.text, True, (0, 0, 0))
        else:
            txt_surface = self.font.render(self.placeholder, True, (150, 150, 150))

        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 8))

        # Symbol X przy nieprawidłowym tekście
        symbol = "" if self.is_valid() else "X"
        symbol_color = (174, 12, 23)
        symbol_surface = self.font.render(symbol, True, symbol_color)
        screen.blit(symbol_surface, (self.rect.right - 22, self.rect.y + 9))

    def get_text(self):
        return self.text.strip()

    def is_valid(self):
        return 3 <= len(self.text) <= 10

def wrap_text(text, font, max_width):
    """Dzieli tekst na linie, by zmieściły się w max_width."""
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())

    return lines

def parse_message(msg, players_info, enemy_name=None):
    """Dzieli wiadomość na fragmenty, kolorując odpowiednio imiona graczy i przeciwnika."""
    fragments = []

    words = msg.split(" ")
    i = 0
    while i < len(words):
        word = words[i]
        clean_word = word.strip(",.!?")

        # Match gracza
        player_matched = False
        for p_idx, p in enumerate(players_info):
            if clean_word == p["name"]:
                fragments.append((word, PLAYER_COLORS[p_idx]))
                player_matched = True
                break

        if not player_matched:
            # Match przeciwnika
            if enemy_name and clean_word == enemy_name:
                fragments.append((word, ENEMY_COLOR))
            else:
                fragments.append((word, DEFAULT_COLOR))

        i += 1

    # Dodanie spacji do fragmentów
    spaced_fragments = []
    for i, (txt, color) in enumerate(fragments):
        spaced_fragments.append((txt, color))
        if i != len(fragments) - 1:
            spaced_fragments.append((" ", DEFAULT_COLOR))

    return spaced_fragments
