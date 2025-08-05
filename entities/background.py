import pygame

pygame.init()
tela_comprimento = 800
tela_largura = 200
tela = pygame.display.set_mode((tela_comprimento,tela_largura))

class BACKGROUND:
    
    # Para a proporcao 800x200, 135p é a altura mínima do chao

    # init com variaveis, percorre as imagens na pasta
    def __init__(self):
        self.scroll = 0

        self.chao = pygame.image.load(fr'C:\Users\Nóbrega\Desktop\dev\PYGAME PROJETO\entities\bg\ground.png').convert_alpha()
        self.chao_largura = self.chao.get_width()
        self.chao_comprimento = self.chao.get_height()
        self.imagens = []

        for i in range(1,6):
            imagem_atual = pygame.image.load(fr'C:\Users\Nóbrega\Desktop\dev\PYGAME PROJETO\entities\bg\Jungle Asset Pack\Jungle Asset Pack\parallax background\plx-{i}.png').convert_alpha()
            self.imagens.append(imagem_atual)

        self.imagem_comprimento = imagem_atual.get_width()

    # faz o draw com blit, nn sei como vai funcionar com o draw numa funcao maior la no main
    def draw_bg(self):

        for x in range (5):
            speed = 1
            for i in self.imagens:
                tela.blit(i,((x*self.imagem_comprimento) - self.scroll*speed,0))
                speed+=0.2

    # msm coisa da ultima funcao nn sei como vai funcionar com o draw na main
    def draw_ground(self):

        for x in range(15):
            tela.blit(self.chao, ((x* self.chao_largura) - self.scroll *2.5,tela_largura - self.chao_comprimento))
