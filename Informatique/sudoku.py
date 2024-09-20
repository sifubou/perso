import tkinter as tk  # Importer la bibliothèque tkinter pour créer l'interface graphique
from tkinter import messagebox  # Importer messagebox pour afficher des messages d'alerte ou d'information
from random import sample  # Importer sample pour mélanger les éléments d'une liste

class Sudoku:  # Définir une classe Sudoku pour regrouper toutes les fonctionnalités du jeu
    def __init__(self, fenetre):  # Initialiser le jeu de Sudoku
        self.fenetre = fenetre  # Stocker la fenêtre principale
        self.fenetre.title("Sudoku - Jeu épuré")  # Définir le titre de la fenêtre
        self.taille_grille = 9  # Définir la taille de la grille de Sudoku (9x9)
        self.taille_sous_grille = 3  # Définir la taille des sous-grilles (3x3)
        self.erreurs_max = 5  # Définir le nombre maximum d'erreurs autorisées
        self.erreurs = 0  # Initialiser le compteur d'erreurs à 0

        self.difficulte = 'facile'  # Définir la difficulté par défaut sur "facile"

        # Générer la solution complète du Sudoku
        self.solution = self.generer_grille_complete()
        # Créer une grille jouable en retirant des chiffres de la solution
        self.grille = self.creer_grille_jouable(self.solution)

        # Créer tous les éléments graphiques de l'interface utilisateur
        self.creer_widgets()

    def creer_widgets(self):
        """Créer les éléments de l'interface graphique."""
        self.cadre = tk.Frame(self.fenetre)  # Créer un cadre dans la fenêtre principale pour contenir la grille
        self.cadre.pack()  # Ajouter ce cadre à la fenêtre

        # Créer un canvas pour dessiner les lignes de la grille
        self.canvas = tk.Canvas(self.cadre, width=450, height=450, bg="white")  # Taille fixe 450x450 px
        self.canvas.grid(row=0, column=0)  # Placer le canvas dans le cadre

        self.taille_cellule = 50  # Définir la taille de chaque cellule dans la grille

        # Créer une grille 2D pour les cellules et les entrées (9x9)
        self.cellules = [[None for _ in range(self.taille_grille)] for _ in range(self.taille_grille)]
        self.entrees = [[None for _ in range(self.taille_grille)] for _ in range(self.taille_grille)]

        # Remplir la grille avec les entrées et les cellules
        for ligne in range(self.taille_grille):  # Parcourir chaque ligne de la grille
            for colonne in range(self.taille_grille):  # Parcourir chaque colonne de la grille
                x1 = colonne * self.taille_cellule  # Calculer la coordonnée x de la cellule
                y1 = ligne * self.taille_cellule  # Calculer la coordonnée y de la cellule
                x2 = x1 + self.taille_cellule  # Calculer la coordonnée x de la cellule suivante
                y2 = y1 + self.taille_cellule  # Calculer la coordonnée y de la cellule suivante

                valeur_cellule = tk.StringVar()  # Créer une variable pour stocker la valeur saisie dans chaque cellule
                self.cellules[ligne][colonne] = valeur_cellule  # Associer cette variable à la cellule correspondante

                # Créer une entrée (champ de texte) pour chaque cellule
                entree = tk.Entry(self.cadre, textvariable=valeur_cellule, width=2, justify='center', font=("Arial", 20))
                self.entrees[ligne][colonne] = entree  # Stocker l'entrée dans la grille d'entrées

                # Placer l'entrée dans la fenêtre (sur le canvas)
                entree.place(x=x1 + 2, y=y1 + 2, width=self.taille_cellule - 4, height=self.taille_cellule - 4)

                # Si la cellule contient une valeur dans la grille initiale, la verrouiller
                if self.grille[ligne][colonne] != 0:
                    valeur_cellule.set(str(self.grille[ligne][colonne]))  # Afficher la valeur dans l'entrée
                    entree.config(state='disabled')  # Verrouiller l'entrée (non modifiable)
                else:
                    # Si la cellule est vide, permettre la saisie et vérifier lors du changement de focus
                    entree.bind("<FocusOut>", lambda e, l=ligne, c=colonne: self.verifier_cellule(l, c))

        # Dessiner les lignes pour séparer les sous-grilles
        self.dessiner_grille()

        # Ajouter un label pour afficher le compteur d'erreurs
        self.label_erreurs = tk.Label(self.fenetre, text=f"Erreurs: {self.erreurs}/{self.erreurs_max}", font=("Arial", 12))
        self.label_erreurs.pack(pady=10)  # Placer le label sous la grille avec un espacement vertical

        # Créer un cadre pour contenir les boutons
        self.cadre_boutons = tk.Frame(self.fenetre)
        self.cadre_boutons.pack(pady=10)

        # Ajouter un bouton pour vérifier la solution
        self.bouton_verifier = tk.Button(self.cadre_boutons, text="Vérifier", command=self.verifier_solution)
        self.bouton_verifier.pack(side='left', padx=10)

        # Ajouter un bouton pour réinitialiser la grille
        self.bouton_reinitialiser = tk.Button(self.cadre_boutons, text="Réinitialiser", command=self.reinitialiser_grille)
        self.bouton_reinitialiser.pack(side='left', padx=10)

        # Ajouter un bouton pour quitter le jeu
        self.bouton_quitter = tk.Button(self.cadre_boutons, text="Quitter", command=self.fenetre.quit)
        self.bouton_quitter.pack(side='left', padx=10)

        # Créer un cadre pour les boutons de sélection de difficulté
        self.cadre_difficulte = tk.Frame(self.fenetre)
        self.cadre_difficulte.pack(pady=10)

        # Ajouter un bouton pour sélectionner la difficulté "facile"
        self.bouton_facile = tk.Button(self.cadre_difficulte, text="Facile", command=lambda: self.definir_difficulte('facile'))
        self.bouton_facile.pack(side='left', padx=5)

        # Ajouter un bouton pour sélectionner la difficulté "moyen"
        self.bouton_moyen = tk.Button(self.cadre_difficulte, text="Moyen", command=lambda: self.definir_difficulte('moyen'))
        self.bouton_moyen.pack(side='left', padx=5)

        # Ajouter un bouton pour sélectionner la difficulté "difficile"
        self.bouton_difficile = tk.Button(self.cadre_difficulte, text="Difficile", command=lambda: self.definir_difficulte('difficile'))
        self.bouton_difficile.pack(side='left', padx=5)

    def dessiner_grille(self):
        """Dessiner les lignes épaisses pour séparer les sous-grilles."""
        for i in range(self.taille_grille + 1):  # Parcourir chaque ligne et colonne
            largeur = 1  # Définir la largeur par défaut des lignes
            if i % 3 == 0 and i != 0:  # Si c'est une ligne/colonne après 3 cases
                largeur = 3  # Augmenter la largeur des lignes

            # Dessiner les lignes horizontales
            x1, y1 = 0, i * self.taille_cellule  # Coordonnées de départ
            x2, y2 = self.taille_grille * self.taille_cellule, i * self.taille_cellule  # Coordonnées de fin
            self.canvas.create_line(x1, y1, x2, y2, width=largeur)  # Créer la ligne horizontale

            # Dessiner les lignes verticales
            x1, y1 = i * self.taille_cellule, 0  # Coordonnées de départ
            x2, y2 = i * self.taille_cellule, self.taille_grille * self.taille_cellule  # Coordonnées de fin
            self.canvas.create_line(x1, y1, x2, y2, width=largeur)  # Créer la ligne verticale

    def definir_difficulte(self, difficulte):
        """Changer la difficulté du jeu et réinitialiser la grille."""
        self.difficulte = difficulte  # Mettre à jour la difficulté sélectionnée
        self.reinitialiser_grille()  # Réinitialiser la grille avec la nouvelle difficulté

    def reinitialiser_grille(self):
        """Réinitialiser la grille à l'état initial."""
        self.erreurs = 0  # Réinitialiser le compteur d'erreurs
        self.label_erreurs.config(text=f"Erreurs: {self.erreurs}/{self.erreurs_max}")  # Mettre à jour l'affichage des erreurs
        self.solution = self.generer_grille_complete()  # Générer une nouvelle solution complète
        self.grille = self.creer_grille_jouable(self.solution)  # Créer une grille jouable en fonction de la solution

        # Réinitialiser chaque cellule
        for ligne in range(self.taille_grille):
            for colonne in range(self.taille_grille):
                valeur_cellule = self.cellules[ligne][colonne]  # Récupérer la variable associée à la cellule
                entree = self.entrees[ligne][colonne]  # Récupérer l'entrée associée
                if self.grille[ligne][colonne] != 0:  # Si la cellule est pré-remplie
                    valeur_cellule.set(str(self.grille[ligne][colonne]))  # Mettre la valeur dans la cellule
                    entree.config(state='disabled')  # Verrouiller la cellule
                else:
                    valeur_cellule.set("")  # Vider la cellule si elle est modifiable
                    entree.config(state='normal')  # Déverrouiller la cellule

    def verifier_cellule(self, ligne, colonne):
        """Vérifier si la valeur entrée dans une cellule est correcte."""
        valeur = self.cellules[ligne][colonne].get()  # Récupérer la valeur saisie
        if valeur.isdigit():  # Si la valeur est un chiffre
            if int(valeur) == self.solution[ligne][colonne]:  # Si la valeur est correcte
                self.grille[ligne][colonne] = int(valeur)  # Mettre à jour la grille avec la bonne valeur
            else:
                # Si la valeur est incorrecte, la retirer et augmenter le compteur d'erreurs
                self.cellules[ligne][colonne].set("")  # Vider la cellule
                self.erreurs += 1  # Incrémenter le compteur d'erreurs
                self.label_erreurs.config(text=f"Erreurs: {self.erreurs}/{self.erreurs_max}")  # Mettre à jour l'affichage des erreurs
                if self.erreurs >= self.erreurs_max:  # Si le nombre maximum d'erreurs est atteint
                    messagebox.showinfo("Sudoku", "Vous avez atteint le nombre maximum d'erreurs.")  # Afficher un message d'alerte
                    self.reinitialiser_grille()  # Réinitialiser la grille

    def verifier_solution(self):
        """Vérifier si toute la grille est correctement remplie."""
        for ligne in range(self.taille_grille):  # Parcourir chaque ligne
            for colonne in range(self.taille_grille):  # Parcourir chaque colonne
                valeur = self.cellules[ligne][colonne].get()  # Récupérer la valeur de la cellule
                if valeur.isdigit() and int(valeur) != self.solution[ligne][colonne]:  # Si une valeur est incorrecte
                    messagebox.showwarning("Sudoku", "Il y a des erreurs dans la solution.")  # Alerter l'utilisateur
                    return  # Sortir de la fonction sans valider
        messagebox.showinfo("Sudoku", "Félicitations ! Vous avez résolu le puzzle.")  # Afficher un message de réussite

    def generer_grille_complete(self):
        """Générer une solution complète de Sudoku."""
        def motif(r, c):  # Générer le motif de remplissage de la grille
            return (self.taille_sous_grille * (r % self.taille_sous_grille) + r // self.taille_sous_grille + c) % self.taille_grille

        def melanger(s):  # Mélanger les éléments d'une liste
            return sample(s, len(s))  # Retourne une liste mélangée

        base = range(self.taille_sous_grille)  # Créer une base pour le mélange
        lignes = [g * self.taille_sous_grille + r for g in melanger(base) for r in melanger(base)]  # Créer les lignes mélangées
        colonnes = [g * self.taille_sous_grille + c for g in melanger(base) for c in melanger(base)]  # Créer les colonnes mélangées
        numeros = melanger(range(1, self.taille_grille + 1))  # Générer et mélanger les numéros

        # Créer la grille complète en appliquant le motif sur les lignes et les colonnes
        grille = [[numeros[motif(r, c)] for c in colonnes] for r in lignes]
        return grille

    def creer_grille_jouable(self, grille_complete):
        """Créer une grille jouable en retirant des chiffres de la solution complète."""
        grille = [ligne[:] for ligne in grille_complete]  # Faire une copie de la grille complète
        nb_cases = self.taille_grille * self.taille_grille  # Calculer le nombre total de cases
        nb_cases_vides = int(nb_cases * {'facile': 0.4, 'moyen': 0.5, 'difficile': 0.6}[self.difficulte])  # Calculer le nombre de cases à vider selon la difficulté

        # Retirer des chiffres de la grille pour créer une grille jouable
        for i in sample(range(nb_cases), nb_cases_vides):
            grille[i // self.taille_grille][i % self.taille_grille] = 0  # Remplacer certaines cases par 0 (vides)
        return grille  # Retourner la grille jouable


if __name__ == "__main__":
    fenetre = tk.Tk()  # Créer la fenêtre principale
    jeu = Sudoku(fenetre)  # Instancier le jeu de Sudoku
    fenetre.mainloop()  # Lancer la boucle principale de l'application
