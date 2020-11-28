import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from play_button import Play_Button
from exit_button import Exit_Button
from scoreboard import Scoreboard
import monster_aliens
from reward import Reward

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("  Alien Invasion")

    # 创建Play按钮
    play_button = Play_Button(ai_settings, screen, 'Play')

    # 创建exit按钮
    exit_button = Exit_Button(ai_settings, screen, 'exit game')

    # 创建一艘飞船，创建一个用于存储子弹的编组，创建一个外星人编组
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()

    # 创建外星人群
    monster_aliens.create_fleet(ai_settings, screen, ship, aliens)

    # 创建一个用于存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # 开始游戏的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, exit_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets, play_button)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, exit_button)

if __name__ == '__main__':
    run_game()