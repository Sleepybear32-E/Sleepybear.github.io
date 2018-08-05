import random
import pygame

# 屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 帧率常量
CLOCK_FRAME = 60
# 创建敌机定时器
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 创建子弹定时器
CREATE_BULLET_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image, speed):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    # 背景精灵 背景的移动
    def __init__(self, alt=False):
        super().__init__("./image/background.png", 1)
        if alt == True:
            self.rect.y = -self.rect.height

    def update(self):
        # 1.调用父类方法update
        super().update()
        # 2. 半段图像是否移除屏幕, 如果移除，将图像移到screen最上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    # 敌机精灵
    def __init__(self):

        # 1.调用父类方法
        super().__init__("./image/enemy1.png", 1)
        # 2.敌机的初始速度
        self.speed = random.randint(1, 3)
        # 3.敌机的初始位置
        self.rect.y = -self.rect.height
        enemy_appear_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, enemy_appear_x)

    def update(self):
        # 1.调用父类方法，保持垂直飞行
        super().update()
        # 2.判断是否飞出屏幕，如果是，从精灵组内删除
        if self.rect.y >= SCREEN_RECT.height:
            # kill方法可以所有精灵从精灵组销毁
            self.kill()

    def __del__(self):
        pass


class MainPlane(GameSprite):
    def __init__(self):
        super().__init__("./image/me1.png", 0)
        # 把主飞机放在屏幕最中间
        self.plane_x = 0.5 * SCREEN_RECT.width - 0.5 * self.rect.width
        self.rect.x = self.plane_x
        # 把主飞机放在离屏幕底端120的地方
        self.plane_y = SCREEN_RECT.height - 120 - self.rect.height
        self.rect.y = self.plane_y
        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()

    # 设置主飞机的移动速度
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > (SCREEN_RECT.width - self.rect.width):
            self.rect.x = (SCREEN_RECT.width - self.rect.width)

    def fire(self):
        # 创建子弹精灵
        self.bullet = Bullet()
        # 创建子弹位置
        self.bullet.rect.y = self.plane_y - 20
        self.bullet.rect.x = self.rect.x + 0.5 * self.rect.width
        # 添加精灵
        self.bullet.add(self.bullet_group)


# 子弹精灵
class Bullet(GameSprite):
    def __init__(self):
        super().__init__("./image/bullet1.png", -2)
        pass

    def update(self):
        # 子弹沿上方飞行
        super().update()
        # 判断子弹时候飞出屏幕
        if self.rect.y < -self.rect.height:
            self.kill()

    def __del__(self):
        pass
