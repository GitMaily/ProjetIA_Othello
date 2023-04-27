import pygame


def chargerImages(chemin, taille, facteur_echelle=1.0):
    """ Charge une image dans le jeu et la redimensionne en fonction du facteur d'échelle"""
    
    image = pygame.image.load(f"{chemin}").convert_alpha()
    nouvelle_taille = (float(taille[0] * facteur_echelle), float(taille[1] * facteur_echelle))
    image = pygame.transform.scale(image, nouvelle_taille)

    return image

def chargerImageDeFond(taille):
    """ Cette fonction prend en entrée la taille souhaitée pour les motifs.
        Elle retourne un dictionnaire contenant les images des motifs de l'image de fond"""

    alpha = 'ABCDEFGHI'  # lettres pour nommer les colonnes du plateau

    motifs = pygame.image.load('assets/JungleFond.png').convert_alpha()  # chargement de l'image de fond contenant tous les motifs
    # l'image contient 3 lignes et 7 colonnes (7 carrés de motifs distincts)

    dictionnaireImage = {}  # dictionnaire qui va contenir les images des motifs
    for i in range(3):
        for j in range(7):
            # création de la clé correspondant à la lettre de la colonne et au numéro de ligne,
            # et assignation de l'image du motif correspondant à cette clé dans le dictionnaire
            dictionnaireImage[alpha[j]+str(i)] = chargerMotifs(motifs, j, i, taille, (32, 32))

    return dictionnaireImage

def chargerMotifs(motif, ligne, colonne, nouvelleTaille, taille):
    """ Cette fonction va créer une surface vide.
    Elle va y charger le motif entré puis retourner la nouvelle surface en tant qu'image"""

    image = pygame.Surface((32, 32)).convert_alpha()
    image.blit(motif, (0, 0), (ligne * taille[0], colonne * taille[1], taille[0], taille[1]))
    image = pygame.transform.scale(image, nouvelleTaille)
    image.set_colorkey('Black')

    return image


def directions(x, y, minX=0, minY=0, maxX=7, maxY=7):
    """ Cette fonction va déterminer quelles directions sont valides pour la case courante
        En résumé, va ajouter tous les voisins, en vérifiant le cas où la case est un côté ou un coin """

    directionsValides = []

    #  En haut (Nord)
    if x != minX:  # Toute la première colonne
        directionsValides.append((x-1, y))
    if x != minX and y != minY:
        directionsValides.append((x-1, y-1))
    if x != minX and y != maxY:
        directionsValides.append((x-1, y+1))

    if x != maxX:  # Toute la dernière colonne
        directionsValides.append((x+1, y))
    if x != maxX and y != minY:
        directionsValides.append((x+1, y-1))
    if x != maxX and y != maxY:
        directionsValides.append((x+1, y+1))

    if y != minY:  # Toute la première ligne
        directionsValides.append((x, y-1))
    if y != maxY:  # Toute la dernière ligne
        directionsValides.append((x, y+1))

    return directionsValides