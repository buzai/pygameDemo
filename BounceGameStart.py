import pygame, sys, math, random

def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap

class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def set_position(self, new_position):
        self.rectangle.center = new_position

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)


class Enemy:
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()

        self.rx = random.randint(0,width) + 25
        self.ry = random.randint(0,height) + 25
        self.set_position(self.rx, self.ry)

        self.vtuple = tuple([1, 1])
        self.width = width
        self.height = height

    def set_position(self, rx, ry):
        self.rectangle.centerx = rx
        self.rectangle.centery = ry

    def move(self):
        self.rectangle.move_ip(self.vtuple[0], self.vtuple[1])

    def bounce(self, width, height):
        vx = self.vtuple[0]
        vy = self.vtuple[1]
        if(self.rectangle.left < 0):
            vx *= -1
        elif(self.rectangle.right > width):
            vx *= -1
        elif(self.rectangle.top < 0):
            vy *= -1
        elif(self.rectangle.bottom > height):
            vy *= -1
        self.vtuple = tuple([vx, vy])

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

class DropEnemy(Enemy):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.postion = self.rectangle.center
    def move(self):
        vx = self.vtuple[0]
        vy = self.vtuple[1]
        vy = vy + 0.1
        self.vtuple = tuple([vx, vy])

        x = self.postion[0]
        y = self.postion[1]
        x = vx + x
        y = vy + y
        self.postion = tuple([x, y])
        self.rectangle.center = self.postion

class PowerUp:
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()

        self.rx = random.randint(0,width) + 25
        self.ry = random.randint(0,height) + 25
        self.set_position(self.rx, self.ry)

    def set_position(self, rx, ry):
        self.rectangle.centerx = rx
        self.rectangle.centery = ry

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

class PowerUpRotate(PowerUp):
    def __init__(self, image, width, height):
        self.angle = 0
        self.original_image = image
        super().__init__(image, width, height)

    def draw(self, screen):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        center = self.rectangle.center
        self.rectangle = self.image.get_rect()
        self.rectangle.center = center
        self.mask = pygame.mask.from_surface(self.image)

        super().draw(screen)
        self.angle += 10

Enemycount = 10
def main():
    pygame.init()
    myfont = pygame.font.SysFont('monospace', 24)
    width, height = 600, 400
    size = width, height
    screen = pygame.display.set_mode((width, height))
    enemy = pygame.image.load("GolfBall.png").convert_alpha()
    enemy_image = pygame.transform.smoothscale(enemy, (50, 50))
    enemy2 = pygame.image.load("DropEnemy.png").convert_alpha()
    enemy_image2 = pygame.transform.smoothscale(enemy2, (50, 50))
    enemy_sprites = []
    for tmp in range(0, Enemycount):
        if (tmp > (Enemycount / 2 - 1)):
            enemy_sprites.append(Enemy(enemy_image, width, height))
        else:
            enemy_sprites.append(DropEnemy(enemy_image2, width, height))

    player_image = pygame.image.load("Wizard.gif").convert_alpha()
    player_sprite = Sprite(player_image)
    life = 3
    powerup_image = pygame.image.load("knight.gif").convert_alpha()
    powerup_image2 = pygame.image.load("power2.gif").convert_alpha()
    powerups = []
    powerupsToDel = []
    harms = []
    is_playing = True
    while is_playing:
        if (life <= 0):
            is_playing = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False

        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)
        sublife = 0
        for enemy_sprite in enemy_sprites:
            if (pixel_collision(player_sprite.mask, player_sprite.rectangle, enemy_sprite.mask, enemy_sprite.rectangle)):
                sublife = sublife + 1
        harms.append(sublife)
        if len(harms) == 10:
            life = life - min(harms)
            harms = []
        for powerup in powerups:
            if (pixel_collision(player_sprite.mask, player_sprite.rectangle, powerup.mask, powerup.rectangle)):
                life = life + 1
                powerupsToDel.append(powerup)
        for delp in powerupsToDel:
            print("del")
            powerups.remove(delp)
        powerupsToDel = []
        for enemy_sprite in enemy_sprites:
            enemy_sprite.move()
            enemy_sprite.bounce(width, height)
        prandm = random.randint(0, 100)
        if (prandm == 20):
            powerups.append(PowerUp(powerup_image, width, height))
        elif(prandm == 40):
            powerups.append(PowerUpRotate(powerup_image2, width, height))
        screen.fill((0,100,50)) 
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
   
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)
        player_sprite.draw(screen)
        text = "Life: " + str('%.1f'%life)
        label = myfont.render(text, True, (255, 255, 0))
        screen.blit(label, (20, 20))
        pygame.display.update()
        pygame.time.wait(20)
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
