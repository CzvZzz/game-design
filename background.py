import pygame
from pygame.sprite import Sprite

class Background(Sprite):
    def __init__(self, screen, ai_settings, path):
        # 初始化背景并设置其初始位置
        self.screen = screen
        self.ai_settings = ai_settings
        self.path = path

        # 加载背景图像并获取其外接矩形
        #self.image = pygame.image.load('images/background.jpg')
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()

        # 获取窗口的外接矩形
        self.screen_rect = screen.get_rect()

    def blitme(self):
        # 在指定位置绘制背景
        self.screen.blit(self.image, self.rect)