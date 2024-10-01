import pygame
import sys

# Initialisierung
pygame.init()

# Bildschirmgröße
BREITE = 800
HOEHE = 600

# Farben
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)
BLAU = (0, 0, 255)
START_ZIEL = (181, 254, 180)  # B5FEB4
HINTERGRUND_1 = (230, 230, 255)  # E6E6FF
HINTERGRUND_2 = (247, 247, 255)  # F7F7FF
AUSSENBEREICH = (180, 181, 254)  # B4B5FE

# Spielfeld
SPIELFELD_X = 50
SPIELFELD_Y = 50
SPIELFELD_BREITE = BREITE - 100
SPIELFELD_HOEHE = HOEHE - 100

# Spieler
spieler_groesse = 20
spieler_x = SPIELFELD_X + 50
spieler_y = SPIELFELD_Y + SPIELFELD_HOEHE // 2
spieler_geschwindigkeit = 5

# Start- und Zielfläche
start_flaeche = pygame.Rect(SPIELFELD_X, SPIELFELD_Y + SPIELFELD_HOEHE // 2 - 50, 100, 100)
ziel_flaeche = pygame.Rect(SPIELFELD_X + SPIELFELD_BREITE - 100, SPIELFELD_Y + SPIELFELD_HOEHE // 2 - 50, 100, 100)

# Gegner
gegner = [
    {'x': SPIELFELD_X + 200, 'y': SPIELFELD_Y + 100, 'richtung_x': 1, 'richtung_y': 0, 'geschwindigkeit': 3},
    {'x': SPIELFELD_X + 400, 'y': SPIELFELD_Y + 200, 'richtung_x': 0, 'richtung_y': 1, 'geschwindigkeit': 2},
    {'x': SPIELFELD_X + 300, 'y': SPIELFELD_Y + 300, 'richtung_x': -1, 'richtung_y': 0, 'geschwindigkeit': 4},
    {'x': SPIELFELD_X + 500, 'y': SPIELFELD_Y + 400, 'richtung_x': 0, 'richtung_y': -1, 'geschwindigkeit': 3},
]

# Bildschirm erstellen
bildschirm = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Meine Version des schwersten Spiels der Welt")

# Hilfsfunktion zum Zeichnen des karierten Hintergrunds
def zeichne_karierten_hintergrund():
    kachel_groesse = 40
    for x in range(SPIELFELD_X, SPIELFELD_X + SPIELFELD_BREITE, kachel_groesse):
        for y in range(SPIELFELD_Y, SPIELFELD_Y + SPIELFELD_HOEHE, kachel_groesse):
            farbe = HINTERGRUND_1 if ((x - SPIELFELD_X) // kachel_groesse + (y - SPIELFELD_Y) // kachel_groesse) % 2 == 0 else HINTERGRUND_2
            breite = min(kachel_groesse, SPIELFELD_X + SPIELFELD_BREITE - x)
            hoehe = min(kachel_groesse, SPIELFELD_Y + SPIELFELD_HOEHE - y)
            pygame.draw.rect(bildschirm, farbe, (x, y, breite, hoehe))

# Spielschleife
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spielersteuerung
    keys = pygame.key.get_pressed()
    neue_x = spieler_x
    neue_y = spieler_y
    if keys[pygame.K_LEFT]:
        neue_x -= spieler_geschwindigkeit
    if keys[pygame.K_RIGHT]:
        neue_x += spieler_geschwindigkeit
    if keys[pygame.K_UP]:
        neue_y -= spieler_geschwindigkeit
    if keys[pygame.K_DOWN]:
        neue_y += spieler_geschwindigkeit

    # Spieler im Spielfeld halten
    spieler_x = max(SPIELFELD_X, min(neue_x, SPIELFELD_X + SPIELFELD_BREITE - spieler_groesse))
    spieler_y = max(SPIELFELD_Y, min(neue_y, SPIELFELD_Y + SPIELFELD_HOEHE - spieler_groesse))

    # Gegnerbewegung
    for g in gegner:
        g['x'] += g['geschwindigkeit'] * g['richtung_x']
        g['y'] += g['geschwindigkeit'] * g['richtung_y']
        
        # Richtungsänderung bei Kollision mit Spielfeldrand
        if g['x'] <= SPIELFELD_X or g['x'] >= SPIELFELD_X + SPIELFELD_BREITE:
            g['richtung_x'] *= -1
        if g['y'] <= SPIELFELD_Y or g['y'] >= SPIELFELD_Y + SPIELFELD_HOEHE:
            g['richtung_y'] *= -1

    # Kollisionserkennung mit Gegnern
    spieler_rect = pygame.Rect(spieler_x, spieler_y, spieler_groesse, spieler_groesse)
    for g in gegner:
        gegner_rect = pygame.Rect(g['x'] - 10, g['y'] - 10, 20, 20)
        if spieler_rect.colliderect(gegner_rect):
            print("Game Over!")
            running = False

    # Ziel erreicht?
    if ziel_flaeche.collidepoint(spieler_x, spieler_y):
        print("Gewonnen!")
        running = False

    # Zeichnen
    bildschirm.fill(AUSSENBEREICH)  # Hintergrund für den Außenbereich
    zeichne_karierten_hintergrund()  # Karierter Spielbereich
    
    # Schwarzer Rand um das Spielfeld
    pygame.draw.rect(bildschirm, SCHWARZ, (SPIELFELD_X - 2, SPIELFELD_Y - 2, SPIELFELD_BREITE + 4, SPIELFELD_HOEHE + 4), 2)
    
    # Start- und Zielfläche zeichnen
    pygame.draw.rect(bildschirm, START_ZIEL, start_flaeche)
    pygame.draw.rect(bildschirm, START_ZIEL, ziel_flaeche)
    
    # Spieler zeichnen
    pygame.draw.rect(bildschirm, BLAU, (spieler_x, spieler_y, spieler_groesse, spieler_groesse))
    
    # Gegner zeichnen
    for g in gegner:
        pygame.draw.circle(bildschirm, ROT, (int(g['x']), int(g['y'])), 10)

    pygame.display.flip()
    clock.tick(60)

# Spiel beenden
pygame.quit()
sys.exit()