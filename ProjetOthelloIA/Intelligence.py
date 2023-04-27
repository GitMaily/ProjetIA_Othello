import copy
import math
import random

from FonctionsEvaluation import *


class Intelligence:

    def __init__(self, objet_grille):
        self.grille = objet_grille

    def intelligence_aveugle(self, grille, joueur):
        """ Permet de simuler un agent aveugle qui va choisir aléatoirement son coup """

        nouvelle_grille = copy.deepcopy(grille)  # initialiser la grille courante
        coups_jouables = self.grille.chercherCoupsJouables(nouvelle_grille, joueur)  # initialiser les coups jouables
        coup_choisi = 0, 0

        aleatoire = random.randrange(len(coups_jouables))  # générer un entier aléatoire
        cpt = 0

        #  parcourir le premier coup qui correspond à l'entier aléatoire
        for coup in coups_jouables:
            if cpt == aleatoire:
                coup_choisi = coup[0], coup[1]
                break
            cpt += 1

        return coup_choisi

    def minimax(self, grille, profondeur, joueur):
        """ Algorithme minimax basique"""

        # Copier le plateau de jeu courant (en interne)
        nouvelle_grille = copy.deepcopy(grille)

        # insérer la liste des coups jouables de la grille courante et pour le joueur courant
        coups_jouables = self.grille.chercherCoupsJouables(nouvelle_grille, joueur)

        # Vérification de fin de récursion lorsque la profondeur maximale de recherche a été atteinte
        # ou qu'il n'y a plus aucun coups jouables
        if profondeur == 0 or len(coups_jouables) == 0:
            meilleur_coup, score = None, evaluer_plateau(grille, joueur)  # Appel à la fonction d'évaluation
            return meilleur_coup, score

        # Le joueur max. Par exemple dans le cas humain vs IA
        # ici, l'IA cherche à maximiser son score
        if joueur < 0:
            meilleur_score = -math.inf  # Initialiser le meilleur score avec la pire valeur possible
            meilleur_coup = None

            for coup in coups_jouables:
                # Récupérer les cases retournées par le coup joué
                x, y = coup
                cases_reversibles = self.grille.reversible(x, y, nouvelle_grille, joueur)

                # va mettre à jour la grille de jeu avec le joueur courant
                nouvelle_grille[x][y] = joueur

                # mettre à jour toutes les cases retournées selon le joueur courant
                for case in cases_reversibles:
                    nouvelle_grille[case[0]][case[1]] = joueur

                # fonction de récursion
                meilleurCoup, valeur = self.minimax(nouvelle_grille, profondeur - 1, joueur * -1)

                if valeur > meilleur_score:  # comparer si on a un meilleur score que le score trouvé jusqu'à présent
                    meilleur_score = valeur
                    meilleur_coup = coup

                # il faut régénérer la grille après avoir placé un pion pour évaluer le prochain coup jouable
                nouvelle_grille = copy.deepcopy(grille)

            return meilleur_coup, meilleur_score

        # Le joueur min. Par exemple dans le cas humain vs IA
        # ici, on cherche à minimiser le score de l'humain
        if joueur > 0:
            meilleur_score = math.inf
            meilleur_coup = None

            for coup in coups_jouables:
                x, y = coup
                cases_reversibles = self.grille.reversible(x, y, nouvelle_grille,
                                                           joueur)  # fait un coup, va tourner les pions
                nouvelle_grille[x][y] = joueur

                for case in cases_reversibles:
                    nouvelle_grille[case[0]][case[1]] = joueur

                # fonction de récursion
                meilleurCoup, valeur = self.minimax(nouvelle_grille, profondeur - 1, joueur * -1)

                if valeur < meilleur_score:
                    meilleur_score = valeur
                    meilleur_coup = coup

                nouvelle_grille = copy.deepcopy(grille)

            return meilleur_coup, meilleur_score

    def minimax2(self, grille, profondeur, joueur):
        """ Algorithme minimax basique
            La même chose que la première, juste, on a changé le rôle de min et max.
            Ici, c'est le cas ordinateur vs ordinateur,
            donc le deuxième ordinateur (joueur = 1) est celui qui cherche à maximiser son score"""

        # Copier le plateau de jeu courant (en interne)
        nouvelle_grille = copy.deepcopy(grille)

        # insérer la liste des coups jouables de la grille courante et pour le joueur courant
        coups_jouables = self.grille.chercherCoupsJouables(nouvelle_grille, joueur)

        # Vérification de fin de récursion lorsque la profondeur maximale de recherche a été atteinte
        # ou qu'il n'y a plus aucun coups jouables
        if profondeur == 0 or len(coups_jouables) == 0:
            meilleur_coup, score = None, evaluer_plateau(grille, joueur)  # Appel à la fonction d'évaluation
            return meilleur_coup, score

        # Le joueur max. Par exemple dans le cas humain vs IA
        # ici, l'IA cherche à maximiser son score
        if joueur > 0:
            meilleur_score = -math.inf  # Initialiser le meilleur score avec la pire valeur possible
            meilleur_coup = None

            for coup in coups_jouables:
                # Récupérer les cases retournées par le coup joué
                x, y = coup
                cases_reversibles = self.grille.reversible(x, y, nouvelle_grille, joueur)

                # va mettre à jour la grille de jeu avec le joueur courant
                nouvelle_grille[x][y] = joueur

                # mettre à jour toutes les cases retournées selon le joueur courant
                for case in cases_reversibles:
                    nouvelle_grille[case[0]][case[1]] = joueur

                # fonction de récursion
                meilleurCoup, valeur = self.minimax(nouvelle_grille, profondeur - 1, joueur * -1)

                if valeur > meilleur_score:  # comparer si on a un meilleur score que le score trouvé jusqu'à présent
                    meilleur_score = valeur
                    meilleur_coup = coup

                # il faut régénérer la grille après avoir placé un pion pour évaluer le prochain coup jouable
                nouvelle_grille = copy.deepcopy(grille)

            return meilleur_coup, meilleur_score

        # Le joueur min. Par exemple dans le cas humain vs IA
        # ici, on cherche à minimiser le score de l'humain
        if joueur < 0:
            meilleur_score = math.inf
            meilleur_coup = None

            for coup in coups_jouables:
                x, y = coup
                cases_reversibles = self.grille.reversible(x, y, nouvelle_grille,
                                                           joueur)  # fait un coup, va tourner les pions
                nouvelle_grille[x][y] = joueur

                for case in cases_reversibles:
                    nouvelle_grille[case[0]][case[1]] = joueur

                # fonction de récursion
                meilleurCoup, valeur = self.minimax(nouvelle_grille, profondeur - 1, joueur * -1)

                if valeur < meilleur_score:
                    meilleur_score = valeur
                    meilleur_coup = coup

                nouvelle_grille = copy.deepcopy(grille)

            return meilleur_coup, meilleur_score

    def minimax_elagage(self, grille, profondeur, niveauIA, alpha, beta, joueur):
        """ Algorithme minimax avec élagage alpha-beta """
        # Copier le plateau de jeu courant (en interne)
        nouvelle_grille = copy.deepcopy(grille)

        # insérer la liste des coups jouables de la grille courante et pour le joueur courant
        coups_jouables = self.grille.chercherCoupsJouables(nouvelle_grille, joueur)
        coups_jouables_opposant = self.grille.chercherCoupsJouables(nouvelle_grille, joueur * -1)

        # Vérification de fin de récursion lorsque la profondeur maximale de recherche a été atteinte
        # ou qu'il n'y a plus aucun coups jouables
        if profondeur == 0 or len(coups_jouables) == 0:
            if niveauIA == 1: #  Niveau IA2 facile = minimax alpha-beta avec somme des pions
                meilleur_coup, score = None, evaluer_plateau(grille, joueur)  # Appel à la fonction d'évaluation

            elif niveauIA == 2:  #  Niveau IA2 moyen = minimax alpha-beta avec somme des pions et + profondeur
                meilleur_coup, score = None, evaluer_plateau(grille, joueur)  # Appel à la fonction d'évaluation

            elif niveauIA == 3:  #  Niveau IA2 difficile = minimax alpha-beta avec heuristique à 3 critères
                meilleur_coup, score = None, evaluer_heuristiques(grille, joueur, len(coups_jouables), len(coups_jouables_opposant))  # Appel à la fonction d'évaluation

            else:  # Aucun, humain vs IA
                meilleur_coup, score = None, evaluer_heuristiques(grille, joueur, len(coups_jouables), len(coups_jouables_opposant))  # Appel à la fonction d'évaluation

            # meilleur_coup, score = None, evaluer_coins_cotes(grille, joueur, len(coups_jouables), len(coups_jouables_opposant))  # Appel à la fonction d'évaluation

            return meilleur_coup, score

        # Le joueur max. Par exemple dans le cas humain vs IA
        # ici, l'IA cherche à maximiser son score
        if joueur < 0:
            meilleur_score = -math.inf  # Initialiser le meilleur score avec la pire valeur possible
            meilleur_coup = None

            for coup in coups_jouables:
                # Récupérer les cases retournées par le coup joué
                x, y = coup
                cases_reversibles = self.grille.reversible(x, y, nouvelle_grille, joueur)

                # va mettre à jour la grille de jeu avec le joueur courant
                nouvelle_grille[x][y] = joueur

                # mettre à jour toutes les cases retournées selon le joueur courant
                for case in cases_reversibles:
                    nouvelle_grille[case[0]][case[1]] = joueur

                # fonction de récursion
                meilleurCoup, valeur = self.minimax_elagage(nouvelle_grille, profondeur - 1, niveauIA, alpha, beta, joueur * -1)

                if valeur > meilleur_score:  # comparer si on a un meilleur score que le score trouvé jusqu'à présent
                    # print("nouveau score est ", valeur)
                    #print(valeur, "est superieur a", meilleur_score, "donc meilleur coup est ", coup)

                    meilleur_score = valeur
                    meilleur_coup = coup


                #print("score est:", meilleur_score, "coup est:", meilleur_coup)

                # Partie élagage, pour économiser des recherches
                alpha = max(alpha, meilleur_score)  # mettre à jour alpha avec le max

                # Si beta est inférieur ou égal à alpha, on peut arrêter de chercher d'autres coups
                if beta <= alpha:
                    break

                # il faut régénérer la grille après avoir placé un pion pour évaluer le prochain coup jouable
                nouvelle_grille = copy.deepcopy(grille)
            return meilleur_coup, meilleur_score

        # Le joueur min. Par exemple dans le cas humain vs IA
        # ici, on cherche à minimiser le score de l'humain
        if joueur > 0:
            meilleur_score = math.inf
            meilleur_coup = None

            for coup in coups_jouables:
                x, y = coup
                cases_reversibles = self.grille.reversible(x, y, nouvelle_grille,
                                                           joueur)  # fait un coup, va tourner les pions
                nouvelle_grille[x][y] = joueur

                for case in cases_reversibles:
                    nouvelle_grille[case[0]][case[1]] = joueur

                # fonction de récursion
                meilleurCoup, valeur = self.minimax_elagage(nouvelle_grille, profondeur - 1, niveauIA, alpha, beta, joueur * -1)

                if valeur < meilleur_score:
                    meilleur_score = valeur
                    meilleur_coup = coup

                beta = min(beta, meilleur_score)

                if beta <= alpha:
                    break

                nouvelle_grille = copy.deepcopy(grille)

            return meilleur_coup, meilleur_score

    def minimax_elagage2(self, grille, profondeur, niveauIA, alpha, beta, joueur):
        """ Algorithme minimax avec élagage alpha-beta
            La même chose que la première, juste, on a changé le rôle de min et max.
            Ici, c'est le cas ordinateur vs ordinateur,
            donc le deuxième ordinateur (joueur = 1) est celui qui cherche à maximiser son score """

        # Copier le plateau de jeu courant (en interne)
        nouvelle_grille = copy.deepcopy(grille)

        # insérer la liste des coups jouables de la grille courante et pour le joueur courant
        coups_jouables = self.grille.chercherCoupsJouables(nouvelle_grille, joueur)
        coups_jouables_opposant = self.grille.chercherCoupsJouables(nouvelle_grille, joueur * -1)

        # Vérification de fin de récursion lorsque la profondeur maximale de recherche a été atteinte
        # ou qu'il n'y a plus aucun coups jouables
        if profondeur == 0 or len(coups_jouables) == 0:
            if niveauIA == 1:  # Niveau IA1 facile = minimax alpha-beta avec somme des pions
                meilleur_coup, score = None, evaluer_plateau_joueur_positif(grille, joueur)  # Appel à la fonction d'évaluation

            elif niveauIA == 2:  # Niveau IA1 moyen = minimax alpha-beta avec somme des pions et + profondeur
                meilleur_coup, score = None, evaluer_plateau_joueur_positif(grille, joueur)  # Appel à la fonction d'évaluation

            elif niveauIA == 3:  # Niveau IA1 difficile = minimax alpha-beta avec heuristique à 3 critères
                meilleur_coup, score = None, evaluer_heuristiques2(grille, joueur, len(coups_jouables),
                                                                  len(coups_jouables_opposant))  # Appel à la fonction d'évaluation
            else:  # Aucun, humain vs IA
                meilleur_coup, score = None, evaluer_heuristiques2(grille, joueur, len(coups_jouables), len(coups_jouables_opposant))  # Appel à la fonction d'évaluation

            return meilleur_coup, score
        # max
        if joueur > 0:
            meilleur_score = -math.inf  # Initialiser le meilleur score avec la pire valeur possible pour l'IA
            meilleur_coup = None

            for coup in coups_jouables:
                # Récupérer les cases retournées par le coup joué
                x, y = coup
                cases_reversibles = self.grille.reversible(x, y, nouvelle_grille,
                                                           joueur)  # fait un coup, va tourner les pions

                # va mettre à jour la grille de jeu avec le joueur courant
                nouvelle_grille[x][y] = joueur

                # mettre à jour toutes les cases selon le joueur courant
                for case in cases_reversibles:
                    nouvelle_grille[case[0]][case[1]] = joueur

                # fonction de récursion
                meilleurCoup, valeur = self.minimax_elagage2(nouvelle_grille, profondeur - 1, niveauIA, alpha, beta, joueur * -1)

                if valeur > meilleur_score:
                    meilleur_score = valeur
                    meilleur_coup = coup

                alpha = max(alpha, meilleur_score)

                if beta <= alpha:
                    break

                # il faut régénérer la grille après avoir placé un pion pour évaluer le prochain coup jouable
                nouvelle_grille = copy.deepcopy(grille)

            return meilleur_coup, meilleur_score

        if joueur < 0:
            meilleur_score = math.inf
            meilleur_coup = None

            for coup in coups_jouables:
                x, y = coup
                cases_reversibles = self.grille.reversible(x, y, nouvelle_grille,
                                                           joueur)  # fait un coup, va tourner les pions
                nouvelle_grille[x][y] = joueur

                for case in cases_reversibles:
                    nouvelle_grille[case[0]][case[1]] = joueur

                # fonction de récursion
                meilleurCoup, valeur = self.minimax_elagage2(nouvelle_grille, profondeur - 1, niveauIA, alpha, beta, joueur * -1)

                if valeur < meilleur_score:
                    meilleur_score = valeur
                    meilleur_coup = coup

                beta = min(beta, meilleur_score)

                if beta <= alpha:
                    break

                nouvelle_grille = copy.deepcopy(grille)

            return meilleur_coup, meilleur_score
