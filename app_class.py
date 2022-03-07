import pygame, sys
from settings import *


pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

############################# HELPER FUNCTIONS ##########################################
    def draw_text(self, words, screen, pos, size, color, font_name):
        font  = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        pos[0] = pos[0]-text_size[0]//2
        pos[1] = pos[1]-text_size[0]//2
        screen.blit(text, pos)




############################# INTRO FUNCTIONS ##########################################

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'


    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(black)
        self.draw_text('Push Space Bar', self.screen, [width//2, height//2], start_text_size, (80,205,78), start_font)
        pygame.display.update()

        