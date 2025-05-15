from pygame import *

#parameters
res_x = 700
res_y = 500


game = True
finish = False

actor_x = 100
actor_y = 100

#coordinates
plr_x = 0
plr_y = 0

cyborg_x = 0
cyborg_y = 0

#sets framerate
FPS = 60
clock = time.Clock()

#clasess
class GameSprite(sprite.Sprite):
    def __init__(self, plr_img, plr_x, plr_y, plr_speed):
        super().__init__()
        self.image = transform.scale(image.load(plr_img), (75, 75))
        self.speed = plr_speed
        self.rect = self.image.get_rect()
        self.rect.x = plr_x
        self.rect.y = plr_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 

class Player(GameSprite):    
    def update(self):    
        keys_pressed = key.get_pressed() 
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < (res_x-80):
            self.rect.x += self.speed
        if keys_pressed[K_DOWN] and self.rect.y < (res_y-80):
            self.rect.y += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5 : 
            self.rect.y -= self.speed
            
class Enemy(GameSprite):
    direction = "left"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= (res_x-80):
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy2(GameSprite):
    direction = "up"
    def update(self):
        if self.rect.y <= (res_y-80):
            self.direction = "down"
        if self.rect.y >= 5:
            self.direction = "up"
        if self.direction == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed  


class Wall(sprite.Sprite):
    def __init__(self, c1,c2,c3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((c1,c2,c3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
    



#win
window = display.set_mode((res_x, res_y))
display.set_caption("Labirinte")

mixer.init()
#assets

background = transform.scale(image.load("background.jpg"), (res_x, res_y))
'''
plr =     transform.scale(image.load("hero.png"), (actor_x, actor_y))
cyborg  =     transform.scale(image.load("cyborg.png"), (actor_x, actor_y))
treasure  =  transform.scale(image.load("treasure.png"), (actor_x, actor_y))
'''
hero = Player("hero.png", 0, 400, 4)
cyborg = Enemy("cyborg.png", 620, 250, 2)
cyborg2 = Enemy2("cyborg.png", 250, 100, 2)
treasure  = GameSprite("treasure.png", 620, 400, 0)

sfx_bg_music =  mixer.Sound("jungles.ogg")
sfx_kick =      mixer.Sound("kick.ogg")
sfx_money =     mixer.Sound("money.ogg")

font.init()
font = font.SysFont('arial', 40)
win =  font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

w1 = Wall(150, 205, 50, 100, 20, 450, 10)
w2 = Wall(150, 205, 50, 250, 450, 350, 10)
w3 = Wall(150, 205, 50, 100, 20, 10, 380)

#game init
#sfx_bg_music.play()

#cycle
while game:
    #game quitting obrabotka
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background, (0,0))

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()

        hero.update()
        cyborg.update() 
        cyborg2.update()

        hero.reset()
        cyborg.reset()
        cyborg2.reset()
        treasure.reset()
        
        if sprite.collide_rect(hero, cyborg) or sprite.collide_rect(hero, cyborg2) or sprite.collide_rect(hero, w1) or sprite.collide_rect(hero, w2) or sprite.collide_rect(hero, w3):
            finish = True
            window.blit(lose, (200,200))
            sfx_kick.play()
        
        if sprite.collide_rect(hero, treasure):
            finish = True
            window.blit(win, (200,200))
            sfx_money.play()

    #update
    display.update()
    clock.tick(FPS)
    