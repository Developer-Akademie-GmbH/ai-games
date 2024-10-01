import pygame
import sys
import time

# Initialisierung von Pygame
pygame.init()

# Bildschirmgröße
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump and Run mit Münzen")

# Schriftart für Textanzeigen
font = pygame.font.SysFont(None, 36)

# Farben
GRASS_COLOR = (34, 139, 34)  # Grasgrün
SKY_COLOR = (135, 206, 235)  # Himmelsblau
PLATFORM_COLORS = [
    (255, 99, 71),    # Tomate
    (60, 179, 113),   # Mittelgrün
    (65, 105, 225),   # Kobaltblau
    (255, 215, 0),    # Gold
    (255, 140, 0),    # Dunkelorange
    (138, 43, 226)    # Blauviolett
]
BALL_COLOR = (255, 0, 0)        # Roter Ball
BALL_OUTLINE_COLOR = (0, 0, 0)  # Schwarzer Rand
COIN_COLOR = (255, 223, 0)      # Münzgelb

# Spielkonstanten
BALL_RADIUS = 20
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 5
MAX_SCROLL = 300          # Maximales Scrollen nach rechts
MAP_WIDTH = 6000           # Breite der Karte (doppelt so groß)
COIN_RADIUS = 10
TOTAL_COINS = 20           # Gesamtanzahl der Münzen

# Uhr für Framerate
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.vel_y = 0
        self.on_ground = False
        self.move_left = False
        self.move_right = False

    def update(self, platforms):
        # Horizontale Bewegung
        if self.move_left:
            self.rect.x -= PLAYER_SPEED
        if self.move_right:
            self.rect.x += PLAYER_SPEED

        # Begrenzen der Bewegung innerhalb der Karte
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > MAP_WIDTH:
            self.rect.right = MAP_WIDTH

        # Anwenden von Gravitation
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Kollision mit dem Boden
        ground_y = SCREEN_HEIGHT - 50
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Kollision mit Plattformen
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Überprüfen, ob der Spieler von oben kommt
                if self.vel_y > 0 and (self.rect.bottom - self.vel_y) <= platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

    def draw(self, screen, scroll):
        # Schatten zeichnen
        shadow_surface = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surface, (0, 0, 0, 50), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        screen.blit(shadow_surface, (self.rect.x + 5 - scroll, self.rect.y + 5))

        # Ball mit schwarzem Rand zeichnen
        pygame.draw.circle(screen, BALL_OUTLINE_COLOR, (self.rect.x - scroll + BALL_RADIUS, self.rect.y + BALL_RADIUS), BALL_RADIUS + 2)
        pygame.draw.circle(screen, BALL_COLOR, (self.rect.x - scroll + BALL_RADIUS, self.rect.y + BALL_RADIUS), BALL_RADIUS)

class Platform:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, scroll):
        # Schatten zeichnen
        shadow_offset = 5
        shadow_rect = self.rect.move(shadow_offset - scroll, shadow_offset)
        shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 50), shadow_surface.get_rect(), border_radius=10)
        screen.blit(shadow_surface, shadow_rect)

        # Plattform zeichnen
        pygame.draw.rect(screen, self.color, pygame.Rect(self.rect.x - scroll, self.rect.y, self.rect.width, self.rect.height), border_radius=10)

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - COIN_RADIUS, y - COIN_RADIUS, COIN_RADIUS * 2, COIN_RADIUS * 2)
        self.collected = False

    def draw(self, screen, scroll):
        if not self.collected:
            pygame.draw.circle(screen, COIN_COLOR, (self.rect.x - scroll + COIN_RADIUS, self.rect.y + COIN_RADIUS), COIN_RADIUS)

    def collect(self):
        self.collected = True

def main():
    # Spieler erstellen
    player = Player(100, SCREEN_HEIGHT - 100)

    # Plattformen erstellen
    platforms = []
    platform_specs = [
        (200, SCREEN_HEIGHT - 150, 200, 20),
        (500, SCREEN_HEIGHT - 250, 200, 20),
        (800, SCREEN_HEIGHT - 350, 200, 20),
        (1100, SCREEN_HEIGHT - 450, 200, 20),
        (1400, SCREEN_HEIGHT - 350, 200, 20),
        (1700, SCREEN_HEIGHT - 250, 200, 20),
        (2000, SCREEN_HEIGHT - 150, 200, 20),
        (2300, SCREEN_HEIGHT - 250, 200, 20),
        (2600, SCREEN_HEIGHT - 350, 200, 20),
        (2900, SCREEN_HEIGHT - 450, 200, 20),
        (3200, SCREEN_HEIGHT - 350, 200, 20),
        (3500, SCREEN_HEIGHT - 250, 200, 20),
        (3800, SCREEN_HEIGHT - 150, 200, 20),
        (4100, SCREEN_HEIGHT - 250, 200, 20),
        (4400, SCREEN_HEIGHT - 350, 200, 20),
        (4700, SCREEN_HEIGHT - 450, 200, 20),
        (5000, SCREEN_HEIGHT - 350, 200, 20),
        (5300, SCREEN_HEIGHT - 250, 200, 20),
        (5600, SCREEN_HEIGHT - 150, 200, 20),
        (5900, SCREEN_HEIGHT - 200, 200, 20)
    ]
    for spec in platform_specs:
        color = PLATFORM_COLORS[platform_specs.index(spec) % len(PLATFORM_COLORS)]
        platforms.append(Platform(*spec, color))

    # Münzen erstellen
    coins = []
    coin_positions = [
        (300, SCREEN_HEIGHT - 180),
        (600, SCREEN_HEIGHT - 280),
        (900, SCREEN_HEIGHT - 380),
        (1200, SCREEN_HEIGHT - 480),
        (1500, SCREEN_HEIGHT - 380),
        (1800, SCREEN_HEIGHT - 280),
        (2100, SCREEN_HEIGHT - 180),
        (2400, SCREEN_HEIGHT - 280),
        (2700, SCREEN_HEIGHT - 380),
        (3000, SCREEN_HEIGHT - 480),
        (3300, SCREEN_HEIGHT - 380),
        (3600, SCREEN_HEIGHT - 280),
        (3900, SCREEN_HEIGHT - 180),
        (4200, SCREEN_HEIGHT - 280),
        (4500, SCREEN_HEIGHT - 380),
        (4800, SCREEN_HEIGHT - 480),
        (5100, SCREEN_HEIGHT - 380),
        (5400, SCREEN_HEIGHT - 280),
        (5700, SCREEN_HEIGHT - 180),
        (5800, SCREEN_HEIGHT - 250),
        (5900, SCREEN_HEIGHT - 200)
    ]
    for pos in coin_positions:
        coins.append(Coin(*pos))

    coin_count = 0
    start_time = time.time()
    game_over = False
    end_time = 0

    running = True
    scroll = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Tastendruckereignisse
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_LEFT:
                    player.move_left = True
                if event.key == pygame.K_RIGHT:
                    player.move_right = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.move_left = False
                if event.key == pygame.K_RIGHT:
                    player.move_right = False

        if not game_over:
            # Aktualisieren
            player.update(platforms)

            # Überprüfen der Münzen
            for coin in coins:
                if not coin.collected and player.rect.colliderect(coin.rect):
                    coin.collect()
                    coin_count += 1
                    if coin_count == TOTAL_COINS:
                        game_over = True
                        end_time = time.time()

            # Scrollen, wenn der Spieler sich nach rechts bewegt und die Scrollgrenze nicht überschreitet
            if player.rect.centerx - scroll > SCREEN_WIDTH - MAX_SCROLL and scroll < MAP_WIDTH - SCREEN_WIDTH:
                scroll += PLAYER_SPEED
            elif player.rect.centerx - scroll < MAX_SCROLL and scroll > 0:
                scroll -= PLAYER_SPEED

            # Begrenzen des Scrolls
            if scroll < 0:
                scroll = 0
            elif scroll > MAP_WIDTH - SCREEN_WIDTH:
                scroll = MAP_WIDTH - SCREEN_WIDTH

        # Zeichnen
        screen.fill(SKY_COLOR)

        for platform in platforms:
            platform.draw(screen, scroll)

        for coin in coins:
            coin.draw(screen, scroll)

        player.draw(screen, scroll)

        # Anzeige der gesammelten Münzen
        score_surface = pygame.Surface((180, 50))
        score_surface.set_alpha(180)
        score_surface.fill((0, 0, 0))
        screen.blit(score_surface, (10, 10))
        score_text = font.render(f"Münzen: {coin_count}/{TOTAL_COINS}", True, (255, 255, 255))
        screen.blit(score_text, (20, 15))

        if game_over:
            # Gewinnmeldung anzeigen
            win_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            win_surface.fill((0, 0, 0, 180))  # Halbtransparenter schwarzer Hintergrund
            screen.blit(win_surface, (0, 0))
            win_text = font.render("Gewonnen!", True, (255, 255, 255))
            time_taken = end_time - start_time
            time_text = font.render(f"Zeit: {int(time_taken)} Sekunden", True, (255, 255, 255))
            screen.blit(win_text, ((SCREEN_WIDTH - win_text.get_width()) // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(time_text, ((SCREEN_WIDTH - time_text.get_width()) // 2, SCREEN_HEIGHT // 2 + 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()