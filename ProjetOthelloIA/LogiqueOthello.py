import pygame

import JeuOthello
import Pion
import Utilitaires
import main


class Grille:
    """ Cette classe va participer à la création de la logique du jeu Othello """

    def __init__(self, lignes, colonnes, taille, main, choix):
        self.JEU = main
        self.y = lignes
        self.x = colonnes
        self.taille = taille
        self.choix = choix

        self.blanc = Utilitaires.chargerImages('Assets/WhiteToken.png', taille, 0.7)
        self.noir = Utilitaires.chargerImages('Assets/BlackToken.png', taille, 0.7)

        self.transitionBlancNoir = []
        self.transitionNoirBlanc = []

        #  Permet de faire un effet de retournement lorsqu'un pion est retourné
        for i in range(1, 4):
            image1 = Utilitaires.chargerImages(f'Assets/BlackToWhite{i}.png', self.taille, 0.7)
            image2 = Utilitaires.chargerImages(f'Assets/WhiteToBlack{i}.png', self.taille, 0.7)
            self.transitionBlancNoir.append(image1)
            self.transitionNoirBlanc.append(image2)

        self.fond = Utilitaires.chargerImageDeFond(taille)

        self.pions = {}

        self.fondGrille = self.creerFond()

        self.grille = self.genererGrille(self.y, self.x)

        self.score_joueur1 = 0
        self.score_joueur2 = 0

        self.font = pygame.font.SysFont('Arial', 20, True, False)
        self.fontFin = pygame.font.SysFont('Arial', 50, True, False)

        #self.choixJcJ = False
        #self.choixJcIA = False
        #self.choixIAcIA = False


    def genererGrille(self, lignes, colonnes):
        """ Va générer une grille vide """

        grille = []
        for y in range(lignes):
            ligne = []

            for x in range(colonnes):
                ligne.append(0)
            grille.append(ligne)

        #  Placer les 4 pions initiaux du milieu
        self.placerPion(grille, 1, 3, 3)
        self.placerPion(grille, -1, 3, 4)
        self.placerPion(grille, 1, 4, 4)
        self.placerPion(grille, -1, 4, 3)

        return grille

    def afficherTableauGrille(self):
        """ Permet d'afficher dans la console l'état de la grille """

        # Afficher la première ligne avec les lettres des colonnes
        print('  | A | B | C | D | E | F | G | H |')

        for i, row in enumerate(self.grille):
            ligne = f'{i} |'.ljust(3, " ")  # créer un string pour afficher le numéro de ligne courant

            for item in row:
                ligne += f"{item}".center(3, " ") + '|'  # ajouter chaque élément au string ligne, centré sur 3 caractères

            print(ligne)
        print()

    def creerFond(self):
        """Cette fonction crée le fond du jeu en utilisant les images du dictionnaire (où on a inséré les motifs).
            Elle retourne l'image de la surface du fond."""

        # Liste des noms d'images pour créer le fond, selon les noms associés dans le dictionnaire.
        # C'est pour savoir quelle image on veut afficher, et à quelle position
        fondGrille = [
            ['C0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'D0', 'E0'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C1', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'E1'],
            ['C1', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'B0', 'A0', 'E1'],
            ['C2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'D2', 'E2'],
                    ]

        image = pygame.Surface((1000, 1000))  # Création d'une surface vide pour le fond

        # Parcours de chaque image dans la grille pour les ajouter à la surface du fond
        for j, ligne in enumerate(fondGrille):
            for i, img in enumerate(ligne):
                # Récupération de l'image correspondante dans le dictionnaire d'images de fond
                # et ajoute l'image à la surface du fond
                image.blit(self.fond[img], (i * self.taille[0], j * self.taille[1]))

        return image

    def dessinerGrille(self, fenetre):
        """ Va dessiner la grille du plateau de jeu ainsi que les pions existants dans le dictionnaire pions """

        fenetre.blit(self.fondGrille, (0, 0))  # En haut à gauche

        for pion in self.pions.values():
            pion.dessiner(fenetre)  # Dessine le pion courant sur la fenêtre de jeu

        # Dessiner les coups jouables (aide visuelle)
        coupsJouables = self.chercherCoupsJouables(self.grille, self.JEU.joueurCourant)

        if self.choix == 1:
            if self.JEU.joueurCourant == 1:
                for coup in coupsJouables:
                    pygame.draw.circle(fenetre, 'White', (80 + (coup[1] * 80) + 40, 80 + (coup[0] * 80) + 40), 5)
            else:
                for coup in coupsJouables:
                    pygame.draw.circle(fenetre, 'Black', (80 + (coup[1] * 80) + 40, 80 + (coup[0] * 80) + 40), 5)

        elif self.choix == 2:
            if self.JEU.joueurCourant == 1:
                for coup in coupsJouables:
                    pygame.draw.circle(fenetre, 'White', (80 + (coup[1] * 80) + 40, 80 + (coup[0] * 80) + 40), 5)
        elif self.choix == 3:
            pass

        if self.JEU.partie_terminee:
            fenetre.blit(self.fin_partie(), (0, 0))

        fenetre.blit(self.afficher_score('Joueur blanc', self.score_joueur1), (50, 825))
        fenetre.blit(self.afficher_score('Joueur noir', self.score_joueur2), (50, 850))
        #fenetre.blit(self.afficher_niveau, (100, 850))

        self.dessiner_bouton_menu(fenetre) #dessiner le bouton retour au menu

    def placerPion(self, grille, joueurCourant, y, x):
        """ Cette fonction va permettre de placer un pion dans la grille de jeu """

        # Détermine l'image à utiliser pour le pion en fonction du joueur courant
        if joueurCourant == 1:
            imagePion = self.blanc
        else:
            imagePion = self.noir

        # Crée un objet Pion et l'ajoute dans le dictionnaire de pions à la position (y, x)
        self.pions[(y, x)] = Pion.Pion(joueurCourant, y, x, imagePion, self.JEU)

        # Place le pion dans la grille en assignant la valeur du joueur (1 ou 2) à la position (y,x)
        grille[y][x] = self.pions[(y, x)].joueur

    def verifierValide(self, grille, joueurCourant):
        """ Cette fonction va chercher toutes les cases vides adjacentes à l'opposant du joueur courant
        Procédure : chercher une case vide
        Chercher si les cases voisines sont habitées par l'opposant
        Si elle existe et qu'elle est adjacente à la case courante, alors la case vide est valide
        """

        valides = []

        # Parcours de toutes les cases de la grille
        for grilleX, ligne in enumerate(grille):
            for grilleY, colonne in enumerate(ligne):
                if grille[grilleX][grilleY] != 0:  # Si la case n'est pas vide, on passe à la suivante
                    continue

                DIRECTIONS = Utilitaires.directions(grilleX, grilleY)  # valides pour la case courante

                for direction in DIRECTIONS:
                    directionX, directionY = direction
                    caseVerifiee = grille[directionX][directionY]

                    if caseVerifiee == 0 or caseVerifiee == joueurCourant:  # passer si la case n'est pas habitée par l'opposant
                        continue

                    if (grilleX, grilleY) in valides:  # passer si déjà dans la liste des cases valides
                        continue

                    valides.append((grilleX, grilleY))

        return valides

    def reversible(self, x, y, grille, joueur):
        """ Cette fonction permet de renvoyer la liste des cases réversibles pour le joueur courant à partir de la case (x, y).

            Procédure :
            chercher les cases qui peuvent potentiellement être retournées dans chaque direction
            vérifier si chaque case dans ces directions peut être retournée.

            La fonction prend en entrée les coordonnées (x, y) d'une case, la grille de jeu, et le joueur courant. """

        adjacentes = Utilitaires.directions(x, y)

        if len(adjacentes) == 0:  # Si la case n'a pas de cases adjacentes donc pas de case réversible
            return []

        reversibles = []

        # parcourir les cases adjacentes pour déterminer les cases réversibles dans chaque direction
        for checkCell in adjacentes:
            verifierX, verifierY = checkCell
            difX, difY = verifierX - x, verifierY - y
            ligneCourante = []

            RUN = True
            while RUN:
                if grille[verifierX][verifierY] == joueur * -1:  # si la case est habitée par l'opposant, elle est réversible
                    ligneCourante.append((verifierX, verifierY))
                elif grille[verifierX][verifierY] == joueur:
                    RUN = False
                    break
                elif grille[verifierX][verifierY] == 0:
                    ligneCourante.clear()
                    RUN = False

                #  mettre à jour les coordonnées pour continuer dans la direction de la ligne
                verifierX += difX
                verifierY += difY

                #  Cas où on sort du plateau de jeu : on ne peut pas continuer la ligne
                if verifierX < 0 or verifierX > 7 or verifierY < 0 or verifierY > 7:
                    ligneCourante.clear()
                    RUN = False

            if len(ligneCourante) > 0:
                reversibles.extend(ligneCourante)

        return reversibles

    def chercherCoupsJouables(self, grid, joueurCourant):
        """ Va vérifier si les cases qui ont été identifiées comme valides sont jouables
            (donc après avoir vérifié que des pions étaient réversibles). """

        valides = self.verifierValide(grid, joueurCourant)
        jouables = []

        for case in valides:
            x, y = case
            if case in jouables:  # existe déjà
                continue

            # récupérer les cases réversibles pour la case courante
            casesReversibles = self.reversible(x, y, grid, joueurCourant)

            if len(casesReversibles) > 0:
                jouables.append(case)

        return jouables

    def transitionReverser(self, case, joueur):
        """ La fonction permet de changer la couleur d'un pion avec un effet de transition """

        if joueur == 1:
            self.pions[(case[0], case[1])].transition(self.transitionBlancNoir, self.blanc)
        else:
            self.pions[(case[0], case[1])].transition(self.transitionNoirBlanc, self.noir)

    def calculerScore(self, joueur):
        """ Cette fonction va calculer le score du joueur entré en paramètre"""

        score = 0
        for ligne in self.grille:
            for colonne in ligne:
                if colonne == joueur:
                    score += 1
        return score

    def afficher_score(self, player, score):
        """ Cette fonction va afficher le score du joueur entré en paramètre """
        if player == 1:
            player_score = str(player) + " : " + str(score)
        else:
            player_score = str(player) + " : " + str(score)

        image_texte = self.font.render(player_score, 1, 'White')

        return image_texte

    def fin_partie(self):
        """ Cette fonction va afficher un panel de fin de jeu, en annoncant le gagnant ainsi que de proposer de rejouer"""

        if self.JEU.partie_terminee:
            panel_fin = pygame.Surface((800, 900))
            panel_fin.set_alpha(200)

            if self.score_joueur1 > self.score_joueur2:
                texte_fin = self.fontFin.render('Joueur blanc a gagné', 1, 'White')
            else:
                texte_fin = self.fontFin.render('Joueur noir a gagné', 1, 'White')

            panel_fin.blit(texte_fin, (160, 300))

            self.bouton_rejouer(panel_fin)

            #pygame.draw.circle(panel_fin, pygame.Color('white'), replay_button_rect.center, 200 // 2, 2)
            #pygame.draw.circle(panel_fin, pygame.Color('white'), replay_button_rect.center, 200 // 2 - 10)

        return panel_fin

    def bouton_rejouer(self, panel):
        replay_button = pygame.Surface((150, 50))
        replay_button.fill('White')
        replay_button.set_alpha(255)
        replay_button_rect = replay_button.get_rect()
        replay_button_rect.center = (panel.get_width() // 2, 850)
        texte_rejouer = self.font.render('Rejouer', 1, 'Black')
        replay_button.blit(texte_rejouer, (40, 10))
        panel.blit(replay_button, replay_button_rect)

    def rejouer(self):
        self.pions.clear()
        self.grille = self.genererGrille(self.y, self.x)
    
    def dessiner_bouton_menu(self, fenetre):
        self.bouton_menu = pygame.draw.rect(fenetre, (0, 0, 0), (600, 825, 150, 50))
        bouton_texte = self.font.render('Revenir au menu', 1, (255,255,255))
        fenetre.blit(bouton_texte, (605, 835))
    
    

    def revenir_au_menu(self):
    #revenir au menu principal et mettre fin à la partie en cours.
        pass


