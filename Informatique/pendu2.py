import tkinter as tk

class Pendu:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Jeu du Pendu")

        self.mot_a_deviner = ""
        self.lettres_trouvees = []
        self.lettres_essayees = []
        self.erreurs = 0
        self.erreurs_max = 8

        self.cadre_saisie_mot = tk.Frame(racine)
        self.etiquette_instruction = tk.Label(self.cadre_saisie_mot, text="Saisissez un mot à deviner :", font=('Arial', 16))
        self.etiquette_instruction.pack(pady=10)

        self.saisie_mot = tk.Entry(self.cadre_saisie_mot, font=('Arial', 16), show="*")
        self.saisie_mot.pack(pady=10)

        self.bouton_valider_mot = tk.Button(self.cadre_saisie_mot, text="Valider", command=self.valider_mot)
        self.bouton_valider_mot.pack(pady=10)

        self.cadre_saisie_mot.pack(pady=20)

    def valider_mot(self):
        self.mot_a_deviner = self.saisie_mot.get().lower()
        if self.mot_a_deviner.isalpha() and len(self.mot_a_deviner) > 0:
            self.cadre_saisie_mot.pack_forget()
            self.lancer_jeu()
        else:
            self.etiquette_instruction.config(text="Veuillez saisir un mot valide (lettres uniquement).")

    def afficher_mot(self):
        return ' '.join([lettre if lettre in self.lettres_trouvees else '_' for lettre in self.mot_a_deviner])

    def lancer_jeu(self):
        self.etiquette_mot = tk.Label(self.racine, text=self.afficher_mot(), font=('Arial', 24))
        self.etiquette_mot.pack(pady=20)

        self.canvas = tk.Canvas(self.racine, width=300, height=300)
        self.canvas.pack(pady=20)

        self.saisie_lettre = tk.Entry(self.racine, font=('Arial', 16))
        self.saisie_lettre.pack(pady=10)
        self.saisie_lettre.bind("<Return>", self.verifier_lettre)

        self.etiquette_erreurs = tk.Label(self.racine, text=f"Erreurs : {self.erreurs}/{self.erreurs_max}", font=('Arial', 16))
        self.etiquette_erreurs.pack(pady=10)

        self.etiquette_message = tk.Label(self.racine, text="", font=('Arial', 16))
        self.etiquette_message.pack(pady=10)

    def verifier_lettre(self, event):
        lettre = self.saisie_lettre.get().lower()
        self.saisie_lettre.delete(0, tk.END)

        if lettre in self.lettres_essayees:
            self.etiquette_message.config(text="Vous avez déjà essayé cette lettre.")
            return

        self.lettres_essayees.append(lettre)

        if lettre in self.mot_a_deviner:
            self.lettres_trouvees.append(lettre)
            self.etiquette_message.config(text=f"Bonne réponse, la lettre '{lettre}' est dans le mot.")
        else:
            self.erreurs += 1
            self.etiquette_message.config(text=f"Faux ! La lettre '{lettre}' n'est pas dans le mot.")
            self.dessiner_pendu()

        self.etiquette_mot.config(text=self.afficher_mot())
        self.etiquette_erreurs.config(text=f"Erreurs : {self.erreurs}/{self.erreurs_max}")

        if all(lettre in self.lettres_trouvees for lettre in self.mot_a_deviner):
            self.etiquette_message.config(text=f"Félicitations ! Vous avez trouvé le mot : {self.mot_a_deviner}")
            self.saisie_lettre.config(state=tk.DISABLED)
            self.afficher_bouton_rejouer()
        elif self.erreurs == self.erreurs_max:
            self.etiquette_message.config(text=f"Dommage ! Le mot à trouver était : {self.mot_a_deviner}")
            self.saisie_lettre.config(state=tk.DISABLED)
            self.afficher_bouton_rejouer()

    def dessiner_pendu(self):
        if self.erreurs == 1:
            self.canvas.create_line(50, 250, 250, 250)
        elif self.erreurs == 2:
            self.canvas.create_line(150, 250, 150, 50)
        elif self.erreurs == 3:
            self.canvas.create_line(150, 50, 220, 50)
        elif self.erreurs == 4:
            self.canvas.create_line(220, 50, 220, 80)
        elif self.erreurs == 5:
            self.canvas.create_oval(200, 80, 240, 120)
        elif self.erreurs == 6:
            self.canvas.create_line(220, 120, 220, 180)
        elif self.erreurs == 7:
            self.canvas.create_line(220, 140, 200, 160)
            self.canvas.create_line(220, 140, 240, 160)
        elif self.erreurs == 8:
            self.canvas.create_line(220, 180, 200, 220)
            self.canvas.create_line(220, 180, 240, 220)

    def afficher_bouton_rejouer(self):
        self.bouton_rejouer = tk.Button(self.racine, text="Rejouer", font=('Arial', 16), command=self.reinitialiser_jeu)
        self.bouton_rejouer.pack(pady=10)

    def reinitialiser_jeu(self):
        self.racine.destroy()
        nouvelle_fenetre= tk.Tk()
        jeu = Pendu(nouvelle_fenetre)
        nouvelle_fenetre.mainloop()


racine = tk.Tk()
jeu = Pendu(racine)
racine.mainloop()


