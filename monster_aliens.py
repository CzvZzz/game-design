#coding:utf-8
from monster_alien import Alien

def get_number_aliens_x(ai_settings, alien_width):
    # 计算每行可容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_heigt):
    # 计算屏幕可容纳多少行外星人
    available_space_y = (ai_settings.screen_height - (3 * alien_heigt) - ship_height)
    number_rows = int(available_space_y / (2 * alien_heigt))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建一个外星人并将其放入当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    # 创建外星人群
    # 创建一个外星人，并计算一行可容纳都少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)