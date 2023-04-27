class Pion:
    """ Cette classe concerne les comportements d'un pion """

    def __init__(self, joueur, grilleX, grilleY, image, main):
        self.joueur = joueur
        self.grilleX = grilleX
        self.grilleY = grilleY
        self.positionX = 80 + (grilleY * 80)
        self.positionY = 80 + (grilleX * 80)
        self.JEU = main

        self.image = image

    def transition(self, imagesDeTransition, imagePion):
        """ Anime une transition entre deux images en faisant un fondu enchaîné"""

        for i in range(30):
            self.image = imagesDeTransition[i // 10]
            self.JEU.draw()

        self.image = imagePion

    
    def dessiner(self, fenetre):
        """Dessiner le jeton sur la fenêtre"""

        #Calculer les décalages pour centrer l'image du jeton dans la cellule
        decalage_x = (self.JEU.grille.taille[0] - self.image.get_width()) // 2
        decalage_y = (self.JEU.grille.taille[1] - self.image.get_height()) // 2

        # Afficher l'image du jeton à la position calculée
        fenetre.blit(self.image, (80 + (self.grilleY * 80) + decalage_x, 80 + (self.grilleX * 80) + decalage_y))

