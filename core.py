import random

import pygame.image



class Array2D:
    """
    二维数组具体用来给地图划分建立地图表
    说明：
        1.构造方法需要两个参数，即二维数组的宽和高
        2.成员变量w和h时二维数组的宽和高
        3.数组值时记录该位置是否可以行走，默认为0
    """
    def __init__(self, w, h, default=0):
        """初始化二维数组"""
        self.w = w
        self.h = h
        self.data = [[default for y in range(self.h)] for x in range(self.w)]  #将二维数组的值置0

    def show_array2D(self):
        """显示制定的二维数组的具体情况"""
        for x in range(self.w):
            for y in range(self.h):
                print(self.data[x][y], end=' ')
            print("")

    def __getitem__(self, item):
        """可以让定义的Array2D的对象直接像二维数组一样使用"""
        return self.data[item]


class GameBarrier:
    """可消除障碍类"""
    def __init__(self, barrier, x, y, sign):
        self.barrier = barrier
        self.x = x
        self.y = y
        self.sign = sign   #表示这个障碍物消除后不会产生补给包
        self.img1 = pygame.image.load('images/blood.png').convert_alpha()


    def draw_barrier(self, screen_surf):
        """绘制障碍"""
        if self.y == 1: #因为图片素材稍微有一点问题，这样调了之后可以让可消除障碍刚还在格子上
            screen_surf.blit(self.barrier, (self.x * 64+200, self.y * 26))  #整个地图素材的上面一点是被作为第0行舍弃了
        else:
            y = (self.y-1) * 65 + 26    #后面的坐标在加载时，要保持第0行的变化
            screen_surf.blit(self.barrier, (self.x * 64+200, y))

    def after_bomb(self, screen_surf):
        """表示这个障碍物消除后会产生补给包，显示补给包的图片"""
        if self.sign == 1:
            screen_surf.blit(self.img1, (self.x * 64 + 200, self.y * 65))

    # def Get_x(self):
    #     return self.x * 64 + 200
    # def Get_y(self):
    #     if self.y == 1:
    #         return self.y * 26
    #     else:
    #         return (self.y-1)*65+26


class GameMap(Array2D):
    """游戏地图类"""
    def __init__(self, font, bottom, top, barrier_img1, barrier_img2, role_img1, role_img2, role_img3, role_img4, role_img5, x, y):
        """将地图划分成w*h个小格子，每个格子的像素为64*65，第0行并不是标准的格子
        像素根据图片素材而定
        最终形成的地图是14*15的
        """
        h = int(bottom.get_width() / 64)    #记录有多少列
        w = int(top.get_height() / 65) + 1  #记录有多少行
        super().__init__(w, h)  #调用父类的构造函数
        self.bottom = bottom
        self.top = top
        self.x = x
        self.y = y
        #有2种障碍图片
        self.barrier_img1 = barrier_img1
        self.barrier_img2 = barrier_img2
        #侧面人物信息的加载
        self.role_img1 = role_img1
        self.role_img2 = role_img2
        self.role_img3 = role_img3
        self.role_img4 = role_img4
        self.role_img5 = role_img5
        self.font = font
        self.barriers = []
        self.barrier_num = 0
        self.blood_package = [[]]   #里面嵌套的列表表示坐标


    """地图及障碍物的相关函数"""

    def draw_bottom(self, screen_surf):
        """绘制底部的图"""
        screen_surf.blit(self.bottom, (self.x, self.y))

    def draw_top(self, screen_surf):
        """绘制障碍的图，可以实现遮挡的效果"""
        screen_surf.blit(self.top, (158, -13))  #根据调试让图片恰好覆盖

    """界面二的信息绘制"""
    def draw_role(self, screen_surf, chance, img1, img2, img3, img4, img5):
        """游戏界面侧面的人物图,根据人物选择，确定最终参与游戏的是哪些人物，根据之前的选择，来安排界面绘制，分情况表示"""
        if chance == 1:
            screen_surf.blit(self.role_img1, (0, 10))
            screen_surf.blit(self.role_img2, (0, 183))
            screen_surf.blit(self.role_img3, (0, 352))
            screen_surf.blit(self.role_img4, (0, 497))
            screen_surf.blit(img5, (0, 630))
        elif chance == 2:
            screen_surf.blit(img1, (0, 10))
            screen_surf.blit(self.role_img2, (0, 183))
            screen_surf.blit(self.role_img3, (0, 352))
            screen_surf.blit(self.role_img4, (0, 497))
            screen_surf.blit(self.role_img5, (0, 630))
        elif chance == 3:
            screen_surf.blit(self.role_img1, (0, 10))
            screen_surf.blit(img2, (0, 183))
            screen_surf.blit(self.role_img3, (0, 352))
            screen_surf.blit(self.role_img4, (0, 497))
            screen_surf.blit(self.role_img5, (0, 630))
        elif chance == 4:
            screen_surf.blit(self.role_img1, (0, 10))
            screen_surf.blit(self.role_img2, (0, 183))
            screen_surf.blit(img3, (0, 352))
            screen_surf.blit(self.role_img4, (0, 497))
            screen_surf.blit(self.role_img5, (0, 630))
        elif chance == 5:
            screen_surf.blit(self.role_img1, (0, 10))
            screen_surf.blit(self.role_img2, (0, 183))
            screen_surf.blit(self.role_img3, (0, 352))
            screen_surf.blit(img4, (0, 497))
            screen_surf.blit(self.role_img5, (0, 630))

    def load(self, screen_surf, role):
        """绘制侧面的信息图"""
        role.draw_blood(screen_surf)
        role.draw_star(screen_surf)
        role.draw_speed(screen_surf)

    def show(self, screen_surf, chance, r1, r2, r3, r4, r5, img1, img2, img3, img4, img5):
        """绘制侧面人物的信息，包括血量，速度，炸弹能量
        绘制玩家和npc形象
        """
        if r1.blood == 0:
            self.role_img1 = img1
        if r2.blood == 0:
            self.role_img2 = img2
        if r3.blood == 0:
            self.role_img3 = img3
        if r4.blood == 0:
            self.role_img4 = img4
        if r5.blood == 0:
            self.role_img5 = img5

        #侧面人物信息的提示子字
        text1 = self.font.render('玩家', True, (100, 120, 200))
        text2 = self.font.render('npc1', True, (100, 120, 200))
        text3 = self.font.render('npc2', True, (100, 120, 200))
        text4 = self.font.render('npc3', True, (100, 120, 200))
        text5 = self.font.render('未选择', True, (100, 120, 200))

        if chance == 1:
            #根据人物血量判断胜利与否
            if r1.blood <= 0:
                return 3
            elif r2.blood <= 0 and r3.blood <= 0 and r4.blood <= 0:
                return 4
            else:
                if r1.is_hurt == True:  #这个是玩家人物在被炸后，返回初始位置
                    r1.draw(screen_surf, 200, 0, 0, 0)
                else:
                    r1.draw(screen_surf, r1.x, r1.y, 0, 0)  # 玩家人物图片的绘制
                if r2.blood > 0:
                    r2.draw(screen_surf, r2.x, r2.y, 1, r1.bomb)    #最后一个参数需要注意，因为炸弹是玩家人物生成的，npc玩家并没有
                if r3.blood > 0:
                    r3.draw(screen_surf, r3.x, r3.y, 2, r1.bomb)
                if r4.blood > 0:
                    r4.draw(screen_surf, r4.x, r4.y, 3, r1.bomb)

                #下面是人物行走
                r2.find_path(r1, 1, screen_surf)
                r2.move()
                r3.find_path(r1, 2, screen_surf)
                r3.move()
                r4.find_path(r1, 3, screen_surf)
                r4.move()
                r1.role_move(screen_surf)  # 玩家人物的移动

                #绘制侧面的信息
                self.load(screen_surf, r1)
                self.load(screen_surf, r2)
                self.load(screen_surf, r3)
                self.load(screen_surf, r4)
                screen_surf.blit(text1, (0, 15))
                screen_surf.blit(text2, (0, 185))
                screen_surf.blit(text3, (0, 367))
                screen_surf.blit(text4, (0, 502))
                screen_surf.blit(text5, (0, 636))
                return 2

        elif chance == 2:
            if r2.blood <= 0:
                return 3
            elif r3.blood <= 0 and r4.blood <= 0 and r5.blood <= 0:
                return 4
            else:
                if r2.is_hurt == True:
                    r2.draw(screen_surf, 200, 0, 0, 0)
                else:
                    r2.draw(screen_surf, r2.x, r2.y, 0, 0)  # 玩家人物图片的绘制
                if r3.blood > 0:
                    r3.draw(screen_surf, r3.x, r3.y, 1, r2.bomb)
                if r4.blood > 0:
                    r4.draw(screen_surf, r4.x, r4.y, 2, r2.bomb)
                if r5.blood > 0:
                    r5.draw(screen_surf, r5.x, r5.y, 3, r2.bomb)

                r3.find_path(r2, 1, screen_surf)
                r3.move()
                r4.find_path(r2, 2, screen_surf)
                r4.move()
                r5.find_path(r2, 3, screen_surf)
                r5.move()
                r2.role_move(screen_surf)  # 玩家人物的移动

                self.load(screen_surf, r2)
                self.load(screen_surf, r3)
                self.load(screen_surf, r4)
                self.load(screen_surf, r5)
                screen_surf.blit(text5, (0, 15))
                screen_surf.blit(text1, (0, 185))
                screen_surf.blit(text2, (0, 367))
                screen_surf.blit(text3, (0, 502))
                screen_surf.blit(text4, (0, 636))
                return 2

        elif chance == 3:
            if r3.blood <= 0:
                return 3
            elif r4.blood <= 0 and r5.blood <= 0 and r1.blood <= 0:
                return 4

            else:
                if r3.is_hurt == True:
                    r3.draw(screen_surf, 200, 0, 0, 0)
                else:
                    r3.draw(screen_surf, r3.x, r3.y, 0, 0)  # 玩家人物图片的绘制
                if r4.blood > 0:
                    r4.draw(screen_surf, r4.x, r4.y, 1, r3.bomb)
                if r5.blood > 0:
                    r5.draw(screen_surf, r5.x, r5.y, 2, r3.bomb)
                if r1.blood > 0:
                    r1.draw(screen_surf, r1.x, r1.y, 3, r3.bomb)
                r4.find_path(r3, 1, screen_surf)
                r4.move()
                r5.find_path(r3, 2, screen_surf)
                r5.move()
                r1.find_path(r3, 3, screen_surf)
                r1.move()
                r3.role_move(screen_surf)  # 玩家人物的移动

                self.load(screen_surf, r3)
                self.load(screen_surf, r4)
                self.load(screen_surf, r5)
                self.load(screen_surf, r1)
                screen_surf.blit(text4, (0, 15))
                screen_surf.blit(text5, (0, 185))
                screen_surf.blit(text1, (0, 367))
                screen_surf.blit(text2, (0, 502))
                screen_surf.blit(text3, (0, 636))
                return 2

        elif chance == 4:
            if r4.blood <= 0:
                return 3
            elif r5.blood <= 0 and r1.blood <= 0 and r2.blood <= 0:
                return 4

            else:
                if r4.is_hurt == True:
                    r4.draw(screen_surf, 200, 0, 0, 0)
                else:
                    r4.draw(screen_surf, r4.x, r4.y, 0, 0)  # 玩家人物图片的绘制
                if r5.blood > 0:
                    r5.draw(screen_surf, r5.x, r5.y, 1, r4.bomb)
                if r1.blood > 0:
                    r1.draw(screen_surf, r1.x, r1.y, 2, r4.bomb)
                if r2.blood > 0:
                    r2.draw(screen_surf, r2.x, r2.y, 3, r4.bomb)
                r5.find_path(r4, 1, screen_surf)
                r5.move()
                r1.find_path(r4, 2, screen_surf)
                r1.move()
                r2.find_path(r4, 3, screen_surf)
                r2.move()
                r4.role_move(screen_surf)  # 玩家人物的移动
                self.load(screen_surf, r4)
                self.load(screen_surf, r5)
                self.load(screen_surf, r1)
                self.load(screen_surf, r2)
                screen_surf.blit(text3, (0, 15))
                screen_surf.blit(text4, (0, 185))
                screen_surf.blit(text5, (0, 367))
                screen_surf.blit(text1, (0, 502))
                screen_surf.blit(text2, (0, 636))
                return 2

        elif chance == 5:
            if r5.blood <= 0:
                return 3
            elif r1.blood <= 0 and r2.blood <= 0 and r3.blood <= 0:
                return 4
            else:
                if r5.is_hurt == True:
                    r5.draw(screen_surf, 200, 0, 0, 0)
                else:
                    r5.draw(screen_surf, r5.x, r5.y, 0, 0)  # 玩家人物图片的绘制
                if r1.blood > 0:
                    r1.draw(screen_surf, r1.x, r1.y, 1, r5.bomb)
                if r2.blood > 0:
                    r2.draw(screen_surf, r2.x, r2.y, 2, r5.bomb)
                if r3.blood > 0:
                    r3.draw(screen_surf, r3.x, r3.y, 3, r5.bomb)
                r1.find_path(r5, 1, screen_surf)
                r1.move()
                r2.find_path(r5, 2, screen_surf)
                r2.move()
                r3.find_path(r5, 3, screen_surf)
                r3.move()
                r5.role_move(screen_surf)  # 玩家人物的移动
                self.load(screen_surf, r5)
                self.load(screen_surf, r1)
                self.load(screen_surf, r2)
                self.load(screen_surf, r3)
                screen_surf.blit(text2, (0, 15))
                screen_surf.blit(text3, (0, 185))
                screen_surf.blit(text4, (0, 367))
                screen_surf.blit(text5, (0, 502))
                screen_surf.blit(text1, (0, 636))
                return 2


    def load_walk_file(self, path):
        """读取可行走区域的文件
        方便加载障碍物及之后人物的行走
        文件中的0表示该处有不可消的障碍
        1表示该处为空地
        2表示该处为传送1
        3为传送2
        4表示该处为可消的障碍
        5表示初始人物位置
        """
        with open(path, 'r', encoding='UTF-8') as file: #有一个初始化的地图文件，确定哪些是不可消除的障碍
            text = file.read()
        v = text.split('\n')
        i = 0
        for x in range(self.w):
            for y in range(self.h):
                self[x][y] = int(v[i])  #将文件中的数据加载到定义的一个二维数组中
                i += 1
        self.show_array2D()


#下面都是关于可消除障碍的代码
    def get_barriers(self):
        """生成可消除的障碍"""
        x = 1
        y = 1
        while self.barrier_num <= 80:   #总共产生80个课消除的障碍
            # 产生随机坐标
            x = random.randint(0, 14)       #这里的x相当是记录列
            y = random.randint(1, 13)   #这里的y相当记录行
            if self[y][x] == 1:
                #当地图的该位置可以放置障碍时，会分别放置2种障碍物各20个
                if self.barrier_num <= 40:  #第一种障碍物
                    if x % 4 != 0 and len(self.blood_package) <= 10:    #设置特殊障碍物
                        game_barrier = GameBarrier(self.barrier_img1, x, y, 1)
                        self.blood_package.append([x, y])   #添加到包列表中
                    else:
                        game_barrier = GameBarrier(self.barrier_img1, x, y, 0)
                    # self[y][x] = 0
                else:   #第二种障碍物
                    if x % 4 != 0 and len(self.blood_package) <= 20:
                        game_barrier = GameBarrier(self.barrier_img2, x, y, 1)
                        self.blood_package.append([x, y])
                    else:
                        game_barrier = GameBarrier(self.barrier_img2, x, y, 0)
                    # self[y][x] = 4  # 改变地图位置的可行标记

                self.barriers.append(game_barrier)
                self.barrier_num += 1
                self[y][x] = 4  # 改变地图位置的可行标记
        return self.barriers


    def draw_barriers(self, screen_surf):
        """绘制初始的障碍物"""
        for one in self.barriers:
           one.draw_barrier(screen_surf)
