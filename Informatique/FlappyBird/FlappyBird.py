import pygame
import random
import os
import sys

# Fonction pour obtenir le chemin du fichier de score, stocké dans le répertoire utilisateur
def chemin_fichier_score():
    home_dir = os.path.expanduser("~")  # Récupère le répertoire de l'utilisateur (fonctionne sur Windows, Linux, Mac)
    return os.path.join(home_dir, "best_score.txt")  # Stocke le fichier dans ce répertoire

# Charger ou créer le fichier contenant le meilleur score
BEST_SCORE_FILE = chemin_fichier_score()

# Lire le meilleur score à partir du fichier. Si le fichier n'existe pas ou est corrompu, retourner 0
def read_best_score():
    if os.path.exists(BEST_SCORE_FILE):
        with open(BEST_SCORE_FILE, 'r') as f:
            try:
                return int(f.read())  # Tenter de lire et convertir en entier
            except ValueError:  # Si le fichier est vide ou corrompu, renvoyer 0
                return 0
    return 0  # Retourner 0 si le fichier n'existe pas

# Écrire un nouveau meilleur score dans le fichier
def write_best_score(new_score):
    with open(BEST_SCORE_FILE, 'w') as f:
        f.write(str(new_score))

# Fonction pour gérer les chemins d'accès aux fichiers dans les bundles créés par PyInstaller
def chemin_relatif(chemin):
    if hasattr(sys, '_MEIPASS'):  # Si le programme est exécuté via un bundle PyInstaller
        return os.path.join(sys._MEIPASS, chemin)  # Utiliser le chemin interne du bundle
    return chemin  # Sinon, retourner le chemin normal

# Initialisation des modules Pygame
pygame.init()

# Définir les dimensions de l'écran, la taille de l'oiseau, et d'autres constantes
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 110
BIRD_HEIGHT = 110
PIPE_WIDTH = 100
PIPE_GAP = 180
GRAVITY = 0.6  # Gravité appliquée à l'oiseau
FLAP_STRENGTH = -9  # Force de chaque battement d'ailes
PIPE_SPEED = 4  # Vitesse initiale des tuyaux

# Créer la fenêtre du jeu
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Charger et redimensionner les images nécessaires au jeu
background_image = pygame.image.load(chemin_relatif("images/background.png")).convert()
bird_image = pygame.image.load(chemin_relatif("images/flappy.png")).convert_alpha()
pipe_image = pygame.image.load(chemin_relatif("images/tuyaux2.png")).convert_alpha()

background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, SCREEN_HEIGHT))

# Générer des masques pour détecter les collisions (basé sur les pixels non transparents)
bird_mask = pygame.mask.from_surface(bird_image)
pipe_mask = pygame.mask.from_surface(pipe_image)

# Position initiale de l'oiseau
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0  # Vitesse verticale initiale de l'oiseau
collided_with_pipe = False  # Indicateur de collision avec un tuyau

pipes = []  # Liste des tuyaux à gérer
score = 0  # Score du joueur
best_score = read_best_score()  # Charger le meilleur score depuis le fichier

# Gestion du temps
clock = pygame.time.Clock()

# Variables liées à l'augmentation de la difficulté
LEVEL_UP_SCORE = 100  # Score nécessaire pour augmenter la difficulté
LEVEL_UP_SCORE_PIPE = 20  # Score pour augmenter la vitesse des tuyaux
pipe_speed_increase = 0  # Augmentation progressive de la vitesse horizontale des tuyaux
pipe_vertical_speed_increase = 0  # Augmentation de la vitesse verticale des tuyaux
MAX_PIPE_SPEED = 6.5  # Limite supérieure pour la vitesse horizontale des tuyaux
MAX_VERTICAL_SPEED = 3  # Limite supérieure pour la vitesse verticale

# Charger les sons pour les interactions du jeu
flap_sound = pygame.mixer.Sound(chemin_relatif("sons/flap.wav"))
point_sound = pygame.mixer.Sound(chemin_relatif("sons/point.wav"))
collision_sound = pygame.mixer.Sound(chemin_relatif("sons/collision.wav"))

# Réinitialisation du jeu (après une collision ou lors du démarrage)
def reset_game():
    global bird_y, bird_velocity, pipes, score, collided_with_pipe, pipe_speed_increase, pipe_vertical_speed_increase
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    pipe_speed_increase = 0  # Réinitialiser la vitesse des tuyaux
    pipe_vertical_speed_increase = 0  # Réinitialiser le mouvement vertical des tuyaux
    pipes = [{"x": SCREEN_WIDTH, "height": random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50), 
              "passed": False, "direction": random.choice([-1, 1])}]  # Ajouter un premier tuyau
    score = 0
    collided_with_pipe = False  # Réinitialiser la collision

# Fonction pour faire voler l'oiseau
def flap():
    global bird_velocity, collided_with_pipe
    if not collided_with_pipe:  # Empêcher de voler après une collision
        bird_velocity = FLAP_STRENGTH
        flap_sound.play()  # Jouer le son du battement d'ailes

# Met à jour la position de l'oiseau
def update_bird():
    global bird_y, bird_velocity
    bird_velocity += GRAVITY  # Appliquer la gravité pour faire tomber l'oiseau
    bird_y += bird_velocity
    if bird_y > SCREEN_HEIGHT - BIRD_HEIGHT:  # Empêcher l'oiseau de sortir par le bas de l'écran
        bird_y = SCREEN_HEIGHT - BIRD_HEIGHT
        return True  # Retourner True si l'oiseau touche le sol
    return False

# Calculer l'angle de rotation de l'oiseau en fonction de sa vitesse
def calculate_bird_angle():
    angle = min(max(bird_velocity * -3, -90), 25)  # Limiter l'angle pour qu'il reste naturel
    return angle

# Dessiner l'oiseau avec la bonne rotation
def draw_bird():
    angle = calculate_bird_angle()
    rotated_bird = pygame.transform.rotate(bird_image, angle)  # Appliquer la rotation
    bird_rect = rotated_bird.get_rect(center=(bird_x + BIRD_WIDTH // 2, bird_y + BIRD_HEIGHT // 2))  # Centrer l'image
    screen.blit(rotated_bird, bird_rect.topleft)  # Dessiner l'oiseau

# Mise à jour des tuyaux
def update_pipes():
    global PIPE_SPEED, pipe_speed_increase, pipe_vertical_speed_increase
    
    # Augmenter la vitesse des tuyaux progressivement
    if score >= 30 and (score - 30) % LEVEL_UP_SCORE_PIPE == 0:
        pipe_speed_increase += 0.0075
    
    current_pipe_speed = min(PIPE_SPEED + pipe_speed_increase, MAX_PIPE_SPEED)  # Limiter la vitesse max
    
    if score >= 100 and score % LEVEL_UP_SCORE == 0:
        pipe_vertical_speed_increase += 0.10
    
    current_vertical_speed = min(1.2 + pipe_vertical_speed_increase, MAX_VERTICAL_SPEED)  # Limiter la vitesse verticale
    
    for pipe in pipes:
        pipe['x'] -= current_pipe_speed  # Déplacer les tuyaux horizontalement
        if score >= 75:  # Déplacement vertical après un certain score
            pipe['height'] += pipe['direction'] * current_vertical_speed  # Ajuster la hauteur
            if pipe['height'] <= 50 or pipe['height'] >= SCREEN_HEIGHT - PIPE_GAP - 50:
                pipe['direction'] *= -1  # Inverser la direction si les tuyaux dépassent certaines limites

    # Ajouter de nouveaux tuyaux quand il y a assez d'espace
    if pipes[-1]['x'] < SCREEN_WIDTH - 420:
        pipes.append({"x": SCREEN_WIDTH, "height": random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50), 
                      "passed": False, "direction": random.choice([-1, 1])})
    
    if pipes[0]['x'] + PIPE_WIDTH < 0:  # Supprimer les tuyaux hors écran
        pipes.pop(0)

# Dessiner les tuyaux à l'écran
def draw_pipes():
    for pipe in pipes:
        # Dessiner le tuyau du haut (inversé verticalement)
        screen.blit(pygame.transform.flip(pipe_image, False, True), (pipe['x'], pipe['height'] - SCREEN_HEIGHT))
        # Dessiner le tuyau du bas
        screen.blit(pipe_image, (pipe['x'], pipe['height'] + PIPE_GAP))

# Vérification des collisions avec les tuyaux
def check_collision():
    global score, collided_with_pipe
    bird_mask = pygame.mask.from_surface(bird_image)
    bird_rect = pygame.Rect(bird_x, bird_y, bird_image.get_width(), bird_image.get_height())
    
    for pipe in pipes:
        # Rectangles de collision pour les tuyaux
        pipe_top_rect = pygame.Rect(pipe['x'], 0, pipe_image.get_width(), pipe['height'])
        pipe_bottom_rect = pygame.Rect(pipe['x'], pipe['height'] + PIPE_GAP, pipe_image.get_width(), SCREEN_HEIGHT - pipe['height'] - PIPE_GAP)
        
        # Masques pour les collisions précises
        pipe_top_mask = pygame.mask.from_surface(pygame.transform.flip(pipe_image, False, True))
        pipe_bottom_mask = pygame.mask.from_surface(pipe_image)
        
        # Offsets pour ajuster la position relative des masques
        offset_top = (pipe['x'] - bird_x, pipe['height'] - bird_y - SCREEN_HEIGHT)
        offset_bottom = (pipe['x'] - bird_x, pipe['height'] + PIPE_GAP - bird_y)
        
        # Si une collision est détectée avec l'un des tuyaux
        if bird_mask.overlap(pipe_top_mask, offset_top) or bird_mask.overlap(pipe_bottom_mask, offset_bottom):
            collided_with_pipe = True
            collision_sound.play()  # Jouer le son de collision
            pygame.time.delay(250)  # Pause pour que la collision soit visible
            return True  # Retourner True pour signaler la collision
        
        # Comptabiliser les points lorsque l'oiseau passe un tuyau
        if not pipe['passed'] and pipe['x'] + PIPE_WIDTH < bird_x:
            score += 1
            point_sound.play()  # Jouer le son du point
            pipe['passed'] = True
    return False

# Écran de fin de jeu (après une collision)
def game_over_screen():
    global best_score
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    screen.blit(text, text_rect)
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    # Si le score actuel est supérieur au meilleur score, mettre à jour le fichier de score
    if score > best_score:
        best_score = score
        write_best_score(best_score)
    
    best_score_text = font.render(f"Best Score: {best_score}", True, (0, 0, 0))
    best_score_rect = best_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    
    # Texte pour rejouer
    replay_text_outline = font.render("Appuyez sur Espace pour rejouer", True, (0, 0, 0))
    replay_text = font.render("Appuyez sur Espace pour rejouer", True, (255, 255, 255))
    replay_rect = replay_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    
    # Dessiner un effet de contour noir autour du texte
    screen.blit(replay_text_outline, (replay_rect.x - 2, replay_rect.y))
    screen.blit(replay_text_outline, (replay_rect.x + 2, replay_rect.y))
    screen.blit(replay_text_outline, (replay_rect.x, replay_rect.y - 2))
    screen.blit(replay_text_outline, (replay_rect.x, replay_rect.y + 2))
    
    screen.blit(replay_text, replay_rect)
    screen.blit(score_text, score_rect)
    screen.blit(best_score_text, best_score_rect)
    
    pygame.display.flip()  # Mettre à jour l'écran
    
    waiting = True
    while waiting:  # Boucle pour attendre que le joueur appuie sur Espace
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False  # Quitter l'écran de fin et recommencer le jeu

# Écran de démarrage avant le début du jeu
def start_screen():
    font = pygame.font.Font(None, 40)
    text = font.render("Appuyez sur Espace", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    screen.blit(background_image, (0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()  # Mettre à jour l'écran
    
    waiting = True
    while waiting:  # Attendre que le joueur appuie sur Espace pour commencer
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

# Boucle principale du jeu
def main():
    global collided_with_pipe
    reset_game()  # Réinitialiser l'état du jeu
    start_screen()  # Afficher l'écran de démarrage
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Dessiner le fond
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flap()  # Faire voler l'oiseau si Espace est pressé
        
        if not collided_with_pipe:  # L'oiseau continue de voler jusqu'à une collision
            if check_collision():  # Vérifier les collisions avec les tuyaux
                collided_with_pipe = True  # L'oiseau arrête de voler après une collision
        
        update_bird()  # Mettre à jour la position de l'oiseau
        
        if bird_y >= SCREEN_HEIGHT - BIRD_HEIGHT:  # Vérifier si l'oiseau a touché le sol
            running = False  # Arrêter le jeu si l'oiseau touche le sol
        
        update_pipes()  # Mettre à jour les tuyaux
        draw_bird()  # Dessiner l'oiseau
        draw_pipes()  # Dessiner les tuyaux
        
        # Afficher le score à l'écran
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()  # Mettre à jour l'écran
        clock.tick(60)  # Limiter le jeu à 60 FPS
    
    game_over_screen()  # Afficher l'écran de fin
    pygame.time.delay(1000)  # Petite pause avant de relancer le jeu
    main()  # Redémarrer le jeu automatiquement après la fin

# Lancer le jeu
if __name__ == "__main__":
    main()