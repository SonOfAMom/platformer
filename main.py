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
clock = time.Clock()
FPS = 60

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
        self.speedX = 0
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def gravity(self):
        if self.rect.y <= 360:
            self.speedY -= 0.4
        else:
            self.speedY = 0

    def update(self):
        self.rect.y -= self.speedY
        self.rect.x += self.speedX
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 650:
            if self.speedX < 5:
                self.speedX += 1

            if self.turn == 'left':
                self.image = transform.scale(image.load('right_side.png'), (70,80)) 
                self.turn = 'right'
        elif keys_pressed[K_a] and self.rect.x > 5:
            if self.speedX > -5:
                self.speedX -= 1
            if self.turn == 'right':
                self.image = transform.scale(image.load('left_side.png'), (70,80)) 
                self.turn = 'left'
        else:
            if self.speedX > 0:
                self.speedX = 0
            elif self.speedX < 0:
                self.speedX = 0
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


class Enemy(GameSprite):
    def update(self):
        if self.direction == 'left':
            self.rect.x -= 4
        if self.direction != 'left':
            self.rect.x += 4
        if self.rect.x <= 400:
            self.direction = 'right'
        if self.rect.x >= 600:
            self.direction = 'left'
    def update2(self):
        if self.direction == 'up':
            self.rect.y -= 4
        if self.direction != 'up':
            self.rect.y += 4
        if self.rect.y >= 435:
            self.direction = 'up'
        if self.rect.y <= 5:
            self.direction = 'down'
    
class Wall(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height):
        super().__init__(player_image, player_x*50, player_y*35, 0, width, height)


spr1 = Player('right_side.png', 0, 100, 5, 70, 80)
button_1 = Button(380,250,180,50,(250, 0, 0),(0, 250, 0, 0),'Уровень 2')
button_2 = Button(180,100,350,50,(250, 0 , 0),(0, 250, 0, 0),'Выберите уровень')
button_3 = Button(130,250,180,50,(250, 0 , 0),(0, 250, 0, 0),'Уровень 1')
button_4 = Button(250,350,180,50,(250, 0 , 0),(0, 250, 0, 0),'Уровень 3')
enemy_one = Enemy(('rocket.png'),200,200,1,35,45)
enemy_one.direction = 'left'

game = True
start = False

walls = sprite.Group()

def load_level(level):
    with open(f'Setka{level}.txt', 'r') as file:
        data = file.readlines()
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == '1':
                    walls.add(Wall(('steni 2.jpg'), j, i, 50, 35))


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    '''меню'''
    if start == False:
        button_1.reset()
        button_2.reset()
        button_3.reset()
        button_4.reset()

        if e.type == MOUSEBUTTONDOWN:
                x,y = e.pos

                if button_1.collidepoint(x,y):
                    load_level(2)
                    spr1.rect.y = 350
                    spr1.rect.x = 0
                    start = True
                    

                if button_3.collidepoint(x,y):
                    load_level(1)
                    spr1.rect.y = 350
                    spr1.rect.x = 0
                    start = True

                if button_4.collidepoint(x,y):
                    load_level(3)
                    spr1.rect.y = 350
                    spr1.rect.x = 0
                    start = True
    '''игра'''
    if start:
        window.blit(backgr,(0,0))
        spr1.reset()
        spr1.update()
        spr1.gravity()
        enemy_one.reset()
        enemy_one.update()
        if sprite.collide_rect(spr1,enemy_one):
            start = False
        if sprite.spritecollide(spr1, walls, False):
            wall = sprite.spritecollide(spr1, walls, False)
            if spr1.speedX > 0:
                spr1.rect.right = wall[0].rect.left
            elif spr1.speedY > 0:
                spr1.rect.bottom = wall[0].rect.top
        

        walls.draw(window)


    clock.tick(FPS)
    display.update()









