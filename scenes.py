import pygame
import random
from options import *
from objects import *

# define the key to exit the game
QUIT = pygame.QUIT

# declare the object to operate FPS and measure the time
clock = pygame.time.Clock()


# define the superclass of whole scenes
class Scene:
    def __init__(self, row, col, display):
        self.row = row
        self.col = col
        self.display = display
        self.bgImage = None
        self.score = 0

    # define the function to resize the image of the background
    def resize_img(self):
        self.bgImage = pygame.transform.scale(self.bgImage, (self.row * TILE, self.col * TILE))

    # define the function to draw the background
    def draw_screen(self, img, screen, x, y):
        screen.blit(img, (x, y))

    def run(self):
        pass


# define the class of the starting screen
class Start(Scene):
    def __init__(self, row, col, display):
        super().__init__(row, col, display)
        self.bgImage = pygame.image.load(STARTIMAGE)

        # resize the background
        self.resize_img()

    def run(self):
        start = False
        screen = self.display
        loop = 0
        screen.fill(WHITE)  # initialize the screen

        # declare the variables that indicate the size of the screen
        screenWth = self.row * TILE
        screenHgt = self.col * TILE

        # declare the main character to appear on the display
        gooreum = Player(screenWth * 0.15, screenHgt * 0.65)
        gooreum.save_floor()

        # play the music repeatedly
        pygame.mixer.music.load(BEGIN)
        pygame.mixer.music.play(-1)

        while not start:
            loop += 1
            gooreum.tick(playing=False)  # move the player without playing the sounds

            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.stop()  # stop the music
                        start = True

            self.draw_screen(self.bgImage, screen, 0, 0)
            gooreum.draw(screen)

            pygame.display.update()
            clock.tick(FPS)

            # make the main character repeat jumping
            if loop % (FPS // 2) in [n for n in range(8)]:
                gooreum.jump = True

        return start


# define the class to show the intro
class Intro(Scene):
    def __init__(self, row, col, display):
        super().__init__(row, col, display)
        self.bgImage = pygame.image.load(INTRO)

        # resize the background
        self.resize_img()

    def run(self):
        skip = False
        screen = self.display

        # declare the variables that indicate the size of the screen
        screenWth = self.row * TILE
        screenHgt = self.col * TILE

        # sey the text that indicates the key to skip
        skipText = Text(screenWth * 0.05, screenHgt * 0.8)
        skipText.write_text("[S]: skip and start", screenWth)
        # set the text that indicates the key to see how to play
        nextText = Text(screenWth * 0.05, screenHgt * 0.85)
        nextText.write_text("[N]: go to the next page", screenWth)
        # declare the list of texts
        texts = [skipText, nextText]

        while not skip:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        skip = True
                    elif event.key == pygame.K_n:
                        return False

            # draw the image on screen
            self.draw_screen(self.bgImage, screen, 0, 0)
            # show the texts on screen
            for t in texts:
                screen.blit(t.text, (t.x, t.y))

            pygame.display.update()
            clock.tick(FPS)

        return skip


# define the class to show how to play
class HowToPlay(Scene):
    def __init__(self, row, col, display):
        super().__init__(row, col, display)
        self.bgImage = pygame.image.load(HOWTO)

        # resize the background
        self.resize_img()

    def run(self):
        ready = False
        screen = self.display
        loop = 0
        screen.fill(WHITE)  # initialize the screen

        # declare the variables that indicate the size of the screen
        screenWth = self.row * TILE
        screenHgt = self.col * TILE

        # declare the main character to show jumping
        gooreum = Player(screenWth * 0.85, screenHgt * 0.4)
        gooreum.save_floor()
        # set the text that contains the key to user
        showTxt = Text(screenWth * 0.65, screenHgt * 0.3)
        showTxt.write_text("This is Gooreum.", screenWth)

        while not ready:
            loop += 1
            gooreum.tick()  # move the player without playing the sounds

            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gooreum.sounds['jump'].stop()
                        ready = True

            self.draw_screen(self.bgImage, screen, 0, 0)
            # draw all elements declared before
            gooreum.draw(screen)
            screen.blit(showTxt.text, (showTxt.x, showTxt.y))

            pygame.display.update()
            clock.tick(FPS)

            # make the main character repeat jumping
            if loop % (FPS // 2) in [n for n in range(8)]:
                gooreum.jump = True

        return ready


# define the class of the playing screen
class Playing(Scene):
    def __init__(self, row, col, display):
        super().__init__(row, col,  display)
        self.bgImage = pygame.image.load(BACKGROUND)
        self.gameClear = pygame.image.load(GAMECLEAR)
        self.music = pygame.mixer.Sound(PLAYING)

        # resize the background
        self.resize_img()

    # define the function to move the background
    def move_background(self, bg1, bg2, wth):
        rate = TILE / 4  # set the rate where the background moves
        bg1 -= rate
        bg2 -= rate  # move all images to the left
        if bg1 == -wth:
            bg1 = wth  # move an image to the right side of the screen
        elif bg2 == -wth:
            bg2 = wth  # move an image to the right side of the screen
        return bg1, bg2

    # count the score during playing the game
    def count_score(self, loop):
        if loop % (FPS * 5) == 0:
            self.score += 10

    # function to implement the main game
    def run(self):
        screen = self.display
        music = self.music
        game_over = False  # the program ends if this variable is 'True'
        objects = []  # declare the list to save the objects in the screen
        monsters = []  # declare the list to handle monsters
        loop = 0  # declare the variable to count the loop

        # save the time when the game started
        startTime = pygame.time.get_ticks()

        # declare the variables that indicate the size of the screen
        screenWth = self.row * TILE
        screenHgt = self.col * TILE

        # declare the variable of the floor in the game display
        gameGround = screenHgt * 0.67

        bg1 = 0  # set the location of the background
        bg2 = screenWth  # set the location of the copy of the background

        player = Player(screenWth / 10, gameGround)  # create the object of the player
        player.save_floor()  # save the value of the floor for making player walk
        objects.append(player)

        shots = Shoot(screenWth / 10 + TILE * 5, gameGround + TILE * 2.5)
        objects.append(shots)

        # define the objects that shows the progress of the game
        score = Score(screenWth / 20, FONTSIZE * 1.5)
        remainLife = Lives(screenWth * 0.8, FONTSIZE * 1.5)
        # declare the list to control the objects that shows the progress of the game
        status = [score, remainLife]

        # play the music repeatedly
        music.play(-1)

        while not game_over:
            screen.fill(WHITE)  # initialize the screen
            loop += 1  # count the loop to measure the time to add the monster and count the score
            self.count_score(loop)  # count the score using the value of the loop
            score.set_message(self.score)

            # measure the elapsed time after the game started
            elapedTime = (pygame.time.get_ticks() - startTime) / 1000

            if elapedTime <= RUNNING:
                # appear monsters at the constant gap
                if loop % (FPS * 5) == 0 or loop % (FPS * 3) == 0:
                    monster = Monster(screenWth, gameGround)
                    objects.append(monster)
                    monsters.append(monster)

                # decide whether or not make an item appear and execute it
                elif loop % (FPS * 2) == 0 or loop % (FPS * 7) == 0:
                    isThere = random.randint(1, 5)  # the items randomly appears
                    if isThere % 2:  # the item appears if 'isThere' is odd
                        # determine at random whether the position of the item is high or not
                        isHigh = random.randint(0, 1)
                        itemY = gameGround + TILE
                        if isHigh:  # the item floats if the value of 'isHigh' is 1
                            itemY = HIGH
                        choice = random.randint(0, 5)  # declare the number at random to choose the item
                        if choice % 2:  # create 'Star' if chosen number is odd
                            item = Star(screenWth, itemY)
                        else:  # create 'Heart' if chosen number is even
                            item = Heart(screenWth, itemY)
                        objects.append(item)

            # handle the event that the user entered
            for event in pygame.event.get():
                if event.type == QUIT:
                    music.stop()  # stop the music
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == player.jumpKey:
                        player.jump = True

            # move and draw images of the background
            bg1, bg2 = self.move_background(bg1, bg2, self.row * TILE)
            self.draw_screen(self.bgImage, screen, bg1, 0)
            self.draw_screen(self.bgImage, screen, bg2, 0)

            # check and run the operation of shooting
            player.shoot(shots)
            shots.reset_height(player)
            shots.decide_pop(screenWth, screenHgt)  # remove shots out of the screen

            # move all objects
            for e in objects:
                e.tick()

            # draw all objects in the screen
            for e in objects:
                e.draw(screen)

            # handle if the player get the item
            for e in objects[1:]:
                gotten = player.handle_item(e)
                if gotten == PLUS:  # if the player gets the star
                    self.score += PLUS
                elif gotten == 1:  # if the player gets the key
                    music.stop()  # stop the music
                    return False

            # check if the player has been attacked if there is at least one monster
            if monsters:
                for m in monsters:
                    player.crash(m)

            # count the remaining life and save the value
            remainLife.count(player)

            # make the monster attack and decide if it is attacked
            for m in monsters:
                m.attack(player)
                m.crash(shots)

            # show the progress of the game on the display
            for e in status:
                e.draw(screen)

            pygame.display.update()
            clock.tick(FPS)

            for e in objects:
                e.check_dead()
                if not e.exist:
                    if type(e) == Monster:
                        e.sounds['dead'].play()  # play the sound effect
                        monsters.remove(e)
                        self.score += PLUS // 2
                    objects.remove(e)

            if not player.exist:
                music.stop()  # stop the music
                game_over = True

            # the key appears if the player defeats all monsters
            if elapedTime >= RUNNING * 1.1:
                # check if the key has appeared before
                keyExist = any([isinstance(e, Key) for e in objects])
                if not keyExist:
                    endKey = Key(screenWth, gameGround)
                    objects.append(endKey)
                for e in objects[1:]:
                    if type(e) == Key:
                        # the games is clear even if the player jumps over the key
                        if player.x >= e.x:
                            music.stop()  # stop the music
                            return False

        return game_over


# define the superclass of the ending scene from class 'Scene'
class GameEnd(Scene):
    def set_score(self, score):
        self.score = score


# define the class to display when the user lose the game
class GameOver(GameEnd):
    def __init__(self, row, col, display):
        super().__init__(row, col, display)
        self.bgImage = pygame.image.load(GAMEOVER)
        # resize the image
        self.resize_img()

    def run(self):
        screen = self.display
        score = self.score
        retry = False

        # initialize the screen
        screen.fill(WHITE)

        # set the variable to count the loop
        loop = 0

        # declare the variables that indicate the size of the screen
        screenWth = self.row * TILE
        screenHgt = self.col * TILE

        # set the text that shows the score
        scoreTxt = Text(screenWth // 2, screenHgt * 0.55)
        scoreTxt.write_text(f"FINAL SCORE: {score}", screenWth)
        # set the text that contains the key to user
        retryTxt = Text(screenWth // 2, screenHgt - FONTSIZE * 2)
        retryTxt.write_text("[Y]: retry   |   [N]: exit", screenWth)
        # declare the object of the monster that shows joyful moment
        monster = Monster(screenWth * 0.67, screenHgt * 0.41)

        # declare the list of the objects that displays on the screen
        objects = [scoreTxt, retryTxt, monster]

        pygame.mixer.music.load(LOSE)

        while not retry:
            loop += 1

            # implement that the monster jumping of joy from victory
            if loop % (FPS // 2) in [n for n in range(10)]:
                monster.y = screenHgt * 0.41 - TILE * 2
            else:
                monster.y = screenHgt * 0.41

            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    pygame.mixer.music.stop()  # stop the music if it is playing
                    if event.key == pygame.K_y:
                        retry = True
                    elif event.key == pygame.K_n:
                        return False

            # display the image that indicates the game is over
            self.draw_screen(self.bgImage, screen, 0, 0)
            # draw all elements in the list declared before
            for ele in objects:
                ele.draw(screen)

            # play the music once
            if loop == 1:
                pygame.mixer.music.play()

            pygame.display.update()
            clock.tick(FPS)

        return retry


# define the class to display when the user win the game
class GameClear(GameEnd):
    def __init__(self, row, col, display):
        super().__init__(row, col, display)
        self.bgImage = pygame.image.load(GAMECLEAR)
        # resize the image
        self.resize_img()

    def run(self):
        screen = self.display
        score = self.score
        restart = False

        # initialize the screen
        screen.fill(WHITE)

        # set the variable to count the loop
        loop = 0

        # declare the variables that indicate the size of the screen
        screenWth = self.row * TILE
        screenHgt = self.col * TILE

        # set the text that shows the score
        scoreTxt = Text(screenWth // 2, screenHgt * 0.55)
        scoreTxt.write_text(f"FINAL SCORE: {score}", screenWth)
        # set the text that contains the key to user
        retryTxt = Text(screenWth // 2, 0)
        retryTxt.write_text("[Y]: restart   |   [N]: exit", screenWth)
        # declare the object of the main character that shows joyful moment
        gooreum = Player(screenWth * 0.24, screenHgt * 0.41)

        # declare the list of the objects that displays on the screen
        objects = [scoreTxt, retryTxt, gooreum]

        # add the music
        pygame.mixer.music.load(WIN)

        while not restart:
            loop += 1

            # implement that the monster jumping of joy from victory
            if loop % (FPS // 2) in [n for n in range(10)]:
                gooreum.y = screenHgt * 0.41 - TILE * 2
            else:
                gooreum.y = screenHgt * 0.41

            for event in pygame.event.get():
                if event.type == QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    pygame.mixer.music.stop()  # stop the music if it is playing
                    if event.key == pygame.K_y:
                        restart = True
                    elif event.key == pygame.K_n:
                        return False

            # display the image that indicates the game is over
            self.draw_screen(self.bgImage, screen, 0, 0)
            # draw all elements in the list declared before
            for ele in objects:
                ele.draw(screen)

            # play the music once
            if loop == 1:
                pygame.mixer.music.play()

            pygame.display.update()
            clock.tick(FPS)

        return restart
