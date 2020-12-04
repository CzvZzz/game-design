class Settings():
#存储《外星人入侵》的所有设置的类
    def __init__(self):
        # 初始化游戏的设置
        # 屏幕设置
        self.screen_width = 450
        self.screen_height = 700
        self.bg_color = (240, 255, 255)

        # 飞船的设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 300
        self.bullet_height = 20
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # 外星人设置
        self.fleet_drop_speed = 30

        # 加快游戏节奏的速度
        self.speedup_scale = 1.1

        # 外星人点数的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''初始化随游戏进行而变化的设置'''
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 2.3
        self.alien_speed_factor = 1
        self.enemy_move_speed = 1.5

        # fleet_direction为1表示向右；为-1表示向左
        self.fleet_direction = 1


        #记分
        self.alien_points = 50


    def increase_speed(self):
        # 提高速度设置和分数设置
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

