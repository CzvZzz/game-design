import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from background import Background

def run_game():
    # 初始化混音器模块
    pygame.mixer.init()

    # 无线循环的背景音乐
    pygame.mixer.music.load('voice/123.mp3')
    # -1代表无限循环（背景音乐）
    pygame.mixer.music.play(-1)

    # 枪声
    fireSound = pygame.mixer.Sound('voice/5313.wav')

    # 爆炸声
    explosiveSound = pygame.mixer.Sound('voice/9730.wav')

    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("plane go!")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, 'Play', 50, 50)

    # 创建exit按钮
    exit_button = Button(ai_settings, screen, 'exit game', 50, 200)

    # 创建一艘飞船，创建一个用于存储子弹的编组，创建一个外星人编组
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()
    die_aliens = Group()

    # 创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 创建背景图片
    start_background = Background(screen, ai_settings, 'images/background.jpg')
    end_background = Background(screen, ai_settings, 'images/background.jpg')

    pygame.time.set_timer(pygame.USEREVENT, 3000)
    # 游戏循环帧率设置
    clock = pygame.time.Clock()

    # 开始游戏的主循环
    while True:

        clock.tick(200)
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, exit_button, ship, aliens, bullets, fireSound)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, die_aliens, explosiveSound)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, play_button)
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, exit_button, start_background, die_aliens)
        elif not stats.game_active and stats.level == 0:
            gf.start_meun(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, exit_button, start_background)
        elif not stats.game_active and stats.level == 5:
            gf.end_meun(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, exit_button, end_background)

if __name__ == '__main__':
    run_game()