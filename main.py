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
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Devils Zone")


def print_text(text,font,pos,color):
    screen.blit(pygame.font.Font(None,font).render(text,True,color),pos)

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
" $ Devils Possesion : GAME OVER"
]


def load_image(path,pos,size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image,size)

def print_spellBook(rect):
    for i in range(len(spell_book)):
        print_text(spell_book[i],30,(rect.left+10,rect.top+10+30*i),WHITE)

class Animation():
    def __init__(self):
        pass


class SpellBook(pygame.sprite.Sprite):
    def __init__(self):
        self.pos = (100,100)
        self.size = (screen_width-100,screen_height-100)
        self.image = load_image("./images/dialogue.png",self.pos,self.size)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width*0.1,screen_height//2)


    def draw(self,screen):
        screen.blit(self.image,self.rect)
        print_spellBook(self.rect)

    def toggle(self):
        if self.rect.center == (screen_width*0.1,screen_height//2):
            self.rect.center = (screen_width//2,screen_height//2)
        else:
            self.rect.center = (screen_width*0.1,screen_height//2)


# Define menu settings
menu_width = screen_width - 100
menu_height = screen_height-100
menu_x = -menu_width  # Initially hidden off-screen
menu_slide_speed = 10  # Speed at which the menu slides in/out

# Font for text
font = pygame.font.SysFont('Arial', 36)

# Create button
button_rect = pygame.Rect(650, 50, 120, 50)

green = (0,0,255)
black = (0,0,0)
# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
clicks = 0
background = pygame.image.load("./images/background.png").convert_alpha() 
background = pygame.transform.scale(background,(800,600))
spellBook = SpellBook()


def scene_dialogue(scene_text):
    print_text(scene_text[clicks],30,(10,50),black)


def f0thLayer():
    screen.blit(background,(0,0))

def f1stLayer():
    spellBook.draw(screen)


def toggle_menu():
    global menu_x
    if menu_x == -menu_width:
        menu_x = 0
    else:
        menu_x = -menu_width

def intro_loop():
    global clicks
    while(True):
        screen.fill((0,0,0))
        screen.blit(background,(0,0))
        print_spellBook()
        pygame.display.update()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            handle_general_events(event)


def game_loop():
    clicks = 5
    while(True):
        f0thLayer()
        f1stLayer()
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            start_ticks = pygame.time.get_ticks()
            pygame.quit()
            sys.exit()
            break
        if keys[pygame.K_a]:
            toggle_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    toggle_menu()
                    spellBook.toggle()

def initGame():
    global reviveChancesHero,reviveChancesDevil
    reviveChancesHero = 3
    reviveChancesDevil = 3
    isPossesed = False
    initState()

def initState():
    global devilHealth,heroHealth,isHeroCursed,isDevilCursed,isHeroProtected,isDevilProtected,allSpells,heroSpells,devilSpells
    global devilsProbability
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


def spellDamage(caster,target,isProtected, num):
    if(num == 0 ):
        print("Devil has used Basic Spell")
        if(isDevilProtected):
            print("Your Spell has failed to damage the devil")
        else:
            devilHealth-=10
            print("You have damaged the devil")

def castSpell(hero,devil):
    global isFinisherUsed, isPossesed, heroHealth , devilHealth, isHeroProtected, isDevilProtected, isHeroCursed, isDevilCursed
    spH=-1
    spD=-1
    try:
        spD = devilSpells.index(devil)
        spH = heroSpells.index(hero)
    except:
        print("You have chosen devils spell")
        if(spD < spH):
            spD = devilSpells.index(hero)
            spH = -1
            print("Devil is happy with your decision and chose to take your advice")
        else:
            spH = -2
            print("But Devil is happy with his own decision")
    isHeroProtected = False
    isDevilProtected = False
    print("\n")
    if(spD==1):
        print("Devil Has used Protect Spell, with Probability : ",(20/31))
        isDevilProtected = True
    if(spH==1):
        print("You have used Protect Spell")
        isHeroProtected = True
    if(spH == 0):
        print("You have used Basic Spell")
        if(isDevilProtected):
            print("Your Spell has failed to damage the devil")
        else:
            devilHealth-=10
            print("You have damaged the devil")
    if(spD == 0):
        print("Devil has used Basic Spell, with Probability : ",(30/31))
        if(isHeroProtected):
            print("Devils Spell has failed to damage you")
        else:
            heroHealth-=10
            print("Devil has damaged you")
    if(spH==2):
        print("You have used Curse")
        if(isDevilProtected):
            print("Curse failed to damage the devil")
        else:
            isDevilCursed = True
            print("Devil is Cursed")
    if(spD==2):
        print("Devil has used Curse , with Probability : ",(10/31))
        if(isHeroProtected):
            print("Curse failed to damage you")
        else:
            isHeroCursed = True
            print("You are Cursed")
    if(spH==3):
        print("You have used Revelation")
        print("Your Spells are revealed : ",heroSpells)
    if(spH==4):
        print("You have used Finisher Spell")
        isFinisherUsed = True
        print("Due to using Finisher you have lost your memories")
        print("You have forgotten your spells")
        if(isDevilProtected):
            print("Finisher failed to damage the Devil")
        else:
            devilHealth = 0
            print("Devil has been Defeated")
            return
    if(spD==3):
        print("Devil has used Finisher Spell, with Probability : ",(1/31))
        if(isHeroProtected):
            print("Finisher failed to damage you")
        else:
            heroHealth = 0
            print("YOu have been Defeated")
            return
    if(spH==5):
        print("You have used Devil Possesion Spell")
        print("You have been Possesed by Devil")
        heroHealth = 0
        print("You have become devil")
        isPossesed = True
        return
    if(isHeroCursed):
        heroHealth -= 10
    if(isDevilCursed):
        devilHealth -= 10
    print("\n")


        
def firstLevel():
    global isFinisherUsed,heroHealth,reviveChancesHero,reviveChancesDevil,devilHealth
    print("You have entered the Devils Zone")
    print("You have 6 spells and Devil has 4 spells")
    print("\nYour spells are ")
    print(" $ Basic Spell                : 10 damage")
    print(" $ Protect Spell              : Protects from any attack")
    print(" $ Curse Spell                : Curses target, once cursed 10 damage per turn")
    print(" $ Revelation Spell           : Reveals all your hidden spells")
    print(" $ Finisher Spell             : 100 damage , Loose all your memories about spells")
    print(" $ Devils Possesion Spell     : User will be possesed by Devil and can't revive , GAME OVER")
    print("\nDevils Spells are ")
    print(" * Basic Spell")
    print(" * Protect Spell")
    print(" * Curse Spell")
    print(" * Finisher Spell")
    print("\nYou can choose one spell and devil will choose his spell")
    print("You can choose spell by clicking a number from 0 to 9")
    print("Currently you don't have memory about your spells")
    print("Both have 100 life")
    while(1):
        print("\nHero Health   : ", heroHealth)
        print("Devils Health : ", devilHealth)
        print("Hero revives   : ", reviveChancesHero)
        print("Devils revives : ", reviveChancesDevil)
        devilsChoice = random.choice(devilsProbability)
        print("\nHaha... a new Hero has appeared to concour the dungeon")
        print("On behalf of entertaining me I will tell you the Finisher Spell")
        devilsGuess = random.choice([heroSpells[-2],heroSpells[-1],heroSpells[-1]]) 
        print("Its : ",devilsGuess)
        herosChoice = int(input("\nChoose your spell : "))
        if(devilsGuess == herosChoice):
            if(herosChoice == heroSpells[-1]):
                print("You fool you really fell for my trick, do you think I will tell you the truth")
            else:
                print("No.... you shouldn't have chosen it")
        castSpell(herosChoice,devilsChoice)
        if(heroHealth <= 0):
            print("\nHero Health   : ", heroHealth)
            print("Devils Health : ", devilHealth)
            if(isPossesed):
                print("Hero has become Devil can't revive")
            elif(reviveChancesHero>0):
                print("Hero has been revived with his revive chances")
                reviveChancesHero-=1
                heroHealth = 100
                continue
            print("Game Over : You have failed the challenge to concour the Devils zone")
            print("heroSpells : ", heroSpells)
            print("devilSpells : ",devilSpells)
            break
        elif(devilHealth <= 0):
            print("\nHero Health   : ", heroHealth)
            print("Devils Health : ", devilHealth)
            if(reviveChancesDevil>0):
                print("Devil has been revived with his revive chance")
                reviveChancesDevil-=1
                devilHealth = 100
                if(isFinisherUsed):
                    isFinisherUsed = False
                    print("Forgetting memories.... ")
                    initState()
                continue
            print("Game Over : You have successfully concoured the Devils zone")
            print("heroSpells : ", heroSpells)
            print("devilSpells : ",devilSpells)
            break



def mainLoop():
    updateState();


def game():
    print("This is Devils zone")
    initState()
    firstLevel()

game_loop()
game()
