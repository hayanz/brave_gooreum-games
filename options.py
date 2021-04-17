# set the tuple of each color
WHITE = (255, 255, 255)

# define the value of FPS and the standard time that the time until the boss appears
FPS = 40
RUNNING = 90

# define the size of the screen
WIDTH = 80
HEIGHT = 45
TILE = 10

# define the variable of the speed of the player moving left to right
SPEED = TILE / 4
# define the variable of the speed to jump and move left and right
JUMP = 6
MOVE = 5
# define the variable of the gap between the shots the player has
GAP = (TILE * WIDTH) * 0.04

# set the distance that the monster starts to attack to the player
DX = (TILE * WIDTH) * 0.75

# set the number of lives and the added score if player meets the star
LIFE = 5
PLUS = 100
# set the number of the maximum height of the position that the item is placed
HIGH = 160

# set the image of the player
NORMAL = "images/gooreum.png"  # normal mode of the player

# set the image of the attack
# Created by studioworkstock - Freepik.com
# https://www.freepik.com/studioworkstock
SHOOT = "images/shoot.png"  # player makes the light to attack the monster

# set the image of the monster and its bullets
# Created by tartila - Freepik.com
# https://www.freepik.com/tartila
M1 = "images/monster1.png"
M2 = "images/monster2.png"
M3 = "images/monster3.png"
M4 = "images/monster4.png"
M5 = "images/monster5.png"
BULLET = "images/lightening.png"

# set the image of the item
# Created by tartila - Freepik.com
# https://www.freepik.com/tartila
HEART = "images/heart.png"
STAR = "images/star.png"
ENDKEY = "images/key.png"

# set the image of the icon to show the number of lives and the indicate the score
# Created by tartila - Freepik.com
# https://www.freepik.com/tartila
SMALL_HEART = "images/small_heart.png"
SMALL_STAR = "images/small_star.png"

# set the image for displaying before starting the game
# the original image is from the following website: https://hipwallpaper.com/8-bit-backgrounds-green/
STARTIMAGE = "backgrounds/start_image.png"

# set the images of the introduction of the game
INTRO = "backgrounds/intro.png"
HOWTO = "backgrounds/how_to_play.png"

# set the image of the background
# https://www.wallpaperflare.com/white-clouds-illustration-pixel-art-8-bit-cloud-sky-blue-wallpaper-cjeg
BACKGROUND = "backgrounds/playing.jpg"

# set the image that shows if the game is over and clear
# the image in clouds are created by user7030688
# https://www.freepik.com/user7030688
GAMEOVER = "backgrounds/game_over.png"
GAMECLEAR = "backgrounds/game_clear.png"

# set the font in the game and its size
# Created by Andrew Tyler - font@andrewtyler.net
# https://www.AndrewTyler.net
FONT = "fonts/Minecraftia-Regular.ttf"
FONTSIZE = 15

# set the background music and the sound effect
BEGIN = "musics/beginning.wav"  # when the program begins
# created by Alec Weesner - http://www.alecweesner.com/video-game-composer
PLAYING = "musics/playing.mp3"  # during playing the game
# created by Alec Weesner - http://www.alecweesner.com/video-game-composer
WIN = "musics/game_clear.ogg"  # when the game is clear
# created by AUDIO ALCHEMIST - AudioAlchemistStore@gmail.com
LOSE = "musics/game_over.wav"  # when the game is over
# created by Alec Weesner - http://www.alecweesner.com/video-game-composer

# set the sound effects
# all files are from the following website: https://freesound.org/
GETITEM = "effects/get_item.ogg"  # when the player gets the item
SHOTSOUND = "effects/shots.mp3"  # when the player attacks to the monster
HEAL = "effects/heal.wav"  # when the number of lives increases
JUMPSOUND = "effects/jump.wav"  # when the player jumps
DAMAGE = "effects/damage.wav"  # when the player takes damage
ATTACK = "effects/attack.wav"  # when the monster takes damage
KILL = "effects/kill.wav"  # when the player kills the monster
M_SHOTSOUND = "effects/m_shots.wav"  # when the monster attacks to the monster
