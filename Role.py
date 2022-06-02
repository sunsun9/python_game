import math
from cmath import sqrt

import pygame.key

from Fire import fire
from bomb import Bomb
from core import Array2D, GameMap

"""该文件主要是创建人物，根据不同的人物标记创建不同的人物。同时加载人物行走的功能，以及玩家人物放炸弹、npc人物喷火的功能；还有人物捡包的功能。
同时对于第二个界面侧边的信息加载
"""


class Sprite:
    """用于绘制游戏人物形象的工具类，产生人物形象"""

    @staticmethod   #设置静态方法
    def draw(dest, source, x, y, cell_x, cell_y, cell_w=50, cell_h=75):
        """
        Sprite.draw(screen_surf, self.hero_surf, map_x+cell_x, map_y+cell_y, cell_x, cell_y)
        surface对象就是用来表示图像的
        在绘制时指定，x,y的图像
        :param dest: surface类型，绘制目标的surface，及放置新图片的界面
        :param source: surface类型，来源surface，即我们加载的原始图片
        :param x: 要绘制的图像在dest中的坐标
        :param y: 要绘制的图像在dest中的坐标
        :param cell_x: 要绘制的图像在原始图片中的坐标
        :param cell_y: 要绘制的图像在原始图片中的坐标
        :param cell_w: 单个人物的宽度
        :param cell_h: 单个人物的高度
        :return:
        """
        dest.blit(source, (x, y), (cell_x * cell_w, cell_y * cell_h, cell_w, cell_h))

class role:
    """人物类"""
    def __init__(self, role_img, speed, font, id):
        self.role_img = role_img
        self.blood = 1
        self.speed = speed
        self.star = 1
        self.font = font
        self.id = id    #在地图中的位置标记，便于设置初始位置

    def draw_blood(self, screen_surf):
        """侧面人物的血量显示"""
        blood = str(self.blood)
        blood1 = self.font.render(blood, True, 'red')
        if self.id == 1:
            screen_surf.blit(blood1, (140, 23))
        elif self.id == 2:
            screen_surf.blit(blood1, (150, 186))
        elif self.id == 3:
            screen_surf.blit(blood1, (170, 360))
        elif self.id == 4:
            screen_surf.blit(blood1, (155, 503))
        elif self.id == 5:
            screen_surf.blit(blood1, (165, 683))

    def draw_star(self, screen_surf):
        """侧面人物的炸弹威力显示"""
        star = str(self.star)
        star1 = self.font.render(star, True, 'blue')
        if self.id == 1:
            screen_surf.blit(star1, (140, 45))
        elif self.id == 2:
            screen_surf.blit(star1, (150, 205))
        elif self.id == 3:
            screen_surf.blit(star1, (170, 386))
        elif self.id == 4:
            screen_surf.blit(star1, (155, 523))
        elif self.id == 5:
            screen_surf.blit(star1, (165, 703))

    def draw_speed(self, screen_surf):
        """侧面人物的速度显示"""
        speed = str(self.speed)
        speed1 = self.font.render(speed, True, 'purple')
        if self.id == 1:
            screen_surf.blit(speed1, (140, 67))
        elif self.id == 2:
            screen_surf.blit(speed1, (150, 222))
        elif self.id == 3:
            screen_surf.blit(speed1, (170, 416))
        elif self.id == 4:
            screen_surf.blit(speed1, (155, 543))
        elif self.id == 5:
            screen_surf.blit(speed1, (165, 723))



class RoleWalk(role):
    """ 角色人物行走类    """
    #这四个数值的设定依据图片设置
    DIR_DOWN = 0  #选择向上走的人物形象
    DIR_LEFT = 1    #选择向下走的人物形象
    DIR_RIGHT = 2    #选择向左走的人物形象
    DIR_UP = 3   #选择向右走的人物形象

    def __init__(self, hero_surf, dir, map, font, id, barriers):
        """

        :param hero_surf: 加载人物形象的原始图片
        :param dir: 人物行走的方向，也用来改变人物形象的方向
        :param map: GameMap类，这里主要用到了地图，便于判断该点能否放置可消除障碍类，以及人物是否可行走
        :param font: 字体
        :param id: 选中的人物
        """
        self.step = 1  # 每帧移动的像素,即速度
        super().__init__(hero_surf, self.step, font, id)  # 调用父类的构造函数
        self.hero_surf = hero_surf  #人物图片
        self.dir = dir  #人物方向
        self.px = 0     #初始化坐标在第几列
        self.py = 0 #初始化坐标在第几行
        self.is_walking = False #判断角色是否在移动
        self.frame = 1  #角色形象当前帧
        self.x = 200
        self.y = 0
        self.next_px = 0    #下一步要去的格子在第几列
        self.next_py = 0    #下一步要去的格子在第几行
        self.map = map  #地图，主要是看该点的标记是什么
        self.first_draw = True  #是不是第一次绘制人物形象，方便绘制初始位置及人物被炸后的重新绘制
        self.last = True    #主要是标记玩家人物上一次是否走了传送门
        self.path = []  #存放寻路路径
        self.path_index = 0 #角色在当前path中的下标
        self.bomb = []
        self.barriers = barriers
        self.id = id
        self.is_hurt = False    #人物是否受伤

    def draw(self, screen_surf, map_x, map_y, id, bomb):
        """绘制游戏中的人物 & 产生炸弹"""

        if id != 0: #npc人物被炸的炸弹产生于玩家人物
            self.bomb = bomb
        if len(self.bomb) > 0:
            for i in self.bomb:
                if i.bombing == True:   #表示正在爆炸，不是前面的倒计时阶段了
                    """当位于炸弹的上下左右时，会被炸"""
                    if self.px == i.x + 1 and self.py == i.y:
                        self.blood -= 1
                        self.px = self.get_return_position(id)[1]   #被炸后回到初始位置
                        self.py = self.get_return_position(id)[0]
                        self.next_py = self.py
                        self.next_px = self.px
                        self.is_hurt = True #受伤标志为True
                        self.first_draw = True  #重新初始绘制
                        return
                    #下面都是一样的，只是不同的判断情况
                    if self.px == i.x and self.py == i.y - 1:
                        self.blood -= 1
                        self.px = self.get_return_position(id)[1]
                        self.py = self.get_return_position(id)[0]
                        self.next_py = self.py
                        self.next_px = self.px
                        self.is_hurt = True
                        self.first_draw = True
                        return
                    if self.px == i.x and self.py == i.y + 1:
                        self.blood -= 1
                        self.px = self.get_return_position(id)[1]
                        self.py = self.get_return_position(id)[0]
                        self.next_py = self.py
                        self.next_px = self.px
                        self.is_hurt = True
                        self.first_draw = True
                        return
                    if self.px == i.x - 1 and self.py == i.y:
                        self.blood -= 1
                        self.px = self.get_return_position(id)[1]
                        self.py = self.get_return_position(id)[0]
                        self.next_py = self.py
                        self.next_px = self.px
                        self.is_hurt = True
                        self.first_draw = True
                        return

        if self.first_draw == True and id == 0:     #这就是初始化的人物绘制
            self.px = 0
            map_x = self.px * 64 + 200
            map_y = self.py*65
            self.x = map_x
            self.y = map_y
            self.is_hurt = False
            if self.is_walking == True:
                self.first_draw = False

        if self.first_draw == True and id == 1:
            self.px = 14
            map_x = self.px * 64 + 200
            map_y = self.py*65
            self.x = map_x
            self.y = map_y
            self.is_hurt = False
            if self.is_walking == True:
                self.first_draw = False

        elif self.first_draw == True and id == 2:
            self.py = 12
            map_x = self.px * 64 + 200
            map_y = self.py * 65
            self.x = map_x
            self.y = map_y
            self.is_hurt = False
            if self.is_walking == True:
                self.first_draw = False

        elif self.first_draw == True and id == 3:
            self.py = 12
            self.px = 14
            map_x = self.px * 64 + 200
            map_y = self.py * 65
            self.x = map_x
            self.y = map_y
            self.is_hurt = False
            if self.is_walking == True:
                self.first_draw = False
        cell_x = int(self.frame)    #该放该方向上的哪一步照片，图片中第几列
        cell_y = self.dir
        #绘制该方向该时刻的图像
        Sprite.draw(screen_surf, self.hero_surf, map_x + cell_x, map_y + cell_y, cell_x, cell_y)


        #产生炸弹
        for i in self.bomb:
            if i.draw(screen_surf, self.barriers, self.map) == False:   #炸弹已经爆炸了，删除
                self.bomb.remove(i)
                continue




    def get_return_position(self, id):
        """改变人物方向， 同时返回应该初始化的位置
        根据不同的人物标记，进行不同的反应
        """
        if id == 0:
            self.dir = RoleWalk.DIR_DOWN
            return [0, 0]
        elif id == 1:
            self.dir = RoleWalk.DIR_DOWN
            return [0, 14]
        elif id == 2:
            self.dir = RoleWalk.DIR_UP
            return [12, 0]
        elif id == 3:
            self.dir = RoleWalk.DIR_UP
            return [12, 14]

    def is_go(self):
        """根据map的该点值，判断下一个格子是否可行"""
        if self.map[self.next_py+1][self.next_px] == 1 or self.map[self.next_py+1][self.next_px] == 2 or self.map[self.next_py+1][self.next_px] == 3:
            return True
        else:
            return False

    def role_move(self, screen_surf):
        """人物角色移动，这个只是格子上的移动，具体的移动需要下面一个函数来实现"""
        #下面的几个大的语句是用来判断传送位置的

        if self.last == True and self.py == 0 and self.px == 7: #根据特殊位置，进行传送
            self.next_py = 9
            self.next_px = 6
            self.x = self.next_px*64+200
            self.y = self.next_py*65
            self.last = False
        elif self.last == True and self.py == 9 and self.px == 6:
            self.next_py = 0
            self.next_px = 7
            self.x = self.next_px * 64+200
            self.y = self.next_py * 65
            self.last = False
        elif self.last == True and self.py == 3 and self.px == 1:
            self.next_py = 7
            self.next_px = 11
            self.x = self.next_px * 64+200
            self.y = self.next_py * 65
            self.last = False
        elif self.last == True and self.py == 7 and self.px == 11:
            self.next_py = 3
            self.next_px = 1
            self.x = self.next_px * 64+200
            self.y = self.next_py * 65
            self.last = False

        #下面就所处位置不是传送位置，通过按键行走
        else:
            x = self.next_px
            y = self.next_py
            keys_pressed = pygame.key.get_pressed()

            self.map[1][0] = 1
            #通过触发键盘上的某些键，来移动人物
            if keys_pressed[pygame.K_w]:    #向上走
                if self.is_walking == False:    #第一次按键，改变人物方向
                    self.dir = RoleWalk.DIR_UP
                self.next_py = self.py - 1
                if self.is_go() == False:   #需要判断下一个格子是否可走
                    self.next_py = self.py
                self.is_walking = True  #表示人物正在行走
                if self.py == y:
                    self.last = True

            elif keys_pressed[pygame.K_a]:  #向下走
                if self.is_walking == False:
                    self.dir = RoleWalk.DIR_LEFT
                self.next_px = self.px - 1
                if self.is_go() == False:
                    self.next_px = self.px
                self.is_walking = True
                if self.px == x:
                    self.last = True

            elif keys_pressed[pygame.K_s]:  #向下走
                if self.is_walking == False:
                    self.dir = RoleWalk.DIR_DOWN
                self.next_py = self.py + 1
                if self.is_go() == False:
                    self.next_py = self.py
                self.is_walking = True
                if self.py == y:
                    self.last = True

            elif keys_pressed[pygame.K_d]:  #向右走
                if self.is_walking == False:
                    self.dir = RoleWalk.DIR_RIGHT
                self.next_px = self.px + 1
                if self.is_go() == False:
                    self.next_px = self.px
                self.is_walking = True
                if self.px == x:
                    self.last = True

            elif keys_pressed[pygame.K_j]:  #按键放炸弹
                bomb1 = Bomb(self.px, self.py)
                self.bomb.append(bomb1) #添加该炸弹到列表
            self.move()


    def move(self):
        """实现人物的行走"""
        if self.is_hurt == False:   #不是受伤标记的时候，才会进行移动
            if not self.is_walking:
                return

            aim_x = self.next_px * 64 + 200
            aim_y = self.next_py * 65
            #下面的到达边界判断
            if self.next_py == 13 and self.dir == RoleWalk.DIR_DOWN:
                aim_y = 882
                self.next_py = self.py
            if self.next_px == 15 and self.dir == RoleWalk.DIR_RIGHT:
                aim_x = 1200
                self.next_px = self.px
            if self.next_py == -1 and self.dir == RoleWalk.DIR_UP:
                aim_y = 0
                self.next_py = self.py
            if self.next_px == -1 and self.dir == RoleWalk.DIR_LEFT:
                aim_x = 0
                self.next_px = self.px

            #向下一个格子前进
            if self.x < aim_x:
                self.x += self.step
                if self.x >= aim_x:
                    self.x = aim_x
            elif self.x > aim_x:
                self.x -= self.step
                if self.x <= aim_x:
                    self.x = aim_x

            elif self.y < aim_y:
                self.y += self.step
                if self.y >= aim_y:
                    self.y = aim_y
            elif self.y > aim_y:
                self.y -= self.step
                if self.y <= aim_y:
                    self.y = aim_y

            self.frame = (self.frame + 0.1) % 4  # 每一帧有4张图片，实现人物的动态行走
            self.px = int((self.x-200)/64)
            self.py = int(self.y/65)
            self.get_package()  #人物的捡包操作

            if self.x == aim_x and self.y == aim_y: #到达目的地后不再移动
                self.frame = 1
                self.is_walking = False


     #下面都是关于npc玩家的相关函数
    def dis(self, x1, y1, x2, y2):
        """求2点间距离"""
        dis = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))
        return dis

    def min(self, x, y):
        """比较大小，返回较小值的序号"""
        if x <= y:
            return 1
        else:
            return 0

    def get_package(self):
        """人物的捡包"""
        for i in self.barriers:
            if self.px == i.x and self.py+1 == i.y and i.sign == 1:
                self.blood += 1
                self.barriers.remove(i) #最后一次显示，被触碰后消除


    def b_remove(self, x, y):
        """判断该包所在的障碍列表的位置"""
        for i in self.barriers:
            if i.x == x and i.y == y:
                self.barriers.remove(i)
                return



    def find_path(self, role, num, screen_surf):
        """npc玩家的移动,寻路"""
        s1, s2, s3, s4 = [0, 0], [0, 0], [0, 0], [0, 0] #包含两个元素，第一个表示距离，第二个代表该点状态
        #让初始化的地点可走
        if num == 1:
            self.map[1][14] = 1
        elif num == 2:
            self.map[13][0] = 1
        elif num == 3:
            self.map[13][14] = 1

        #和玩家碰到了是静止的
        if math.fabs(self.px - role.px) == 1 and self.py == role.py or math.fabs(self.py - role.py) == 1 and self.px == role.py:
            if math.fabs(self.px - role.px) == 1 and math.fabs(self.py - role.py) == 1:
                self.is_walking = False

        elif self.is_walking == False:
            #判断4个方向，如果朝这个方向走了，距离有没有变小
            x1 = self.px - 1    #所处位置的上面左边的格子，向左走
            if x1 < 0:
                x1 = self.px
                s1[0] = 10000
            elif self.map[self.py+1][self.px-1] != 1:
                x1 = self.px
                s1[0] = 10000
                if self.map[self.py+1][self.px-1] == 4:
                    x1 = self.px - 1
                    s1[0] = 0
                    s1[1] = 4
                elif self.map[self.py + 1][self.px - 1] == 2:
                    s1[1] = 2
                elif self.map[self.py+1][self.px-1] == 3:
                    s1[1] = 3
            y1 = self.py

            x2 = self.px + 1    #所处位置的右边的格子，向右走
            if x2 > 14:
                x2 = self.px
                s2[0] = 0
            elif self.map[self.py+1][self.px+1] != 1:
                x2 = self.px
                s2[0] = 0
                if self.map[self.py+1][self.px+1] == 4:
                    x2 = self.px + 1
                    s2[0] = 0
                    s2[1] = 4
                elif self.map[self.py+1][self.px+1] == 2:
                    s2[1] = 2
                elif self.map[self.py+1][self.px+1] == 3:
                    s2[1] = 3
            y2 = self.py

            x3 = self.px    #所处位置的上边的格子，向上走
            y3 = self.py - 1
            if y3 < 0:
                y3 = self.py
                s3[0] = 0
            elif self.map[self.py][self.px] != 1:
                y3 = self.py
                s3[0] = 0
                if self.map[self.py][self.px] == 4:
                    y3 = self.py - 1
                    s3[0] = 0
                    s3[1] = 4
                elif self.map[self.py][self.px] == 2:
                    s3[1] = 2
                elif self.map[self.py][self.px] == 3:
                    s3[1] = 3

            x4 = self.px    #所处位置的下面的格子，向下走
            y4 = self.py + 1
            if y4 > 12:
                y4 = self.py
                s4[0] = 0
            elif self.map[self.py+2][self.px] != 1:
                y4 = self.py
                s4[0] = 0
                if self.map[self.py+2][self.px] == 4:
                    y4 = self.py + 1
                    y4 = self.py + 1
                    s4[0] = 0
                    s4[1] = 4
                elif self.map[self.py + 2][self.px] == 2:
                    s4[1] = 2
                elif self.map[self.py+2][self.px] == 3:
                    s4[1] = 3

            if s1[0] == 0: #如果可走的话，判断该玩家于游戏玩家的距离
                s1[0] = self.dis(x1*64+200, y1*65, role.x, role.y)

            if s2[0] == 0:
                s2[0] = self.dis(x2*64+200, y2*65, role.x, role.y)

            if s3[0] == 0:
                s3[0] = self.dis(x3*64+200, y3*65, role.x, role.y)

            if s4[0] == 0:
                s4[0] = self.dis(x4*64+200, y4*65, role.x, role.y)


            id1 = self.min(s1[0], s2[0])
            id2 = self.min(s3[0], s4[0])

            if id1 == 1 and id2 == 1:       #哪个地方可以减小距离，就走向哪
                id = self.min(s1[0], s3[0])
                if id == 1:
                    self.next_px = x1
                    self.next_py = y1
                    if s1[1] == 4:  #如果要前进的方向，有可消除障碍，就喷火消除
                        fire1 = fire(self.px, self.py, 3)
                        fire1.draw(screen_surf)
                        self.b_remove(self.px-1, self.py+1)
                        self.map[self.py+1][self.px-1] = 1  #修改坐标值
                    if self.next_py == role.py and self.next_px == role.px:
                        fire1 = fire(self.px, self.py, 3)
                        fire1.draw(screen_surf)
                        role.blood -= 1
                    if self.is_walking == False:
                        self.dir = RoleWalk.DIR_LEFT
                else:
                    self.next_px = x3
                    self.next_py = y3
                    if s3[1] == 4:
                        fire1 = fire(self.px, self.py, 1)
                        fire1.draw(screen_surf)
                        self.b_remove(self.px, self.py)
                        self.map[self.py][self.px] = 1
                    if self.next_py == role.py and self.next_px == role.px:
                        fire1 = fire(self.px, self.py, 1)
                        fire1.draw(screen_surf)
                        role.blood -= 1
                    if self.is_walking == False:
                        self.dir = RoleWalk.DIR_UP
            elif id1 == 1 and id2 == 0:
                id = self.min(s1[0], s4[0])
                if id == 1:
                    self.next_px = x1
                    self.next_py = y1
                    if s1[1] == 4:
                        fire1 = fire(self.px, self.py, 3)
                        fire1.draw(screen_surf)
                        self.b_remove(self.px-1, self.py+1)
                        self.map[self.py+1][self.px-1] = 1
                    if self.next_py == role.py and self.next_px == role.px:
                        fire1 = fire(self.px, self.py, 3)
                        fire1.draw(screen_surf)
                        role.blood -= 1
                    if self.is_walking == False:
                        self.dir = RoleWalk.DIR_LEFT
                else:
                    self.next_px = x4
                    self.next_py = y4
                    if s4[1] == 4:
                        fire1 = fire(self.px, self.py, 2)
                        fire1.draw(screen_surf)
                        self.b_remove(self.px, self.py+2)
                        self.map[self.py+2][self.px] = 1
                    if self.next_py == role.py and self.next_px == role.px:
                        fire1 = fire(self.px, self.py, 2)
                        fire1.draw(screen_surf)
                        role.blood -= 1
                    if self.is_walking == False:
                        self.dir = RoleWalk.DIR_DOWN
            elif id1 == 0 and id2 == 1:
                id = self.min(s2[0], s3[0])
                if id == 1:
                    self.next_px = x2
                    self.next_py = y2
                    if s2[1] == 4:
                        fire1 = fire(self.px, self.py, 4)
                        fire1.draw(screen_surf)
                        self.b_remove(self.px+1, self.py+1)
                        self.map[self.py+1][self.px+1] = 1
                    if self.next_py == role.py and self.next_px == role.px:
                        fire1 = fire(self.px, self.py, 4)
                        fire1.draw(screen_surf)
                        role.blood -= 1
                    if self.is_walking == False:
                        self.dir = RoleWalk.DIR_RIGHT
                else:
                    self.next_px = x3
                    self.next_py = y3
                    if s3[1] == 4:
                        fire1 = fire(self.px, self.py, 1)
                        fire1.draw(screen_surf)
                        self.b_remove(self.px, self.py)
                        self.map[self.py][self.px] = 1
                    if self.next_py == role.py and self.next_px == role.px:
                        fire1 = fire(self.px, self.py, 1)
                        fire1.draw(screen_surf)
                        role.blood -= 1
                    if self.is_walking == False:
                        self.dir = RoleWalk.DIR_UP
            elif id1 == 0 and id2 == 0:
                id = self.min(s2[0], s4[0])
                if id == 1:
                    self.next_px = x2
                    self.next_py = y2
                    if s2[1] == 4:
                        fire1 = fire(self.px, self.py, 4)
                        fire1.draw(screen_surf)
                        self.b_remove(self.px+1, self.py+1)
                        self.map[self.py+1][self.px+1] = 1
                    if self.next_py == role.py and self.next_px == role.px:
                        fire1 = fire(self.px, self.py, 4)
                        fire1.draw(screen_surf)
                        role.blood -= 1
                    if self.is_walking == False:
                        self.dir = RoleWalk.DIR_RIGHT
                else:
                    self.next_px = x4
                    self.next_py = y4
                    if s4[1] == 4:
                        fire1 = fire(self.px, self.py, 2)
                        fire1.draw(screen_surf)
                        self.b_remove(self.px, self.py+2)
                        self.map[self.py+2][self.px] = 1
                    if self.next_py == role.py and self.next_px == role.px:
                        fire1 = fire(self.px, self.py, 2)
                        fire1.draw(screen_surf)
                        role.blood -= 1
                    if self.is_walking == False:
                        self.dir = RoleWalk.DIR_DOWN
            self.is_walking = True










    #后面是一开始在网上学的一个AStar算法，结果没有调好，又自己写了走路的函数
    # def find_path(self, end_point):
    #     """end_point就是要到达的终点"""
    #     start_point = (self.py, self.px)
    #     path = AStar(self.map, start_point, end_point).start()
    #     if path is None:
    #         return
    #     self.path = path
    #     self.path_index = 0
    #
    # def goto(self, x, y):
    #     self.next_px = x
    #     self.next_py = y
    #
    #     if self.next_px > self.px:
    #         self.dir = RoleWalk.DIR_RIGHT
    #     elif self.next_px < self.px:
    #         self.dir = RoleWalk.DIR_LEFT
    #
    #     if self.next_py > self.py:
    #         self.dir = RoleWalk.DIR_DOWN
    #     elif self.next_py < self.py:
    #         self.dir = RoleWalk.DIR_UP
    #
    # def logic(self):
    #
    #     self.move()
    #     #如果角色正在移动就不管
    #     if self.is_walking:
    #         return
    #     #如果寻路走到终点
    #     if self.path_index == len(self.path):
    #         self.path = []
    #         self.path_index = 0
    #     else:   #如果没走到终点，就向下一个格子走
    #         self.goto(self.path[self.path_index].x, self.path[self.path_index].y)
    #         self.path_index += 1
    #
    #
