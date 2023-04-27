def evaluer_plateau(grille, joueur):
    """ Fonction d'évaluation du plateau prenant en considération le nombre de pions disposés,
        perspective joueur négatif (joueur = -1) """

    score = 0
    for y, ligne in enumerate(grille):
        for x, colonne in enumerate(ligne):
            score -= colonne

    return score


def evaluer_plateau_joueur_positif(grille, joueur):
    """ Fonction d'évaluation du plateau prenant en considération le nombre de pions disposés,
        perspective joueur positif (joueur = 1) """

    score = 0
    for y, ligne in enumerate(grille):
        for x, colonne in enumerate(ligne):
            if colonne == 1:
                score += abs(colonne)

            elif colonne == -1:
                score -= abs(colonne)

    return score


def evaluer_heuristiques(grille, joueur, nb_coups_joueur, nb_coups_adversaire):
    """ Fonction d'évaluation du plateau prenant en considération les critères sur les coins, les côtés et la mobilité.
        Il s'agit de la fonction d'évaluation pour la perspective du joueur négatif (-1)"""

    score = 0
    coin_poids = 50
    cote_poids = 10
    centre_poids = 5

    # On parcourt toute la grille
    for y, ligne in enumerate(grille):
        for x, colonne in enumerate(ligne):

            # Evaluation pour les coins
            if (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
                if grille[x][y] == -1:
                    score += coin_poids
                elif grille[x][y] == 1:
                    score -= coin_poids

            # Evaluation pour les côtés
            elif x == 0 or x == 7 or y == 0 or y == 7:
                if grille[x][y] == -1:
                    score += cote_poids
                elif grille[x][y] == 1:
                    score -= cote_poids

            # Evaluation pour les cases adjacentes aux côtés
            elif x == 1 or x == 6 or y == 1 or y == 6:
                if grille[x][y] == -1:
                    score -= cote_poids
                elif grille[x][y] == 1:
                    score += cote_poids

            # Evaluation pour les cases adjacentes aux cases adjacentes aux côtés
            elif x == 2 or x == 5 or y == 2 or y == 5:
                if grille[x][y] == -1:
                    score += centre_poids
                elif grille[x][y] == 1:
                    score -= cote_poids

            else:
                score += centre_poids

            score -= colonne

    # Evaluation de la mobilité
    score += nb_coups_joueur
    score -= nb_coups_adversaire

    return score

def evaluer_heuristiques2(grille, joueur, nb_coups_joueur, nb_coups_adversaire):
    """ Fonction d'évaluation du plateau prenant en considération les critères sur les coins, les côtés et la mobilité.
        Il s'agit de la fonction d'évaluation pour la perspective du joueur positif (1)"""

    score = 0
    coin_poids = 50
    cote_poids = 10
    centre_poids = 5

    # On parcourt toute la grille
    for y, ligne in enumerate(grille):
        for x, colonne in enumerate(ligne):

            # Evaluation pour les coins
            if (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
                if grille[x][y] == 1:
                    score += coin_poids
                elif grille[x][y] == -1:
                    score -= coin_poids

            # Evaluation pour les côtés
            elif x == 0 or x == 7 or y == 0 or y == 7:
                if grille[x][y] == 1:
                    score += cote_poids
                elif grille[x][y] == -1:
                    score -= cote_poids

            # Evaluation pour les cases adjacentes aux côtés
            elif x == 1 or x == 6 or y == 1 or y == 6:
                if grille[x][y] == 1:
                    score -= cote_poids
                elif grille[x][y] == -1:
                    score += cote_poids

            # Evaluation pour les cases adjacentes aux cases adjacentes aux côtés
            elif x == 2 or x == 5 or y == 2 or y == 5:
                if grille[x][y] == 1:
                    score += centre_poids
                elif grille[x][y] == -1:
                    score -= cote_poids

            else:
                score += centre_poids

            # Somme des pions
            if colonne == 1:
                score += abs(colonne)
            elif colonne == -1:
                score -= abs(colonne)

    # Evaluation de la mobilité
    score += nb_coups_joueur
    score -= nb_coups_adversaire

    return score


def evaluer_coins_cotes(grille, joueur, nb_coups_joueur, nb_coups_adversaire):
    """ Fonction d'évaluation du plateau prenant en considération les coins et les côtés  """

    score = 0
    coin_poids = 50
    cote_poids = 10
    centre_poids = 5

    for y, ligne in enumerate(grille):
        for x, colonne in enumerate(ligne):
            if (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
                if grille[x][y] == -1:
                    score += coin_poids
                elif grille[x][y] == 1:
                    score -= coin_poids
            elif x == 0 or x == 7 or y == 0 or y == 7:
                # Ajouter un bonus pour chaque case sur le côté
                score += cote_poids
            elif x == 1 or x == 6 or y == 1 or y == 6:
                # Ajouter un bonus pour chaque case adjacente au côté
                score -= cote_poids
            elif x == 2 or x == 5 or y == 2 or y == 5:
                # Ajouter un bonus pour chaque case adjacente aux cases adjacentes au côté
                score += centre_poids

            score -= colonne

    return score


