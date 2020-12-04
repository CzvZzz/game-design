import sys
import pygame
from bullet import Bullet
from time import sleep
from reward import Reward
from alien import Alien
import random

def start_game(ai_settings, screen, stats, sb, play_button, ship, aliens,bullets):
    #重置游戏设置
    ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏统计信息
    stats.reset_stats()
    stats.game_active = True

    # 重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, aliens)
    ship.center_ship()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    #在玩家单击Play按钮时开始新游戏
    play_button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if play_button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

def check_exit_button(ai_settings, screen, stats, sb, exit_button, ship, aliens, bullets, mouse_x, mouse_y):
    exit_button_clicked = exit_button.rect.collidepoint(mouse_x, mouse_y)
    if exit_button_clicked and not stats.game_active:
        sys.exit()

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, play_button, aliens, fireSound):
    # 响应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_UP:
        ship.moving_up = True
    if event.key == pygame.K_DOWN:
        ship.moving_down = True
    if event.key == pygame.K_p:
        if stats.game_active == False:
            start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
    elif event.key == pygame.K_SPACE:
        if stats.game_active == True:
            fireSound.play()
            fire_bullet(ai_settings, screen, ship, bullets)

def check_keyup_events(event,ship):
    # 响应松开
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_UP:
        ship.moving_up = False
    if event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ai_settings, screen, stats, sb, play_button, exit_button, ship, aliens, bullets, fireSound):
    #响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, play_button, aliens, fireSound)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            check_exit_button(ai_settings, screen, stats, sb, exit_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.USEREVENT and stats.game_active:
            create_fleet(ai_settings, screen, aliens)

def fire_bullet(ai_settings, screen, ship,bullets):
    #如果还没有到达限制，就发射一颗子弹'
    #创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, exit_button, start_background, die_aliens):
    # 更新屏幕上的图像，并且换到新屏幕
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    image_path_list = ['', 'images/reward1.bmp', 'images/reward2.bmp', 'images/reward3.bmp', 'images/reward4.bmp', 'images/wingame.bmp']
    if stats.score == 800 or stats.score == 1600 or stats.score == 2400 or stats.score == 3200:
        if stats.level < 5:
            # 创建一个奖品
            reward = Reward(screen, ai_settings, image_path_list[stats.level])
            reward.blitme()
            ship.blitme()
            sb.show_score()
        else:
            # 创建通关结束画面
            reward = Reward(screen, ai_settings, image_path_list[stats.level])
            reward.blitme()

            # 如果游戏处于非活动状态，就绘制Play按钮
            if not stats.game_active:
                exit_button.draw_button()
                play_button.draw_button()
        update_reward(ai_settings, sb, screen, ship, reward, stats, bullets, aliens)
    else:
        ship.blitme()
        aliens.draw(screen)
        sb.show_score()
        # 在飞船和外星人后面重绘所有的子弹
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        for die_alien in die_aliens:

            if die_alien.down_index == 0:
                pass
            if die_alien.down_index > 7:
                die_aliens.remove(die_alien)
                continue
            # 显示碰撞图片
            screen.blit(pygame.image.load('images/bump.png'), die_alien.rect)
            die_alien.down_index += 1
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def start_meun(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, exit_button, start_background):
    screen.fill(ai_settings.bg_color)
    start_background.blitme()
    play_button.draw_button()
    exit_button.draw_button()
    pygame.display.flip()

def end_meun(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, exit_button, end_background):
    screen.fill(ai_settings.bg_color)
    play_button.draw_button()
    exit_button.draw_button()
    pygame.display.flip()


def start_new_level(ai_settings, stats, sb, bullets):
    # 删除现有的子弹
    bullets.empty()
    ai_settings.increase_speed()

    # 提高等级
    stats.level += 1
    sb.prep_level()

def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, die_aliens, explosiveSound):
    # 响应子弹和外星人的碰撞
    # 删除发生碰撞的子弹和外星人
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        # 爆炸音效
        explosiveSound.play()
        for alien in collisions.values():
            stats.score += ai_settings.alien_points * len(alien)
            sb.prep_score()
        for die_alien in collisions.values():
            die_aliens.add(die_alien)
        check_high_score(stats, sb)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, die_aliens, explosiveSound):
    # 更新子弹的位置，并删除已消失的子弹
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets, die_aliens, explosiveSound)

def check_high_score(stats, sb):
    # 检查是否诞生了新的最高分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open('stats\max_score.txt', 'w') as ms:
            ms.write(str(stats.high_score))
        sb.prep_high_score()

def update_reward(ai_settings, sb, screen, ship, reward, stats, bullets, aliens):
    # 检测奖品和飞船之间的碰撞
    if pygame.sprite.collide_rect(ship, reward):
        if stats.level >= 4 and stats.game_active:
            stats.level += 1
            stats.game_active = False
            pygame.mouse.set_visible(True)
        elif stats.game_active:
            start_new_level(ai_settings, stats, sb, bullets)
            create_fleet(ai_settings, screen, aliens)
            ship.center_ship()

def create_alien(ai_settings, screen, aliens):
    alien = Alien(ai_settings, screen)
    alien.x = random.choice(range(200, 300, 30))
    alien.rect.x = alien.x
    aliens.add(alien)

def create_fleet(ai_settings, screen, aliens):
    number_aliens_x = 1
    for alien_number in range(number_aliens_x):
        create_alien(ai_settings, screen, aliens)


def change_fleet_direction(ai_settings, aliens):
    # 将整群外星人下移，并改变他们的方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
    # 有外星人到达边缘时采取相应的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets, play_button):
    # 响应被外星人撞到的飞船
    # 将ship_left减1
    if stats.ship_left > 0:
        stats.ship_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 子弹列表
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕低端中央
        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.level = 5
        stats.game_active = False
        pygame.mouse.set_visible(True)
        play_button.draw_button()

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets, play_button):
    # 检查是否有外星人到达了屏幕低端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, play_button)
            break

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button):
    # 更新外星人群中所有外星人的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button)

    # 检查是否有外星人到达屏幕低端
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button)


