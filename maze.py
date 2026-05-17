#создай игру "Лабиринт"



from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, speed_sprite, x_sprite, y_sprite, image_sprite):
        super().__init__()
        self.image = transform.scale(image.load(image_sprite), (65, 65))
        self.speed = speed_sprite
        self.rect = self.image.get_rect()
        self.rect.x = x_sprite
        self.rect.y = y_sprite

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill((100, 100, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_h - 80:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def __init__(self, speed_sprite, x_sprite, y_sprite, image_sprite):
        super().__init__(speed_sprite, x_sprite, y_sprite, image_sprite)
        self.direction = 'left'

    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= win_w - 85:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

def reset_game():
    global finish, player, enemy, treasure, lives, has_key, key_sprite

    has_key = False
    finish = False
    lives = 3

    
    all_sprites.empty()
    walls_group.empty()

    
    player = Player(7, 100, win_h - 150, 'hero.png')
    enemy = Enemy(2, win_w - 200, win_h - 250, 'cyborg.png')
    treasure = GameSprite(0, win_w - 150, win_h - 150, 'treasure.png')
    key_sprite = GameSprite(0, 200, 100, 'i.jpg') 
    all_sprites.add(key_sprite)

    all_sprites.add(player)
    all_sprites.add(enemy)
    all_sprites.add(treasure)

    
    walls_group.add(wall_left_border)
    walls_group.add(wall_right_border)
    walls_group.add(wall_top_border)
    walls_group.add(wall_bottom_border)
    walls_group.add(inner_wall_1)
    walls_group.add(inner_wall_2)
    walls_group.add(inner_wall_3)
    walls_group.add(inner_wall_4)


win_w = 700
win_h = 500

window = display.set_mode((win_w, win_h))
display.set_caption('maze')
background = transform.scale(image.load('background.jpg'), (win_w, win_h))

all_sprites = sprite.Group()
walls_group = sprite.Group()
key_sprite = GameSprite(0, 200, 100, 'i.jpg')  
all_sprites.add(key_sprite)


player = Player(7, 100, win_h - 150, 'hero.png')
enemy = Enemy(2, win_w - 200, win_h - 250, 'cyborg.png')
treasure = GameSprite(0, win_w - 150, win_h - 150, 'treasure.png')

all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(treasure)


wall_left_border = Wall(0, 0, 10, win_h)
wall_right_border = Wall(win_w - 10, 0, 10, win_h)
wall_top_border = Wall(0, 0, win_w, 10)
wall_bottom_border = Wall(0, win_h - 10, win_w - 100, 10)

inner_wall_1 = Wall(200, 150, 400, 10)
inner_wall_2 = Wall(450, 150, 10, 350)
inner_wall_3 = Wall(200, 350, 250, 10)
inner_wall_4 = Wall(0, 250, 180, 10)

walls_group.add(wall_left_border)
walls_group.add(wall_right_border)
walls_group.add(wall_top_border)
walls_group.add(wall_bottom_border)
walls_group.add(inner_wall_1)
walls_group.add(inner_wall_2)
walls_group.add(inner_wall_3)
walls_group.add(inner_wall_4)

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play(-1)

win_sound = mixer.Sound('money.ogg')
lose_sound = mixer.Sound('kick.ogg')

font.init()
font_winner = font.SysFont('Arial', 72, True, False)
font_loser = font.SysFont('Arial', 72, True, False)
font_restart = font.SysFont('Arial', 36, True, False)
font_lives = font.SysFont('Arial', 36, True, False)  

text_win = font_winner.render('YOU WIN!', True, (255, 215, 0))
text_lose = font_loser.render('YOU LOSE!', True, (178, 34, 34))
text_restart = font_restart.render('Press R to play again', True, (255, 255, 255))


has_key = False
lives = 3
game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif finish and e.type == KEYDOWN:
            if e.key == K_r:
                reset_game()

    if not finish:
        window.blit(background, (0, 0))

        all_sprites.update()
        all_sprites.draw(window)
        walls_group.draw(window)

        # Отображаем количество жизней
        text_lives = font_lives.render(f'Lives: {lives}', True, (255, 255, 255))
        window.blit(text_lives, (10, 10))

        # Отображаем статус ключа (опционально)
        if has_key:
            text_key_status = font_lives.render('Key: YES', True, (0, 255, 0))
        else:
            text_key_status = font_lives.render('Key: NO', True, (255, 0, 0))
        window.blit(text_key_status, (10, 50))

        # Проверка подбора ключа
        if sprite.collide_rect(player, key_sprite):
            has_key = True
            key_sprite.kill()

        # Логика игры
        # Победа возможна только с ключом
        if sprite.collide_rect(player, treasure) and has_key:
            finish = True
            win_sound.play()
        elif sprite.collide_rect(player, treasure) and not has_key:
            # Сообщение о том, что нужен ключ
            text_no_key = font_lives.render('Get the key first!', True, (255, 0, 0))
            window.blit(text_no_key, (win_w/2 - text_no_key.get_width()/2, win_h - 50))
        elif sprite.spritecollide(player, walls_group, False) or sprite.collide_rect(player, enemy):
            lives -= 1
            lose_sound.play()
            player.rect.x = 100
            player.rect.y = win_h - 150
            if lives <= 0:
                finish = True

    else:
        if sprite.collide_rect(player, treasure) and has_key:
            window.blit(text_win, (win_w/2 - text_win.get_width()/2, win_h/2 - 50))
        else:
            if lives <= 0:
                window.blit(text_lose, (win_w/2 - text_lose.get_width()/2, win_h/2 - 50))
            else:
                pass
        window.blit(text_restart, (win_w/2 - text_restart.get_width()/2, win_h/2 + 50))

    clock.tick(FPS)
    display.update()