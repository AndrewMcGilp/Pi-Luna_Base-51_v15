#Luna Base 51 and Pi-Luna Base by Andrew McGilp (c) 2020
#A Python Pygame for the Raspberry Pi
# 'Pi-Luna Base 51-v15'

"""
Notice:

  Please note that this software is used entirely at your own RISK and comes with 
  absolutely no guarantee or warrantee and by using this software you agree to these
  terms. It is free to be used by a private individual but not for commercial use
  without permission.
  
"""

import pygame, math, sys, random, glob
from pygame.locals import *

pygame.init()

RES_LIST = [(640, 480), (800, 480), (800, 600), (480, 640)]

SCR_RES = 0
SCR_FULL = 0
FX_LEVEL = 3 #FX Volume level
TX_LEVEL = 3 #Soundtrack volume level
IMG_NO = 0
MENU_SET = 0

SCREEN_WIDTH, SCREEN_HEIGHT = RES_LIST[SCR_RES]

#Color    R    G    B
WHITE  = (255, 255, 255)
GREEN  = (0  , 255,   0)
RED    = (255, 0  ,   0)
BLUE   = ( 80, 150, 255)
YELLOW = (255, 255,  80)
BR_COLOR = BLUE

LEFT = 1
MIDDLE = 2
RIGHT = 3
UP = 4
DOWN = 5
MENU_NO = 0
InputNo = 0
TrackNo = 0
TX_MODE = 0

jsx = int(SCREEN_WIDTH / 2)
jsy = int(SCREEN_HEIGHT / 2)

# All the bool stuff true/false
done = False
showMsg = False
pauseGame = False
endGame = False
editName = False
testMode = False
changeCol = 0

#Player Position
posX = 0
posY = 0
towerPosY = 0
offsetX = 0
#Mouse Pos
posx = 0
posy = 0
loopCount = 0
numIndex = 0
imgSelect = 0

useJoystick = 1#1=Look for a joystick and if so use it | 0=If joystick Don't init it!!

char = '_'
strName0 = 'Pi_0.........'#Edit this Name to yours in Hall of Fame, use right mouse button to delete! 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, 16)# plays better in full screen mode
pygame.display.set_caption('Pi-Luna_Base 51-v15')
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

#----------Load sprites images sound and fonts----------
#Load Font's
myHudFont = pygame.font.SysFont("Courier", 18)#Use a mono block font
mySelFont = pygame.font.SysFont("Courier", 24)
myMsgFont = pygame.font.SysFont("Courier", 78)#92

strMsg = myMsgFont.render('Update ME-0!', True, GREEN)
strMsg1 = myHudFont.render('Update ME-1!', True, WHITE)

settList = []
nameList = []
sndTrxList = []
charList = ['','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','U','R','S','T','V','W','X','Y','Z',
            '0','1','2','3','4','5','6','7','8','9','$','@','*','&','!','.','<','>','_']

#Load image's
bgImg = pygame.image.load('Images/Stars_Earth1.png').convert()
startImg = pygame.image.load('Images/GameStart1.png').convert_alpha()
underLayImg = pygame.image.load('Images/UnderLay2.png').convert_alpha()
overLayImg = pygame.image.load('Images/OverLay1.png').convert_alpha()
crossHairImg = pygame.image.load('Images/CrossHair.png').convert_alpha()
baseImg = pygame.image.load('Images/MoonBase6.png').convert_alpha()
tower0Img = pygame.image.load('Images/Tower1.png').convert_alpha()
tower1Img = pygame.image.load('Images/Tower3.png').convert_alpha()
coverImg = pygame.image.load('Images/MtlPlate2.png').convert_alpha()
laserImg = pygame.image.load('Images/Laser.png').convert_alpha()
alienImg1 = pygame.image.load('Images/ufoBug1.png').convert_alpha()#
alienImg2 = pygame.image.load('Images/ufoBug3.png').convert_alpha()#
alienImg3 = pygame.image.load('Images/ufoBug2.png').convert_alpha()#Alien ufoBug damaged
holeImg1= pygame.image.load('Images/hole7.png').convert_alpha()#
asteroidImg3 = pygame.image.load('Images/Asteroid3.png').convert_alpha()#
expoldImg = pygame.image.load('Images/Explod5.png').convert_alpha()
damageImg = pygame.image.load('Images/Damage3.png').convert_alpha()
playerImg = pygame.image.load('Images/player4.png').convert_alpha()
ufoImg1 = pygame.image.load('Images/UFO4.png').convert_alpha()
ufoImg2 = pygame.image.load('Images/UFO6.png').convert_alpha()
missileImg = pygame.image.load('Images/Bomb2.png').convert_alpha()
powerUpImg = pygame.image.load('Images/PowerUp1.png').convert_alpha()
shieldUpImg = pygame.image.load('Images/ShieldUp1.png').convert_alpha()
shieldGridImg = pygame.image.load('Images/ShieldGrid.png').convert_alpha()
jsIcn1Img = pygame.image.load('Images/JS1.png').convert_alpha()
mouseIcn1Img = pygame.image.load('Images/MS1.png').convert_alpha()

#Init and Load Sounds
if (pygame.mixer.get_init() != None):
    pygame.mixer.pre_init(44100,16, 2, 4096)#pygame.mixer.init()
    pygame.mixer.set_reserved(4)
    
    sndTrxEnd = pygame.USEREVENT+1
    pygame.mixer.music.set_endevent(sndTrxEnd)
    
    laserSnd = pygame.mixer.Sound('Sounds/laser.ogg')
    explodSnd = pygame.mixer.Sound('Sounds/explos.ogg')
    btnSnd = pygame.mixer.Sound('Sounds/btnSound.ogg')
    buzzSnd = pygame.mixer.Sound('Sounds/Buzzer4.ogg')
    pwrDnSnd = pygame.mixer.Sound('Sounds/powerDown.ogg')
    pwrUpSnd = pygame.mixer.Sound('Sounds/powerUp.ogg')
    drillSnd = pygame.mixer.Sound('Sounds/DrillSound4.ogg')
    hitSnd = pygame.mixer.Sound('Sounds/hitSound2.ogg')
    fx1Snd = pygame.mixer.Sound('Sounds/fxSound1.ogg')

else:
    print('ERROR_:_No sound mixer!')
    done = True

#Global variables
hiScore = 0
score = 0
ufosToShoot = 0
bonusPoints = 0
levelNo = 0
health = 0
oldHealth = 0
rank = 0
rndRangeY = -400
shieldLevel = 0
bombCount = 0
vibePosX  = 0
vibeTime = 0

# The player sprite
player_list = pygame.sprite.Group()
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.myTexture1 = playerImg
        self.position = (posX, posY)
        self.direction = 0
        self.rect = self.myTexture1.get_rect()
        self.radius = int(self.rect.width / 2)#* .90
        if (testMode):
            pygame.draw.rect(self.myTexture1, RED, self.rect, 1)
            pygame.draw.circle(self.myTexture1, YELLOW, self.rect.center, self.radius, 1)
            
    def update(self):

        self.position = (posX, posY)
        tan = math.atan2((posy - posY), (posx - posX))
        deg = round(math.degrees(tan), 0)
        self.dir = -(deg + 90)
        if (self.dir < 80 and self.dir > -80):
            self.direction = self.dir
        self.image = pygame.transform.rotate(self.myTexture1, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def fireLaser(self):#Fire the laser

        laser = Laser(self.direction)
        laser_list.add(laser)
        laser.rect.x = posX
        laser.rect.y = posY
        if (FX_LEVEL > 0):
            PlaySound(0)       
       
#Add the player
player = Player()
player_list.add(player)

# The laser sprite
laser_list = pygame.sprite.Group()
class Laser(pygame.sprite.Sprite):

    def __init__(self, Direction):
        super().__init__()
        self.myTexture1 = laserImg
        self.position = (posX, posY)# player position
        self.speed = 40
        self.direction = Direction
        self.image = pygame.transform.rotate(self.myTexture1, self.direction)
        self.rect = self.image.get_rect()
        self.radius = 3
        self.x = int(self.rect.width / 2 - 3)
        self.y = int(self.rect.height / 2 - 3)
        if (testMode):
            pygame.draw.rect(self.image, YELLOW, (self.x, self.y, 6, 6), 1)
            pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 1)
            
    def update(self):
        x, y = self.position
        rad = self.direction * math.pi / 180
        x += - self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.speed = 5
        
        if (self.rect.y < -20 or self.rect.y > SCREEN_HEIGHT + 20 or self.rect.x < -10 or self.rect.x > SCREEN_WIDTH + 10):
            self.kill()
            
    def takeHit(self):
        self.kill()
        
#The asteroid's aliens bombs and other bad stuff
asteroid_list = pygame.sprite.Group()
class Asteroid(pygame.sprite.Sprite):
    
    def __init__(self, speedY, Type, image, size, rot, posX, posY):
        super().__init__()
        self.image = image
        self.image = pygame.transform.rotate(image, rot)
        self.image = pygame.transform.scale(self.image, (size , size))
        self.rect = pygame.Rect(self.image.get_rect())
        self.radius = int(self.rect.width / 2)
        if (testMode):
            pygame.draw.rect(self.image, RED, self.rect, 1)
            pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius, 1)
        self.rect.x = posX
        self.rect.y = posY
        self.type = Type
        self.speedY = speedY
        self.health = 10
        
    def update(self):

        if (self.rect.y > SCREEN_HEIGHT -50):
            self.giveHit()
        else:
            self.rect.y += self.speedY
        
    def takeHit(self):
        
        global score
        global health
        global oldHealth

        mag = 2
        num = 0
        
        if (self.type == 0):#Bomb
            score += 40 * rank
            self.health -= 10
            mag = 4         
        elif (self.type == 1):#Asteroid
            score += 10
            self.health -= 10
        elif (self.type == 2):#Health shield icon
            num = 1
            self.health -= 10
            PlaySound(5)
            CreateShields() 
        elif (self.type == 3):#Power up icon
            num = 2 
            score += 50
            if(health > 0):
                health += 50
            PlaySound(5)
            self.health -= 10
             
            if (health == oldHealth):
                oldHealth = health

        elif (self.type == 4):#small alien craft must shoot two times
            PlaySound(7)
            self.image = image = alienImg3
            self.health -= 5
            score += 20

        if (self.health <= 0):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, mag, num)
            self.kill()
        
    def giveHit(self):#Hits player and leaves damage

        global health

        if (self.type == 0):#Bomb
            CreateDamage(self.rect.x + 20, self.rect.y, 50, 0)
            CreateDamage(self.rect.x - 25, self.rect.y + 10, 50, 0)
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 8, 0)
            health -= 50
            
        elif (self.type == 1):#Asteroid
            health -= 10
            CreateDamage(self.rect.x - 5, self.rect.y - 5, 10, 0)
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 2, 0)
            
        elif (self.type == 2):#Health shield icon
            #PlaySound(4)
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, -2, 1)
            
        elif (self.type == 3):#Power Up icon
            #PlaySound(4)
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, -2, 2)

        elif (self.type == 4):#Alien ship
            if (self.health <= 5):#Crash land and explod
                CreateDamage(self.rect.x - 5, self.rect.y - 5, 10, 0)
                CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 2, 0)                
                health -= 10
            else:
                CreateDamage(self.rect.x - 5, self.rect.y -5, 10, 1)#Land and make a hole in the base
                CreateEffectsFX(self.rect.x, self.rect.y + 10, self.rect.width, -2, 3)
                health -= 20
            
        self.kill()
                    
    def removeMe(self):#Make me shrink or explod if it hits the shield and leave no damage
        
        if (self.type == 0 or self.type == 1):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 2, 0)
            
        elif (self.type == 2):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, -2, 1)
            
        elif (self.type == 3):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, -2, 2)

        elif (self.type == 4):
            CreateEffectsFX(self.rect.x, self.rect.y, self.rect.width, 2, 0)
            
        self.kill()
        
#Create Ufo's aka Mothership or UFO's
ufo_list = pygame.sprite.Group()
class Ufo(pygame.sprite.Sprite):
    
    def __init__(self, speed, posX, posY):
        super().__init__()
        self.image = ufoImg1
        self.timer = 0
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = posX
        self.rect.y = posY
        self.health = 100
        self.speed = speed
        self.radius = int(self.rect.width * .35 / 2)
        self.x = int(0)
        self.y = int(self.rect.height * .25)
        self.w = int(self.rect.width)
        self.h = int(self.rect.height * .50)        
        if (testMode):
            pygame.draw.rect(self.image, RED, (self.x, self.y, self.w, self.h), 1)
            pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius, 1)
            
    def update(self):
        
        if (self.timer > 0):
            self.timer -= 1
            self.image = ufoImg2
        else:
            self.image = ufoImg1
        
        if (self.rect.x > SCREEN_WIDTH + 600 or self.rect.x < -600):
            self.kill()
        else:
            self.rect.x += self.speed
        
    def takeHit(self):
        
        global bombCount
        global score
        global bonusPoints
        global ufosToShoot
        
        PlaySound(7)
        self.timer = 5
        dropY = self.rect.bottom - 25
        
        if (self.rect.x > 80 and self.rect.x < (offsetX + 600) and self.speed > -5 and self.speed < 5):
            
            self.speed = self.speed * 2
            bombCount += 1
                
            if (self.speed > 0):
                dropX = self.rect.x + 40
            else:
                dropX = self.rect.x + 30               

            if (bombCount == 3):
                CreatePowerUpIcn()
            elif (bombCount == 6):
                CreateShieldIcn()
                bombCount = 0
                
            CreateMissile(dropX, dropY)
            score += 20

        else: #add bonus UFOs and points
                       
            if (self.speed == 5 or self.speed == -5):
                ufosToShoot -= 1
                bonusPoints += 50
                self.speed = self.speed * 4        
           
#Explosion or implosion effect     
effectsFX_list = pygame.sprite.Group()       
class EffectsFX(pygame.sprite.Sprite):
    
    def __init__(self, posx, posy, size, mag, num):
        super().__init__()
        if (num == 0):
            self.myTexture1 = expoldImg
        elif (num == 1):
            self.myTexture1 = shieldUpImg
        elif (num == 2):
            self.myTexture1 = powerUpImg
        else:
            self.myTexture1 = alienImg2

        self.image = self.myTexture1
        self.rect = pygame.Rect(self.myTexture1.get_rect())
        self.rect.x = posx
        self.rect.y = posy
        self.timer = 0
        self.size = size
        self.mag = mag
       
    def update(self):
        
        self.size += self.mag
        if (self.size < 0):
            self.size = 0
        self.rect.y -= int(self.mag * 0.5)
        self.rect.x -= int(self.mag * 0.5)
        self.image = pygame.transform.scale(self.myTexture1, (self.size , self.size)) 
        self.timer += 1
        if (self.timer > 26):
            self.kill()        
              
#Shield
shield_list = pygame.sprite.Group()
class Shield(pygame.sprite.Sprite):

    def __init__(self, posx, posy, health):
        super().__init__()
        self.image = shieldGridImg
        self.rect = pygame.Rect(self.image.get_rect())
        self.radius = int(self.rect.height / 2)
        self.w = self.rect.width
        self.h = self.rect.height
        if (testMode):
            pygame.draw.rect(self.image, RED, self.rect, 1)
            pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius, 1)
        self.rect.x = posx
        self.rect.y = posy
        self.health = health
        
    def takeHit(self, aType):#, dValue):
        
        PlaySound(4)
        if (aType == 1):
            self.health -= 50
        else:
            self.health -= 100
            
        if (self.health <= 0):
            self.kill()
        else:
            self.image = pygame.transform.scale(self.image, (int(self.w), int(self.health * .01 * self.h)))
                          
#Create Damage        
damage_list = pygame.sprite.Group()
class Damage(pygame.sprite.Sprite):
    
    def __init__(self, posx, posy, num):
        super().__init__()
        if (num == 1):
            self.image = holeImg1
        else:
            self.image = damageImg

        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.x = posx
        self.rect.y = posy
        
    def update(self):
        self.rect.x = self.rect.x - vibePosX
                
def CreateMissile(dropX, dropY):#Drop the Missile using the asteroid class
    
    asteroid = Asteroid(3.0, 0, missileImg, 50, 0, dropX, dropY)
    asteroid_list.add(asteroid)
    
def CreateShieldIcn():#Shield icon
    
    asteroid = Asteroid(2.0, 2, shieldUpImg, 50, 0, random.randrange(60, (SCREEN_WIDTH - 60)), -100)
    asteroid_list.add(asteroid)

def CreatePowerUpIcn():#Power Up icon
    
    asteroid = Asteroid(2.0, 3, powerUpImg, 50, 0, random.randrange(60, (SCREEN_WIDTH - 60)), -100)
    asteroid_list.add(asteroid)
    
def CreateAsteroids():
    
    qty = levelNo * 10 + 20

    if (imgSelect == 1):#Aliens and asteroids
        for i in range(int(qty * 0.8)):#Asteroids
            rndSize = random.randrange(30, 55)
            rndRot = random.randrange(0, 3)
            rndRot = rndRot * 90
            asteroid = Asteroid(1.0, 1, asteroidImg3, rndSize, rndRot, random.randrange(20, (SCREEN_WIDTH - 60)), random.randrange(rndRangeY, -200))
            asteroid_list.add(asteroid)
            
        for i in range(int(qty * 0.2)):#Aliens 
            asteroid = Asteroid(1.5, 4, alienImg1, 50, 0, random.randrange(50, (SCREEN_WIDTH - 90)), random.randrange(rndRangeY, -200))
            asteroid_list.add(asteroid)
            
    elif (imgSelect == 2):#Aliens only
        for i in range(int(qty * 0.5)):
            asteroid = Asteroid(1.0, 4, alienImg1, 50, 0, random.randrange(50, (SCREEN_WIDTH - 90)), random.randrange(rndRangeY, -200))
            asteroid_list.add(asteroid)

    else:#Atreroids only random sizes
        
        for i in range(qty):
            rndSize = random.randrange(30, 55)
            rndRot = random.randrange(0, 3)
            rndRot = rndRot * 90
            asteroid = Asteroid(1.0, 1, asteroidImg3, rndSize, rndRot, random.randrange(20, (SCREEN_WIDTH - 60)), random.randrange(rndRangeY, -200))
            asteroid_list.add(asteroid)
              
#Create UFO  
def CreateUfo(spd, x, y):
    
    ufo = Ufo(spd, x, y)
    ufo_list.add(ufo)    


def CreateUfos(type):
    
    global ufosToShoot
    ufosToShoot = 0      

    if (type == 0):
        CreateUfo(2, -350, 30)
    elif (type == 1):
        CreateUfo(-2, offsetX + 1150, 30)
    elif (type == 2):
        CreateUfo(2, -350, 30)
        CreateUfo(-2, offsetX + 1150, 30)
    elif (type == 5):
        ufosToShoot = 4  
        CreateUfo(5, -500, 50)
        CreateUfo(-5, offsetX + 1300, 50)
        CreateUfo(5, -350, 150)
        CreateUfo(-5, offsetX + 1150, 150) 
    elif (type == 10):
        ufosToShoot = 6
        CreateUfo(5, -500, 50)
        CreateUfo(-5, offsetX + 1175, 100)
        CreateUfo(5, -350, 150)
        CreateUfo(-5, offsetX + 1025, 200) 
        CreateUfo(5, -500, 250)
        CreateUfo(-5, offsetX + 1175, 300)
    else:
        ufosToShoot = 6
        CreateUfo(5, -350, 50)
        CreateUfo(5, -500, 100)
        CreateUfo(5, -350, 150)
        CreateUfo(5, -500, 200) 
        CreateUfo(5, -350, 250)
        CreateUfo(5, -500, 300)

#Create Shields
def CreateShields():
    
    global shieldLevel
    
    posYadder = shieldLevel * 30
    shield = [
    Shield(offsetX + 25, SCREEN_HEIGHT - 100 - posYadder, 100),
    Shield(offsetX + 175, SCREEN_HEIGHT - 130 - posYadder, 100),
    Shield(offsetX + 325, SCREEN_HEIGHT - 160 - posYadder, 100),
    Shield(offsetX + 475, SCREEN_HEIGHT - 130 - posYadder, 100),
    Shield(offsetX + 625, SCREEN_HEIGHT - 100 - posYadder, 100)
    ]
    shield_list.add(*shield)
 
    if (shieldLevel < 2):
        shieldLevel += 1
    else:
        shieldLevel = 0
        
#Create damage
def CreateDamage(posx, posy, vTime, num):
    
    global vibeTime
    
    damage = Damage(posx, posy, num)
    damage_list.add(damage)
    vibeTime = vTime
    
#Create explotion effect   
def CreateEffectsFX(posx, posy, size, mag, num):
    
    if (FX_LEVEL > 0):
        if (num == 3):
            PlaySound(6)
        else:
            if (mag >= 0):
                PlaySound(1)
            else:
                PlaySound(4)
        
    effectsFX = EffectsFX(posx, posy, size, mag, num)  
    effectsFX_list.add(effectsFX)

        
#Write all the game settings        
def WriteFile(content):
    
    try:
        f = open('settings15.txt', "w")
        f.write(content)#\n
        f.close()
         
    except IOError:
        print('Could not create a file!')


#Read and load all the game settings        
def ReadFile():

    try:    
        f = open('settings15.txt', "r")
        if f.mode == 'r':
            objFile = f.read()                  
            f.close()
            ParseData(objFile)
            SetMenu(0)
    except:#If no file create it
        #print('Could not Find File!')
        SetDefaults()

def ParseData(strMain):#Parse data load the settings

    global IMG_NO
    global settList
    global nameList
    global strName0
    global FX_LEVEL
    global TX_LEVEL
    global TX_MODE
    global TrackNo

    FX_LEVEL = 0
    TX_LEVEL = 0
    TX_MODE = 0
    TrackNo = 0
    
    try:
        listMain = strMain.split('~')
        
        settList.clear()
        for i in range(0, 7, 1):
            settList.append(int(listMain[i]))
        #Set the screen & sound
        SetScreen(settList[0], settList[1])
        SetSndFx(settList[2])
        IMG_NO = settList[3]
        SetSndTx(settList[4])
        TX_MODE = settList[5]
        TrackNo = settList[6]
        nameList.clear()
        for i in range(7, 12, 1):
            subStr = listMain[i]
            subList = subStr.split('|')
            nameList.append([subList[0], int(subList[1])])
            
        strName0 = listMain[12]
        listMain.clear()

    except:
        print('Could not Parse Data!')

    UpdateRank(0)
    UpdateTxList()
    
    if (TX_MODE > 0 and len(sndTrxList) != 0):
        PlaySndTrx(TrackNo, TX_MODE)
    
    if (useJoystick):
        InitJoysticks()
        

def PlaySound(num):
    
    #Default 8 channels 0-7   
    if (num == 0):#Laser sound
        pygame.mixer.Channel(0).play(laserSnd)
    elif (num == 1):#Explod sound
        pygame.mixer.Channel(1).play(explodSnd)
    elif (num == 2):#Button sound
        pygame.mixer.Channel(2).play(btnSnd)
    elif (num == 3):#Buzzer sound
        pygame.mixer.Channel(3).play(buzzSnd)
    elif (num == 4):#Power Down sound
        pygame.mixer.Channel(4).play(pwrDnSnd)
    elif (num == 5):#Power Up Sound
        pygame.mixer.Channel(4).play(pwrUpSnd)
    elif (num == 6):#Bug drill sound
        pygame.mixer.Channel(2).play(drillSnd)
    elif (num == 7):#Bug UFO hit sound
        pygame.mixer.Channel(2).play(hitSnd)
    elif (num == 8):#Fx Sound 
        pygame.mixer.Channel(2).play(fx1Snd)
    else:
        pygame.mixer.Channel(2).play(fx1Snd)
        #print('ERROR_:_Out_Of_Range_:_PlaySound!')


def PlaySndTrx(num, mode):
    
    global TrackNo
    global TX_MODE
    
    if (len(sndTrxList) != 0):      
        try:
            if (mode == 0):#Stop song
                TX_MODE = 0
                pygame.mixer.music.stop()
            elif (mode == 1):#Play song from start
                TX_MODE = 1
                pygame.mixer.music.stop()
                soundTrk = pygame.mixer.music.load(sndTrxList[num])
                pygame.mixer.music.play()
            elif (mode == 2):#Loop one song
                pygame.mixer.music.stop()
                soundTrk = pygame.mixer.music.load(sndTrxList[num])
                pygame.mixer.music.play(-1)
            elif (mode == 3):#Pause song
                pygame.mixer.music.pause()
            elif (mode == 4):
                pygame.mixer.music.unpause()
            elif (mode == 5):#Play next song
                pygame.mixer.music.stop()
                if (len(sndTrxList)- 1 > TrackNo):
                    TrackNo += 1
                else:
                    TrackNo = 0
                soundTrk = pygame.mixer.music.load(sndTrxList[TrackNo])
                pygame.mixer.music.play()
            elif (mode == 6):#play prev song
                pygame.mixer.music.stop()
                if (TrackNo > 0):
                    TrackNo -= 1
                else:
                    TrackNo = len(sndTrxList)- 1
                soundTrk = pygame.mixer.music.load(sndTrxList[TrackNo])
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.stop()
                
        except:
            print('ERROR_:_PlaySound_:_Could not load soundtrack')


    if (MENU_NO == 1):
        SetMenu(0)
        
 
def SetDefaults():#Load default settings
    
    ParseData(('0~0~3~0~3~1~0~Pi_5.........|100~Pi_4.........|200~Pi_3.........|300~Pi_2.........|400~Pi_1.........|500~' + strName0))
    SetMenu(6)
 
def SetScreen(resValue, fullScr):

    global SCR_RES
    global SCR_FULL
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global posX
    global posY
    global towerPosY
    global jsx
    global jsy
    global offsetX
    
    SCR_RES = resValue
    SCR_FULL = fullScr

    SCREEN_WIDTH = RES_LIST[SCR_RES][0]
    SCREEN_HEIGHT = RES_LIST[SCR_RES][1]
        
    jsx = int(SCREEN_WIDTH / 2)
    jsy = int(SCREEN_HEIGHT / 2)
    offsetX = int(-(800 - SCREEN_WIDTH) * 0.5)
    
    if (fullScr == 1):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN, 16)  
    else:      
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF, 16)

    #Set the position of the player
    posX = SCREEN_WIDTH / 2 
    posY = SCREEN_HEIGHT - 20
    towerPosY = SCREEN_HEIGHT - 210
    SetMenu(0)
    pygame.mouse.set_pos(offsetX + 242, 400)


def SetSndFx(value):
    
    global FX_LEVEL

    FX_LEVEL += value
    
    if (FX_LEVEL < 0):
        FX_LEVEL = 0
    elif (FX_LEVEL > 10):
        FX_LEVEL = 10
    try:# Set sound effect volume
        explodSnd.set_volume(FX_LEVEL * 0.025)#
        laserSnd.set_volume(FX_LEVEL * 0.05)#
        btnSnd.set_volume(FX_LEVEL * 0.09)#
        buzzSnd.set_volume(FX_LEVEL * 0.1)#
        pwrDnSnd.set_volume(FX_LEVEL * 0.04)#
        pwrUpSnd.set_volume(FX_LEVEL * 0.04)#
        drillSnd.set_volume(FX_LEVEL * 0.04)#
        hitSnd.set_volume(FX_LEVEL * 0.03)#
    except:
        print('ERROR_:_SetSndFx')

    SetMenu(0)
    

def SetSndTx(value):
    
    global TX_LEVEL 

    TX_LEVEL += value
    
    if (TX_LEVEL < 0):
        TX_LEVEL = 0
    elif (TX_LEVEL > 10):
        TX_LEVEL = 10
        
    try:
        #print('Track volum level', TX_LEVEL)
        pygame.mixer.music.set_volume(TX_LEVEL * 0.05)
       
    except:
        print('ERROR_:_SetSndTx Set Volume!')
    
    SetMenu(0)
    

def SetMenu(value):

    global MENU_NO
    global strMsg1
    
    MENU_NO += value   
    
    if (MENU_NO < 0):
        MENU_NO = 9
    elif (MENU_NO > 9):
        MENU_NO = 0    
    #print (value, MENU_NO)
    if MENU_NO == 0:   
        strMsg1 = mySelFont.render('START GAME:', True, WHITE)#
        
    elif MENU_NO == 1:
        if (len(sndTrxList) > 0):
            strMsg1 = mySelFont.render((sndTrxList[TrackNo])[6:28], True, YELLOW)#
        else:
            strMsg1 = mySelFont.render('NO SOUND TRACK:', True, RED)#
        
    elif MENU_NO == 2:
        strMsg1 = mySelFont.render('SOUND TX LEVEL: %s' %(TX_LEVEL * 10), True, GREEN)#Sound track level
    elif MENU_NO == 3:
        strMsg1 = mySelFont.render('SOUND FX LEVEL: %s' %(FX_LEVEL * 10), True, GREEN)#Fx Sound level
    elif MENU_NO == 4:
        strMsg1 = mySelFont.render(('RESOLUTION: ' + str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT)), True, YELLOW)#
    elif MENU_NO == 5:
        if SCR_FULL == 1:
            strMsg1 = mySelFont.render('FULL SCREEN: OFF', True, GREEN)#
        else:
            strMsg1 = mySelFont.render('FULL SCREEN: ON', True, YELLOW)#
    elif MENU_NO == 6:   
        strMsg1 = mySelFont.render('HELP SCREEN:', True, GREEN)#
        SetText(0)

    elif MENU_NO == 7:
        strMsg1 = mySelFont.render('HALL OF FAME:', True, BLUE)#
        SetText(1)
 
    elif MENU_NO == 8:
        strMsg1 = mySelFont.render('CREDITS:', True, YELLOW)#
        SetText(3) 
 
    elif MENU_NO == 9:     
        strMsg1 = mySelFont.render('QUIT:', True, RED)#
        

def EditName(num0, num1):
    
    global nameList
    global strName0
    global strMsg1
    global numIndex
    global editName
    
    char = charList[numIndex]
    listLen = len(charList) - 1
 
    if (num1 == 0):#Scroll up and down through the alphabet and numbers

        if (len(strName0) < 13):
            
            numIndex += num0
            
            if (numIndex < 0):
                numIndex = listLen
            elif (numIndex > listLen):
                numIndex = 0
            
            char = charList[numIndex]
        else:
            char = charList[0]

    elif (num1 == 1):#Add Selected char

        if (len(strName0) < 13):
            strName0 += char
        
        numIndex = 0
        char = charList[numIndex]
        
    elif (num1 == 2):
        
        if (len(strName0)>0):
            strName0 = strName0[:-1]
            
        numIndex = 0
        char = charList[numIndex]
        
    elif (num1 == 3):#Save and Exit

        i = 0
        s = 0
        search = '..***~~~***..'
        
        try:
            for sublist in nameList:
                if (sublist[0] == search):
                    s = sublist[1]
                    nameList.pop(i)
                    break
                i += 1
                
            for l in range(13 - len(strName0)):
                strName0 += '.'
                
            nameList.insert(i, [strName0, s])
                
        except:#print('COULD NOT EDIT NAME!')
            strMsg1 = myHudFont.render('COULD NOT EDIT NAME!', True, RED)
           
        numIndex = 0
        UpdateRank(0)
        SetText(1)
        editName = False

    else:
        print('Out Of Range!')
    
    if (editName):  
        strMsg1 = myHudFont.render('EDIT NAME: ' + strName0 + '[' + char + ']', True, RED)
    else:
        SetMenu(0)
        

def UpdateRank(score0):

    global strName1
    global strName2
    global strName3
    global strName4 
    global strName5
    
    global score1 
    global score2 
    global score3 
    global score4 
    global score5
    global hiScore
    
    global editName    
    global nameList

    search = '..***~~~***..'
    
    try:#Update Rankings
        nameList.append([search, score0])
        nameList.sort(key = lambda nameList: nameList[1])
        
        strName1 = nameList[1][0]
        strName2 = nameList[2][0]
        strName3 = nameList[3][0]
        strName4 = nameList[4][0]
        strName5 = nameList[5][0]

        score1 = nameList[1][1]
        score2 = nameList[2][1]
        score3 = nameList[3][1]
        score4 = nameList[4][1]
        score5 = nameList[5][1]
               
        hiScore = score5
        
    except:
        print('Could not Update Rank!')

    if (nameList[0][0] != search):
        SetMenu(7)       
        editName = True
        EditName(0, 0)
        SetText(2)

    nameList.remove(nameList[0])

            
def SetText(num):

    global strLine0
    global strLine1
    global strLine2
    global strLine3
    global strLine4   
    global strLine5
    global strLine6

    try:
        if (num == 0):#Mouse help screen    
    
            strLine0 = '_________***HELP-SCREEN***_________'
            
            if (InputNo == 0):#Mouse
                strLine1 = 'MOUSE-MOVE TO AIM'
                strLine2 = 'LEFT CLICK-ENTER OR FIRE OR DOWN'
                strLine3 = 'RIGHT CLICK-BACK OR PAUSE OR UP'
                strLine4 = 'MIDDLE CLICK-SELECT OR SCREENSHOT'
                strLine5 = 'WHEEL-SCROLL UP OR DOWN MENU'
            else:#Joystick help screen
                strLine1 = 'USE ANALOGUE STICK-MOVE TO AIM'
                strLine2 = 'BUTTON A/1-ENTER OR FIRE OR DOWN'
                strLine3 = 'BUTTON Y/4-BACK OR PAUSE OR UP'
                strLine4 = 'BUTTON RB/6-SELECT OR SCREENSHOT'
                strLine5 = 'X/3 & B/2-SCROLL MENU LEFT/RIGHT'
            
            strLine6 = '__________________________HAVE FUN!'             
            
            
        elif (num == 1):#Hall of fame
        
            strLine0 = '_________***HALL-OF-FAME***________'
            strLine1 = 'RANK_1 : ' + strName5 + ' : ' + str(score5)
            strLine2 = 'RANK_2 : ' + strName4 + ' : ' + str(score4)
            strLine3 = 'RANK_3 : ' + strName3 + ' : ' + str(score3)
            strLine4 = 'RANK_4 : ' + strName2 + ' : ' + str(score2)
            strLine5 = 'RANK_5 : ' + strName1 + ' : ' + str(score1)            
            strLine6 = '_______________________________END.'

        elif (num == 2):#Help screen (Edit hall of fame)
            
            strLine0 = '_________***HALL-OF-FAME***________'
            strLine1 = '1.TO_EDIT_THE_NAME'
            
            if (InputNo == 0):#Mouse
                strLine2 = '2.USE_RMB_TO_DELETE_'
                strLine3 = '3.USE_MOUSE_WHEEL_TO_SCROLL'
                strLine4 = '4.USE_CMB_TO_SELECT_CHARACTER'
                strLine5 = '5.USE_LMB_SAVE_AND_EXIT'                
                strLine6 = 'LMB=SAVE_:_CMB=SELECT_:_RMB=DEL'
            else:#Joystick
                strLine2 = '2.USE_Y_TO_DELETE_'
                strLine3 = '3.USE_X_&_B_TO_SCROLL'
                strLine4 = '4.USE_RB_TO_SELECT_CHARACTER'
                strLine5 = '5.USE_A_SAVE_AND_EXIT'                
                strLine6 = 'A=SAVE_:_RB=SELECT_:_Y=DEL'
                
        elif (num == 3):#Credit Screen

            strLine0 = '___________***CREDITS***___________'
            strLine1 = 'SPECTIAL THANKS TO:'
            strLine2 = 'CODE:PYTHON_&_PYGAME'
            strLine3 = 'SOUND:AUDACITY_&_LMMS'
            strLine4 = 'GRAPHICS:GIMP_&_BLENDER'
            strLine5 = 'AND THE OPEN-SOURCE COMMUNITY.'                
            strLine6 = '_______________________________END.'

        strLine0 = myHudFont.render(strLine0, True, BLUE)#
        strLine1 = myHudFont.render(strLine1, True, WHITE)
        strLine2 = myHudFont.render(strLine2, True, WHITE)
        strLine3 = myHudFont.render(strLine3, True, WHITE)
        strLine4 = myHudFont.render(strLine4, True, WHITE)
        strLine5 = myHudFont.render(strLine5, True, WHITE)
        strLine6 = myHudFont.render(strLine6, True, RED)            
                
    except:
        print('Could not set text!')
        
           
def ResetGame():# Reset all game values

    global health 
    global oldHealth 
    global bombCount
    global shieldLevel
    global score
    global rank
    global rndRangeY
    global pauseGame
    global levelNo
    global endGame
    global vibeTime
    global towerPosY
    global playBuzz 
    
    UpdateRank(score)
    score = 0
    pauseGame = False
    endGame = False
    playBuzz = True
    health = 0
    oldHealth = 0
    bombCount = 0
    shieldLevel = 0   
    rank = 0
    rndRangeY = -400
    RemoveSprites()
    levelNo = 0
    vibeTime = 0
    towerPosY = SCREEN_HEIGHT - 210
    pygame.mouse.set_pos(242, 400)
       
def RemoveSprites():

    for damage in damage_list:
        damage_list.remove(damage)
    for laser in laser_list:
        laser_list.remove(laser)
    for asteroid in asteroid_list:
        asteroid_list.remove(asteroid)
    for ufo in ufo_list:
        ufo_list.remove(ufo)
    for shield in shield_list:
        shield_list.remove(shield)
    for effectsFX in effectsFX_list:
        effectsFX_list.remove(EffectsFX)
        
def NewLevel():

    global levelNo 
    global rndRangeY 
    global loopCount
    global strMsg
    global health
    global oldHealth
    global rank
    global bonusPoints
    global score
    global bonusPoints
    global imgSelect

    levelNo += 1
    rndRangeY -= 50
    loopCount = -50
    
    if (levelNo % 5 == 0):
        bonusPoints = 50
        CreateUfos(levelNo)
        strMsg = myMsgFont.render('BONUS UFOs', True, RED)
        
        if (levelNo == 5):
            imgSelect = 1#Aliens and asteroids
        else:
            imgSelect = 2#Aliens only
    else:
        #imgSelect = 2#Remove this code later Aliens only
        CreateAsteroids()
        imgSelect = 0#Reset for next level Asteroids only
    
        if (bonusPoints == 0):
            if (health == oldHealth):
                rank += 1
                strMsg = myMsgFont.render(' PERFECT!', True, BLUE)           
            else:
                strMsg = myMsgFont.render('GET READY!', True, YELLOW)
        else:
            if (ufosToShoot == 0):
                bonusPoints = bonusPoints * 2
                strMsg = myMsgFont.render('***' + str(bonusPoints) + '***', True, RED)
            else:
                strMsg = myMsgFont.render('***' + str(bonusPoints) + '***', True, YELLOW)

        if (levelNo % 2 == 0):
            rndUfo = random.randrange(0,2)
            CreateUfos(rndUfo)
    
    score += bonusPoints
    oldHealth = health
    bonusPoints = 0
        
def GameOver():
    
    global strMsg
    global endGame
    global loopCount

    endGame = True
    loopCount = -200
    strMsg = myMsgFont.render('GAME OVER!', True, RED)

    for i in range(30):
        x = random.randrange(0, 760)
        y = random.randrange(15, 50)
        CreateDamage(x, SCREEN_HEIGHT - y, 150, 0)
        
    effectsFX = [
    EffectsFX(0, SCREEN_HEIGHT - 50, 50, 4, 0),
    EffectsFX(125, SCREEN_HEIGHT - 50, 50, 5, 0),
    EffectsFX(250, SCREEN_HEIGHT - 50, 50, 6, 0),
    EffectsFX(375, SCREEN_HEIGHT - 50, 50, 6, 0),
    EffectsFX(500, SCREEN_HEIGHT - 50, 50, 5, 0),
    EffectsFX(625, SCREEN_HEIGHT - 50, 50, 6, 0)
    ]
    effectsFX_list.add(*effectsFX)

    if FX_LEVEL  > 0:
        PlaySound(1)

def ScreenShot():
    
    global IMG_NO
    global strMsg1
    
    if (1==1):#Save to desktop
        fileName = ('/home/pi/Desktop/Pi-Luna_Base_51-' + str(IMG_NO) + '-.png')
    else:
        fileName = ('scrShot-' + str(IMG_NO) + '-.png')
        
    pygame.image.save(screen, fileName)
    strMsg1 = myHudFont.render('SCREENSHOT TAKEN! :', True, YELLOW)
    IMG_NO += 1

def SaveGame():
    
    global nameList
    
    if (editName):
        EditName(0, 3)
        
    try:
        content = (str(SCR_RES) + '~' + str(SCR_FULL) + '~' + str(FX_LEVEL) + '~' + str(IMG_NO) + '~' + str(TX_LEVEL) + '~' + str(TX_MODE) + '~' + str(TrackNo))
    
        for sublist in nameList:
            sub0 = sublist[0]
            sub1 = str(sublist[1])
            content += '~' + sub0 + '|' + sub1
        
        content += '~' + strName0
        WriteFile(content)
    except:
        print('Could not save game settings!')
                
def BtnLeft():#Update Inter and or Fire btn

    global MENU_NO
    global levelNo
    global strMsg
    global pauseGame
    global health
    global SCR_FULL
    global SCR_RES
    global FX_LEVEL
    global done
     
    if (MENU_NO == 0 and endGame == False):
        if (health > 0):
            if (loopCount == 0):
                player.fireLaser()
            pauseGame = False
            PlaySndTrx(0, 4)
        else:
            if (levelNo > 0):
                ResetGame()
            else:
                health = 100
                pygame.mouse.set_pos(int(SCREEN_WIDTH / 2), 300)

    elif (MENU_NO == 1):
        PlaySndTrx(TrackNo, 1)
        
    elif (MENU_NO == 2):
        SetSndTx(-1)

    elif (MENU_NO == 3):       
        SetSndFx(-1)
        PlaySound(0)
        
    elif (MENU_NO == 4):
        if (SCR_RES < 3):
            SCR_RES += 1
        else:
            SCR_RES = 0
            
        SetScreen(SCR_RES, SCR_FULL)
        
    elif (MENU_NO == 5):
        if (SCR_FULL == 1):
            SCR_FULL = 0
        else:
            SCR_FULL = 1
        SetScreen(SCR_RES, SCR_FULL)        
        
    elif (MENU_NO == 6):
        SetMenu(-6)
        
    elif (MENU_NO == 7):
        
        if (editName):
            EditName(0, 3)
        else:
            SetMenu(-7)
            
    elif (MENU_NO == 8):
        SetMenu(-8)
        
    elif (MENU_NO == 9):
        done = True
        
def BtnCenter():
    
    global pauseGame
    global TrackNo
    
    if (MENU_NO == 0 and endGame == False):
        ScreenShot()
    else:
        
        if (editName):
            PlaySound(2)
            EditName(0, 1)
            
        elif(MENU_NO == 1):           
            if (len(sndTrxList)- 1 > TrackNo):
                TrackNo += 1
            else:
                TrackNo = 0
            SetMenu(0)
            
        else:
            ScreenShot()
 
 
def BtnRight():#Update return or back

    global levelNo
    global pauseGame
    global strMsg
    global health
    global done

    if (levelNo > 0):
        if (pauseGame == False and health > 0):
            pauseGame = True
            PlaySndTrx(0, 3)
            strMsg = myMsgFont.render('  PAUSED', True, GREEN)
        else:
            ResetGame()            
    else:
        
        if (MENU_NO == 1):
            #print('Play-Stop')
            PlaySndTrx(0, 0)
            
        elif (MENU_NO == 2):
            SetSndTx(1)
            
        elif (MENU_NO == 3):
            SetSndFx(1)
            PlaySound(0)
            
        elif (MENU_NO == 4):
            SetMenu(-4)          
            
        if (MENU_NO == 5):
            SetMenu(-5)
            
        elif (MENU_NO == 6):
            SetMenu(-6)
        
        elif (MENU_NO == 7):
            if (editName):
                EditName(0, 2)
            else:
                SetMenu(-7)
                
        elif (MENU_NO == 8):
            SetMenu(-8)
            
        elif (MENU_NO == 9):
            done = True

def BtnUp():#Up btn
    
    if (testMode and levelNo != 0):
        CreateShields()

    if (editName):
        EditName(1, 0)
    else:
        if (levelNo == 0):
            PlaySound(2)
            SetMenu(1)
               
def BtnDown():#Down btn
    
    if (testMode and levelNo != 0):    
        CreateUfo(2, -350, 30)

    if (editName):
        EditName(-1, 0)
    else:
        if (levelNo == 0):
            PlaySound(2)
            SetMenu(-1)
            
def UpdateTxList():
    
    global sndTrxList
    
    sndTrxList.clear()
    trxList = glob.glob('Music/*')
    
    for i in range(0, len(trxList), 1):#Filter ogg/wav/mp3
        if (trxList[i][-4:] == '.ogg' or trxList[i][-4:] == '.wav' or trxList[i][-4:] == '.mp3'):
            sndTrxList.append(trxList[i])
    #print(sndTrxList)
            
          
def UpdateMouse():    #Handel input **Mouse** or **RAT**

    global posx
    global posy
    global done
    
    for event in pygame.event.get():
        
        pos = pygame.mouse.get_pos()
        posx = pos[0]
        posy = pos[1]#
        
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:#Left click
                BtnLeft()
                    
            elif event.button == MIDDLE:# Middle click 
                BtnCenter()

            elif event.button == RIGHT:#Right click
                BtnRight()

            elif event.button == UP:# Wheel Up 
                BtnUp()
                
            elif event.button == DOWN:# Wheel Down
                BtnDown()

        if event.type == sndTrxEnd:
            PlaySndTrx(TrackNo, 6)#5=Next 6=prev
        
def InitJoysticks():
    
    global InputNo
    global joystick
    
    JS_COUNT = pygame.joystick.get_count()

    if (JS_COUNT == 0):#Use mouse
        InputNo = 0
    else:#Use Joystick
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        name = joystick.get_name()
        id = joystick.get_id()
        #print('Name:', name,'ID:', str(id))
        axesCount = joystick.get_numaxes()
        btnCount = joystick.get_numbuttons()
        hatCount = joystick.get_numhats()
        #print(axesCount, btnCount, hatCount)
        if (axesCount >= 2 and btnCount >= 8 and hatCount >= 1):#Other joystick
            InputNo = 1
            #print('Using number 1')
        else:
            InputNo = 0
            print('AxesCount', axesCount, 'btnCount', BtnCount, 'HatCount', hatCount)
            print("Sorry you must use a mouse!")


def UpdateJs1():

    global posx
    global posy
    global done
    global pauseGame
    global InputNo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        axis0 = round(joystick.get_axis(0),2)#LAX
        axis1 = round(joystick.get_axis(1),2)#LAY

        if event.type == pygame.JOYBUTTONDOWN:

            button0 = joystick.get_button(0)#js-A
            button1 = joystick.get_button(1)#js-B
            button2 = joystick.get_button(2)#js-X
            button3 = joystick.get_button(3)#js-Y
            button4 = joystick.get_button(4)#js-LB
            button5 = joystick.get_button(5)#js-RB
            button6 = joystick.get_button(6)#js-Back
            button7 = joystick.get_button(7)#js-Start

            if(button0 == 1):#print('js-A')
                BtnLeft()
            elif(button1 == 1): #print('js-B')
                BtnUp()
            elif(button2 == 1):#print('js-X')
                BtnDown()
            elif(button3 == 1):#print('js-Y')
                BtnRight()
            elif(button4 == 1):#print('js-LB')
                pass                    
            elif(button5 == 1):#print('js-RB')
               BtnCenter()
            elif(button6 == 1):#print('js-Back')
                BtnRight()
            elif (button7 == 1):#print('js-Start')
                SetMenu(10)
                BtnLeft()
            
        posx = int((axis0 * jsx) + jsx)
        posy = int((axis1 * jsx) + jsy)
        
        if (posy < 0):
            posy = 0
        elif (posy > SCREEN_HEIGHT):
            posy = SCREEN_HEIGHT   
            
        if event.type == sndTrxEnd:
            PlaySndTrx(TrackNo, 5)#5=Next 6=prev
            
            
def UpdateGame():#check for collitions
    
    
    for laser in laser_list:
        
        laser_hit_list = pygame.sprite.spritecollide(laser, asteroid_list, False, pygame.sprite.collide_circle)  
            
        for asteroid in laser_hit_list:
            laser.takeHit()
            asteroid.takeHit()
            
        ufo_hit_list = pygame.sprite.spritecollide(laser, ufo_list, False)
        
        for ufo in ufo_hit_list:
            laser.takeHit()
            ufo.takeHit()

    for shield in shield_list:
        
        shield_hit_list = pygame.sprite.spritecollide(shield, asteroid_list, False) 
        
        for asteroid in shield_hit_list:
            shield.takeHit(asteroid.type)
            asteroid.removeMe()   
            
            
def DrawScreen():#___________________RENDERING________________

    global towerPosY
    global vibePosX
    
    screen.fill((0, 0, 0))
    screen.blit(bgImg, (offsetX, 0))
    
    if(vibePosX == 0 and endGame != True):
        screen.blit(tower0Img, (offsetX + 610 + vibePosX , towerPosY))
    else:
        screen.blit(tower1Img, (offsetX + 610 + vibePosX , towerPosY))
        if (health <= 0):
            towerPosY += 1
    screen.blit(baseImg, (offsetX + vibePosX, SCREEN_HEIGHT - 71))
    laser_list.draw(screen)
    player_list.draw(screen)
    shield_list.draw(screen)
    screen.blit(coverImg, (offsetX + 338 + vibePosX, SCREEN_HEIGHT - 28))
    damage_list.draw(screen)
    asteroid_list.draw(screen)
    ufo_list.draw(screen)
    effectsFX_list.draw(screen)
       
    if (levelNo > 0):        
        hudScore = myHudFont.render('SCORE:%s' % score, True, BLUE )#score
        hudHealth = myHudFont.render('POWER:%s'% health, True, BR_COLOR)#health
        hudLevel = myHudFont.render('LEVEL:%s'% levelNo, True, BLUE)#Level
        hudHiScore = myHudFont.render('HI-SCORE:%s' % hiScore, True, BLUE)#hi score
        hudRank = myHudFont.render('RANK:%s'% rank, True, BLUE)#strFPS
        #Draw the HUD
        screen.blit(hudScore, (10, 10))
        screen.blit(hudHealth, (180, 10))
        screen.blit(hudLevel, (360, 10))#560
        screen.blit(hudHiScore, (480, 10))
        screen.blit(hudRank, (700, 10))
        if (showMsg or pauseGame):
            screen.blit(strMsg, (offsetX + 175, 200))#140, 200          
    else:
        screen.blit(underLayImg, (offsetX + 185, 30))
      
        if (InputNo == 0):
            screen.blit(mouseIcn1Img, (offsetX + 188, 304))#195
        else:
            screen.blit(jsIcn1Img, (offsetX + 188, 304))
            
        if (MENU_NO == 6 or MENU_NO == 7 or MENU_NO == 8):#Hall of Fame, Help Screen, Credits
            
            screen.blit(overLayImg, (offsetX + 185, 30))
            
            screen.blit(strLine0, (offsetX + 205, 55))
            screen.blit(strLine1, (offsetX + 205, 85))
            screen.blit(strLine2, (offsetX + 205, 115))
            screen.blit(strLine3, (offsetX + 205, 145))
            screen.blit(strLine4, (offsetX + 205, 175))
            screen.blit(strLine5, (offsetX + 205, 205))
            screen.blit(strLine6, (offsetX + 205, 235))
            
        screen.blit(strMsg1, (offsetX + 290, 386))
        screen.blit(startImg, (offsetX + 100, 10))
    
    if (testMode):
        # String Info text
        strFPS = str(round(clock.get_fps(),2))
        #List of stuff to test -rank ranking vibePosX vibeTime endGame loopCount bonusPoints str(len(asteroid_list)) imgSelect-
        strInfo = myHudFont.render('Info: %s' % strFPS, True, YELLOW )#score editName
        screen.blit(strInfo, (offsetX + 20, 30))
    
    screen.blit(crossHairImg, (posx - 15, posy - 15))

     
ReadFile()#Read and load the game settings    
    
while not done:#____________________The Main game loop___________________


    if (InputNo == 0):
        UpdateMouse()        
    else:
        UpdateJs1()

    UpdateGame()

    if (health > 0):#Game Logik
        
        if (len(asteroid_list) == 0  and len(ufo_list) == 0):#Move to next level
            NewLevel()
            
        if (hiScore < score):
            hiScore = score

        if (loopCount < 0):
            loopCount += 1
            showMsg = True
        else:
            showMsg = False    
    else:        
        
        if (levelNo != 0):
            
            if (endGame == False):
                GameOver()
                loopCount = -200

            if (loopCount < 0):
                loopCount += 1
                showMsg = True
            else:
                showMsg = False
                
                ResetGame()      

    if (pauseGame == False):#Update all the sprites if not paused
        asteroid_list.update()
        laser_list.update()    
        player_list.update()
        effectsFX_list.update()
        ufo_list.update()
        damage_list.update()
        
        if (vibeTime > 0):
            if (vibeTime % 2 == 0):
                vibePosX = 1
            else:
                vibePosX = -1
            vibeTime -= 1
        else:
            vibePosX = 0

        if (health <= 0):
            health = 0
            BR_COLOR = RED
        elif (health < 50):
            changeCol += 1
            if (changeCol < 30):
                BR_COLOR = RED
            elif (changeCol < 60):
                BR_COLOR = YELLOW
            else:
                PlaySound(3)
                changeCol = 0       
        else:
            BR_COLOR = BLUE
        
    DrawScreen()
    
    pygame.display.flip()
    clock.tick(30)#FPS
    
#__________________EXIT_THE_GAME____________
    
SaveGame()#Save the game settings
pygame.quit()
sys.exit()

#Still_To_Do_List!
#Find and Fix Buggs
