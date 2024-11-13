import pygame
import random
import sys
import os
import platform

# Initialiser Pygame
pygame.init()

# Dimensions de la fenêtre de jeu pour un ratio 16:9
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 675
CELL_SIZE = 20

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialisation de la fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu du Serpent")

# Initialiser l'horloge pour contrôler les FPS
clock = pygame.time.Clock()

# Définir le chemin du fichier de score en fonction du système
def get_score_file_path():
    """Définit un chemin pour enregistrer le fichier de score dans un emplacement accessible à tous."""
    if platform.system() == "Windows":
        # Dossier AppData pour Windows
        base_dir = os.getenv("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
    elif platform.system() == "Darwin":
        # Dossier Application Support pour Mac
        base_dir = os.path.expanduser("~/Library/Application Support")
    else:
        # Dossier Documents pour Linux (ou par défaut)
        base_dir = os.path.expanduser("~/Documents")

    # Créer le dossier de l'application s'il n'existe pas
    app_dir = os.path.join(base_dir, "SnakeGame")
    os.makedirs(app_dir, exist_ok=True)

    # Chemin complet pour le fichier de score
    return os.path.join(app_dir, "meilleurs_scores.txt")

# Utiliser get_score_file_path() pour charger et sauvegarder le fichier de score
BEST_SCORES_FILE = get_score_file_path()

# Variables globales
snake_pos = [(100, 50), (90, 50), (80, 50)]
snake_direction = "DROITE"
change_direction = snake_direction
apple_pos = (
    random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
    random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE,
)
score = 0
SPEED = 15
fullscreen = False
difficulty = "Moyen"  # Options: Facile, Moyen, Difficile

# Charger les meilleurs scores depuis le fichier
def load_best_scores():
    scores = {"Facile": 0, "Moyen": 0, "Difficile": 0}
    try:
        with open(BEST_SCORES_FILE, "r") as file:
            for line in file:
                level, score = line.strip().split(":")
                scores[level] = int(score)
    except FileNotFoundError:
        save_best_scores(scores)
    return scores

# Sauvegarder les meilleurs scores dans le fichier
def save_best_scores(scores):
    with open(BEST_SCORES_FILE, "w") as file:
        for level, score in scores.items():
            file.write(f"{level}:{score}\n")

# Réinitialiser les meilleurs scores
def reset_best_scores():
    global best_scores
    best_scores = {"Facile": 0, "Moyen": 0, "Difficile": 0}
    save_best_scores(best_scores)

best_scores = load_best_scores()

def change_snake_direction(event_key, current_direction):
    """
    Change la direction du serpent en fonction de la touche pressée.
    """
    if event_key == pygame.K_UP and current_direction != "BAS":
        return "HAUT"
    elif event_key == pygame.K_DOWN and current_direction != "HAUT":
        return "BAS"
    elif event_key == pygame.K_LEFT and current_direction != "DROITE":
        return "GAUCHE"
    elif event_key == pygame.K_RIGHT and current_direction != "GAUCHE":
        return "DROITE"
    return current_direction

def toggle_fullscreen():
    """
    Bascule le mode plein écran.
    """
    global fullscreen, screen, SCREEN_WIDTH, SCREEN_HEIGHT
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    else:
        screen = pygame.display.set_mode((1200, 675))
        SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 675

def set_difficulty(level):
    """
    Définit la vitesse du serpent en fonction du niveau de difficulté.
    """
    global SPEED, difficulty
    difficulty = level
    if level == "Facile":
        SPEED = 10
    elif level == "Moyen":
        SPEED = 15
    elif level == "Difficile":
        SPEED = 20

def start_screen():
    """
    Affiche l'écran de démarrage avec des options pour démarrer, aller aux paramètres ou quitter.
    """
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 48)
        title = font.render("Jeu du Serpent", True, WHITE)
        play_text = font.render("Appuyez sur Entrée pour jouer", True, WHITE)
        settings_text = font.render("Appuyez sur S pour les paramètres", True, WHITE)
        quit_text = font.render("Appuyez sur Q pour quitter", True, WHITE)

        # Afficher les meilleurs scores
        score_text_easy = font.render(f"Meilleur score (Facile) : {best_scores['Facile']}", True, WHITE)
        score_text_medium = font.render(f"Meilleur score (Moyen) : {best_scores['Moyen']}", True, WHITE)
        score_text_hard = font.render(f"Meilleur score (Difficile) : {best_scores['Difficile']}", True, WHITE)

        # Centrage des éléments
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        play_text_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        settings_text_rect = settings_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        quit_text_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        score_text_easy_rect = score_text_easy.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140))
        score_text_medium_rect = score_text_medium.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 180))
        score_text_hard_rect = score_text_hard.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 220))

        # Dessin des éléments
        screen.blit(title, title_rect)
        screen.blit(play_text, play_text_rect)
        screen.blit(settings_text, settings_text_rect)
        screen.blit(quit_text, quit_text_rect)
        screen.blit(score_text_easy, score_text_easy_rect)
        screen.blit(score_text_medium, score_text_medium_rect)
        screen.blit(score_text_hard, score_text_hard_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Utiliser Entrée pour commencer
                    return  # Sortir de la fonction pour démarrer le jeu
                elif event.key == pygame.K_s:
                    settings_menu()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def settings_menu():
    """
    Panneau de paramètres pour modifier le plein écran, la difficulté, et réinitialiser les scores.
    """
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        title = font.render("Paramètres", True, WHITE)
        fullscreen_text = font.render("Appuyez sur F pour le plein écran", True, WHITE)
        reset_text = font.render("Appuyez sur R pour réinitialiser les meilleurs scores", True, WHITE)
        difficulty_text = font.render("Appuyez sur D pour changer la difficulté", True, WHITE)
        current_difficulty = font.render(f"Difficulté actuelle : {difficulty}", True, WHITE)

        # Centrage des éléments
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        fullscreen_text_rect = fullscreen_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        reset_text_rect = reset_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        difficulty_text_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        current_difficulty_rect = current_difficulty.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))

        # Dessin des éléments
        screen.blit(title, title_rect)
        screen.blit(fullscreen_text, fullscreen_text_rect)
        screen.blit(reset_text, reset_text_rect)
        screen.blit(difficulty_text, difficulty_text_rect)
        screen.blit(current_difficulty, current_difficulty_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    toggle_fullscreen()
                elif event.key == pygame.K_r:
                    reset_best_scores()
                elif event.key == pygame.K_d:
                    if difficulty == "Facile":
                        set_difficulty("Moyen")
                    elif difficulty == "Moyen":
                        set_difficulty("Difficile")
                    else:
                        set_difficulty("Facile")
                elif event.key == pygame.K_ESCAPE:
                    return

def game_loop():
    """
    Boucle principale du jeu.
    """
    global snake_direction, change_direction, score, apple_pos, SCREEN_WIDTH, SCREEN_HEIGHT, best_scores
    snake_pos = [(100, 50), (90, 50), (80, 50)]
    snake_direction = "DROITE"
    change_direction = snake_direction
    score = 0
    apple_pos = (
        random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE,
    )
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                change_direction = change_snake_direction(event.key, snake_direction)

        # Mise à jour de la direction du serpent
        snake_direction = change_direction
        x, y = snake_pos[0]

        if snake_direction == "HAUT":
            y -= CELL_SIZE
        elif snake_direction == "BAS":
            y += CELL_SIZE
        elif snake_direction == "GAUCHE":
            x -= CELL_SIZE
        elif snake_direction == "DROITE":
            x += CELL_SIZE

        new_head = (x, y)
        snake_pos.insert(0, new_head)

        snake_head_rect = pygame.Rect(new_head[0], new_head[1], CELL_SIZE, CELL_SIZE)
        apple_rect = pygame.Rect(apple_pos[0], apple_pos[1], CELL_SIZE, CELL_SIZE)

        if snake_head_rect.colliderect(apple_rect):
            score += 1
            apple_pos = (
                random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE,
            )
        else:
            snake_pos.pop()

        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT or new_head in snake_pos[1:]:
            running = False

        screen.fill(BLACK)
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, apple_rect)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score : {score}", True, WHITE)
        best_score_text = font.render(f"Meilleur Score ({difficulty}) : {best_scores[difficulty]}", True, WHITE)
        screen.blit(score_text, [10, 10])
        screen.blit(best_score_text, [10, 40])

        pygame.display.flip()
        clock.tick(SPEED)

    game_over()

def game_over():
    global best_scores, score, difficulty
    # Mettre à jour le meilleur score pour le niveau actuel
    if score > best_scores[difficulty]:
        best_scores[difficulty] = score
        save_best_scores(best_scores)

    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 48)
        text_game_over = font.render("Jeu Terminé", True, RED)
        text_restart = font.render("Appuyez sur R pour revenir à l'accueil ou Q pour quitter", True, WHITE)
        
        # Centrage du texte
        text_game_over_rect = text_game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        text_restart_rect = text_restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        
        screen.blit(text_game_over, text_game_over_rect)
        screen.blit(text_restart, text_restart_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()  # Retourner à l'écran d'accueil en relançant `main()`
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    """
    Fonction principale qui gère le cycle du jeu.
    """
    while True:
        start_screen()
        game_loop()

# Lancer la fonction principale pour démarrer le jeu
main()
pygame.quit()
