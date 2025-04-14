import random
import pygame
import sys
import os
import asyncio

heroSpells = []
devilSpells = []
allSpells = [0,1,2,3,4,5,6,7,8,9]
heroHealth = 100
devilHealth = 100
isHeroCursed = False
isDevilCursed = False
isHeroProtected = False
isDevilProtected = False
devilsProbability = []
reviveChancesHero = 3
reviveChancesDevil = 3
isPossesed = False
isFinisherUsed = False
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()
pygame.mixer.music.load("music/background.ogg")
pygame.mixer.music.set_volume(0.008)
pygame.mixer.music.play(-1)
thunder_sound = pygame.mixer.Sound("music/thunder.ogg")
thunder_sound.set_volume(0.05)
curse_sound = pygame.mixer.Sound("music/curse.ogg")
curse_sound.set_volume(0.01)
basic_sound = pygame.mixer.Sound("music/basic.ogg")
basic_sound.set_volume(0.03)
screen_width = 800
w = 800
screen_height = 600
h = 600

GREY = (100,100,100)
GREEN = (0,255,0)
WHITE = (255, 255, 255)
black = (0, 0, 0)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Devils Zone")


action_book = []

def print_text(text,font,pos,color):
    screen.blit(pygame.font.Font(None,font).render(text,True,color),pos)

def handle_general_keys(keys):
    pass

def handle_general_events(event):
    global clicks
    if event.type == pygame.QUIT:
        pygame.quit()
        return True
    if event.type == pygame.KEYDOWN:
        clicks += 1
    return False

def load_image(path,size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image,size)

def load_image_colorkey(path,size,color):
    image = pygame.image.load(path).convert()
    image.set_colorkey(color)
    return pygame.transform.scale(image,size)


def print_Book(rect,book,color):
    for i in range(len(book)):
        if color != WHITE and i==0:
            print_text(book[i],30,(rect.left+10,rect.top+10+30*i),(0,0,255))
        else:
            print_text(book[i],30,(rect.left+10,rect.top+10+30*i),color)

intro_text = [
"You are hero Entered Devils Zone to defeat Devil",
"You can defeat devils using Spells",
"Spells you can cast using keys 0 to 9",
"Be careful while using Spells as you have only 6 Spells",
"Other 4 belong to Devil if you press them you will be in trouble"
]


first_scene_text = [
"You have seen the Devil",
"Devil has seen you",
"Use your spell click any number from 0 to 9"
]

spell_book = [
" Spells ",
" $ Basic Spell : 10 damage",
" $ Protect Spell : Protects from any attack",
" $ Curse Spell : Curses target, once cursed 10 damage per turn",
" $ Revelation Spell : Reveals all your hidden spells",
" $ Finisher Spell : 100 damage , Spells lost",
" $ Devils Possesion : You will become Devil , GAME OVER",
"   Click S to return"
]

rule_book = [
"Click on button 0-9 to use a spell",
"You aren't aware of which are your spells and which are Devil's Spells",
"Out of 10 , 6 spells are yours",
"4 Spells are Devils",
"You have 3 lives and Devil also has 3",
"Each life can take 100 damage",
"Click R to return"
]


game_over_book = []

background = pygame.image.load("images/background_cave.png")
background = pygame.transform.scale(background,(800,600))
shield = pygame.image.load("images/shield.png").convert()
shield.set_colorkey(WHITE)
shield = pygame.transform.scale(shield,(200,200))
basicAttack = load_image_colorkey("images/basic.png",(50,50),WHITE)
curse = load_image_colorkey("images/curse.png",(150,150),WHITE)
path_to_images = "images"
folder_path = "images/Thunder"
thunder = []
for i in range(len(os.listdir(folder_path))):
    fullpath = os.path.join(folder_path,str(i)+".png")
    thunder.append(load_image_colorkey(fullpath,(500,500),WHITE))


def initGame():
    global  game_over_book,gameOverBook,action_book,reviveChancesHero,reviveChancesDevil,spellBook,ruleBook,actionBook,attacks,finisherSpell
    reviveChancesHero = 3
    reviveChancesDevil = 3
    isPossesed = False
    clicks = 0
    spellBook = Book(spell_book)
    ruleBook = Book(rule_book)
    action_book = ["R : Rules , S : Spells , 0-9 : Spells", "[IMP] : Never Use Devil's Possession Spell"
                   ,"You don't know your spells and might use Devil's Spells by mistake"]
    actionBook = Book(action_book)
    attacks = Attacks()
    finisherSpell = FinisherSpell()
    game_over_book = []
    gameOverBook = Book(game_over_book,(screen_width,screen_height//2))
    initState()

def initState():
    global devilHealth,heroHealth,isHeroCursed,isDevilCursed,isHeroProtected,isDevilProtected,allSpells,heroSpells,devilSpells
    global devilsProbability,hero,devil
    devilsProbability = []
    devilHealth = 100
    heroHealth = 100
    isHeroCursed = False
    isDevilCursed = False
    isHeroProtected = False
    isDevilProtected = False
    heroSpells = []
    devilSpells = []
    allSpells = [0,1,2,3,4,5,6,7,8,9]
    while(len(heroSpells)<6):
        num = random.choice(allSpells)
        allSpells.remove(num)
        heroSpells.append(num)
    while(len(devilSpells)<4):
        num = random.choice(allSpells)
        allSpells.remove(num)
        devilSpells.append(num)
    for i in range(4):
        for j in range((3-i)*10):
            devilsProbability.append(devilSpells[i])
    devilsProbability.append(devilSpells[-1])
    if(isFinisherUsed):
        hero.spells = heroSpells
        devil.spells = devilSpells
    else:
        curse_sound.stop()
        hero = Player("Hero",heroSpells,load_image_colorkey("images/hero.png",(150,150),WHITE),(150,150),(150,400),reviveChancesHero)
        devil = Player("Devil",devilSpells,load_image_colorkey("images/devil.png",(150,150),WHITE),(150,150),(650,330),reviveChancesDevil)

def castSpell(h,d):
    global isFinisherUsed, isPossesed, heroHealth , devilHealth, isHeroProtected, isDevilProtected, isHeroCursed, isDevilCursed
    global action_book,devil,hero
    action_book = ["R : Rules , S : Spells , 0-9 : Spells"]
    spH=-1
    spD=-1
    try:
        spD = devilSpells.index(d)
        spH = heroSpells.index(h)
    except:
        action_book.append("You have chosen devils spell")
        if(spD < spH):
            spD = devilSpells.index(h)
            spH = -1
            action_book.append("Devil is happy with your decision and chose to take your advice")
        else:
            spH = -2
            action_book.append("But Devil is happy with his own decision")
    isHeroProtected = False
    isDevilProtected = False
    if(spD==1):
        #print_text("Devil Has used Protect Spell, with Probability : "+str(20/31),30,(100,250),black)
        isDevilProtected = True
        devil.protect(-1)
    if(spH==1):
        #print_text("You have used Protect Spell",30,(100,300),black)
        isHeroProtected = True
        hero.protect(1)
    if(spH == 0):
        hero.used_attack = "Basic Spell"
        #print_text("You have used Basic Spell",30,(100,250),black)
        if(isDevilProtected):
            pass
            #print_text("Your Spell has failed to damage the devil",30,(100,300),black)
        else:
            attacks.attackBySpell(hero.rect.center,devil.rect.center,10,basicAttack,screen,devil)
            #print_text("You have damaged the devil",30,(100,300),black)
    if(spD == 0):
        devil.used_attack = "Basic Spell"
        #print_text("Devil has used Basic Spell, with Probability : "+str(30/31),30,(100,250),black)
        if(isHeroProtected):
            pass
            #print_text("Devils Spell has failed to damage you",30,(100,300),black)
        else:
            attacks.attackBySpell(devil.rect.center,hero.rect.center,10,basicAttack,screen,hero)
            #print_text("Devil has damaged you",30,(100,300),black)
    if(spH==2):
        hero.used_attack = "Curse"
        #print_text("You have used Curse",30,(100,250),black)
        if(isDevilProtected):
            pass
            #print_text("Curse failed to damage the devil",30,(100,300),black)
        else:
            devil.attacked_by_curse()
            isDevilCursed = True
            #print_text("Devil is Cursed",30,(100,300),black)
    if(spD==2):
        devil.used_attack = "Curse"
        #print_text("Devil has used Curse , with Probability : "+str(10/31),30,(100,250),black)
        if(isHeroProtected):
            pass
            #print_text("Curse failed to damage you",30,(100,300),black)
        else:
            hero.attacked_by_curse()
            isHeroCursed = True
            #print_text("You are Cursed",30,(100,300),black)
    if(spH==3):
        #print_text("You have used Revelation",30,(100,250),black)
        action_book.append("Your Spells are revealed : "+str(heroSpells))
    if(spH==4):
        hero.used_attack = "Finisher"
        #print_text("You have used Finisher Spell",30,(100,250),black)
        #print_text("Due to using Finisher you have lost your memories",30,(100,300),black)
        if(isDevilProtected):
            pass
            #print_text("Finisher failed to damage the Devil",30,(100,400),black)
        else:
            isFinisherUsed = True
            action_book.append("You have forgotten your spells")
            finisherSpell.finisher(devil.rect.center,devil)
            #print_text("Devil has been Defeated",30,(100,400),black)
            actionBook.update_book(action_book)
            return
    if(spD==3):
        devil.used_attack = "Finisher"
        #print_text("Devil has used Finisher Spell, with Probability : "+str(1/31),30,(100,250),black)
        if(isHeroProtected):
            pass
            #print_text("Finisher failed to damage you",30,(100,300),black)
        else:
            finisherSpell.finisher(hero.rect.center,hero)
            #print_text("You have been Defeated",30,(100,300),black)
            action_book.append("You died couldn't use your attack")
            actionBook.update_book(action_book)
            return
    if(spH==5):
        action_book.append("You Used Devil Possesion Spell")
        hero.became_devil()
        action_book.append("You have became devil")
        action_book.append("Devil is laughing at you for falling into his trap")
        isPossesed = True
        actionBook.update_book(action_book)
        return
    if(isHeroCursed):
        curse_sound.play()
        hero.attacked_by_spell(10)
    if(isDevilCursed):
        devil.attacked_by_spell(10)

def devilsTalk():
        global action_book
        #print_text("Haha... a new Hero has appeared to concour the dungeon",30,(100,500),black)
        #print_text("On behalf of entertaining me I will tell you the Finisher Spell",30,(100,550),black)
        if hero.lives >= 0:
            devilsGuess = random.choice([heroSpells[-2],heroSpells[-1],heroSpells[-1]]) 
            action_book.append("Devil tells you to use this : "+str(devilsGuess))

def checkPlayerStatus():
    global hero,devil,status,game_over_book,gameOverBook,action_book
    if(status):
        return
    if(hero.health <= 0):
        if(hero.lives == 0):
            game_over_book.append("GAME OVER : You are defeated")
            game_over_book.append("")
            game_over_book.append("")
            game_over_book.append("Click on P to restart")
            #print_text("GAME OVER : You are defeated",30,(100,600),black)
            #print_text("Click on P to restart",30,(100,650),black)
            status = True
        elif(hero.lives > 0):
            action_book.append("You have lost a life")
            hero.died()
    if(devil.health <= 0):
        if(devil.lives == 0):
            game_over_book.append("Congratulations : You have Defeated the Devil")
            game_over_book.append("")
            game_over_book.append("")
            game_over_book.append("Click on P to restart")
            #print_text("Congratulations : You have Defeated the Devil",30,(100,600),black)
            #print_text("Click on P to restart",30,(100,700),black)
            status = True
        elif(devil.lives > 0):
            action_book.append("Devil has lost a life")
            devil.died()
    if(status):
        pass
            #gameOverBook.update_book(game_over_book)
            #gameOverBook.instantToggle()
            #pygame.display.update()

def spellCasted(sp):
    global count
    count = count + 1
    castSpell(sp,devil.random_attack())
    devilsTalk()
    checkPlayerStatus()
    actionBook.update_book(action_book)

class FinisherSpell(pygame.sprite.Sprite):
    def __init__(self):
        self.image = thunder[0];
        self.rect = self.image.get_rect()
        self.targetPos = (100,100)
        self.attack = False
        self.progress = 0
        self.damage_done = True
        self.player = 0

    def finisher(self,targetPos,player):
        self.image = thunder[0]
        self.progress = 0
        self.targetPos = targetPos
        self.rect.center = (self.targetPos[0]-0,self.targetPos[1]//2)
        self.attack = True
        self.damage_done = False
        self.player = player

    def update(self):
        global isFinisherUsed
        if(self.progress<7):
            self.image = thunder[self.progress%7]
            self.progress = self.progress + 1
            if(self.progress == 7):
                thunder_sound.play()
                if isFinisherUsed:
                    initState()
                    isFinisherUsed = False
        else:
            self.attack = False
            if not self.damage_done:
                self.damage_done = True
                self.player.attacked_by_spell(100)

    def draw(self,screen):
        if(self.attack):
            screen.blit(self.image,self.rect)


class Attacks(pygame.sprite.Sprite):
    def __init__(self):
        self.startPos = (100,100)
        self.endPos = (100,100)
        self.attack = False
        self.currentPos = (100,100)
        self.attackImg = basicAttack;
        self.rect = self.attackImg.get_rect();
        self.rect.center = self.rect.center;
        self.dx = 1
        self.dy = 1
        self.damage_done = True
        self.player = 0

    def attackBySpell(self,startPos,endPos,time,attackImg,screen,player):
        self.startPos = startPos
        self.currentPos = startPos
        self.endPos = endPos
        self.attackImg = attackImg
        self.rect = self.attackImg.get_rect()
        self.rect.center = self.currentPos
        self.attack = True
        self.player = player
        self.damage_done = False
        self.dx = (self.endPos[0] - self.startPos[0])//time
        self.dy = (self.endPos[1] - self.startPos[1])//time

    def update(self):
        if(self.dx>0 and (self.currentPos[0]<self.endPos[0] or self.currentPos[1]>self.endPos[1])):
            self.currentPos = (self.currentPos[0]+self.dx,self.currentPos[1]+self.dy)
            self.rect.center = self.currentPos
        elif(self.dx<0 and (self.currentPos[0]>self.endPos[0] or self.currentPos[1]<self.endPos[1])):
            self.currentPos = (self.currentPos[0]+self.dx,self.currentPos[1]+self.dy)
            self.rect.center = self.currentPos
        else:
            self.attack = False
            if( not self.damage_done):
                self.player.attacked_by_spell(10)
                self.damage_done = True
                basic_sound.play()


    def draw(self,screen):
        if(self.attack):
            screen.blit(self.attackImg,self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self,name,spells,image,size,center,lives):
        self.name = name
        self.fullHealth = 100
        self.health = 100
        self.lives = lives
        self.spells = spells
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.size = size
        self.angle = 0
        self.protected = False
        self.when = 1
        self.shield_rect = pygame.Rect(self.rect.right,self.rect.top-100,100,100)
        self.cursed = False
        self.cursed_img = curse
        self.cursed_rect = self.cursed_img.get_rect()
        self.used_attack = ""

    def random_attack(self):
        return random.choice(self.spells)

    def attacked_by_spell(self,damage):
        global status
        self.health -= damage
        #self.rotate(20)
        self.image = pygame.transform.flip(self.image,True,False)
        checkPlayerStatus()

    def became_devil(self):
        self.lives = 0
        self.health = 0
        self.used_attack = "Devils Possesion"

    def rotate(self,angle):
        self.angle = self.angle+angle
        self.image = pygame.transform.rotate(self.image,angle)
    
    def died(self):
        self.lives = self.lives-1
        self.health = self.fullHealth

    def attacked_by_curse(self):
        self.cursed = True
        self.cursed_rect = pygame.Rect(self.rect.left,self.rect.top+50,200,200)

    def protect(self,pos):
        self.used_attack = "Protect"
        self.protected = True
        self.when = pos
        if(pos == 1):
            self.shield_rect = pygame.Rect(self.rect.right-100,self.rect.top-50,200,200)
        elif(pos == -1):
            self.shield_rect = pygame.Rect(self.rect.left-100,self.rect.bottom-150,200,200)

    def draw(self,screen):
        if(self.used_attack != "Protect"):
            self.protected = False
        if(self.when == 1 and self.protected):
            screen.blit(shield,self.shield_rect)
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,GREY,pygame.Rect(self.rect.left,self.rect.top-20,self.fullHealth,5))
        pygame.draw.rect(screen,GREEN,pygame.Rect(self.rect.left,self.rect.top-20,self.health,5))
        print_text(str(self.lives),30,(self.rect.left,self.rect.top-50),(0,0,10))
        print_text(self.used_attack,30,(self.rect.left,self.rect.top-80),(0,0,10))
        if(self.cursed):
            screen.blit(self.cursed_img,self.cursed_rect)
        if(self.when == -1 and self.protected):
            screen.blit(shield,self.shield_rect)
        

class Book(pygame.sprite.Sprite):
    def __init__(self,book,size = (screen_width,screen_height)):
        self.pos = (0,0)
        self.size = size
        self.image = load_image("images/background_cave.png",self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (-screen_width//2,screen_height//2)
        self.toggle_left = self.rect.left
        self.toggle_right = 0
        self.speed = (self.toggle_right - self.toggle_left)//20
        self.moving = False
        self.target_left = self.rect.left
        self.book = book;

    def update(self):
        if(self.moving):
            if self.target_left > self.rect.left:
                self.rect.left += self.speed
            if self.rect.left > self.target_left:
                self.rect.left -= self.speed
        if self.target_left == self.rect.left:
            self.moving = False

    def update_book(self,book):
        self.book = book

    def draw(self,screen,bgcolor,text_color,img):
        screen.blit(self.image,self.rect)
        if(bgcolor):
            screen.fill(bgcolor)
        if(img):
            self.image = img
            screen.blit(self.image,self.rect)
        print_Book(self.rect,self.book,text_color)

    def toggle(self):
        if not self.moving and self.rect.left == self.toggle_left:
            self.target_left = self.toggle_right
            self.moving = True
        elif not self.moving and self.rect.left == self.toggle_right:
            self.target_left = self.toggle_left
            self.moving = True

    def instantToggle(self):
        if self.rect.left == self.toggle_left:
            self.rect.left = self.toggle_right
        elif self.rect.left == self.toggle_right:
            self.rect.left = self.toggle_left



def f0thLayer():
    screen.blit(background,(0,0))
    #screen.fill((200,200,200))

def f1stLayer():
    global count
    color = black
    if(count%5==0):
        color = black
    elif(count%5==1):
        color = (10,150,10)
    elif(count%5==2):
        color = GREY
    elif(count%5==3):
        color = (0,0,255)
    elif(count%5==4):
        color = (255,0,0)
    actionBook.update()
    actionBook.draw(screen,((255,255,200)),color,background)
    spellBook.update()
    spellBook.draw(screen,False,black,background)
    ruleBook.update()
    ruleBook.draw(screen,False,black,background)

def f2ndLayer():
    hero.draw(screen)
    devil.draw(screen)
    attacks.update()
    attacks.draw(screen)
    finisherSpell.update()
    finisherSpell.draw(screen)
    gameOverBook.update()
    gameOverBook.draw(screen,False,black,background)

async def game_loop():
    global status,count
    count = 0
    initGame()
    devilsTalk()
    actionBook.update_book(action_book)
    actionBook.toggle()
    status = False
    while(True):
        if(count > 100):
            count = 0
        f0thLayer()
        f1stLayer()
        f2ndLayer()
        if(status):
            print_text(game_over_book[0],30,(450,470),(255,0,0))
            print_text(game_over_book[3],30,(450,520),(255,0,0))
        pygame.display.update()
        clock.tick(6000)
        await asyncio.sleep(0)
        if(status):
            f0thLayer()
            f1stLayer()
            f2ndLayer()
            print_text(game_over_book[0],30,(270,500),(255,0,0))
            print_text(game_over_book[3],30,(270,550),(255,0,0))
            pygame.display.update()
            break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    spellBook.toggle()
                if event.key == pygame.K_r:
                    ruleBook.toggle()
                if event.key == pygame.K_a:
                    pass
                    #actionBook.toggle()
                if event.key == pygame.K_0:
                    spellCasted(0)
                if event.key == pygame.K_1:
                    spellCasted(1)
                if event.key == pygame.K_2:
                    spellCasted(2)
                if event.key == pygame.K_3:
                    spellCasted(3)
                if event.key == pygame.K_4:
                    spellCasted(4)
                if event.key == pygame.K_5:
                    spellCasted(5)
                if event.key == pygame.K_6:
                    spellCasted(6)
                if event.key == pygame.K_7:
                    spellCasted(7)
                if event.key == pygame.K_8:
                    spellCasted(8)
                if event.key == pygame.K_9:
                    spellCasted(9)


async def restartLoop():
    await game_loop()
    while(True):
        await asyncio.sleep(0) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    await game_loop()


"""        
def firstLevel():
    global isFinisherUsed,heroHealth,reviveChancesHero,reviveChancesDevil,devilHealth
    print_text("You have entered the Devils Zone",30,(100,300),black)
    print_text("You have 6 spells and Devil has 4 spells",30,(100,300),black)
    print_text("\nYour spells are ",30,(100,300),black)
    print_text(" $ Basic Spell                : 10 damage",30,(100,300),black)
    print_text(" $ Protect Spell              : Protects from any attack",30,(100,300),black)
    print_text(" $ Curse Spell                : Curses target, once cursed 10 damage per turn",30,(100,300),black)
    print_text(" $ Revelation Spell           : Reveals all your hidden spells",30,(100,300),black)
    print_text(" $ Finisher Spell             : 100 damage , Loose all your memories about spells",30,(100,300),black)
    print_text(" $ Devils Possesion Spell     : User will be possesed by Devil and can't revive , GAME OVER",30,(100,300),black)
    print_text("\nDevils Spells are ",30,(100,300),black)
    print_text(" * Basic Spell",30,(100,300),black)
    print_text(" * Protect Spell",30,(100,300),black)
    print_text(" * Curse Spell",30,(100,300),black)
    print_text(" * Finisher Spell",30,(100,300),black)
    print_text("\nYou can choose one spell and devil will choose his spell",30,(100,300),black)
    print_text("You can choose spell by clicking a number from 0 to 9",30,(100,300),black)
    print_text("Currently you don't have memory about your spells",30,(100,300),black)
    print_text("Both have 100 life",30,(100,300),black)
    while(1):
        print_text("\nHero Health   : ", heroHealth)
        print_text("Devils Health : ", devilHealth)
        print_text("Hero revives   : ", reviveChancesHero)
        print_text("Devils revives : ", reviveChancesDevil)
        devilsChoice = random.choice(devilsProbability)
        print_text("\nHaha... a new Hero has appeared to concour the dungeon",30,(100,300),black)
        print_text("On behalf of entertaining me I will tell you the Finisher Spell",30,(100,300),black)
        devilsGuess = random.choice([heroSpells[-2],heroSpells[-1],heroSpells[-1]]) 
        print_text("Its : ",devilsGuess)
        herosChoice = int(input("\nChoose your spell : ",30,(100,300),black))
        if(devilsGuess == herosChoice):
            if(herosChoice == heroSpells[-1]):
                print_text("You fool you really fell for my trick, do you think I will tell you the truth",30,(100,300),black)
            else:
                print_text("No.... you shouldn't have chosen it",30,(100,300),black)
        castSpell(herosChoice,devilsChoice)
        if(heroHealth <= 0):
            print_text("\nHero Health   : ", heroHealth)
            print_text("Devils Health : ", devilHealth)
            if(isPossesed):
                print_text("Hero has become Devil can't revive",30,(100,300),black)
            elif(reviveChancesHero>0):
                print_text("Hero has been revived with his revive chances",30,(100,300),black)
                reviveChancesHero-=1
                heroHealth = 100
                continue
            print_text("Game Over : You have failed the challenge to concour the Devils zone",30,(100,300),black)
            print_text("heroSpells : ", str(heroSpells))
            print_text("devilSpells : ",str(devilSpells))
            break
        elif(devilHealth <= 0):
            print_text("\nHero Health   : ", heroHealth)
            print_text("Devils Health : ", devilHealth)
            if(reviveChancesDevil>0):
                print_text("Devil has been revived with his revive chance",30,(100,300),black)
                reviveChancesDevil-=1
                devilHealth = 100
                if(isFinisherUsed):
                    isFinisherUsed = False
                    print_text("Forgetting memories.... ",30,(100,300),black)
                    initState()
                continue
            print_text("Game Over : You have successfully concoured the Devils zone",30,(100,300),black)
            print_text("heroSpells : ", heroSpells)
            print_text("devilSpells : ",devilSpells)
            break

"""


asyncio.run(restartLoop())
