#Створи власний Шутер!

from pygame import *
from time import time as timer 
from random import randint



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

#Метод постріл
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 5, 15, 20)
        bullets.add(bullet)
        
class Enemy(GameSprite):
   #Рух ворога
   def update(self):
       self.rect.y += self.speed
       global lost
       #пропадая, якщо дойде то краю екрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        #Рух кулі
        self.rect.y -= self.speed
        if self.rect.y < 0: 
            self.kill()
    def __init__(self, bullet_image, bullet_x, bullet_y, bullet_speed,
                bullet_size_x, bullet_size_y):
        super().__init__(bullet_image, bullet_x, bullet_y, bullet_speed)
        self.image = transform.scale(image.load(bullet_image), (bullet_size_x, bullet_size_y))
        


#Вікно
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))



monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), randint(1, 10), 1 )
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,6):
    aster = Enemy("asteroid.png", randint(80, win_width - 80), randint(1, 10), 1 )
    asteroids.add(aster)
    
#Музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#Змінні для контролю гри
lost = 0
score = 0
goal = 10
max_lost = 3
num_fire = 0
max_fire= 3
rel_time = False


font.init()

font1 = font.SysFont("Arail", 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.SysFont("Arial", 36)

bullets = sprite.Group()
ship = Player("rocket.png", 5, win_height - 100, 10)
finish = False
run = True
clock = time.Clock()
FPS = 60
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < max_fire and not rel_time:
                        ship.fire()
                        num_fire += 1
                elif num_fire >= max_fire and not rel_time:
                    rel_time = True
                    current_time = timer()


            if e.key == K_r:
                if finish:
                    restart = True
    
    if not finish:
        window.blit(background,(0, 0))

        restart = False
        if rel_time:
            new_current_time = timer()
            if new_current_time - current_time < 1:
                font3 = font.SysFont("Arial", 20)
                text_wait = font3.render("Зачекай! Іде перезарядка", 1, (150, 0, 0))
                window.blit(text_wait, (ship.rect.x, ship.rect.y))
            else:
                rel_time = False
                num_fire = 0
    
        ship.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
      

        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       
        text = font2.render("Збито: " + str(score), 1, (255, 255, 255))

        window.blit(text, (10, 20))
        window.blit(text_lose, (10, 50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:   
           score += 1
           monster = Enemy('ufo.png', randint(80, win_width - 80), randint(0, 10), 1)
           monsters.add(monster)

        collides_aster = sprite.groupcollide(asteroids, bullets, True, True)
        for c in collides_aster:   
            score += 1
            aster = Enemy('asteroid.png', randint(80, win_width - 80), randint(0,100), 1)
            asteroids.add(aster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))

        if sprite.spritecollide(ship,asteroids, False):
            if ship.speed >= 1:
                ship.speed -= 1
            elif ship.speed == 0:
                finish = True
                window.blit(lose, (200, 200))

        if score >= goal:
           finish = True
           window.blit(win, (200, 200))

    elif finish and restart:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
    
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, win_width - 80), randint(0, 10), 1)
            monsters.add(monster)

        for i in range(1,6):
            aster = Enemy("asteroid.png", randint(80, win_width - 80), randint(1, 10), 1)
            asteroids.add(aster)

    display.update()
    clock.tick(FPS)