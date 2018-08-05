from plane_sprites import *


class Planegame(object):
    def __init__(self):

        # 1.设置游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 设置标题
        pygame.display.set_caption("Michael's PLANEGAME")
        # 3.创建游戏时钟
        self.clock = pygame.time.Clock()
        # 4.调用私有方法
        self.__create_sprites()
        # 5.每隔一秒创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 250)
        # 6. 每隔0.5s发射子弹
        pygame.time.set_timer(CREATE_BULLET_EVENT, 500)

    def __create_sprites(self):
        # 创建背景精灵和精灵组
        self.bg1 = Background()
        self.bg2 = Background(True)
        self.back_group = pygame.sprite.Group(self.bg1, self.bg2)
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建主飞机
        self.hero = MainPlane()
        self.main_plane = pygame.sprite.Group(self.hero)

    def start_game(self):

        while True:
            # 1.设置刷新帧率
            self.clock.tick(CLOCK_FRAME)
            # 2.事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide_()
            # 4. 更新/绘制精灵组
            self.__update_sprites_()
            # 5.更新显示
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                game.__game_over()
            # 创建敌机, 将敌机加入精灵组
            elif event.type == CREATE_ENEMY_EVENT:
                self.enemy = Enemy()
                self.enemy.update()
                # 将敌机加入精灵组
                self.enemy_group.add(self.enemy)
            # 开火
            elif event.type == CREATE_BULLET_EVENT:
                self.hero.fire()

        #  设置摁键，向左或者向右
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.update()
            self.hero.speed = 2
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.update()
            self.hero.speed = -2
        else:
            self.hero.update()
            self.hero.speed = 0

    def __check_collide_(self):
        # 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullet_group, self.enemy_group, True, True)
        if pygame.sprite.groupcollide(self.main_plane, self.enemy_group, False, True):
            self.hero.kill()
            game.__game_over()

    def __update_sprites_(self):
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.main_plane.update()
        self.main_plane.draw(self.screen)

        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)


    # 静态方法
    @staticmethod
    def __game_over():
        pygame.quit()
        exit()


if __name__ == '__main__':

    game = Planegame()

    game.start_game()


