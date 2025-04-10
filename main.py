import random
import pygame
import sys


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
    if color == black:
        action_book.append(text)
        print(action_book)

def handle_general_keys(keys):
    pass

def handle_general_events(event):
    global clicks
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
        return True
    if event.type == pygame.KEYDOWN:
        clicks += 1
    return False

def load_image(path,size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image,size)

def print_Book(rect,book):
    for i in range(len(book)):
        print_text(book[i],30,(rect.left+10,rect.top+10+30*i),WHITE)

intro_text = [
"You are hero Entered Devils Zone to defeat Devils",
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
" $ Devils Possesion : You became Devil , GAME OVER"
]

rule_book = [
"Click on button 0-9 to use a spell",
"You don't know which spells to use",
"Out of 10 , 6 spells are yours",
"4 Spells are Devils",
"You have 3 lives and Devil also has 3",
"Each life can take 100 damage"
]

background = pygame.image.load("./images/background.png") 
background = pygame.transform.scale(background,(800,600))

def initGame():
    global reviveChancesHero,reviveChancesDevil,spellBook,ruleBook,actionBook
    reviveChancesHero = 3
    reviveChancesDevil = 3
    isPossesed = False
    clicks = 0
    spellBook = Book(spell_book)
    ruleBook = Book(rule_book)
    actionBook = Book(action_book)
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
    hero = Player("Hero",heroSpells,load_image("./images/dialogue.png",(150,150)),(150,150),(100,400))
    devil = Player("Devil",devilSpells,load_image("./images/dialogue.png",(150,150)),(150,150),(600,400))

def castSpell(h,d):
    global isFinisherUsed, isPossesed, heroHealth , devilHealth, isHeroProtected, isDevilProtected, isHeroCursed, isDevilCursed
    global action_book
    action_book = []
    spH=-1
    spD=-1
    try:
        spD = devilSpells.index(d)
        spH = heroSpells.index(h)
    except:
        print_text("You have chosen devils spell",30,(100,100),black)
        if(spD < spH):
            spD = devilSpells.index(h)
            spH = -1
            print_text("Devil is happy with your decision and chose to take your advice",30,(100,150),black)
        else:
            spH = -2
            print_text("But Devil is happy with his own decision",30,(100,200),black)
    isHeroProtected = False
    isDevilProtected = False
    if(spD==1):
        print_text("Devil Has used Protect Spell, with Probability : "+str(20/31),30,(100,250),black)
        isDevilProtected = True
    if(spH==1):
        print_text("You have used Protect Spell",30,(100,300),black)
        isHeroProtected = True
    if(spH == 0):
        print_text("You have used Basic Spell",30,(100,250),black)
        if(isDevilProtected):
            print_text("Your Spell has failed to damage the devil",30,(100,300),black)
        else:
            devil.attacked_by_spell(10)
            print_text("You have damaged the devil",30,(100,300),black)
    if(spD == 0):
        print_text("Devil has used Basic Spell, with Probability : "+str(30/31),30,(100,250),black)
        if(isHeroProtected):
            print_text("Devils Spell has failed to damage you",30,(100,300),black)
        else:
            hero.attacked_by_spell(10)
            print_text("Devil has damaged you",30,(100,300),black)
    if(spH==2):
        print_text("You have used Curse",30,(100,250),black)
        if(isDevilProtected):
            print_text("Curse failed to damage the devil",30,(100,300),black)
        else:
            isDevilCursed = True
            print_text("Devil is Cursed",30,(100,300),black)
    if(spD==2):
        print_text("Devil has used Curse , with Probability : "+str(10/31),30,(100,250),black)
        if(isHeroProtected):
            print_text("Curse failed to damage you",30,(100,300),black)
        else:
            isHeroCursed = True
            print_text("You are Cursed",30,(100,300),black)
    if(spH==3):
        print_text("You have used Revelation",30,(100,250),black)
        print_text("Your Spells are revealed : "+str(heroSpells),30,(100,300),black)
    if(spH==4):
        print_text("You have used Finisher Spell",30,(100,250),black)
        isFinisherUsed = True
        print_text("Due to using Finisher you have lost your memories",30,(100,300),black)
        print_text("You have forgotten your spells",30,(100,350),black)
        if(isDevilProtected):
            print_text("Finisher failed to damage the Devil",30,(100,400),black)
        else:
            devil.attacked_by_spell(100)
            print_text("Devil has been Defeated",30,(100,400),black)
            actionBook.update_book(action_book)
            return
    if(spD==3):
        print_text("Devil has used Finisher Spell, with Probability : "+str(1/31),30,(100,250),black)
        if(isHeroProtected):
            print_text("Finisher failed to damage you",30,(100,300),black)
        else:
            hero.attacked_by_spell(100)
            print_text("YOu have been Defeated",30,(100,300),black)
            actionBook.update_book(action_book)
            return
    if(spH==5):
        print_text("You have used Devil Possesion Spell",30,(100,250),black)
        print_text("You have been Possesed by Devil",30,(100,300),black)
        hero.attacked_by_spell(100)
        print_text("You have become devil",30,(100,350),black)
        isPossesed = True
        actionBook.update_book(action_book)
        return
    if(isHeroCursed):
        hero.attacked_by_spell(10)
    if(isDevilCursed):
        devil.attacked_by_spell(10)

def devilsTalk():
        print_text("Haha... a new Hero has appeared to concour the dungeon",30,(100,500),black)
        print_text("On behalf of entertaining me I will tell you the Finisher Spell",30,(100,550),black)
        devilsGuess = random.choice([heroSpells[-2],heroSpells[-1],heroSpells[-1]]) 
        print_text("Its : "+str(devilsGuess),30,(100,600),black)


def spellCasted(sp):
    castSpell(sp,devil.random_attack())
    devilsTalk()
    actionBook.update_book(action_book)


class Animation():
    def __init__(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self,name,spells,image,size,center):
        self.name = name
        self.fullHealth = 100
        self.health = 100
        self.lives = 3
        self.spells = spells
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.size = size

    def random_attack(self):
        return random.choice(self.spells)

    def attacked_by_spell(self,damage):
        self.health -= damage

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,GREY,pygame.Rect(self.rect.left,self.rect.top,self.fullHealth,20))
        pygame.draw.rect(screen,GREEN,pygame.Rect(self.rect.left,self.rect.top,self.health,20))
        

class Book(pygame.sprite.Sprite):
    def __init__(self,book):
        self.pos = (100,100)
        self.size = (screen_width-100,screen_height-100)
        self.image = load_image("./images/dialogue.png",self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (-screen_width*0.4,screen_height//2)
        self.toggle_left = self.rect.left
        self.toggle_right = 50
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

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        print_Book(self.rect,self.book)

    def toggle(self):
        if not self.moving and self.rect.left == self.toggle_left:
            self.target_left = self.toggle_right
            self.moving = True
        elif not self.moving and self.rect.left == self.toggle_right:
            self.target_left = self.toggle_left
            self.moving = True


def f0thLayer():
    screen.blit(background,(0,0))

def f1stLayer():
    spellBook.update()
    spellBook.draw(screen)
    ruleBook.update()
    ruleBook.draw(screen)
    actionBook.update()
    actionBook.draw(screen)

def f2ndLayer():
    hero.draw(screen)
    devil.draw(screen)

def game_loop():
    initGame()
    while(True):
        f0thLayer()
        f1stLayer()
        f2ndLayer()
        pygame.display.update()
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
                    actionBook.toggle()
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



def mainLoop():
    updateState();


def game():
    print_text("This is Devils zone",30,(100,300),black)
    initState()
    firstLevel()

game_loop()
game()
