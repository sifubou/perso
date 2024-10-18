def cesar_chiffrer(message, decalage):
    resultat = ''
    for lettre in message:
        if lettre.isalpha():
            base = ord('A') if lettre.isupper() else ord('a')
            nouvelle_lettre = chr((ord(lettre) - base + decalage) % 26 + base)
            resultat += nouvelle_lettre
        else :
            resultat += lettre
    return resultat

def cesar_dechiffrer(message, decalage):
    resultat = ''
    for lettre in message :
        if lettre.isalpha():
            base = ord('a') if lettre.islower() else ord('A')
            nouvelle_lettre = chr((ord(lettre)-base - decalage)%26 + base )
            resultat += nouvelle_lettre
        else : 
            resultat += lettre
    return resultat

choix = input("Voulez-vous chiffrer ou dechiffrer ? (entrez 'chiffrer' ou 'dechiffrer') : ").lower()

if choix == 'chiffrer':
    texte = input("Veuillez saisir votre texte : ")
    decalage = int(input("Veuillez saisir le décalage : "))
    resultat = cesar_chiffrer(texte, decalage)
    print(f'Texte chiffré : {resultat}')
elif choix == 'dechiffrer':
    texte = input("Veuillez saisir votre texte : ")
    decalage = int(input("Veuillez saisir le décalage : "))
    resultat = cesar_dechiffrer(texte, decalage)
    print(f'Texte déchiffré : {resultat}')
else:
    print("Choix invalide. Veuillez saisir 'chiffrer' ou 'dechiffrer'.")