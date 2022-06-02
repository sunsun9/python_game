import pygame

class role_chance:
    """游戏开始，选择人物形象
    最开始的游戏界面
    """
    def __init__(self):
        self.img = pygame.image.load('images/background.png').convert_alpha()   #开始界面的背景图
        self.font1 = pygame.font.Font('fonts/FZQianLXSJW.TTF', 50)  #字体1
        self.font2 = pygame.font.Font('fonts/FZFWTongQPOPTJW.TTF', 120) #字体2
        self.sign1 = pygame.image.load('images/chance1.png').convert_alpha()    #选择标记的图片
        self.sign2 = pygame.image.load('images/chance2.png').convert_alpha()
        self.number = 1 #标记玩家选择的哪个人物

    def draw_role(self, screen_surf):
        """绘制界面一人物选择的信息"""
        screen_surf.blit(self.img, (0, 0))
        text = self.font2.render('Q 版 泡 泡 堂', True, (200, 200, 200))
        npc1 = self.font1.render('玩家1', True, (200, 150, 100))
        npc2 = self.font1.render('玩家2', True, (200, 150, 100))
        npc3 = self.font1.render('玩家3', True, (200, 150, 100))
        npc4 = self.font1.render('玩家4', True, (200, 150, 100))
        npc5 = self.font1.render('玩家5', True, (200, 150, 100))
        screen_surf.blit(text, (200, 120))
        screen_surf.blit(npc1, (40, 400))
        screen_surf.blit(npc2, (300, 400))
        screen_surf.blit(npc3, (540, 400))
        screen_surf.blit(npc4, (775, 400))
        screen_surf.blit(npc5, (990, 400))


    def draw_sign(self, screen_surf):
        """通过标记的移动来确定玩家选择了哪个人物，特殊的形状框"""
        if self.number == 1:
            screen_surf.blit(self.sign1, (20, 380))
            screen_surf.blit(self.sign2, (135, 425))
        elif self.number == 2:
            screen_surf.blit(self.sign1, (275, 380))
            screen_surf.blit(self.sign2, (405, 425))
        elif self.number == 3:
            screen_surf.blit(self.sign1, (515, 380))
            screen_surf.blit(self.sign2, (645, 425))
        elif self.number == 4:
            screen_surf.blit(self.sign1, (755, 380))
            screen_surf.blit(self.sign2, (885, 425))
        elif self.number == 5:
            screen_surf.blit(self.sign1, (970, 380))
            screen_surf.blit(self.sign2, (1090, 425))

    def chance(self):
        """
        通过a键向左选择人物，通过d键向右选择人物
        通过按空格键确定选择人物
        """
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            if self.number == 0:    #到最坐标仍然按了向左的键，会转移到最右边的人物
                self.number = 5
            else:
                self.number -= 1
            return False
        elif keys_pressed[pygame.K_d]:
            if self.number == 5:
                self.number = 0
            else:
                self.number += 1
            return False

        elif keys_pressed[pygame.K_SPACE]:  #空格键选择人物，也告诉主程序选择的是哪个人物
            return self.number
        else:   #当没有按键的时候，返回False，保持该界面
            return False

#这个界面的建成，主要需要注意的就是chance函数需要告诉主程序选择的人物，同时在没有按键的时候，该函数要返回False，不然无法维护界面1