import math
import time

import pygame
import random
import copy

import Intelligence
import LogiqueOthello
import main


class Othello:
    """ Cette classe permet d'initialiser le jeu """

    def __init__(self, choix, niveau_IA1, niveau_IA2, niveau_IA):
        """ Cette fonction va initialiser la fenêtre de jeu """

        pygame.init()
        self.screen = pygame.display.set_mode((800, 900))  # taille de la fenêtre
        pygame.display.set_caption('Othello')

        self.choix = choix
        self.niveau_IA1 = niveau_IA1
        self.niveau_IA2 = niveau_IA2
        self.niveau_IA = niveau_IA

        self.lignes = 8
        self.colonnes = 8

        self.grille = LogiqueOthello.Grille(self.lignes, self.colonnes, (80, 80), self, choix)
        self.time = 0

        self.joueur1 = 1
        self.joueur2 = -1

        self.joueurCourant = 1

        self.intelligence = Intelligence.Intelligence(self.grille)

        self.partie_terminee = False

        self.font = pygame.font.SysFont('Arial', 20, True, False)

        self.RUN = True

    def run(self):
        """ Cette fonction correspond à la boucle de lancement du jeu """

        while self.RUN:
            self.input()

            if self.choix == 2:
                self.humain_vs_ordi()  # boucle pour le cas Humain vs IA
            elif self.choix == 1:
                self.humain_vs_humain()  # boucle pour le cas Humain vs Humain
            elif self.choix == 3:
                self.time = 5
                self.ordi_vs_ordi()  # boucle pour le cas IA vs IA
            self.draw()

    def jouer(self):
        x, y = pygame.mouse.get_pos()
        x = (x - 80) // 80
        y = (y - 80) // 80

        #  Vérifie si le coup est valide (pour que ce ne soit pas un coup interdit)
        valides = self.grille.chercherCoupsJouables(self.grille.grille, self.joueurCourant)

        if not valides:
            pass
        else:
            if (y, x) in valides:
                self.grille.placerPion(self.grille.grille, self.joueurCourant, y,
                                       x)  # insérer dans la grille

                reversibles = self.grille.reversible(y, x, self.grille.grille,
                                                     self.joueurCourant)  # cases réversibles

                #  pour l'effet de transition lorsqu'on tourne un pion
                for case in reversibles:
                    self.grille.transitionReverser(case, self.joueurCourant)  # transition
                    self.grille.grille[case[0]][case[1]] *= -1  # inverser le côté du pion dans la grille

                self.joueurCourant = self.joueurCourant * -1

                # Ajouter un délai pour laisser le temps à l'animation des pions de terminer
                self.time = pygame.time.get_ticks()

    def input(self):
        """ Correspond aux entrées de l'utilisateur (humain) """

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # bouton revenir au menu
                quit_button_rect = pygame.Rect(600, 825, 150, 50)
                if quit_button_rect.collidepoint(mouse_x, mouse_y):
                    self.RUN = False

            if event.type == pygame.QUIT:
                # Réinitialiser le niveau des IA
                main.level_IA1 = -1
                main.level_IA2 = -1

                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:  # clic droit de la souris
                    self.grille.afficherTableauGrille()

                if event.button == 1:  # clic gauche de la souris
                    if self.choix == 2:  # cas pour jouer contre un ordi
                        if self.joueurCourant == 1 and not self.partie_terminee:
                            self.jouer()
                    elif self.choix == 1:  # cas pour jouer avec 2 personnes
                        if not self.partie_terminee:
                            self.jouer()
                    elif self.choix == 3:  # cas pour regarder 2 IA s'affronter
                        pass

                    if self.partie_terminee:
                        x, y = pygame.mouse.get_pos()
                        if 320 <= x <= 480 and 800 <= y <= 900:
                            self.grille.rejouer()
                            self.joueurCourant = 1
                            self.partie_terminee = False

    def calculer_scores(self):
        """ Cette fonction va calculer le score des joueurs """

        self.grille.score_joueur1 = self.grille.calculerScore(self.joueur1)
        self.grille.score_joueur2 = self.grille.calculerScore(self.joueur2)

    def ordinateur(self, niveau, delai, joueur):
        """ Cette fonction va donner les ordres à l'ordinateur pour qu'il puisse jouer """

        nouveau_temps = pygame.time.get_ticks()
        if nouveau_temps - self.time >= delai:  # On attend 0.5 secs (pour que l'animation soit finie,
            # et un peu un effet de réflexion de la part de l'IA

            # Si aucun coup n'est possible pour le joueur courant, la partie est terminée
            if not self.grille.chercherCoupsJouables(self.grille.grille, self.joueurCourant):
                self.partie_terminee = True
                return
            if niveau == 0:  # agent aveugle
                case = self.intelligence.intelligence_aveugle(self.grille.grille, joueur)
            elif niveau == 99:  # minimax basique
                case, score = self.intelligence.minimax(self.grille.grille, 2, joueur)

            elif niveau == 1:  # niveau facile avec minimax élagage alpha-beta, somme des pions et profondeur = 2
                case, score = self.intelligence.minimax_elagage(self.grille.grille, 2, niveau, -math.inf, math.inf,
                                                                joueur)

            elif niveau == 2:  # niveau moyen avec minimax élagage alpha-beta, somme des pions et profondeur = 5
                case, score = self.intelligence.minimax_elagage(self.grille.grille, 5, niveau, -math.inf, math.inf,
                                                                joueur)

            elif niveau == 3:  # niveau moyen avec minimax élagage alpha-beta, heuristiques à 3 critères
                case, score = self.intelligence.minimax_elagage(self.grille.grille, 5, niveau, -math.inf, math.inf,
                                                                joueur)

            else:  # Humain vs ordi
                case, score = self.intelligence.minimax_elagage(self.grille.grille, 5, niveau, -math.inf, math.inf,
                                                                joueur)

            # else:  # minimax élagage alpha-beta
            #    case, score = self.intelligence.minimax_elagage(self.grille.grille, 5, niveau, -999, 999, joueur)
            #    print("coup choisi est:", case, "avec score ", score)

            if niveau == 0:
                print("coup choisi est:", case)
            else:
                print("coup choisi est:", case, "avec score ", score)


            # placer le pion choisi sur la grille
            self.grille.placerPion(self.grille.grille, self.joueurCourant, case[0], case[1])
            cases_reversibles = self.grille.reversible(case[0], case[1], self.grille.grille, self.joueurCourant)

            # retourner les pions à retourner
            for case in cases_reversibles:
                self.grille.transitionReverser(case, self.joueurCourant)
                self.grille.grille[case[0]][case[1]] *= -1
            self.joueurCourant *= -1

    def ordinateur2(self, niveau, delai, joueur):
        """ Cette fonction va donner les ordres à la deuxième IA pour qu'elle puisse jouer """

        nouveau_temps = pygame.time.get_ticks()
        if nouveau_temps - self.time >= delai:  # On attend 0.5 secs (pour que l'animation soit finie,
            # et un peu un effet de réflexion de la part de l'IA

            # Si aucun coup n'est possible pour le joueur courant, la partie est terminée
            if not self.grille.chercherCoupsJouables(self.grille.grille, self.joueurCourant):
                self.partie_terminee = True
                return
            if niveau == 0:  # agent aveugle
                case = self.intelligence.intelligence_aveugle(self.grille.grille, joueur)
            elif niveau == 99:  # minimax basique
                case, score = self.intelligence.minimax(self.grille.grille, 2, joueur)

            elif niveau == 1:  # niveau facile avec minimax élagage alpha-beta, somme des pions et profondeur = 2
                case, score = self.intelligence.minimax_elagage2(self.grille.grille, 2, niveau, -math.inf, math.inf,
                                                                 joueur)

            elif niveau == 2:  # niveau moyen avec minimax élagage alpha-beta, somme des pions et profondeur = 5
                case, score = self.intelligence.minimax_elagage2(self.grille.grille, 5, niveau, -math.inf, math.inf,
                                                                 joueur)

            elif niveau == 3:  # niveau moyen avec minimax élagage alpha-beta, heuristiques à 3 critères
                case, score = self.intelligence.minimax_elagage2(self.grille.grille, 5, niveau, -math.inf, math.inf,
                                                                 joueur)
            if niveau == 0:
                print("coup choisi est:", case)
            else:
                print("coup choisi est:", case, "avec score ", score)


            # placer le pion choisi sur la grille
            self.grille.placerPion(self.grille.grille, self.joueurCourant, case[0], case[1])
            cases_reversibles = self.grille.reversible(case[0], case[1], self.grille.grille, self.joueurCourant)

            # retourner les pions à retourner
            for case in cases_reversibles:
                self.grille.transitionReverser(case, self.joueurCourant)
                self.grille.grille[case[0]][case[1]] *= -1
            self.joueurCourant *= -1

    def humain_vs_ordi(self):
        """ Cette fonction va démarrer la logique d'une partie humain contre ordinateur """

        if self.joueurCourant == -1:
            if self.niveau_IA == 1:  # Niveau IA facile = minimax alpha-beta avec somme des pions, profondeur = 2
                self.ordinateur(1, 500, -1)

            elif self.niveau_IA == 2:  # Niveau IA moyen = minimax alpha-beta avec somme des pions, profondeur = 5
                self.ordinateur(2, 500, -1)

            elif self.niveau_IA == 3:  # Niveau IA difficile = minimax alpha-beta avec heuristique à 3 critères
                self.ordinateur(3, 500, -1)

            elif self.niveau_IA == 0:  # agent aveugle
                self.ordinateur(0, 500, -1)

        self.calculer_scores()

        # Vérifier s'il n'y a plus de coups jouables
        if not self.grille.chercherCoupsJouables(self.grille.grille, self.joueurCourant):
            self.partie_terminee = True
            return

    def humain_vs_humain(self):
        """ Cette fonction va démarrer la logique d'une partie humain contre humain """

        # Calculer les scores
        self.calculer_scores()

        # Vérifier s'il n'y a plus de coups jouables
        if not self.grille.chercherCoupsJouables(self.grille.grille, self.joueurCourant):
            self.partie_terminee = True
            return

    def ordi_vs_ordi(self):
        """ Cette fonction va démarrer la logique d'une partie ordinateur contre ordinateur """

        if self.joueurCourant == -1:
            if self.niveau_IA2 == 1:  # Niveau IA2 facile = minimax alpha-beta avec somme des pions, profondeur = 2
                self.ordinateur(1, 500, -1)

            elif self.niveau_IA2 == 2:  # Niveau IA2 moyen = minimax alpha-beta avec somme des pions, profondeur = 5
                self.ordinateur(2, 500, -1)

            elif self.niveau_IA2 == 3:  # Niveau IA2 difficile = minimax alpha-beta avec heuristique à 3 critères
                self.ordinateur(3, 500, -1)

            elif self.niveau_IA2 == 0:  # Niveau IA2 difficile = minimax alpha-beta avec heuristique à 3 critères
                self.ordinateur(0, 500, -1)

        if self.joueurCourant == 1:
            if self.niveau_IA1 == 1:  # Niveau IA1 facile = minimax alpha-beta avec somme des pions, profondeur = 2
                self.ordinateur2(1, 500, 1)

            elif self.niveau_IA1 == 2:  # Niveau IA1 moyen = minimax alpha-beta avec somme des pions, profondeur = 5
                self.ordinateur2(2, 500, 1)

            elif self.niveau_IA1 == 3:  # Niveau IA1 difficile = minimax alpha-beta avec heuristique à 3 critères
                self.ordinateur2(3, 500, 1)

            elif self.niveau_IA1 == 0:  # Niveau IA1 difficile = minimax alpha-beta avec heuristique à 3 critères
                self.ordinateur2(0, 500, 1)
        self.calculer_scores()

        # Vérifier s'il n'y a plus de coups jouables
        if not self.grille.chercherCoupsJouables(self.grille.grille, self.joueurCourant):
            self.partie_terminee = True
            return

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.grille.dessinerGrille(self.screen)

        if self.choix == 3:
            self.draw_niveau_IA1()
            self.draw_niveau_IA2()

        if self.choix == 2:
            self.draw_niveau_IA()
        pygame.display.update()

    def draw_niveau_IA1(self):

        if self.niveau_IA1 == 1:
            niveau_IA1_image_texte = self.font.render("(Facile)", 1, 'White')
            niveau_rect = niveau_IA1_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 825

        elif self.niveau_IA1 == 2:
            niveau_IA1_image_texte = self.font.render("(Moyen)", 1, 'White')
            niveau_rect = niveau_IA1_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 825

        elif self.niveau_IA1 == 3:
            niveau_IA1_image_texte = self.font.render("(Difficile)", 1, 'White')
            niveau_rect = niveau_IA1_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 825

        elif self.niveau_IA1 == 0:
            niveau_IA1_image_texte = self.font.render("(Aléatoire)", 1, 'White')
            niveau_rect = niveau_IA1_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 825

        self.screen.blit(niveau_IA1_image_texte, niveau_rect)

    def draw_niveau_IA2(self):

        if self.niveau_IA2 == 1:
            niveau_IA2_image_texte = self.font.render("(Facile)", 1, 'White')
            niveau_rect = niveau_IA2_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 850

        elif self.niveau_IA2 == 2:
            niveau_IA2_image_texte = self.font.render("(Moyen)", 1, 'White')
            niveau_rect = niveau_IA2_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 850

        elif self.niveau_IA2 == 3:
            niveau_IA2_image_texte = self.font.render("(Difficile)", 1, 'White')
            niveau_rect = niveau_IA2_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 850

        elif self.niveau_IA2 == 0:
            niveau_IA2_image_texte = self.font.render("(Aléatoire)", 1, 'White')
            niveau_rect = niveau_IA2_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 850

        self.screen.blit(niveau_IA2_image_texte, niveau_rect)

    def draw_niveau_IA(self):
        """Cette fonction sert à montrer le niveau de l'IA du mode humain vs IA"""

        if self.niveau_IA == 1:
            niveau_IA_image_texte = self.font.render("(Facile)", 1, 'White')
            niveau_rect = niveau_IA_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 850

        elif self.niveau_IA == 2:
            niveau_IA_image_texte = self.font.render("(Moyen)", 1, 'White')
            niveau_rect = niveau_IA_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 850

        elif self.niveau_IA == 3:
            niveau_IA_image_texte = self.font.render("(Difficile)", 1, 'White')
            niveau_rect = niveau_IA_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 850

        elif self.niveau_IA == 0:
            niveau_IA_image_texte = self.font.render("(Aléatoire)", 1, 'White')
            niveau_rect = niveau_IA_image_texte.get_rect()
            niveau_rect.x = 225
            niveau_rect.y = 850

        self.screen.blit(niveau_IA_image_texte, niveau_rect)