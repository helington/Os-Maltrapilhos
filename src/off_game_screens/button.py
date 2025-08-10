import pygame

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface, selected):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if (pygame.mouse.get_pressed()[0] == 1) and not self.clicked:
                self.clicked = True
                action = True

        if selected and key[pygame.K_RETURN] and not self.clicked:
            self.clicked = True
            action = True

        if pygame.mouse.get_pressed()[0] == 0 and not key[pygame.K_RETURN]:
            self.clicked = False

        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action