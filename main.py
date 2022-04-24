from pygame import *
from time import time as timer
import random

window = display.set_mode((700,500))
display.set_caption("Platformer")
backgr = transform.scale(image.load('background.jpg'), (700,500))
window.blit(backgr,(0,0))
font.init()
back = (0, 0, 0)
window.fill(back)
font1 = font.SysFont('Corbel',35)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.turn = 'right'
        self.speedY = 0

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def gravity(self):
        if self.rect.y <= 360:
            self.speedY -= 0.2
        else:
            self.speedY = 0

    def update(self):
        self.rect.y -= self.speedY
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
            if self.turn == 'left':
                self.image = transform.scale(image.load('right_side.png'), (70,80)) 
                self.turn = 'right'
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
            if self.turn == 'right':
                self.image = transform.scale(image.load('left_side.png'), (70,80)) 
                self.turn = 'left'
        if keys_pressed[K_SPACE] and self.rect.y > 0 and self.speedY == 0:
            self.speedY = 8
            self.rect.y -= self.speedY


class Button():
    def __init__(self,x,y,width,height,color,fill_color,text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.label = font.SysFont('verdana', 35).render(text, True, color)
        self.image = Surface((width,height),SRCALPHA)
        # text1 = font1.render(text, True , (0,250,0))
        self.image.fill(fill_color)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

    def color(self,new_color):
        self.fill_color = new_color

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def reset(self):
        # draw.rect(window,self.image,self.rect)
        window.blit(self.label ,(self.x,self.y))
        window.blit(self.image , self.rect)


spr1 = Player('right_side.png', 0, 100, 3, 70, 80)
button_1 = Button(380,250,180,50,(250, 0, 0),(0, 250, 0, 0),'Уровень 2')
button_2 = Button(180,100,350,50,(250, 0 , 0),(0, 250, 0, 0),'Выберите уровень')
button_3 = Button(130,250,180,50,(250, 0 , 0),(0, 250, 0, 0),'Уровень 1')
button_4 = Button(250,350,180,50,(250, 0 , 0),(0, 250, 0, 0),'Уровень 3')

game = True
start = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if start == False:
        button_1.reset()
        button_2.reset()
        button_3.reset()
        button_4.reset()


        if e.type == MOUSEBUTTONDOWN:
                x,y = e.pos

                if button_1.collidepoint(x,y):
                    start = True

                if button_3.collidepoint(x,y):
                    start = True

                if button_4.collidepoint(x,y):
                    start = True

    if start:
        window.blit(backgr,(0,0))
        spr1.reset()
        spr1.update()
        spr1.gravity()
        
    display.update()








