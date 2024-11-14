# Initialiser Pygame d'abord
import pygame
import random
import sys
import os
import platform

# Initialiser Pygame et Pygame Mixer
pygame.init()
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
except pygame.error as e:
    print("Erreur d'initialisation du mixer :", e)
    sys.exit()

if not pygame.mixer.get_init():
    print("Erreur : le mixer n'a pas pu être initialisé.")
    sys.exit()

info_object = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info_object.current_w, info_object.current_h

SCALE_FACTOR = SCREEN_HEIGHT / 1080

# Taille de cellule du serpent et de la pomme
CELL_SIZE = int(20 * SCALE_FACTOR)

# Fonction pour obtenir le chemin des ressources
def resource_path(relative_path):
    """Obtenir le chemin absolu pour une ressource, que ce soit en mode développement ou avec PyInstaller .exe"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Exemple d’utilisation dans le code
pygame.mixer.music.load(resource_path("musique_fond.mp3"))
game_over_sound = pygame.mixer.Sound(resource_path("game_over.wav"))
font = pygame.font.Font(resource_path("PressStart2P.ttf"), int(28*SCALE_FACTOR))

# Police d'écriture rétro
try:
    retro_font = pygame.font.Font(resource_path("PressStart2P.ttf"), int(50*SCALE_FACTOR))
    retro_font2 = pygame.font.Font(resource_path("PressStart2P.ttf"), int(28*SCALE_FACTOR))
except FileNotFoundError:
    retro_font = pygame.font.Font(None, 50)
    retro_font2 = pygame.font.Font(None, 28)

# Utilisez `resource_path` dans tout le script pour accéder aux fichiers, par exemple :
# pygame.mixer.music.load(resource_path("musique_fond.mp3"))

# Autres parties du code restent inchangées...



# Initialiser Pygame et Pygame Mixer pour le son
pygame.init()
pygame.mixer.init()

# Dimensions de la fenêtre de jeu pour un ratio 16:9
# Taille de l'écran en plein écran d'origine
FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT = 1920, 1080
SCREEN_WIDTH, SCREEN_HEIGHT = FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT  # Valeurs initiales

CELL_SIZE = int(20 * SCALE_FACTOR)
  # Taille de cellule par défaut pour le serpent et la pomme

def resize_elements():
    """
    Ajuste la taille des éléments (CELL_SIZE) en fonction de la taille actuelle de la fenêtre
    par rapport aux dimensions en plein écran.
    """
    global CELL_SIZE

    # Calcul du facteur d'échelle en fonction du rapport de l'écran actuel par rapport au plein écran
    width_scale = SCREEN_WIDTH / FULLSCREEN_WIDTH
    height_scale = SCREEN_HEIGHT / FULLSCREEN_HEIGHT
    scale_factor = min(width_scale, height_scale)  # Utilise le facteur le plus petit pour préserver le ratio

    # Ajuste la taille de la cellule en fonction du facteur d'échelle
    CELL_SIZE = int(20 * SCALE_FACTOR)
  # Taille ajustée pour les éléments du jeu

CELL_SIZE = int(20 * SCALE_FACTOR)


# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialisation de la fenêtre de jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

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
    Bascule entre le mode plein écran et le mode fenêtré sans fermer le jeu.
    """
    global fullscreen, screen, SCREEN_WIDTH, SCREEN_HEIGHT
    fullscreen = not fullscreen  # Inverse le mode actuel
    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    else:
        # Mode fenêtré avec dimensions prédéfinies
        SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 675
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Ajuste la taille des éléments en fonction du nouveau mode
    resize_elements()


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
    Affiche l'écran de démarrage avec des options pour démarrer, aller aux paramètres, changer de langue, ou quitter.
    """
    global language  # S'assurer que la langue peut être modifiée

    # Textes pour les langues FR et EN
    texts = {
        "FR": {
            "title": "Snake",
            "play": "Appuyez sur Entrée pour jouer",
            "settings": "Appuyez sur S pour les paramètres",
            "quit": "Appuyez sur Q pour quitter",
            "change_language": "Appuyez sur L pour changer de langue",
            "best_score_easy": "Meilleur score (Facile) :",
            "best_score_medium": "Meilleur score (Moyen) :",
            "best_score_hard": "Meilleur score (Difficile) :"
        },
        "EN": {
            "title": "Snake",
            "play": "Press Enter to Play",
            "settings": "Press S for Settings",
            "quit": "Press Q to Quit",
            "change_language": "Press L to Change Language",
            "best_score_easy": "Best Score (Easy) :",
            "best_score_medium": "Best Score (Medium) :",
            "best_score_hard": "Best Score (Hard) :"
        }
    }

    pygame.mixer.music.load(resource_path("musique_fond.mp3"))  # Assurez-vous que le fichier "musique_fond.mp3" est dans le dossier
    pygame.mixer.music.set_volume(volume_level)  # Applique le volume défini avant de jouer la musique
    pygame.mixer.music.play(-1) # Lecture en boucle

    while True:
        screen.fill(BLACK)

        # Charger les textes en fonction de la langue actuelle
        lang_text = texts[language]

        # Charger la police
        try:
            font = pygame.font.Font(resource_path("PressStart2P.ttf"), int(32*SCALE_FACTOR))  # Police rétro pour titres et textes principaux
        except FileNotFoundError:
            font = pygame.font.Font(None, 32)  # Police par défaut

        # Affichage des textes avec adaptation de la langue
        title = font.render(lang_text["title"], True, WHITE)
        play_text = font.render(lang_text["play"], True, WHITE)
        settings_text = font.render(lang_text["settings"], True, WHITE)
        quit_text = font.render(lang_text["quit"], True, WHITE)
        
        # Meilleurs scores en fonction de la difficulté
        score_text_easy = font.render(f"{lang_text['best_score_easy']} {best_scores['Facile']}", True, WHITE)
        score_text_medium = font.render(f"{lang_text['best_score_medium']} {best_scores['Moyen']}", True, WHITE)
        score_text_hard = font.render(f"{lang_text['best_score_hard']} {best_scores['Difficile']}", True, WHITE)

        # Centrage des éléments
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 180))
        play_text_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        settings_text_rect = settings_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        quit_text_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        
        # Meilleurs scores centrés
        score_text_easy_rect = score_text_easy.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        score_text_medium_rect = score_text_medium.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
        score_text_hard_rect = score_text_hard.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 160))

        # Dessin des éléments sur l'écran
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
                elif event.key == pygame.K_l:
                    # Change la langue entre FR et EN
                    language = "EN" if language == "FR" else "FR"


# Niveau de volume global (initialement à 100 %)
volume_level = 1.0

def settings_menu():
    """
    Panneau de paramètres pour modifier le plein écran, la difficulté, le volume, réinitialiser les scores,
    activer/désactiver la musique, changer la langue et accéder à l'aide.
    """
    global language, volume_level
    line_spacing = 60  # Espacement entre les lignes pour améliorer la lisibilité

    while True:
        screen.fill(BLACK)
        
        # Charger les polices
        try:
            font_large = pygame.font.Font(resource_path("PressStart2P.ttf"), int(40*SCALE_FACTOR))  # Police plus grande pour le titre
            font = pygame.font.Font(resource_path("PressStart2P.ttf"), int(26*SCALE_FACTOR))
        except FileNotFoundError:
            font_large = pygame.font.Font(None, 40)
            font = pygame.font.Font(None, 26)

        # Textes en fonction de la langue sélectionnée
        texts = {
            "FR": {
                "title": "Paramètres",
                "reset_scores": "Appuyez sur R pour réinitialiser les meilleurs scores",
                "difficulty": "Appuyez sur D pour changer la difficulté",
                "current_difficulty": f"Difficulté actuelle : {difficulty}",
                "toggle_music": "Appuyez sur M pour activer/désactiver la musique",
                "toggle_language": "Appuyez sur L pour changer la langue",
                "volume_control": f"Volume : {int(volume_level * 100)}% (← / →)",
                "help": "Appuyez sur H pour voir l'aide"
            },
            "EN": {
                "title": "Settings",
                "reset_scores": "Press R to reset best scores",
                "difficulty": "Press D to change difficulty",
                "current_difficulty": f"Current difficulty: {difficulty}",
                "toggle_music": "Press M to toggle music",
                "toggle_language": "Press L to change language",
                "volume_control": f"Volume: {int(volume_level * 100)}% (← / →)",
                "help": "Press H for help"
            }
        }

        # Charger les textes en fonction de la langue courante
        language_texts = texts[language]

        # Affichage du titre en haut de l'écran
        title = font_large.render(language_texts["title"], True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))  # Position en haut
        screen.blit(title, title_rect)

        # Affichage des options du menu, centrées verticalement
        elements = [
            language_texts["reset_scores"],
            language_texts["difficulty"],
            language_texts["current_difficulty"],
            language_texts["toggle_music"],
            language_texts["toggle_language"],
            language_texts["volume_control"],
            language_texts["help"]
        ]
        
        # Calcul de la position de départ pour centrer les options verticalement
        total_height = line_spacing * len(elements)
        y_position = (SCREEN_HEIGHT // 2) - (total_height // 2) + 80  # Décalage pour descendre sous le titre

        for element in elements:
            rendered_text = font.render(element, True, WHITE)
            text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(rendered_text, text_rect)
            y_position += line_spacing

        pygame.display.flip()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_best_scores()
                elif event.key == pygame.K_d:
                    if difficulty == "Facile":
                        set_difficulty("Moyen")
                    elif difficulty == "Moyen":
                        set_difficulty("Difficile")
                    else:
                        set_difficulty("Facile")
                elif event.key == pygame.K_m:
                    toggle_music()
                elif event.key == pygame.K_l:
                    language = "EN" if language == "FR" else "FR"
                elif event.key == pygame.K_LEFT:
                    volume_level = max(0.0, round(volume_level - 0.05, 2))
                    pygame.mixer.music.set_volume(volume_level)
                elif event.key == pygame.K_RIGHT:
                    volume_level = min(1.0, round(volume_level + 0.05, 2))
                    pygame.mixer.music.set_volume(volume_level)
                elif event.key == pygame.K_h:
                    help_menu()  # Affiche l'aide
                elif event.key == pygame.K_ESCAPE:
                    return

def help_menu():
    """
    Affiche les règles et les touches du jeu.
    """
    global language
    line_spacing = 50  # Espacement entre les lignes dans le menu d'aide

    # Textes pour les règles et touches en FR et EN
    help_texts = {
        "FR": {
            "title": "Aide du Jeu",
            "rules": [
                "Le but du jeu est de contrôler le serpent pour manger",
                "la pomme sans toucher les murs ou le corps du serpent."
            ],
            "controls": [
                "Contrôles :",
                "Flèches pour bouger",
                "P pour mettre en pause",
                "Q pour quitter"
            ],
            "back": "Appuyez sur Echap pour revenir"
        },
        "EN": {
            "title": "Game Help",
            "rules": [
                "The objective is to control the snake to eat the",
                "apple without hitting walls or its own body."
            ],
            "controls": [
                "Controls:",
                "Arrow keys to move",
                "P to pause",
                "Q to quit"
            ],
            "back": "Press Escape to go back"
        }
    }

    while True:
        screen.fill(BLACK)
        try:
            font = pygame.font.Font(resource_path("PressStart2P.ttf"), int(24*SCALE_FACTOR))
        except FileNotFoundError:
            font = pygame.font.Font(None, 24)

        # Charger les textes en fonction de la langue actuelle
        current_help = help_texts[language]

        # Affichage des règles et touches
        y_position = SCREEN_HEIGHT // 2 - (line_spacing * (len(current_help["rules"]) + len(current_help["controls"]) + 3)) // 2
        elements = [current_help["title"]] + current_help["rules"] + [""] + current_help["controls"] + ["", current_help["back"]]

        for element in elements:
            rendered_text = font.render(element, True, WHITE)
            text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
            screen.blit(rendered_text, text_rect)
            y_position += line_spacing

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def resize_elements():
    """
    Ajuste la taille des éléments de jeu (CELL_SIZE, police) en fonction de la taille de la fenêtre actuelle.
    """
    global CELL_SIZE, font_size

    # Calcul du facteur d'échelle en fonction des dimensions actuelles par rapport au plein écran
    width_scale = SCREEN_WIDTH / FULLSCREEN_WIDTH
    height_scale = SCREEN_HEIGHT / FULLSCREEN_HEIGHT
    scale_factor = min(width_scale, height_scale)  # Utilise le facteur le plus petit pour garder le ratio

    # Ajuste la taille de cellule pour le serpent et la pomme
    CELL_SIZE = int(20 * SCALE_FACTOR)
  # Taille ajustée pour les éléments du jeu

    # Ajuste la taille de la police
    font_size = int(32 * SCALE_FACTOR)  # Par exemple, une police de base à 32 réduite proportionnellement



# Volume de la musique en mode de jeu et en pause
# Volume de la musique en mode normal et en mode pause
volume_active = 1.0  # Volume normal à 100 %
volume_paused = 0.3  # Volume réduit à 30 %

def pause_menu():
    """
    Met le jeu en pause, affiche un menu de pause, et permet de quitter la partie sans fermer le jeu.
    """
    paused = True
    pygame.mixer.music.set_volume(volume_level*0.3)  # Réduit le volume pendant la pause

    while paused:
        screen.fill(BLACK)
        font = pygame.font.Font(resource_path("PressStart2P.ttf"), int(32*SCALE_FACTOR)) if os.path.exists(resource_path("PressStart2P.ttf")) else pygame.font.Font(None, 32)
        
        # Texte de pause
        pause_text = font.render("Jeu en Pause", True, WHITE)
        resume_text = font.render("Appuyez sur Espace pour reprendre", True, WHITE)
        quit_text = font.render("Appuyez sur Q pour quitter la partie", True, WHITE)

        # Centrer et afficher le texte
        screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
        screen.blit(resume_text, resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(quit_text, quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Reprendre le jeu
                    pygame.mixer.music.set_volume(volume_level)  # Rétablit le volume normal
                    return False  # Indique de reprendre le jeu
                elif event.key == pygame.K_q:  # Quitter la partie
                    pygame.mixer.music.set_volume(volume_level)  # Rétablit le volume normal
                    return True  # Indique de quitter la partie



music_enabled = True

def toggle_music():
    """
    Active ou désactive la musique.
    """
    global music_enabled
    music_enabled = not music_enabled
    if music_enabled:
        pygame.mixer.music.set_volume(volume_level)
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

language = "FR"
texts = {
    "FR": {
        "start_game": "Appuyez sur Entrée pour jouer",
        "settings": "Appuyez sur S pour les paramètres",
        "quit": "Appuyez sur Q pour quitter",
        "pause": "Jeu en Pause",
        "resume": "Appuyez sur Espace pour reprendre",
        "exit": "Appuyez sur Q pour quitter",
        "music": "Appuyez sur M pour activer/désactiver la musique",
        "language": "Appuyez sur L pour changer de langue",
    },
    "EN": {
        "start_game": "Press Enter to Play",
        "settings": "Press S for Settings",
        "quit": "Press Q to Quit",
        "pause": "Game Paused",
        "resume": "Press Space to Resume",
        "exit": "Press Q to Quit",
        "music": "Press M to Toggle Music",
        "language": "Press L to Change Language",
    }
}

def toggle_language():
    """
    Bascule entre le français et l'anglais.
    """
    global language
    language = "EN" if language == "FR" else "FR"

music_started = False

def game_loop():
    """
    Boucle principale du jeu.
    """
    global snake_direction, change_direction, score, apple_pos, SCREEN_WIDTH, SCREEN_HEIGHT, best_scores, music_started
    snake_pos = [(100, 50), (90, 50), (80, 50)]
    snake_direction = "DROITE"
    change_direction = snake_direction
    score = 0
    apple_pos = (
        random.randrange(0, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
        random.randrange(0, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE,
    )
    running = True

    if music_enabled and not music_started:
        pygame.mixer.music.set_volume(volume_level)  # Applique le volume général
        pygame.mixer.music.play(-1)  # Lecture en boucle
        music_started = True  # Indique que la musique a déjà été lancée


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pause_menu():
                        return
                elif event.key == pygame.K_f:
                    # Bascule le mode plein écran / fenêtré sans fermer le jeu
                    toggle_fullscreen()
                else:
                    change_direction = change_snake_direction(event.key, snake_direction)

        # Mise à jour de la direction et des positions du serpent
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

        # Mise à jour et affichage du jeu
        new_head = (x, y)
        snake_pos.insert(0, new_head)

        # Collision avec la pomme
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

        # Collision avec les murs et le corps
        if x < 0 or x >= SCREEN_WIDTH or y < 0 or y >= SCREEN_HEIGHT or new_head in snake_pos[1:]:
            running = False

        # Dessin des éléments et affichage du score
        screen.fill(BLACK)
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, apple_rect)

        font = pygame.font.Font(resource_path("PressStart2P.ttf"), int(16 * SCALE_FACTOR))

        score_text = font.render(f"Score : {score}", True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.flip()
        clock.tick(SPEED)

    # Arrête la musique si le jeu se termine
    pygame.mixer.music.stop()
    game_over()




def game_over():
    global best_scores, score, difficulty, music_started

    # Arrêter la musique de fond et jouer le son de Game Over
    pygame.mixer.music.stop()
    music_started = False  # Réinitialise pour permettre à la musique de redémarrer dans la nouvelle partie

    if game_over_sound:
        game_over_sound.set_volume(volume_level)  # Applique le volume général au son de Game Over
        game_over_sound.play()

    # Mettre à jour le meilleur score pour le niveau actuel
    if score > best_scores[difficulty]:
        best_scores[difficulty] = score
        save_best_scores(best_scores)

    # Affichage du Game Over avec le score actuel et le meilleur score
    while True:
        screen.fill(BLACK)
        text_game_over = retro_font.render("GAME OVER", True, RED)
        text_score = retro_font2.render(f"Score : {score}", True, WHITE)
        best_score_text = retro_font2.render(f"Meilleur Score ({difficulty}) : {best_scores[difficulty]}", True, WHITE)
        text_restart = retro_font2.render("Appuyez sur Entrée pour revenir à l'accueil", True, WHITE)

        # Centrage du texte
        text_game_over_rect = text_game_over.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        text_score_rect = text_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        best_score_text_rect = best_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        text_restart_rect = text_restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))

        # Affichage du texte
        screen.blit(text_game_over, text_game_over_rect)
        screen.blit(text_score, text_score_rect)
        screen.blit(best_score_text, best_score_text_rect)
        screen.blit(text_restart, text_restart_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Retourner à l'écran d'accueil
                    main()  # Redémarrer le jeu en revenant à l'écran d'accueil
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()




# Charger la police rétro
try:
    retro_font = pygame.font.Font(resource_path("PressStart2P.ttf"), int(50 * SCALE_FACTOR))  # Police rétro arcade
except FileNotFoundError:
    retro_font = pygame.font.Font(None, 50)  # Police par défaut

try:
    retro_font2 = pygame.font.Font(resource_path("PressStart2P.ttf"), int(28 * SCALE_FACTOR))  # Police rétro arcade
except FileNotFoundError:
    retro_font2 = pygame.font.Font(None, 28)  # Police par défaut


# Charger et jouer la musique de fond
try:
    pygame.mixer.music.load(resource_path("musique_fond.mp3"))
    pygame.mixer.music.play(-1)  # Lecture en boucle
except FileNotFoundError:
    print("Musique de fond non trouvée.")

# Charger le son Game Over
try:
    game_over_sound = pygame.mixer.Sound(resource_path("game_over.wav"))
except FileNotFoundError:
    game_over_sound = None

def main():
    """
    Fonction principale qui gère le cycle du jeu et les paramètres.
    """
    while True:
        start_screen()  # Affiche l'écran de démarrage

        # Redimensionne les éléments en fonction du mode plein écran/fenêtré
        resize_elements()
        
        # Lance la boucle de jeu
        game_loop()

        # Arrête la musique si le jeu est terminé
        pygame.mixer.music.stop()

# Lancer la fonction principale pour démarrer le jeu
main()
pygame.quit()