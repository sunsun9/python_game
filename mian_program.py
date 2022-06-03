import os.path
import sys
import pygame
from pgzero.loaders import sounds

from core import GameMap
from Role import Sprite, RoleWalk
from core import GameBarrier
from game_ready import role_chance


class background:
    """游戏背景类"""
    def __init__(self, title, width, height, fps=60):
        """初始化游戏的设置"""
        self.title = title
        self.screen_width = width
        self.screen_height = height
        self.screen_surf = None
        self.page = 1   #游戏界面的一个标志，表示当前是那个界面
        self.change = False #变化页面的一个标志，通过该标志改变page的值
        self.m = 0
        self.fps = fps  #游戏每秒刷新次数
        self.__init_pygame()
        self.__init_game()
        self.update()


    def __init_pygame(self):
        """初始化游戏窗口"""
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(self.title)  #设置当前窗口的标题栏
        self.screen_surf = pygame.display.set_mode((self.screen_width,self.screen_height))  #设置窗口大小
        self.clock = pygame.time.Clock()    #可以控制游戏循环频率，以一个固定的速度运行

    def __init_game(self):
        """加载游戏基本页面"""
        self.music1 = pygame.mixer.Sound('sounds/music_loginBg.wav')
        self.music2 = pygame.mixer.Sound('sounds/music_win.wav')
        self.music3 = pygame.mixer.Sound('sounds/music_lose.wav')
        self.role_background = role_chance()
        #加载选择人物的图片
        self.hero1 = pygame.image.load('images/role/role1.png').convert_alpha() #对图片进行解析，cinvert_alpha对包含透明的图片解析
        self.hero2 = pygame.image.load('images/role/role2.png').convert_alpha()
        self.hero3 = pygame.image.load('images/role/role3.png').convert_alpha()
        self.hero4 = pygame.image.load('images/role/role4.png').convert_alpha()
        self.hero5 = pygame.image.load('images/role/role5.png').convert_alpha()
        #加载游戏地图相关图片素材
        self.map_bottom = pygame.image.load("images/background1.png").convert_alpha()
        self.map_top = pygame.image.load('images/back_top.png').convert_alpha()
        self.barrier1 = pygame.image.load('images/grass1.png').convert_alpha()
        self.barrier2 = pygame.image.load('images/grass2.png').convert_alpha()
        #加载游戏界面侧边的人物信息显示图片
        self.role_img1 = pygame.image.load('images/role1.png').convert_alpha()
        self.role_img2 = pygame.image.load('images/role2.png').convert_alpha()
        self.role_img3 = pygame.image.load('images/role3.png').convert_alpha()
        self.role_img4 = pygame.image.load('images/role4.png').convert_alpha()
        self.role_img5 = pygame.image.load('images/role5.png').convert_alpha()
        #游戏人物死亡或者没有选择，显示灰色图片
        self.role_img1_1 = pygame.image.load('images/role1_1.png').convert_alpha()
        self.role_img2_1 = pygame.image.load('images/role2_1.png').convert_alpha()
        self.role_img3_1 = pygame.image.load('images/role3_1.png').convert_alpha()
        self.role_img4_1 = pygame.image.load('images/role4_1.png').convert_alpha()
        self.role_img5_1 = pygame.image.load('images/role5_1.png').convert_alpha()
        #加载文字
        self.font = pygame.font.Font('fonts/FZQianLXSJW.TTF', 25)
        self.game_map = GameMap(self.font, self.map_bottom, self.map_top, self.barrier1, self.barrier2, self.role_img1, self.role_img2, self.role_img3, self.role_img4, self.role_img5,  200, 0) #建立地图
        self.game_map.load_walk_file('map.map')
        barriers = self.game_map.get_barriers()
        #创建人物，用于人物游戏行走
        self.role1 = RoleWalk(self.hero1, RoleWalk.DIR_DOWN, self.game_map, self.font, 1, barriers)
        self.role2 = RoleWalk(self.hero2, RoleWalk.DIR_DOWN, self.game_map, self.font, 2, barriers)
        self.role3 = RoleWalk(self.hero3, RoleWalk.DIR_DOWN, self.game_map, self.font, 3, barriers)
        self.role4 = RoleWalk(self.hero4, RoleWalk.DIR_DOWN, self.game_map, self.font, 4, barriers)
        self.role5 = RoleWalk(self.hero5, RoleWalk.DIR_DOWN, self.game_map, self.font, 5, barriers)


    def update(self):
        while True:
            self.clock.tick(self.fps)   #设置游戏的最大帧率
            self.event_handler()    #监视键盘和鼠标事件
            #绘制人物图像上的每一帧的小人
            self.screen_surf.fill('white')

            if self.page == 1:  #第一个界面：人物选择
                #游戏人物选择界面
                self.music1.play()
                self.role_background.draw_role(self.screen_surf)
                self.change = self.role_background.chance() #选择好了，改变标志位
                self.role_background.draw_sign(self.screen_surf)    #绘制特殊形状，表示即将选择的人物形象
                #选好之后跳转到游戏界面
                if self.change != False:
                    self.page = 2

            else:#主要的游戏界面了
                # 地图绘制
                self.game_map.draw_bottom(self.screen_surf)
                self.game_map.draw_barriers(self.screen_surf)   #可消除障碍的绘制

                #绘制侧面人物的图片以及角色分配
                self.game_map.draw_role(self.screen_surf, self.change, self.role_img1_1, self.role_img2_1, self.role_img3_1, self.role_img4_1, self.role_img5_1)
                if self.page == 2:
                    self.music1.play()
                    self.page = self.game_map.show(self.screen_surf, self.change, self.role1, self.role2, self.role3, self.role4, self.role5, self.role_img1_1, self.role_img2_1, self.role_img3_1, self.role_img4_1, self.role_img5_1)
                    self.game_map.draw_top(self.screen_surf)
                elif self.page == 3:
                    self.music1.stop()
                    if self.m == 0:
                        self.music3.play()
                        self.m = 1
                    img = pygame.image.load('images/back3.png').convert_alpha()
                    self.screen_surf.blit(img, (500, 400))
                elif self.page == 4:
                    self.music1.stop()
                    if self.m == 0:
                        self.music2.play()
                        self.m = 1
                    img = pygame.image.load('images/back2.png').convert_alpha()
                    self.screen_surf.blit(img, (500, 400))

            pygame.display.update()

    def event_handler(self):
        """监视键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == '__main__':
    background("Q版泡泡堂", 1200, 882)