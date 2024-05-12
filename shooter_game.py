#Создай собственный Шутер!
from random import *
from pygame import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 625:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 470:
            self.rect.y += self.speed
 
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost = lost + 1
      
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()





# bullet = bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)

win_w = 700
win_h = 500
win = display.set_mode((win_w, win_h))
display.set_caption('Maze')
background = transform.scale(image.load('galaxy.jpg'), (win_w, win_h))



lost = 0
score = 0
max_lost = 3
goal = 10


player = Player('rocket.png', 130, 400, 50, 100, 10)
# enemy = Enemy('ufo.png', 600, 350, 2, 200, 10)
# asteroid = GameSprite('asteroid.png', 600, 450, 0)




game = True
finish = False
# clock = time.Clock()
FPS = 120

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()


# bullet.kill()


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
font1 = font.Font(None, 36)

win1 = font1.render('YOU WIN!', True, (50, 150, 50))
lose = font1.render('YOU LOSE!', True, (150, 0, 50))

font2 = font.SysFont('Arial', 36)

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if finish != True:
        win.blit(background,(0, 0))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, 620), -40, 70, 50, randint(1, 5))
            monsters.add(monster)



        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            win.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            win.blit(win1, (200, 200))

        player.update()   
        monster.update()   
        monsters.update()  
        bullets.update()

        player.reset()
        monster.reset()
        # asteroid.reset()

        monsters.draw(win)
        bullets.draw(win)

        text_lose = font2.render('Счет: ' + str(score), 1, (250, 250, 250))
        win.blit(text_lose, (10, 20))
        text_lose2 = font2.render('Пропущено: ' + str(lost), 1, (250, 250, 250))
        win.blit(text_lose2, (10, 50))


        display.update()

        # clock.tick(FPS)

    time.delay(30)