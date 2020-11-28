import sys
import pygame
from bullet import Bullet
from time import sleep
import monster_aliens
from reward import Reward

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
    monster_aliens.create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    #在玩家单击Play按钮时开始新游戏
    play_button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if play_button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

def checl_exit_button(ai_settings, screen, stats, sb, exit_button, ship, aliens, bullets, mouse_x, mouse_y):
    exit_button_clicked = exit_button.rect.collidepoint(mouse_x, mouse_y)
    if exit_button_clicked and not stats.game_active:
        sys.exit()

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, play_button, aliens):
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

def check_events(ai_settings, screen, stats, sb, play_button, exit_button, ship, aliens, bullets):
    #响应按键和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, sb, play_button, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if stats.level < 5:
                check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
            else:
                checl_exit_button(ai_settings, screen, stats, sb, exit_button, ship, aliens, bullets, mouse_x, mouse_y)
def fire_bullet(ai_settings, screen, ship,bullets):
    #如果还没有到达限制，就发射一颗子弹'
    #创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, exit_button):
    # 更新屏幕上的图像，并且换到新屏幕
    # 每次循环时都重绘屏幕
    image_list = ['', 'images/reward1.bmp', 'images/reward2.bmp', 'images/reward3.bmp', 'images/reward4.bmp']
    if len(aliens) == 0:
        screen.fill(ai_settings.bg_color)

        # 在飞船和外星人后面重绘所有的子弹
        for bullet in bullets.sprites():
            bullet.draw_bullet()

        if stats.level < 5:
            # 创建一个奖品
            image = pygame.image.load(image_list[stats.level])
            reward = Reward(screen, ai_settings, image)
            reward.blitme()
        else:
            # 创建通关结束画面
            image = pygame.image.load('images/wingame.bmp')
            reward = Reward(screen, ai_settings, image)
            reward.blitme()
            # 如果游戏处于非活动状态，就绘制Play按钮
            if not stats.game_active:
                exit_button.draw_button()

        ship.blitme()
        sb.show_score()
        if update_reward(ai_settings, sb, screen, ship, reward):
            if stats.level >= 4 and stats.game_active:
                stats.level += 1
                stats.game_active = False
                pygame.mouse.set_visible(True)
            elif stats.game_active:
                start_new_level(ai_settings, stats, sb, bullets)
                monster_aliens.create_fleet(ai_settings, screen, ship, aliens)
                ship.center_ship()
    else:
        screen.fill(ai_settings.bg_color)
        # 在飞船和外星人后面重绘所有的子弹
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)
        sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active and stats.level < 5:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()

def start_new_level(ai_settings, stats, sb, bullets):
    # 删除现有的子弹
    bullets.empty()
    ai_settings.increase_speed()

    # 提高等级
    stats.level += 1
    sb.prep_level()

def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 响应子弹和外星人的碰撞
    # 删除发生碰撞的子弹和外星人
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    '''
    if len(aliens) == 0:
        
        while(flag):
            if update_reward(ai_settings, sb, screen, ship, reward, bullets):
                start_new_level(ai_settings, stats, sb, bullets)
                monster_aliens.create_fleet(ai_settings, screen, ship, aliens)
                flag = 0
        
        start_new_level(ai_settings, stats, sb, bullets)
        #reward.blitme()
        monster_aliens.create_fleet(ai_settings, screen, ship, aliens)
    '''

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 更新子弹的位置，并删除已消失的子弹
    # 更新子弹的位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)

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

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕低端中央
        monster_aliens.create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
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

def check_high_score(stats, sb):
    # 检查是否诞生了新的最高分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open('stats\max_score.txt', 'w') as ms:
            ms.write(str(stats.high_score))
        sb.prep_high_score()

def ship_reward_update(ai_settings, sb, screen, ship, reward):
    # 检测奖品和飞船之间的碰撞
    if pygame.sprite.collide_rect(ship, reward):
        return reward_hit(ai_settings, sb, screen, ship, reward)
    else:
        return False

def reward_hit(ai_settings, sb, screen, ship, reward):
    # 响应被飞船撞到的奖品
    sleep(0.5)
    return True

def update_reward(ai_settings, sb, screen, ship, reward):
    return ship_reward_update(ai_settings, sb, screen, ship, reward)
