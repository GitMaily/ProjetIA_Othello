import pygame, sys
import JeuOthello
import LogiqueOthello


class Menu:
    def __init__(self):
        """ Cette fonction va initialiser la fenêtre du menu principal """

        pygame.init()
        self.screen = pygame.display.set_mode((800, 900))  # taille de la fenêtre

        self.newGameRect = pygame.Rect(80, 160, 160, 80)

        self.font = pygame.font.SysFont('Arial', 20, True, False)
        self.level_font = pygame.font.SysFont('Arial', 15, True, False)

        self.level_IA1 = -1
        self.level_IA2 = -1
        self.level_seul_IA = -1

        self.RUN = True

    def run(self):
        """ Cette fonction correspond à la boucle de lancement du jeu """

        while self.RUN:
            self.input()
            self.draw()

    def input(self):
        """ Correspond aux entrées de l'application"""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.RUN = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button1_rect.collidepoint(event.pos):  # Bouton Humain vs Humain
                    print("Button 1 clicked")
                    JeuOthello.Othello(1, self.level_IA1, self.level_IA2, self.level_seul_IA).run()

                elif self.button2_rect.collidepoint(event.pos):  # Bouton Humain vs IA
                    print("Button 2 clicked")
                    if not self.level_seul_IA == -1:
                        JeuOthello.Othello(2, self.level_IA1, self.level_IA2, self.level_seul_IA).run()

                elif self.button3_rect.collidepoint(event.pos):  # Bouton IA vs IA
                    print("Button 3 clicked")

                    # Faire apparaître le choix de niveau d'IA
                    if not self.level_IA1 == -1 and not self.level_IA2 == -1:
                        # JeuOthello.Othello(3).run()
                        JeuOthello.Othello(3, self.level_IA1, self.level_IA2, self.level_seul_IA).run()

                # Boutons pour sélectionner le niveau de l'IA1
                elif self.facile_button_rect.collidepoint(event.pos):  # Bouton facile IA 1
                    print("bouton facile1 ")
                    self.level_IA1 = 1

                elif self.moyen_button_rect.collidepoint(event.pos):  # Bouton moyen IA 1
                    print("bouton moyen1 ")
                    self.level_IA1 = 2

                elif self.difficile_button_rect.collidepoint(event.pos):  # Bouton difficile IA 1
                    print("bouton difficile1 ")
                    self.level_IA1 = 3

                # Boutons pour sélectionner le niveau de l'IA2
                elif self.facile_button_rect2.collidepoint(event.pos):  # Bouton facile IA 2
                    print("bouton facile2 ")
                    self.level_IA2 = 1

                elif self.moyen_button_rect2.collidepoint(event.pos):  # Bouton moyen IA 2
                    print("bouton moyen2 ")
                    self.level_IA2 = 2

                elif self.difficile_button_rect2.collidepoint(event.pos):  # Bouton difficile IA 2
                    print("bouton difficile2 ")
                    self.level_IA2 = 3

                elif self.random_button_rect.collidepoint(event.pos):  # Bouton aléatoire IA 1
                    print("bouton aléatoire ")
                    self.level_IA1 = 0

                elif self.random_button_rect2.collidepoint(event.pos):  # Bouton aléatoire IA 2
                    print("bouton aléatoire ")
                    self.level_IA2 = 0

                # Boutons pour le niveau de l'IA humain vs hIA
                elif self.f_button_rect2.collidepoint(event.pos):  # Bouton facile IA 1
                    print("bouton facile ")
                    self.level_seul_IA = 1

                elif self.m_button_rect2.collidepoint(event.pos):  # Bouton moyen IA 1
                    print("bouton moyen ")
                    self.level_seul_IA = 2

                elif self.d_button_rect2.collidepoint(event.pos):  # Bouton difficile IA 1
                    print("bouton difficile ")
                    self.level_seul_IA = 3

                elif self.a_button_rect2.collidepoint(event.pos):  # Bouton aléatoire IA
                    print("bouton aléatoire ")
                    self.level_seul_IA = 0

                elif self.quit_button_rect.collidepoint(event.pos):
                    print("bouton quitter clicked")

                    self.RUN = False


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_buttons()
        self.draw_level_buttons()
        self.draw_level_humain_vs_IA()
        self.draw_titre()
        self.draw_credits()

        pygame.display.update()

    def draw_titre(self):
        # Dessin du titre "Othello" en grand en haut de la fenêtre
        title_font = pygame.font.SysFont('Arial', 100, True, False)
        title_text = title_font.render("Othello", True, pygame.Color('white'))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)

    def draw_credits(self):
        """Textes pour les crédits"""

        title_font = pygame.font.SysFont('Arial', 100, True, False)
        title_text = self.font.render("Maily Ciavaldini, Samuel Lavallee", True, pygame.Color('white'))
        title_rect = title_text.get_rect(bottom=(self.screen.get_width()) +100)
        self.screen.blit(title_text, title_rect)

        uni_font = pygame.font.SysFont('Arial', 100, True, False)
        uni_text = self.font.render("Université Paris Cité", True, pygame.Color('white'))
        uni_rect = uni_text.get_rect(bottom=(self.screen.get_width())+75)
        self.screen.blit(uni_text, uni_rect)

    def draw_buttons(self):
        button_size = 200
        button_spacing = 100
        total_width = (button_size * 3) + (button_spacing * 2)
        button_x = (self.screen.get_width() - total_width) // 2
        button_y = self.screen.get_height() // 2 - button_size // 2

        # Button 1
        self.button1_rect = pygame.Rect(button_x, button_y, button_size, button_size)
        pygame.draw.circle(self.screen, pygame.Color('white'), self.button1_rect.center, button_size // 2, 2)
        pygame.draw.circle(self.screen, pygame.Color('white'), self.button1_rect.center, button_size // 2 - 10)

        button_text = self.font.render("Humain vs Humain", True, pygame.Color('black'))
        text_rect = button_text.get_rect(center=self.button1_rect.center)
        self.screen.blit(button_text, text_rect)

        # Button 2
        button_x += button_size + button_spacing
        self.button2_rect = pygame.Rect(button_x, button_y, button_size, button_size)
        pygame.draw.circle(self.screen, pygame.Color('white'), self.button2_rect.center, button_size // 2, 2)
        pygame.draw.circle(self.screen, pygame.Color('white'), self.button2_rect.center, button_size // 2 - 10)

        button_text = self.font.render("Humain vs IA", True, pygame.Color('black'))
        text_rect = button_text.get_rect(center=self.button2_rect.center)
        self.screen.blit(button_text, text_rect)

        # Button 3
        button_x += button_size + button_spacing
        self.button3_rect = pygame.Rect(button_x, button_y, button_size, button_size)
        pygame.draw.circle(self.screen, pygame.Color('white'), self.button3_rect.center, button_size // 2, 2)
        pygame.draw.circle(self.screen, pygame.Color('white'), self.button3_rect.center, button_size // 2 - 10)

        button_text = self.font.render("IA vs IA", True, pygame.Color('black'))
        text_rect = button_text.get_rect(center=self.button3_rect.center)
        self.screen.blit(button_text, text_rect)

        # Bouton Quitter
        button_x = (self.screen.get_width() - 200) // 2
        button_y += button_size + 100
        self.quit_button_rect = pygame.Rect(button_x, button_y, 200, 60)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.quit_button_rect, 2)

        quit_button_text = self.font.render("Quitter le jeu", True, pygame.Color('white'))
        quit_text_rect = quit_button_text.get_rect(center=self.quit_button_rect.center)
        self.screen.blit(quit_button_text, quit_text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def draw_level_buttons(self):
        """Cette fonction va dessiner les boutons pour sélectionner le niveau de difficulté des deux IA"""

        # Texte "VS"
        blanc_x = (self.screen.get_width()) - 105
        blanc_y = (self.screen.get_height()) - 330
        blanc_text = self.level_font.render("VS", True, pygame.Color('red'))
        blanc_rect = pygame.Rect(blanc_x, blanc_y, 80, 30)
        self.screen.blit(blanc_text, blanc_rect)

        # Nom (couleur) du joueur blanc
        blanc_x = (self.screen.get_width()) - 170
        blanc_y = (self.screen.get_height()) - 100
        blanc_text = self.level_font.render("BLANC", True, pygame.Color('white'))
        blanc_rect = pygame.Rect(blanc_x, blanc_y, 80, 30)
        self.screen.blit(blanc_text, blanc_rect)

        # Nom (couleur) du joueur noir
        noir_x = (self.screen.get_width()) - 65
        noir_y = (self.screen.get_height()) - 100
        noir_text = self.level_font.render("NOIR", True, pygame.Color('white'))
        noir_rect = pygame.Rect(noir_x, noir_y, 80, 30)
        self.screen.blit(noir_text, noir_rect)

        # Bouton Random IA1
        button_x = (self.screen.get_width()) - 185
        button_y = (self.screen.get_height()) - 150
        self.random_button_rect = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.random_button_rect, 2)

        random_button_text = self.level_font.render("Aléatoire", True, pygame.Color('white'))
        random_text_rect = random_button_text.get_rect(center=self.random_button_rect.center)
        self.screen.blit(random_button_text, random_text_rect)

        # Bouton Random IA2
        button_x = (self.screen.get_width()) - 85
        button_y = (self.screen.get_height()) - 150
        self.random_button_rect2 = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.random_button_rect2, 2)

        random_button_text2 = self.level_font.render("Aléatoire", True, pygame.Color('white'))
        random_text_rect2 = random_button_text2.get_rect(center=self.random_button_rect2.center)
        self.screen.blit(random_button_text2, random_text_rect2)

        # Boutons pour IA1 (joueur 1 blanc)

        # Bouton Facile
        button_x = (self.screen.get_width()) - 185
        button_y = (self.screen.get_height()) - 300
        self.facile_button_rect = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.facile_button_rect, 2)

        facile_button_text = self.level_font.render("Facile", True, pygame.Color('white'))
        facile_text_rect = facile_button_text.get_rect(center=self.facile_button_rect.center)
        self.screen.blit(facile_button_text, facile_text_rect)

        # Bouton Moyen
        button_x = (self.screen.get_width()) - 185
        button_y = (self.screen.get_height()) - 250
        self.moyen_button_rect = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.moyen_button_rect, 2)

        moyen_button_text = self.level_font.render("Moyen", True, pygame.Color('white'))
        moyen_text_rect = moyen_button_text.get_rect(center=self.moyen_button_rect.center)
        self.screen.blit(moyen_button_text, moyen_text_rect)

        # Bouton Difficile
        button_x = (self.screen.get_width()) - 185
        button_y = (self.screen.get_height()) - 200
        self.difficile_button_rect = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.difficile_button_rect, 2)

        difficile_button_text = self.level_font.render("Difficile", True, pygame.Color('white'))
        difficile_text_rect = difficile_button_text.get_rect(center=self.difficile_button_rect.center)
        self.screen.blit(difficile_button_text, difficile_text_rect)

        # Boutons pour IA2 (joueur -1 noir)

        # Bouton Facile
        button_x = (self.screen.get_width()) - 85
        button_y = (self.screen.get_height()) - 300
        self.facile_button_rect2 = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.facile_button_rect2, 2)

        facile_button_text2 = self.level_font.render("Facile", True, pygame.Color('white'))
        facile_text_rect2 = facile_button_text2.get_rect(center=self.facile_button_rect2.center)
        self.screen.blit(facile_button_text2, facile_text_rect2)

        # Bouton Moyen
        button_x = (self.screen.get_width()) - 85
        button_y = (self.screen.get_height()) - 250
        self.moyen_button_rect2 = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.moyen_button_rect2, 2)

        moyen_button_text2 = self.level_font.render("Moyen", True, pygame.Color('white'))
        moyen_text_rect2 = moyen_button_text2.get_rect(center=self.moyen_button_rect2.center)
        self.screen.blit(moyen_button_text2, moyen_text_rect2)

        # Bouton Difficile
        button_x = (self.screen.get_width()) - 85
        button_y = (self.screen.get_height()) - 200
        self.difficile_button_rect2 = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.difficile_button_rect2, 2)

        difficile_button_text2 = self.level_font.render("Difficile", True, pygame.Color('white'))
        difficile_text_rect2 = difficile_button_text2.get_rect(center=self.difficile_button_rect2.center)
        self.screen.blit(difficile_button_text2, difficile_text_rect2)

    def draw_level_humain_vs_IA(self):
        """Cette fonction va dessiner les different boutons de niveaux pour le mode humain vs IA"""

        # Boutons pour IA2 (joueur -1 noir)

        # Bouton Facile
        button_x = (self.screen.get_width()) // 2 - 90
        button_y = (self.screen.get_height()) // 2 - 200
        self.f_button_rect2 = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.f_button_rect2, 2)

        f_button_text2 = self.level_font.render("Facile", True, pygame.Color('white'))
        f_text_rect2 = f_button_text2.get_rect(center=self.f_button_rect2.center)
        self.screen.blit(f_button_text2, f_text_rect2)

        # Bouton Moyen
        button_x = (self.screen.get_width()) // 2 - 90
        button_y = (self.screen.get_height()) // 2 - 150
        self.m_button_rect2 = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.m_button_rect2, 2)

        m_button_text2 = self.level_font.render("Moyen", True, pygame.Color('white'))
        m_text_rect2 = m_button_text2.get_rect(center=self.m_button_rect2.center)
        self.screen.blit(m_button_text2, m_text_rect2)

        # Bouton Difficile
        button_x = (self.screen.get_width()) // 2 + 20
        button_y = (self.screen.get_height()) // 2 - 200
        self.d_button_rect2 = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.d_button_rect2, 2)

        d_button_text2 = self.level_font.render("Difficile", True, pygame.Color('white'))
        d_text_rect2 = d_button_text2.get_rect(center=self.d_button_rect2.center)
        self.screen.blit(d_button_text2, d_text_rect2)

        # Bouton Aléatoire
        button_x = (self.screen.get_width()) // 2 +20
        button_y = (self.screen.get_height()) // 2 - 150
        self.a_button_rect2 = pygame.Rect(button_x, button_y, 80, 30)
        pygame.draw.rect(self.screen, pygame.Color('white'), self.a_button_rect2, 2)

        a_button_text2 = self.level_font.render("Aléatoire", True, pygame.Color('white'))
        a_text_rect2 = a_button_text2.get_rect(center=self.a_button_rect2.center)
        self.screen.blit(a_button_text2, a_text_rect2)

    def get_level_IA1(self=None):
        return self.level_IA1

    def get_level_IA2(self=None):
        return self.level_IA2


if __name__ == '__main__':
    game = Menu()
    game.run()
    pygame.quit()  # Lorsque RUN est false, va quitter
