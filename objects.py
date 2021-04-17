import pygame
import random
from options import *


class Objects:
    def __init__(self, x, y):
        self.img = None
        self.sounds = {}
        self.x = x
        self.y = y
        self.exist = True

    # define the function to resize the image
    def resize(self, size, img):
        img_small = pygame.transform.scale(img, (size, size))
        return img_small

    def resize_all(self, size):
        pass

    def set_sounds(self):
        pass

    def tick(self):
        pass

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def crash(self, element):
        pass

    def check_dead(self):
        pass


# define the class of the player
class Player(Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.life = LIFE
        self.dy = JUMP
        self.floor = None
        self.jump = False
        self.img = pygame.image.load(NORMAL)  # the image of the normal mode
        self.attack = pygame.KMOD_LSHIFT  # the key to attack to the enemy
        self.jumpKey = pygame.K_SPACE  # the key to attack to the enemy

        self.resize_all(TILE)  # resize and save the image
        self.set_sounds()  # set the sounds

    # define the function to resize all images
    def resize_all(self, size):
        self.img = self.resize(size * 5, self.img)

    # define the function to set the sounds
    def set_sounds(self):
        # load sound effects to the dictionary
        self.sounds['jump'] = pygame.mixer.Sound(JUMPSOUND)
        self.sounds['hurt'] = pygame.mixer.Sound(DAMAGE)
        self.sounds['heal'] = pygame.mixer.Sound(HEAL)
        self.sounds['item'] = pygame.mixer.Sound(GETITEM)
        self.sounds['shoot'] = pygame.mixer.Sound(SHOTSOUND)

    # define the function to save the distance of the floor in the screen
    def save_floor(self):
        self.floor = self.y

    def tick(self, playing=True):
        if self.jump:
            # check to show the player shooting without sound effect before the game starts
            if self.dy == JUMP and playing:
                self.sounds['jump'].play()  # play the sound effect
            if self.dy >= -JUMP:
                self.y -= (self.dy * abs(self.dy)) * 0.5
                self.dy -= 0.25
            if self.dy < -JUMP and self.y == self.floor:
                self.dy = JUMP
                self.jump = False

    # define the function to shoot
    def shoot(self, shoot):
        if pygame.key.get_mods() & self.attack:  # check whether the player shoots or not
            if shoot.elements:
                last = shoot.elements[-1]
                if abs(last[0] - shoot.x) < GAP:  # set the constant gap between elements
                    return
            self.sounds['shoot'].play()
            shoot.add()

    # define the function to handle the player when it hurts by the monster
    def crash(self, element):
        if type(element) != Monster:
            return
        half = TILE * 2.5
        x, y = self.x, self.y
        eX, eY = element.x, element.y
        bullets = element.bullet
        # handle the situation that the player contacts with the monster
        if abs(x - eX) <= half and abs(y - eY) <= half:
            self.exist = False  # the player becomes dead
        # handle the situation that the player take a shot by the monster
        for e in bullets:
            if (x + half - TILE <= e[0] <= x + half) and abs(y - e[1]) <= half:
                self.life -= 1  # the number of life will be decreased
                bullets.remove(e)  # remove the bullets from the screen
                if self.life:
                    self.sounds['hurt'].play()  # play the sound effect

    # define the function to handle the the item gotten
    def handle_item(self, element):
        if not isinstance(element, Item):
            return
        eX, eY = element.x, element.y
        x, y = self.x, self.y
        standard = TILE * 1.5
        if abs(x - eX) > standard or abs(y - eY) > standard:
            return
        element.exist = False
        if type(element) == Star:
            self.sounds['item'].play()  # play the sound effect
            return PLUS  # the score increases if the player meets 'Star'
        elif type(element) == Heart:
            self.sounds['heal'].play()  # play the sound effect
            if self.life < 5:
                self.life += 1
            return 0  # set the result value to distinguish the situation
        elif type(element) == Key:
            return 1  # set the value to decide if the game is clear

    # define the function to check whether the monster is dead or not
    def check_dead(self):
        if self.life <= 0:
            self.exist = False


# define the class of the enemy
class Monster(Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = None
        self.life = random.randint(6, 8)  # the number of life is randomly determined (6 to 8)
        self.bullet = []
        self.bulletImg = None
        self.dx = SPEED

        # set the image of the monster
        self.set_image()

    # define the function to set the image
    def set_image(self):
        images = [M1, M2, M3, M4, M5]
        index = random.randint(0, 4)  # the image is randomly picked

        # load and resize images
        self.img = self.resize(TILE * 5, pygame.image.load(images[index]))
        self.bulletImg = self.resize(TILE * 2, pygame.image.load(BULLET))
        # set the sounds
        self.set_sounds()

    def set_sounds(self):
        self.sounds['dead'] = pygame.mixer.Sound(KILL)
        self.sounds['hurt'] = pygame.mixer.Sound(ATTACK)
        self.sounds['shoot'] = pygame.mixer.Sound(M_SHOTSOUND)

    def tick(self):
        self.x -= self.dx
        bullet = self.bullet
        if bullet:
            for i in range(len(bullet)):
                bullet[i][0] -= (self.dx * 2)

    # overriding the method of <class 'Objects'>
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))
        if self.bullet:
            for e in self.bullet:
                if not e[1]:
                    continue
                screen.blit(self.bulletImg, tuple(e))

    # define the function to attack
    def attack(self, element):
        if type(element) == Player:
            if abs(element.x - self.x) <= DX:
                self.shoot()

    # define the function to shoot
    def shoot(self):
        bullet = self.bullet
        if not bullet:
            bullet.append([self.x - TILE * 2.5, self.y + TILE * 2.5])
        if bullet:
            last = self.bullet[-1]
            if abs(last[0] - self.x) == DX / 5:  # set the constant gap between bullets
                self.sounds['shoot'].play()
                bullet.append([self.x - TILE * 2.5, self.y + TILE * 2.5])

    # define the function to decide if the monster takes a bullet by the player
    def crash(self, element):
        half = TILE * 2.5
        if type(element) != Shoot:
            return
        shoots = element.elements
        bullets = self.bullet
        if shoots:
            # the monster hurts when it take a shot by the player
            for s in shoots:
                if (s[0] >= self.x - half) and (self.y - half <= s[1] <= self.y + half):
                    self.sounds['hurt'].play()  # play the music
                    self.life -= 1
                    shoots.remove(s)
            # the shot of both sides are gone if they bumped each other
            for s in shoots:
                for b in bullets:
                    if not b:
                        continue
                    if abs(s[0] - b[0]) <= TILE * 2 and abs(s[1] - b[1]) <= TILE * 2:
                        shoots.remove(s)
                        b[1] = 0

    # define the function to check whether the monster is dead or not
    def check_dead(self):
        if self.life <= 0:
            self.exist = False


# define the class of the bubble from <class 'Objects'>
# player uses this object to attack the enemy
class Shoot(Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.dx = SPEED
        self.img = pygame.image.load(SHOOT)
        self.elements = []

        self.resize_all(TILE)  # resize and save the image

    # overriding the method of <class 'Objects'>
    def resize(self, size, img):
        img_small = pygame.transform.scale(img, (size * 2, size))
        return img_small

    # define the function to resize all images
    def resize_all(self, size):
        self.img = self.resize(size, self.img)

    def add(self):
        self.elements.append([self.x, self.y])

    # define the function to reset the height of the shooting location as the player moves
    def reset_height(self, player):
        if type(player) == Player:
            self.y = player.y + TILE * 2.5

    def tick(self):
        elements = self.elements
        for i in range(len(elements)):
            elements[i][0] += (self.dx * 2)

    # overriding the method of <class 'Objects'>
    def draw(self, screen):
        elements = self.elements
        for e in elements:
            screen.blit(self.img, tuple(e))  # draw each objects in the list

    # define the function to remove the element out of the screen
    def decide_pop(self, x, y):
        if not self.elements:
            return
        first = self.elements[0]
        if not ((0 <= first[0] <= x) and (0 <= first[1] <= y)):
            self.elements.remove(first)


# define the superclass of other objects in the game
class Item(Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.dx = SPEED
        self.img = None

    # overriding the method of <class 'Objects'>
    def resize(self, size, img):
        img_small = pygame.transform.scale(img, (int(size * 1.2), size))
        return img_small

    # define the function to resize all images
    def resize_all(self, size):
        self.img = self.resize(size * 3, self.img)

    def tick(self):
        self.x -= self.dx

    # decide if the item is out of the screen
    def decide_pop(self, x, y):
        iX, iY = self.x, self.y
        if not (0 <= iX <= x and 0 <= iY <= y):
            self.exist = False


# define the class of the Life from <class 'Item'>
# the number of life increases when the player get this object
class Heart(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load(HEART)

        # resize the image
        self.resize_all(TILE)


# define the class of the star from <class 'Item'>
# the score goes up additionally when the player get this object
class Star(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load(STAR)

        # resize the image
        self.resize_all(TILE)


# define the class of the key from <class 'Item'>
class Key(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load(ENDKEY)

        # resize the image
        self.resize_all(TILE)


# define the class of icons that show the progress of the game above the screen
class Icon(Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.font = pygame.font.Font(FONT, FONTSIZE)
        self.message = None

    # define the function to resize all images
    def resize_all(self, size):
        self.img = self.resize(size * 2, self.img)

    def set_message(self, text):
        pass


# define the class of the score from <class 'Icon'>
class Score(Icon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = pygame.image.load(SMALL_STAR)
        self.font = pygame.font.Font(FONT, FONTSIZE)
        self.message = None

        # resize the image
        self.resize_all(TILE)

    def set_message(self, score):
        text = "SCORE: {:d}".format(score)
        self.message = self.font.render(text, True, WHITE)

    # overriding the method of <class 'Objects'>
    def draw(self, screen):
        screen.blit(self.img, (self.x - TILE * 2, self.y))
        screen.blit(self.message, (self.x + TILE * 2, self.y))


# define the class of the remaining lives from <class 'Icon'>
class Lives(Icon):
    def __init__(self, x, y):
        super().__init__(x, y)  # the initialization is from <class 'Objects'>
        self.img = pygame.image.load(SMALL_HEART)
        self.cnt = 0

        # resize the image
        self.resize_all(TILE)

    # define the function to count the remaining life
    def count(self, player):
        self.cnt = player.life

    # overriding the method of <class 'Objects'>
    def draw(self, screen):
        x = self.x
        for i in range(self.cnt):
            screen.blit(self.img, (x, self.y))
            x += TILE * 2.5


# define the class to insert the text on the screen
class Text(Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.font = pygame.font.Font(FONT, FONTSIZE)
        self.text = None
        self.rect = None

    def write_text(self, text, width):
        self.text = self.font.render(text, True, WHITE)
        # center the text on the screen
        textRect = self.text.get_rect()
        textRect.centerx = width // 2
        textRect.y = self.y
        self.rect = textRect

    # overriding the method of <class 'Objects'>
    def draw(self, screen):
        screen.blit(self.text, self.rect)
