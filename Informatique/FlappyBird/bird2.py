# Importation des modules nécessaires
import pygame  # Module de jeu pour la création et gestion des graphiques et événements
import random  # Pour générer des valeurs aléatoires (utile pour les tuyaux)
import os  # Utilisé pour la gestion des chemins de fichiers
import sys  # Utilisé pour gérer le système de fichiers, notamment avec PyInstaller

# Initialisation de pygame pour préparer l'utilisation des modules internes
pygame.init()

# Définition des paramètres du jeu (dimensions de l'écran, de l'oiseau, tuyaux, etc.)
SCREEN_WIDTH = 400  # Largeur de la fenêtre du jeu
SCREEN_HEIGHT = 600  # Hauteur de la fenêtre du jeu
BIRD_WIDTH = 110  # Largeur de l'oiseau
BIRD_HEIGHT = 110  # Hauteur de l'oiseau
PIPE_WIDTH = 100  # Largeur des tuyaux
PIPE_GAP = 180  # Espace entre le haut et le bas des tuyaux pour que l'oiseau passe
GRAVITY = 0.6  # La gravité qui fait tomber l'oiseau
FLAP_STRENGTH = -9  # Force vers le haut quand l'oiseau "bat des ailes"
PIPE_SPEED = 4  # Vitesse de déplacement des tuyaux vers la gauche

# Création de la fenêtre du jeu avec les dimensions spécifiées
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Chargement des images utilisées dans le jeu
background_image = pygame.image.load("background.png").convert()  # Charger l'image d'arrière-plan
bird_image = pygame.image.load("flappy.png").convert_alpha()  # Charger l'image de l'oiseau
pipe_image = pygame.image.load("tuyaux.png").convert_alpha()  # Charger l'image des tuyaux

# Redimensionnement des images pour les ajuster à la taille de l'écran et des objets du jeu
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Adapter l'image d'arrière-plan à l'écran
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))  # Adapter l'image de l'oiseau
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, SCREEN_HEIGHT))  # Adapter l'image des tuyaux

# Création de masques pour l'oiseau et les tuyaux afin de gérer les collisions précises
bird_mask = pygame.mask.from_surface(bird_image)  # Masque pour détecter les collisions de l'oiseau
pipe_mask = pygame.mask.from_surface(pipe_image)  # Masque pour détecter les collisions des tuyaux

# Position initiale de l'oiseau
bird_x = 50  # Position de départ de l'oiseau sur l'axe horizontal
bird_y = SCREEN_HEIGHT // 2  # Position de départ de l'oiseau sur l'axe vertical (au centre de l'écran)
bird_velocity = 0  # Vitesse initiale de l'oiseau (immobile au départ)

# Liste des tuyaux (sera remplie au fur et à mesure) et score initial du joueur
pipes = []  # Liste vide pour stocker les tuyaux
score = 0  # Score initial du joueur

# Création d'une horloge pour contrôler la fréquence d'images (FPS)
clock = pygame.time.Clock()  # Permet de contrôler le temps du jeu

# Fonction pour obtenir le chemin d'une ressource (comme une image) dans PyInstaller
def resource_path(relative_path):
    """Obtenir le chemin absolu d'une ressource, fonctionne pour PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Si le jeu est emballé avec PyInstaller, les ressources sont dans _MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")  # Sinon, utiliser le chemin normal du système
    return os.path.join(base_path, relative_path)  # Retourner le chemin complet de la ressource

# Fonction pour réinitialiser le jeu (remettre à zéro après une perte)
def reset_game():
    global bird_y, bird_velocity, pipes, score  # Variables globales à réinitialiser
    bird_y = SCREEN_HEIGHT // 2  # Replacer l'oiseau au centre de l'écran verticalement
    bird_velocity = 0  # Réinitialiser la vitesse de l'oiseau à 0
    # Créer un premier tuyau avec une hauteur aléatoire
    pipes = [{"x": SCREEN_WIDTH, "height": random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50), "passed": False}]
    score = 0  # Réinitialiser le score à zéro

# Fonction pour faire voler l'oiseau (appuyer sur espace)
def flap():
    global bird_velocity  # On modifie la vitesse globale de l'oiseau
    bird_velocity = FLAP_STRENGTH  # Appliquer une force vers le haut

# Fonction pour mettre à jour la position de l'oiseau en fonction de la gravité
def update_bird():
    global bird_y, bird_velocity  # Variables globales à modifier
    bird_velocity += GRAVITY  # Appliquer la gravité (l'oiseau descend plus vite)
    bird_y += bird_velocity  # Mettre à jour la position verticale de l'oiseau avec sa vitesse
    # Si l'oiseau tombe au sol, on limite sa position
    if bird_y > SCREEN_HEIGHT - BIRD_HEIGHT:  # Si l'oiseau touche le sol
        bird_y = SCREEN_HEIGHT - BIRD_HEIGHT  # L'oiseau reste collé au sol
        return True  # Retourne True si l'oiseau touche le sol (le jeu est terminé)
    return False  # Sinon, continuer le jeu

# Fonction pour dessiner l'oiseau à sa position actuelle
def draw_bird():
    screen.blit(bird_image, (bird_x, bird_y))  # Dessiner l'image de l'oiseau sur l'écran

# Fonction pour mettre à jour la position des tuyaux (faire bouger les tuyaux vers la gauche)
def update_pipes():
    for pipe in pipes:  # Parcourir tous les tuyaux actuels
        pipe['x'] -= PIPE_SPEED  # Déplacer les tuyaux vers la gauche
    # Ajouter un nouveau tuyau une fois que le dernier s'est suffisamment déplacé
    if pipes[-1]['x'] < SCREEN_WIDTH - 300:
        pipes.append({"x": SCREEN_WIDTH, "height": random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50), "passed": False})
    # Retirer le premier tuyau s'il sort de l'écran
    if pipes[0]['x'] + PIPE_WIDTH < 0:
        pipes.pop(0)

# Fonction pour dessiner les tuyaux à l'écran
def draw_pipes():
    for pipe in pipes:  # Parcourir tous les tuyaux
        # Dessiner la partie supérieure (inversée) du tuyau
        screen.blit(pygame.transform.flip(pipe_image, False, True), (pipe['x'], pipe['height'] - SCREEN_HEIGHT))
        # Dessiner la partie inférieure du tuyau
        screen.blit(pipe_image, (pipe['x'], pipe['height'] + PIPE_GAP))

# Fonction pour vérifier les collisions entre l'oiseau et les tuyaux
def check_collision():
    global score  # Variable du score global à modifier
    bird_mask = pygame.mask.from_surface(bird_image)  # Masque de collision pour l'oiseau
    bird_rect = pygame.Rect(bird_x, bird_y, bird_image.get_width(), bird_image.get_height())  # Rectangle autour de l'oiseau
    for pipe in pipes:  # Parcourir tous les tuyaux
        # Créer des rectangles pour les parties supérieure et inférieure des tuyaux
        pipe_top_rect = pygame.Rect(pipe['x'], 0, pipe_image.get_width(), pipe['height'])
        pipe_bottom_rect = pygame.Rect(pipe['x'], pipe['height'] + PIPE_GAP, pipe_image.get_width(), SCREEN_HEIGHT - pipe['height'] - PIPE_GAP)
        # Masques de collision pour les deux parties des tuyaux
        pipe_top_mask = pygame.mask.from_surface(pygame.transform.flip(pipe_image, False, True))
        pipe_bottom_mask = pygame.mask.from_surface(pipe_image)
        # Calculer les décalages entre l'oiseau et les tuyaux pour vérifier les collisions
        offset_top = (pipe['x'] - bird_x, pipe['height'] - bird_y - SCREEN_HEIGHT)
        offset_bottom = (pipe['x'] - bird_x, pipe['height'] + PIPE_GAP - bird_y)
        # Si une collision est détectée avec la partie supérieure ou inférieure
        if bird_mask.overlap(pipe_top_mask, offset_top) or bird_mask.overlap(pipe_bottom_mask, offset_bottom):
            return True  # Retourner True pour indiquer une collision (game over)
        # Si l'oiseau passe un tuyau, augmenter le score
        if not pipe['passed'] and pipe['x'] + PIPE_WIDTH < bird_x:
            score += 1  # Augmenter le score
            pipe['passed'] = True  # Marquer le tuyau comme "passé"
    return False  # Retourner False si aucune collision n'est détectée

# Fonction pour afficher l'écran de "Game Over"
def game_over_screen():
    # Afficher "Game Over" avec une grande police
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))  # Centrer le texte
    screen.blit(text, text_rect)  # Dessiner le texte à l'écran
    # Afficher le score du joueur
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Centrer le texte
    replay_text_outline = font.render("Appuyez sur Espace pour rejouer", True, (0, 0, 0))  # Texte de redémarrage
    replay_text = font.render("Appuyez sur Espace pour rejouer", True, (255, 255, 255))  # Texte principal
    replay_rect = replay_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))  # Position du texte
    # Affichage avec contour (texte blanc avec un contour noir pour plus de visibilité)
    screen.blit(replay_text_outline, (replay_rect.x - 2, replay_rect.y))
    screen.blit(replay_text_outline, (replay_rect.x + 2, replay_rect.y))
    screen.blit(replay_text_outline, (replay_rect.x, replay_rect.y - 2))
    screen.blit(replay_text_outline, (replay_rect.x, replay_rect.y + 2))
    screen.blit(replay_text, replay_rect)  # Dessiner le texte de redémarrage
    screen.blit(score_text, score_rect)  # Dessiner le score à l'écran
    pygame.display.flip()  # Mettre à jour l'affichage
    # Boucle d'attente pour que le joueur appuie sur "Espace" pour rejouer
    waiting = True
    while waiting:
        for event in pygame.event.get():  # Parcourir les événements
            if event.type == pygame.QUIT:  # Si le joueur ferme la fenêtre
                pygame.quit()  # Quitter pygame
                exit()  # Quitter le programme
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Si le joueur appuie sur espace
                waiting = False  # Sortir de la boucle d'attente

# Fonction principale du jeu, où tout se passe
def main():
    reset_game()  # Réinitialiser le jeu au début
    running = True  # Drapeau pour garder la boucle du jeu en cours
    while running:
        screen.blit(background_image, (0, 0))  # Afficher l'arrière-plan à chaque image
        for event in pygame.event.get():  # Parcourir les événements
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                running = False  # Arrêter le jeu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Si le joueur appuie sur espace
                flap()  # Faire voler l'oiseau
        if update_bird() or check_collision():  # Vérifier si l'oiseau touche un tuyau ou le sol
            running = False  # Si oui, le jeu s'arrête
        update_pipes()  # Mettre à jour la position des tuyaux
        draw_bird()  # Dessiner l'oiseau
        draw_pipes()  # Dessiner les tuyaux
        # Afficher le score à l'écran
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # Texte du score
        screen.blit(score_text, (10, 10))  # Afficher le score en haut à gauche
        pygame.display.flip()  # Mettre à jour l'affichage du jeu
        clock.tick(60)  # Limiter la vitesse du jeu à 60 images par seconde
    # Une fois que l'oiseau perd, afficher l'écran Game Over
    game_over_screen()  
    pygame.time.delay(1000)  # Attendre une seconde avant de redémarrer
    main()  # Redémarrer le jeu

# Lancer le jeu si ce fichier est exécuté directement
if __name__ == "__main__":
    main()  # Appeler la fonction principale pour démarrer le jeu
