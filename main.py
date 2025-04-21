from pygame import *
from random import randint
from time import time as timer
win_x = 700
win_y = 500
window = display.set_mode((win_x,win_y))
background = transform.scale(image.load('galaxy.jpg'),(win_x,win_y))
clock = time.Clock()
game = True
display.set_caption('пиу пиу тыщ тыщ')

#мьюзик
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
piy_pay = mixer.Sound('fire.ogg')


#Персонажи
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,weight,height,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (weight,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))
        

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 636:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx-7,self.rect.top,15,20,15)
        bullets.add(bullet)
propusheno = 0
score = 0

class Monster(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 450:
            self.rect.y = 0
            self.rect.x = randint(0,620)
            self.speed = randint(2,7)
            global propusheno 
            propusheno +=1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 450:
            self.rect.y = 0
            self.rect.x = randint(0,620)
            self.speed = randint(2,7)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

num_fire = 0
rel_time = False

bullets = sprite.Group()

igrok = Player('rocket.png',5,390,70,100, 20)
monsters = sprite.Group()
for i in range(5):
    monsters.add(Monster('ufo.png',randint(0,620),0,80,50,randint(2,7)))
asteroids = sprite.Group()
for i in range(3):
    asteroids.add(Asteroid('asteroid.png',randint(0,620),0,80,50,randint(2,7)))
    


finish = False
font.init()
font1 = font.SysFont('verdana',20)
font2 = font.SysFont('verdana',50)
win = font2.render('You WIN!',True,(0,255,0))
lose = font2.render('You LOSER!!!!',True,(255,0,0))
healts = 3
colors = [(255,0,0),(255,255,0),(0,255,0)]
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1 and num_fire < 5 and not rel_time:
                igrok.fire()
                piy_pay.play()
                num_fire += 1
            if num_fire >= 5 and rel_time == False:
                rel_time = True
                last_time = timer()
            


    window.blit(background,(0,0))  
    if not finish:
        text_lose = font1.render('Пропущено: ' + str(propusheno),1,(255,255,255))
        text_win = font1.render('Счет: ' + str(score),1,(255,255,255))
        healt = font2.render(str(healts),1,colors[healts-1])
        window.blit(text_win, (5,10))
        window.blit(text_lose, (5,40))
        window.blit(healt, (630,0))
        igrok.reset()
        igrok.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        if rel_time:
            new_time = timer()
            if new_time - last_time < 3:
                reload = font1.render('Wait, RELOAD???', True,(255,0,0))
                window.blit(reload,(200,460))
            else:
                num_fire = 0
                rel_time = False
        if sprite.spritecollide(igrok, monsters, True) or propusheno >= 3:
            monsters.add(Monster('ufo.png',randint(0,620),0,80,50,randint(2,7)))
            healts -= 1
        if sprite.spritecollide(igrok, asteroids, True):
            asteroids.add(Asteroid('asteroid.png',randint(0,620),0,80,50,randint(2,7)))
            healts -= 1
        if sprite.groupcollide(bullets, monsters, True,True):
            monsters.add(Monster('ufo.png',randint(0,620),0,80,50,randint(2,7)))
            score += 1
        if score >= 10:
            window.blit(win, (200,220))
            finish = True
        if healts < 1:
            window.blit(lose, (200,220))
            finish = True
        display.update()
    time.delay(70)