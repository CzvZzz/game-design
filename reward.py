import pygame
from pygame.sprite import Sprite

class Reward(Sprite):
    def __init__(self, screen, ai_settings, path):
        # 初始化奖品并设置奖品位置
        super(Reward, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.path = path

        # 加载奖品图像并获取其外接矩形
        self.image = pygame.image.load(self.path)
        self.rect = self.image.get_rect()

        # 获取窗口的外接矩形
        self.screen_rect = screen.get_rect()

        # 将奖品放在屏幕正中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 250

    def blitme(self):
        # 在指定位置绘制奖品
        self.screen.blit(self.image, self.rect)