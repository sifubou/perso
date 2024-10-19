import pygame
import random

# Initialiser Pygame
pygame.init()

# Constantes du jeu
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
PIPE_WIDTH = 80
PIPE_GAP = 220  # Augmenter l'espace entre les tuyaux
GRAVITY = 1
FLAP_STRENGTH = -12
PIPE_SPEED = 7  # Augmenter la vitesse des tuyaux

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Variables globales pour l'oiseau
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0

# Variables globales pour les tuyaux
pipes = []
score = 0

# Créer la fenêtre du jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def reset_game():
    global bird_y, bird_velocity, pipes, score
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipes = [{"x": SCREEN_WIDTH, "height": random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50), "passed": False}]
    score = 0

def flap():
    global bird_velocity
    bird_velocity = FLAP_STRENGTH

def update_bird():
    global bird_y, bird_velocity
    bird_velocity += GRAVITY
    bird_y += bird_velocity

    # Si l'oiseau touche le sol, on arrête le jeu
    if bird_y > SCREEN_HEIGHT - BIRD_HEIGHT:
        bird_y = SCREEN_HEIGHT - BIRD_HEIGHT
        return True  # Game over si l'oiseau touche le sol

    return False  # Le jeu continue

def draw_bird():
    pygame.draw.rect(screen, GREEN, (bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT))

def update_pipes():
    for pipe in pipes:
        pipe['x'] -= PIPE_SPEED  # Vitesse augmentée

    # Ajouter de nouveaux tuyaux et espacer davantage
    if pipes[-1]['x'] < SCREEN_WIDTH - 300:  # Augmenter l'espace entre les tuyaux
        pipes.append({"x": SCREEN_WIDTH, "height": random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50), "passed": False})
    
    if pipes[0]['x'] + PIPE_WIDTH < 0:
        pipes.pop(0)

def draw_pipes():
    for pipe in pipes:
        pygame.draw.rect(screen, RED, (pipe['x'], 0, PIPE_WIDTH, pipe['height']))
        pygame.draw.rect(screen, RED, (pipe['x'], pipe['height'] + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

def check_collision():
    global score
    for pipe in pipes:
        # Collision avec les tuyaux
        if bird_x + BIRD_WIDTH > pipe['x'] and bird_x < pipe['x'] + PIPE_WIDTH:
            if bird_y < pipe['height'] or bird_y + BIRD_HEIGHT > pipe['height'] + PIPE_GAP:
                return True  # Collision détectée
        # Comptage du score si on passe un tuyau
        if not pipe['passed'] and pipe['x'] + PIPE_WIDTH < bird_x:
            score += 1
            pipe['passed'] = True
    return False  # Pas de collision

def game_over_screen():
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    replay_text_outline = font.render("Appuyez sur Espace pour rejouer", True, BLACK)
    replay_text = font.render("Appuyez sur Espace pour rejouer", True, WHITE)
    replay_rect = replay_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(replay_text_outline, (replay_rect.x - 2, replay_rect.y))
    screen.blit(replay_text_outline, (replay_rect.x + 2, replay_rect.y))
    screen.blit(replay_text_outline, (replay_rect.x, replay_rect.y - 2))
    screen.blit(replay_text_outline, (replay_rect.x, replay_rect.y + 2))
    screen.blit(replay_text, replay_rect)

    screen.blit(score_text, score_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def main():
    reset_game()
    running = True
    while running:
        screen.fill(WHITE)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flap()

        # Mise à jour de l'oiseau et des tuyaux
        if update_bird() or check_collision():
            running = False  # Fin du jeu si collision ou touche le sol

        update_pipes()

        # Dessiner l'oiseau et les tuyaux
        draw_bird()
        draw_pipes()

        # Affichage du score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Mise à jour de l'écran
        pygame.display.flip()
        clock.tick(30)

    # Afficher l'écran de fin
    game_over_screen()
    main()  # Relancer le jeu après la fin

if __name__ == "__main__":
    main()