import pygame

class Bomb:
    """炸弹类"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img1 = pygame.image.load('images/bomb1.png').convert_alpha()
        self.img2 = pygame.image.load('images/bomb2.png').convert_alpha()
        self.img3 = pygame.image.load('images/bomb3.png').convert_alpha()
        self.img4 = pygame.image.load('images/bomb4.png').convert_alpha()
        self.img5 = pygame.image.load('images/bomb5.png').convert_alpha()
        self.bz_central = pygame.image.load('images/hit/central.png').convert_alpha()
        self.bz_central_rect = self.bz_central.get_rect()
        self.bz_down = pygame.image.load('images/hit/down.png').convert_alpha()
        self.bz_down_rect = self.bz_down.get_rect()
        self.bz_up = pygame.image.load('images/hit/up.png').convert_alpha()
        self.bz_left = pygame.image.load('images/hit/left.png').convert_alpha()
        self.bz_right = pygame.image.load('images/hit/right.png').convert_alpha()
        self.is_draw = True
        self.bombing = False
        self.clock = pygame.time.get_ticks()    #时钟函数，获得炸弹放下的那刻的时间

    def draw(self, screen_surf, barriers, map): #绘制炸弹
        t = (pygame.time.get_ticks() - self.clock)/1000

        if t <= 1:
            screen_surf.blit(self.img5, (self.x*64+200, self.y*65))
        elif t <= 2 and t > 1:
            screen_surf.blit(self.img4, (self.x*64+200, self.y*65))
        elif t <= 3 and t > 2:
            screen_surf.blit(self.img3, (self.x*64+200, self.y*65))
        elif t <= 4 and t > 3:
            screen_surf.blit(self.img2, (self.x*64+200, self.y*65))
        elif t <= 5 and t > 4:
            screen_surf.blit(self.img1, (self.x*64+200, self.y*65))

        elif t > 5 and t <= 6:
            self.bombing = True
            screen_surf.blit(self.bz_central, (self.x * 64 + 180, self.y * 65 + 5))
            #根据不同的坐标显示不同的爆炸
            if self.y < 12:
                screen_surf.blit(self.bz_down, (self.x * 64 + 190, self.y * 65 + 90))
            if self.x > 0 or map[self.y+1][self.x-1] == 1 or map[self.y+1][self.x-1] == 3 or map[self.y+1][self.x-1] == 2:
                screen_surf.blit(self.bz_left, (self.x * 64 + 100, self.y * 65 + 10))
            if self.x < 14:
                screen_surf.blit(self.bz_right, (self.x * 64 + 250, self.y * 65 + 15))
            if self.y > 0 or map[self.y][self.x] == 1 or map[self.y][self.x] == 3 or map[self.y][self.x] == 2:
                screen_surf.blit(self.bz_up, (self.x * 64 + 195, self.y * 65 - 80))



            if len(barriers) > 0:   #判断炸弹有没有消除障碍
                music = pygame.mixer.Sound('sounds/music_explode.wav')
                music.play()
                if self.x < 14 and self.y < 12:
                    if map[self.y][self.x] == 4:
                        self.is_hava(barriers, self.x, self.y, screen_surf)
                        map[self.y][self.x] = 1
                    if map[self.y+2][self.x] == 4:
                        self.is_hava(barriers, self.x, self.y+2, screen_surf)
                        map[self.y+2][self.x] = 1
                    if map[self.y+1][self.x+1] == 4:
                        self.is_hava(barriers, self.x+1, self.y+1, screen_surf)
                        map[self.y+1][self.x+1] = 1
                    if map[self.y+1][self.x-1] == 4:
                        self.is_hava(barriers, self.x-1, self.y+1, screen_surf)
                        map[self.y+1][self.x-1] = 1
                elif self.x == 14:
                    if map[self.y][self.x] == 4:
                        self.is_hava(barriers, self.x, self.y, screen_surf)
                        map[self.y][self.x] = 1
                    if map[self.y+2][self.x] == 4:
                        self.is_hava(barriers, self.x, self.y+2, screen_surf)
                        map[self.y+2][self.x] = 1
                    if map[self.y+1][self.x-1] == 4:
                        self.is_hava(barriers, self.x-1, self.y+1, screen_surf)
                        map[self.y+1][self.x-1] = 1
                elif self.y == 12:
                    if map[self.y][self.x] == 4:
                        self.is_hava(barriers, self.x, self.y, screen_surf)
                        map[self.y][self.x] = 1
                    if map[self.y+1][self.x+1] == 4:
                        self.is_hava(barriers, self.x+1, self.y+1, screen_surf)
                        map[self.y+1][self.x+1] = 1
                    if map[self.y+1][self.x-1] == 4:
                        self.is_hava(barriers, self.x-1, self.y+1, screen_surf)
                        map[self.y+1][self.x-1] = 1

        elif t > 6:
            self.is_draw = False
        return self.is_draw


    def is_hava(self, barriers, x, y, screen_surf):
        """判断障碍在列表中的位置，同时对于特殊障碍做出改变"""
        for i in barriers:
            if i.x == x and i.y == y:
                if i.sign == 1:
                    i.barrier = pygame.image.load('images/blood.png').convert_alpha()
                elif i.sign == 0:
                    barriers.remove(i)
                break

