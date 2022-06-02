import pygame

class fire:
    """npc人物攻击类"""
    def __init__(self, x, y, sign):
        self.img1 = pygame.image.load('images/hit/fire1.png').convert_alpha()
        self.img2 = pygame.image.load('images/hit/fire2.png').convert_alpha()
        self.img3 = pygame.image.load('images/hit/fire3.png').convert_alpha()
        self.img4 = pygame.image.load('images/hit/fire4.png').convert_alpha()
        self.x = x
        self.y = y
        self.sign = sign

    def draw(self, screen_surf):
        """绘制攻击效果"""
        if self.sign == 1:
            screen_surf.blit(self.img1, (self.x*64+200, self.y*65-50))
        elif self.sign == 2:
            screen_surf.blit(self.img2, (self.x*64+200, self.y*65 + 50))
        elif self.sign == 3:
            screen_surf.blit(self.img3, (self.x*64+200-60, self.y*65))
        elif self.sign == 4:
            screen_surf.blit(self.img4, (self.x*64+200+50, self.y*65))
