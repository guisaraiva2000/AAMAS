import pygame

from utils.settings import BLACK


class Button:
    def __init__(self, color, x, y, width, height, text='', text_color=BLACK):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), border_radius=30)

        if self.text != '':
            font = pygame.font.SysFont('Verdana', 13, True)
            text = font.render(self.text, True, self.text_color)
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height
