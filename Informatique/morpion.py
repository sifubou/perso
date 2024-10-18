def initialiser_plateau():
    return [[' ' for _ in range(3)] for _ in range(3)]

def afficher_plateau(plateau):
    for ligne in plateau :
        print(' | '.join(ligne))
        print('-'*11)

def case_valide(plateau, ligne, colonne):
    return plateau[ligne][colonne] == ' '

def demander_position(joueur):
    while True:
        try:
            ligne=int(input(f'Joueur {joueur}, entrez le numéro de la ligne (0,1,2): '))
            colonne=int(input(f'Joueur {joueur}, entrez le numéro de la colonne (0,1,2): '))
            if ligne in [0,1,2] and colonne in [0,1,2]:
                return ligne, colonne
            else : 
                print('Erreur : entrez des valeurs entre 0 et 2')
        except ValueError:
            print("Erreur : Entrez des nombres valides")

def jouer_coup(plateau, joueur, ligne, colonne):
    plateau[ligne][colonne] = joueur

def verifier_victoire(plateau, joueur):
    for ligne in plateau : 
        if all([case == joueur for case in ligne]):
            return True
    for col in range(3):
        if all([plateau[ligne][col] == joueur for ligne in range(3)]):
            return True
    if plateau[0][0]==plateau[1][1]==plateau[2][2] == joueur:
        return True
    if plateau[2][0]==plateau[1][1]==plateau[0][2] == joueur:
        return True       
    
    return False

def verifier_match_nul(plateau):
    for ligne in plateau:
        if ' ' in ligne:
            return False
    return True

def morpion():
    plateau = initialiser_plateau()
    joueur_actuel = 'X'
    while True:
        afficher_plateau(plateau)
        ligne, colonne = demander_position(joueur_actuel)
        if case_valide(plateau, ligne, colonne):
            jouer_coup(plateau, joueur_actuel, ligne, colonne)
        else:
            print("Case déjà occupée, essayez une autre.")
            continue
        if verifier_victoire(plateau, joueur_actuel):
            afficher_plateau(plateau)
            print(f'Le joueur {joueur_actuel} a gagné !')
            break
        if verifier_match_nul(plateau):
            afficher_plateau(plateau)
            print('Match nul !')
            break

        joueur_actuel = 'O' if joueur_actuel =='X' else 'X'

morpion()
