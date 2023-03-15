import pygame 
import random

pygame.init()
# size of window
screen_width = 400
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('jumping')
#frame-rate
clock = pygame.time.Clock()
fps = 60

scroller = 200
gravity = 1
max_platform = 10
scroll = 0
bg_scroll = 0
game_over = False
score = 0
font_small = pygame.font.SysFont('lucida Sans', 20)
font_large = pygame.font.SysFont('lucida Sans', 24)

#load imgs
character = pygame.image.load('img/palyer1.png')
bg = pygame.image.load('img/bj.png').convert_alpha()
platform_img = pygame.image.load('img/platform.png').convert_alpha()

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))



#infinite moving background
def draw_bg (bg_scroll):
    screen.blit(bg, (0,0 + bg_scroll))
    screen.blit(bg, (0,-600 + bg_scroll))
#player
class player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(character,(45, 45))
        self.width = 45
        self.height = 45
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)
        self.flip = False
        self.vel_y = 0        
    def move (self):
        scroll = 0
        dx = 0
        dy = 0
       #key settings
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 10
            self.flip = True
        if key[pygame.K_RIGHT]:
            dx += 10
            self.flip = False
        #gravity
        self.vel_y += gravity
        dy += self.vel_y
        #border left-right
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width-self.rect.right
        #collision
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy,self.width,self.height):
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20                
 #       if self.rect.bottom + dy > screen_height:
 #          dy = 0
 #           self.vel_y = -20
        #jumping
        if self.rect.top <= scroller:
           if self.vel_y < 0:
                scroll = -dy                 
        #updating rect position
        self.rect.x += dx
        self.rect.y += dy + scroll
   
        return scroll
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x ,self.rect.y)) 
        #pygame.draw.rect(screen, (255,255,255), self.rect,2)
#platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        
        self.rect.y += scroll
        #removing gone platforms
        if self.rect.top > screen_height:
            self.kill()    
#player instance
player = player(screen_width //2 - 50,screen_height-100)
#sprite
platform_group = pygame.sprite.Group()
#creating starting platform
platform = Platform(screen_width //2 - 50,screen_height-50, 100)

platform_group.add(platform)
#game loop
run = True
while run:
    
    clock.tick(fps)
    if game_over == False:
        scroll = player.move()    
        #draw background
        bg_scroll += scroll
        if bg_scroll >= 600 :
            bg_scroll = 0
        draw_bg(bg_scroll)
        
        if len(platform_group) < max_platform:
            p_w = random.randint(40, 60)
            p_x = random.randint(0,screen_width - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            platform = Platform(p_x,p_y,p_w)
            platform_group.add(platform)

        platform_group.update(scroll)
    
        platform_group.draw(screen)
        
        player.draw()
        
        if player.rect.top > screen_height:
            game_over = True
    else:
        draw_text('GAME OVER!!', font_large,(255,255,255), 115, 200)
        draw_text('SCORE : ' + str(score),font_large,(255,255,255),130,250)
        draw_text('PRESS space to start again!!', font_large, (255,255,255), 40, 300)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            game_over = False
            score = 0
            scroll = 0
            platform.rect.center = (screen_width //2 - 50,screen_height-50)
            platform_group.empty()
            platform = Platform(screen_width //2 - 50,screen_height-50, 100)
            platform_group.add(platform)
    
    
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #updating window
    pygame.display.update()
pygame.quit() 
