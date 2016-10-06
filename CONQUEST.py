#Conquest.py
#Nikola Zjalic & Milosh Zelembaba



from pygame import *
from random import *
from pprint import *

screen = display.set_mode((1200,800))
grid = [["g"] * 18 for i in range(24)]
charGrid = [[0] * 18 for i in range(24)]
menu = "home"
mx = my = 0
click = False
attackFlag = False #if the character is attacking or moving
selectedPlayer = (0,0,0)
buycharacterflag = "none"
goldPlayerOne = 50
goldPlayerTwo = 50
turns = 1
stats=[]
statsla = open("stats.txt")
for i in range(7):
    stats.append(int(statsla.readline().strip("\n")))
update = open("stats.txt","w")

#music

init()                                  
mixer.music.load("Two Steps From Hell - Protectors Of The Earth.mp3")      #paly music 
mixer.music.play(-1)




#images

home = image.load("images/home.png")
buttons = image.load("images/buttons/buttons.png")
playclick = image.load("images/buttons/button1click.png")
instructionsclick = image.load("images/buttons/button2click.png")
statsclick = image.load("images/buttons/button3click.png")
quitclick = image.load("images/buttons/button4click.png")
backButton = image.load("images/buttons/backButton.png")

charmenu = image.load("images/charmenu.png")
battlemenu = image.load("images/battlemenu.png")

instructionsscreen = image.load("images/instructionsscreen.png")
statsscreen = image.load("images/statsscreen.png")

grass = image.load("images/tiles/grass.png")
mountain = image.load("images/tiles/mountain.png")
water = image.load("images/tiles/water.png")
forest = image.load("images/tiles/forest.png")

swordsman = image.load("images/characters/swordsman.png")
archer = image.load("images/characters/archer.png")
mage = image.load("images/characters/mage.png")
barbarian = image.load("images/characters/barbarian.png")
paladin = image.load("images/characters/paladin.png")
horseman = image.load("images/characters/horseman.png")
castle = image.load("images/characters/castle.png")
wall = image.load("images/wall.png")
playerOneWin = image.load("images/playerOneWin.png")

swordsmanE = image.load("images/characters/swordsmanE.png")
archerE = image.load("images/characters/archerE.png")
mageE = image.load("images/characters/mageE.png")
barbarianE = image.load("images/characters/barbarianE.png")
paladinE = image.load("images/characters/paladinE.png")
horsemanE = image.load("images/characters/horsemanE.png")
castleE = image.load("images/characters/castleE.png")
playerTwoWin = image.load("images/playerTwoWin.png")

possiblemoves = image.load("images/characters/moveabletile.png")
attacktile = image.load("images/characters/attacktile.png")

cancelbutton = image.load("images/buttons/cancel.png")
nextTurnButton = image.load("images/buttons/nextTurn.png")
attackButton = image.load("images/buttons/attackButton.png")

#Rects

playRect = Rect(500,250,200,50)
instructionsRect = Rect(500,310,200,50)
statsRect = Rect(500,370,200,50)
quitRect = Rect(500,430,200,50)
backRect = Rect(900,100,200,50)

buyswordsmanrect = Rect(1120,40,40,40)
buyarcherrect = Rect(1120,113,40,40)
buymagerect = Rect(1120,186,40,40)
buybarbarianrect = Rect(1120,264,40,40)
buypaladinrect = Rect(1120,342,40,40)
buyhorsemanrect = Rect(1120,425,40,40)
buywallrect = Rect(1120,505,40,40)

cancelRect = Rect(10,600,100,35)
endTurnRect = Rect(10,700,100,35)
attackRect = Rect(10,650,100,35)

goldArea = Rect(395,757,120,25)
turnArea = Rect(570,750,50,50)
fieldRect = Rect(120,0, 24 * 40, 18 * 40)

#Font Stuff
font.init()
text = font.SysFont("Times New Roman", 20)

#Character Details
teamOneAttackers = [10]
teamOneAttackersHealth = [100]
teamOneAttackersPos = [(0,17)]
teamOneAttackersMoves = [0]

teamTwoAttackers = [20]
teamTwoAttackersHealth = [100]
teamTwoAttackersPos = [(23,0)]
teamTwoAttackersMoves = [0]

#Tree Growing Back Stuff
treePos = []
treeTurn = []

#functions


def gen(grid): #messing around with map generator
    areas = [(0,17),(23,0),(0,16),(1,16),(1,17),(22,0),(22,1),(23,1)]
    options = ["f","f","f","f","m","m","w","w","w","w"]
    ##m = mountain
    ##w = water
    ##f = forest
    ##g = grass
    shuffle(options)
    for terrain in options:
        x = randint(2,21)#choses Random spot in the grid
        y = randint(2,15)
        for i in range(15):
            xpos = x + choice([0,1,2,-1,-2])#choses random spots around the seleced spot
            ypos = y + choice([0,1,2,-1,-2])
            if ((xpos,ypos)) not in areas:
                grid[xpos][ypos] = terrain
                areas.append((xpos,ypos))
                
    return grid

def drawMap(grid):
    for x in range(24):
        for y in range(18):
            if grid[x][y] == "g":
                screen.blit(grass,(120 + x * 40, y * 40))
            if grid[x][y] == "m":
                screen.blit(mountain,(120 + x * 40, y * 40))
            if grid[x][y] == "w":
                screen.blit(water,(120 + x * 40, y * 40))
            if grid[x][y] == "f":
                screen.blit(forest,(120 + x * 40, y * 40))

def drawCharacters(charGrid):
    for x in range(24):
        for y in range(18):
            if charGrid[x][y] == 1:
                screen.blit(swordsman,(120 + x * 40, y * 40))
            if charGrid[x][y] == 2:
                screen.blit(archer,(120 + x * 40, y * 40))
            if charGrid[x][y] == 3:
                screen.blit(mage,(120 + x * 40, y * 40))
            if charGrid[x][y] == 4:
                screen.blit(barbarian,(120 + x * 40, y * 40))
            if charGrid[x][y] == 5:
                screen.blit(paladin,(120 + x * 40, y * 40))
            if charGrid[x][y] == 6:
                screen.blit(horseman,(120 + x * 40, y * 40))
            if charGrid[x][y] == 7:
                screen.blit(wall,(120 + x * 40, y * 40))
            if charGrid[x][y] == 10:
                screen.blit(castle,(120 + x * 40, y * 40))
            if charGrid[x][y] == 11:
                screen.blit(swordsmanE,(120 + x * 40, y * 40))
            if charGrid[x][y] == 12:
                screen.blit(archerE,(120 + x * 40, y * 40))
            if charGrid[x][y] == 13:
                screen.blit(mageE,(120 + x * 40, y * 40))
            if charGrid[x][y] == 14:
                screen.blit(barbarianE,(120 + x * 40, y * 40))
            if charGrid[x][y] == 15:
                screen.blit(paladinE,(120 + x * 40, y * 40))
            if charGrid[x][y] == 16:
                screen.blit(horsemanE,(120 + x * 40, y * 40))
            if charGrid[x][y] == 17:
                screen.blit(wall,(120 + x * 40, y * 40))
            if charGrid[x][y] == 20:
                screen.blit(castleE,(120 + x * 40, y * 40))
                
def playerSelect(grid):
    global click, mx, my
    for x in range(24): #searches threw the grid, through* ;)
        for y in range(18):
            if 119 + x * 40 < mx < 121 + (x + 1) * 40 and (y + 1) * 40 + 1 > my > y * 40 - 1 and click == True: #finds what box the player is clicking on
                if charGrid[x][y] != 0:#displays the menu only if something is slected
                    showCharMenu(x,y)
                if turns%2 == 1 and grid[x][y] < 11:#if player selects his own player return info
                    showCharMenu(x,y)
                    return grid[x][y],x,y
                if turns%2 == 1 and grid[x][y] > 10:#if player does not select his own player return 0  so they cannot move the other teams player
                    showCharMenu(x,y)
                    return 0,x,y
                if turns%2 == 0 and grid[x][y] < 11:#if player does not select his own player return 0 so they cannot move the other teams player
                    showCharMenu(x,y)
                    return 0,x,y
                if turns%2 == 0 and grid[x][y] > 10:#if player selects his own player return info
                    showCharMenu(x,y)
                    return grid[x][y],x,y
              
def charMove(char,x,y,):
    global click, mx, my, charGrid, selectedPlayer, grid, teamOneAttackersMoves, teamTwoAttackersMoves
    if turns%2 == 1:#checks that it is first player or secondplayers turn
        if char in range(1,6):#possible moves for repective characters
            posmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)] #for character 1-5, these are their possible moves
        if char == 6:#same as above, just for the horsemen
            posmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(2,0),(2,1),(2,2),(1,2),(0,2),(-1,2),(-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2),(-1,-2),(0,-2),(1,-2),(2,-2),(2,-1)]
        if char == 10 or char == 7:
            posmove = [(0,0)]
        for x1 in range(24):
            for y1 in range(18):
                if 120 + x1 * 40 < mx < 120 + (x1 + 1) * 40 and (y1 + 1) * 40 > my > y1 * 40 and click == True:
                    if grid[x1][y1] == "g" and charGrid[x1][y1] == 0:#checks to make sure the place i want to move is a valid location
                        for i in range(len(posmove)):
                            if x + posmove[i][0] == x1 and y + posmove[i][1] == y1:#checks to make sure that its a possible move
                                if teamOneAttackersMoves[teamOneAttackersPos.index((x,y))] != 0:
                                    teamOneAttackersPos[teamOneAttackersPos.index((x,y))] = (x1,y1) #updates the character that is moving's current poition
                                    teamOneAttackersMoves[teamOneAttackersPos.index((x1,y1))] -= 1
                                    charGrid[x][y] = 0 #previous spot becomes 0 because he isnt there anymore
                                    charGrid[x1][y1] = char#where the player wants him to go becomes the respective number
                                    selectedPlayer=list(selectedPlayer)
                                    selectedPlayer[0] = 0
                                
    if turns%2 == 0:#checks that it is first player or second players turn
        if char in range(11,16):#possible moves for repective characters
            posmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        if char == 16 :#same as above, just for the horsemen
            posmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(2,0),(2,1),(2,2),(1,2),(0,2),(-1,2),(-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2),(-1,-2),(0,-2),(1,-2),(2,-2),(2,-1)]
        if char == 20 or char == 17:
            posmove = [(0,0)]
        for x1 in range(24):
            for y1 in range(18):
                if 120 + x1 * 40 < mx < 120 + (x1 + 1) * 40 and (y1 + 1) * 40 > my > y1 * 40 and click == True:
                    if grid[x1][y1] == "g" and charGrid[x1][y1] == 0:
                        for i in range(len(posmove)):
                            if x + posmove[i][0] == x1 and y + posmove[i][1] == y1:
                                if teamTwoAttackersMoves[teamTwoAttackersPos.index((x,y))] != 0:
                                    teamTwoAttackersPos[teamTwoAttackersPos.index((x,y))] = (x1,y1)
                                    teamTwoAttackersMoves[teamTwoAttackersPos.index((x1,y1))] -= 1
                                    charGrid[x][y] = 0
                                    charGrid[x1][y1] = char
                                    selectedPlayer=list(selectedPlayer)
                                    selectedPlayer[0] = 0
    
def buyCharacter():
    global mx,my,mb,charGrid,buyswordsmanrect, teamOneAttackersMoves, teamTwoAttackersMoves, teamOneAttackers, teamTwoAttackers, turns, buyarcherrect, buycharacterflag, goldPlayerOne, goldPlayerTwo, teamTwoAttackersHealth,teamTwoAttackersPos,teamOneAttackersHealth,teamOneAttackersPos
    options = ["swordsman","archer","mage","barb","paladin","horseman","wall"]
    numberOne = [1,2,3,4,5,6,7]
    numberTwo = [11,12,13,14,15,16,17]
    price = [25,25,25,125,125,125,10]
    health = [10,5,5,15,20,25,10]
    if turns%2 == 1:#checks that it is first player or secondplayers turn
#checks whos trying to be bought and if he can be bought
        if buyswordsmanrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerOne > 24:
            buycharacterflag = "swordsman"
        if buyarcherrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerOne > 24:
            buycharacterflag = "archer"
        if buymagerect.collidepoint(mx,my) and mb[0]==1 and goldPlayerOne > 24:
            buycharacterflag = "mage"
        if buybarbarianrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerOne > 124:
            buycharacterflag = "barb"
        if buypaladinrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerOne > 124:
            buycharacterflag = "paladin"
        if buyhorsemanrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerOne > 124:
            buycharacterflag = "horseman"
        if buywallrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerOne > 9:
            buycharacterflag = "wall"

        for character in options:
            if character == buycharacterflag:#checks whos gonna be bought
                for x in range(24):
                    for y in range(18):
                        if 119 + x * 40 < mx < 121 + (x + 1) * 40 and (y + 1) * 40 + 1 > my > y * 40 - 1 and mb[0]==1 and charGrid[x][y] == 0 and grid[x][y] == "g":#where the character wants to be placed and makes sure its a valid place to be put
                            if (x,y) in [(0,16),(1,16),(1,17),(2,17),(2,16),(2,15),(1,15),(0,15)] and character != "wall":#the wall can be put where on the map, however the characters can only be put close to the castle
                                charGrid[x][y] = numberOne[options.index(character)]#places the character where necessary
                                goldPlayerOne -= price[options.index(character)]#takes away gold
                                buycharacterflag = "none"
                                teamOneAttackers.append(numberOne[options.index(character)])#adds the respective character number to the list of the teams attackers
                                teamOneAttackersHealth.append(health[options.index(character)])#adds the respective character health to the list of the teams attackers
                                teamOneAttackersPos.append((x,y))#adds the respective character position to the list of the teams attackers
                                teamOneAttackersMoves.append(2)#adds 2 moves for each character
                            if character == "wall":
                                charGrid[x][y] = numberOne[options.index(character)]
                                goldPlayerOne -= price[options.index(character)]
                                buycharacterflag = "none"
                                teamOneAttackers.append(numberOne[options.index(character)])
                                teamOneAttackersHealth.append(health[options.index(character)])
                                teamOneAttackersPos.append((x,y))
                                teamOneAttackersMoves.append(0)
    if turns%2 == 0:#checks that it is first player or secondplayers turn
        if buyswordsmanrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerTwo > 24:
            buycharacterflag = "swordsman"
        if buyarcherrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerTwo > 24:
            buycharacterflag = "archer"
        if buymagerect.collidepoint(mx,my) and mb[0]==1 and goldPlayerTwo > 24:
            buycharacterflag = "mage"
        if buybarbarianrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerTwo > 124:
            buycharacterflag = "barb"
        if buypaladinrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerTwo > 124:
            buycharacterflag = "paladin"
        if buyhorsemanrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerTwo > 124:
            buycharacterflag = "horseman"
        if buywallrect.collidepoint(mx,my) and mb[0]==1 and goldPlayerTwo > 9:
            buycharacterflag = "wall"

        for character in options:
            if character == buycharacterflag:
                for x in range(24):
                    for y in range(18):
                        if 119 + x * 40 < mx < 121 + (x + 1) * 40 and (y + 1) * 40 + 1 > my > y * 40 - 1 and mb[0]==1 and charGrid[x][y] == 0 and grid[x][y] == "g":
                            if (x,y) in [(22,0),(22,1),(23,1),(23,2),(22,2),(21,2),(21,1),(21,0)] and character != "wall":
                                charGrid[x][y] = numberTwo[options.index(character)]
                                goldPlayerTwo -= price[options.index(character)]
                                buycharacterflag = "none"
                                teamTwoAttackers.append(numberTwo[options.index(character)])
                                teamTwoAttackersHealth.append(health[options.index(character)])
                                teamTwoAttackersPos.append((x,y))
                                teamTwoAttackersMoves.append(2)
                            if character == "wall":
                                charGrid[x][y] = numberTwo[options.index(character)]
                                goldPlayerTwo -= price[options.index(character)]
                                buycharacterflag = "none"
                                teamTwoAttackers.append(numberTwo[options.index(character)])
                                teamTwoAttackersHealth.append(health[options.index(character)])
                                teamTwoAttackersPos.append((x,y))
                                teamTwoAttackersMoves.append(0)
    


def possibleMoves(char,x,y):
    global charGrid, grid
    posmove=[]
    if turns%2 == 1:
        if char in range(1,6):#these characters can only move a block around themselves
            posmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        if char == 6:#horse man can move 2
            posmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(2,0),(2,1),(2,2),(1,2),(0,2),(-1,2),(-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2),(-1,-2),(0,-2),(1,-2),(2,-2),(2,-1)]
        for i in range(len(posmove)):
            if -1<x + posmove[i][0]<24 and -1<y + posmove[i][1]<18:
                if grid[x + posmove[i][0]][y + posmove[i][1]] != "m" and grid[x + posmove[i][0]][y + posmove[i][1]] != "w":
                    screen.blit(possiblemoves,(120 + (x + posmove[i][0])*40,(y + posmove[i][1])*40))
    if turns%2 == 0:
        if char in range(11,16):
            posmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        if char == 16:
            posmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(2,0),(2,1),(2,2),(1,2),(0,2),(-1,2),(-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2),(-1,-2),(0,-2),(1,-2),(2,-2),(2,-1)]
        for i in range(len(posmove)):
            if -1<x + posmove[i][0]<24 and -1<y + posmove[i][1]<18:
                if grid[x + posmove[i][0]][y + posmove[i][1]] != "m" and grid[x + posmove[i][0]][y + posmove[i][1]] != "w":
                    screen.blit(possiblemoves,(120 + (x + posmove[i][0])*40,(y + posmove[i][1])*40))

def cutTree(char,x,y):
    global charGrid, grid, mx, my, mb, goldPlayerOne, click, goldPlayerTwo, treePos, treeTurn
    posmove = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(+1,-1)]
    if char != 0:
        for x1 in range(24):
            for y1 in range(18):
                if 119 + x1 * 40 < mx < 121 + (x1 + 1) * 40 and (y1 + 1) * 40 + 1 > my > y1 * 40 - 1 and click==True and grid[x1][y1]=="f":
                    for i in range(8):
                        if x + posmove[i][0]==x1 and y + posmove[i][1]==y1:                            
                            if turns%2 == 1:
                                if teamOneAttackersMoves[teamOneAttackersPos.index((x,y))] != 0:#makes sure they still have moves left in the current turn
                                    grid[x1][y1]= "g"#tree goes away
                                    goldPlayerOne += 25#team gets money
                                    stats[2] += 25
                                    stats[4] += 1
                                    
                            if turns%2 == 0:
                                if teamTwoAttackersMoves[teamTwoAttackersPos.index((x,y))] != 0:
                                    goldPlayerTwo += 25
                                    grid[x1][y1]= "g"
                                    stats[3] += 25
                                    stats[4] += 1
                            treeTurn.append(1)#appends that it has been gone for 1 turn so far
                            treePos.append((x1,y1))#position of the cut down tree
                        
def treeGrow():
    global charGrid, treePos, treeTurn, grid
    for number in treeTurn:
        if number > 10:#when the tree hasbeen gone for more than 10 turns
            x = treePos[treeTurn.index(number)][0]
            y = treePos[treeTurn.index(number)][1]
            if charGrid[x][y] == 0:#makes sure it wont kill a character growing a tree
                treePos.remove(treePos[treeTurn.index(number)])
                treeTurn.remove(treeTurn[treeTurn.index(number)])
                grid[x][y] = "f"


def attack(char,x,y):
    global charGrid, grid, mx, my, click, posattack, teamOneAttackersMoves, teamTwoAttackersMoves
    if turns%2 == 0:
        if char in [11,14,15,16]:#checks what character it is and creates a list respective to how far it can attack
            posattack = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        if char in [12,13]:
            posattack = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(2,0),(2,1),(2,2),(1,2),(0,2),(-1,2),(-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2),(-1,-2),(0,-2),(1,-2),(2,-2),(2,-1)]
        if char == 20 or char == 17:
            posattack = [(0,0)]
        for x1 in range(24):
            for y1 in range(18):
                if 119 + x1 * 40 < mx < 121 + (x1 + 1) * 40 and (y1 + 1) * 40 + 1 > my > y1 * 40 - 1 and click==True and charGrid[x1][y1]!=0:
                    for i in range(len(posattack)):
                        if x + posattack[i][0]==x1 and y + posattack[i][1]==y1:
                            if charGrid[x1][y1]<11:#No friendly fire
                                if teamTwoAttackersMoves[teamTwoAttackersPos.index((x,y))] != 0:
                                    #checks what player and takes away damage respective to the amount of damage that character can give
                                    if char == 11:
                                        teamOneAttackersHealth[teamOneAttackersPos.index((x1,y1))] -= randint(1,3)
                                    if char == 14:
                                        teamOneAttackersHealth[teamOneAttackersPos.index((x1,y1))] -= randint(0,7)
                                    if char == 15:
                                        teamOneAttackersHealth[teamOneAttackersPos.index((x1,y1))] -= randint(0,5)
                                    if char == 16:
                                        teamOneAttackersHealth[teamOneAttackersPos.index((x1,y1))] -= randint(0,4)
                                    if char == 12:
                                        teamOneAttackersHealth[teamOneAttackersPos.index((x1,y1))] -= randing(2,4)
                                    if char == 13:
                                        teamOneAttackersHealth[teamOneAttackersPos.index((x1,y1))] -= randint(2,4)
                                    teamTwoAttackersMoves[teamTwoAttackersPos.index((x,y))] -= 1#one less move left after an attack
                                    attackFlag = False
                                                                   
    if turns%2 == 1:
        if char in [1,4,5,6]:
            posattack = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        if char in [2,3]:
            posattack = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(2,0),(2,1),(2,2),(1,2),(0,2),(-1,2),(-2,2),(-2,1),(-2,0),(-2,-1),(-2,-2),(-1,-2),(0,-2),(1,-2),(2,-2),(2,-1)]
        if char == 10 or char == 7:
            posattack = [(0,0)]
        for x1 in range(24):
            for y1 in range(18):
                if 119 + x1 * 40 < mx < 121 + (x1 + 1) * 40 and (y1 + 1) * 40 + 1 > my > y1 * 40 - 1 and click==True and charGrid[x1][y1]!=0:
                    for i in range(len(posattack)):
                        if x + posattack[i][0]==x1 and y + posattack[i][1]==y1:
                            if charGrid[x1][y1]>10:
                                if teamOneAttackersMoves[teamOneAttackersPos.index((x,y))]!= 0:
                                    if char == 1:
                                        teamTwoAttackersHealth[teamTwoAttackersPos.index((x1,y1))] -= randint(1,3)
                                    if char == 4:
                                        teamTwoAttackersHealth[teamTwoAttackersPos.index((x1,y1))] -= randint(0,7)
                                    if char == 5:
                                        teamTwoAttackersHealth[teamTwoAttackersPos.index((x1,y1))] -= randint(0,5)
                                    if char == 6:
                                        teamTwoAttackersHealth[teamTwoAttackersPos.index((x1,y1))] -= randint(0,4)
                                    if char == 2:
                                        teamTwoAttackersHealth[teamTwoAttackersPos.index((x1,y1))] -= randint(2,4)
                                    if char == 3:
                                        teamTwoAttackersHealth[teamTwoAttackersPos.index((x1,y1))] -= randint(2,4)
                                    teamOneAttackersMoves[teamOneAttackersPos.index((x,y))] -= 1
                                    attackFlag = False

def checkDeath():
    global charGrid, grid
    if turns %2 == 1:
        for health in teamTwoAttackersHealth:
            if teamTwoAttackersHealth[0]<1:
                checkGameOver()
                break
            elif health < 1 :
                x = teamTwoAttackersPos[teamTwoAttackersHealth.index(health)][0]
                y = teamTwoAttackersPos[teamTwoAttackersHealth.index(health)][1]
                grid[x][y] = "g"
                charGrid[x][y] = 0
                pos = teamTwoAttackersHealth.index(health)
                teamTwoAttackersPos.remove(teamTwoAttackersPos[pos])
                teamTwoAttackers.remove(teamTwoAttackers[pos])
                teamTwoAttackersHealth.remove(teamTwoAttackersHealth[pos])
                
    if turns %2 == 0:
        for health in teamOneAttackersHealth:
            if teamOneAttackersHealth[0]<1:
                checkGameOver()
                break
            elif health < 1 :
                x = teamOneAttackersPos[teamOneAttackersHealth.index(health)][0]
                y = teamOneAttackersPos[teamOneAttackersHealth.index(health)][1]
                grid[x][y] = "g"
                charGrid[x][y] = 0
                pos = teamOneAttackersHealth.index(health)
                teamOneAttackersPos.remove(teamOneAttackersPos[pos])
                teamOneAttackers.remove(teamOneAttackers[pos])
                teamOneAttackersHealth.remove(teamOneAttackersHealth[pos])
                
 
def showCharMenu(x,y):
    global charGrid, teamOneAttackers, teamOneAttackersHealth, teamOneAttackersPos, teamOneAttackersMoves, teamTwoAttackers, teamTwoAttackersHealth, teamTwoAttackersPos, teamTwoAttackersMoves

    if 0 < charGrid[x][y] < 10 and len(teamOneAttackers) > 0:
        screen.blit(charmenu,(5,100))
        chars = [1,2,3,4,5,6,7,10]
        names = ["","Swordsman","Archer","Wizard","Barbarian","Paladin","Horseman","Wall","","","Castle","","Swordsman","Archer","Wizard","Barbarian","Paladin","Horseman","Wall","Castle"]
        pics = ["",swordsman,archer,mage,barbarian,paladin,horseman,wall,"","",castle]
        hp = ["",10,5,5,15,20,25,10,"","",100]
        atk = ["","1-3","2-4","2-4","0-7","3-5","5","","","",""]
        ranges = ["","1","2","2","1","1","1","","",""]
        screen.blit(pics[teamOneAttackers[teamOneAttackersPos.index((x,y))]],(40,120))
        charName = text.render(names[teamOneAttackers[teamOneAttackersPos.index((x,y))]], True, (0,0,0))
        charHp = text.render(( "HP: " + str(teamOneAttackersHealth[teamOneAttackersPos.index((x,y))]) + "/" + str(hp[teamOneAttackers[teamOneAttackersPos.index((x,y))]])), True, (0,0,0))
        charAtk = text.render( "ATK: " + atk[teamOneAttackers[teamOneAttackersPos.index((x,y))]], True, (0,0,0))
        charRange = text.render( "Range: " + ranges[teamOneAttackers[teamOneAttackersPos.index((x,y))]], True, (0,0,0))
        charMoves = text.render( "Moves: " + str(teamOneAttackersMoves[teamOneAttackersPos.index((x,y))]) + "/2" , True, (0,0,0))
        screen.blit(charName,(55 - len(names[teamOneAttackers[teamOneAttackersPos.index((x,y))]]) / 2 *10,100))
        screen.blit(charHp,(20,160))
        screen.blit(charAtk,(20,180))
        screen.blit(charRange,(20,200))
        screen.blit(charMoves,(20,220))
        
    if 10 < charGrid[x][y] < 20 and len(teamTwoAttackers) > 0:
        screen.blit(charmenu,(5,100))
        chars = [11,12,13,14,15,16,17,20]
        names = ["","Swordsman","Archer","Wizard","Barbarian","Paladin","Horseman","Wall","","","Castle","","Swordsman","Archer","Wizard","Barbarian","Paladin","Horseman","Wall","Castle"]
        pics = ["",swordsmanE,archerE,mageE,barbarianE,paladinE,horsemanE,wall,"","",castleE]
        hp = ["",10,5,5,15,20,25,10,"","",100]
        atk = ["","1-3","2-4","2-4","0-7","3-5","5","","","",""]
        ranges = ["","1","2","2","1","1","1","","","",""]
        screen.blit(pics[teamTwoAttackers[teamTwoAttackersPos.index((x,y))]-10],(40,120))
        charName = text.render(names[teamTwoAttackers[teamTwoAttackersPos.index((x,y))]-10], True, (0,0,0))
        charHp = text.render(( "HP:" + str(teamTwoAttackersHealth[teamTwoAttackersPos.index((x,y))]) + "/" + str(hp[teamTwoAttackers[teamTwoAttackersPos.index((x,y))]-10])), True, (0,0,0))
        charAtk = text.render( "ATK: " + atk[teamTwoAttackers[teamTwoAttackersPos.index((x,y))]-10], True, (0,0,0))
        charRange = text.render( "Range: " + ranges[teamTwoAttackers[teamTwoAttackersPos.index((x,y))]-10], True, (0,0,0))
        charMoves = text.render( "Moves: " + str(teamTwoAttackersMoves[teamTwoAttackersPos.index((x,y))]) + "/2" , True, (0,0,0))
        screen.blit(charName,(55 - len(names[teamTwoAttackers[teamTwoAttackersPos.index((x,y))]-10]) / 2 *10,100))
        screen.blit(charHp,(20,160))
        screen.blit(charAtk,(20,180))
        screen.blit(charRange,(20,200))
        screen.blit(charMoves,(20,220))

def updateStats():
    global stats, update
    for stat in stats:
        update.write(str(stat)+"\n")
    update.close()

def checkGameOver():
    global teamOneAttackersHealth, teamTwoAttackersHealth
    if teamOneAttackersHealth[0]<1:
        screen.blit(playerTwoWin,(0,0))
        running = False
        stats[5] += 1
    if teamTwoAttackersHealth[0]<1:
        screen.blit(playerOneWin,(0,0))
        running = False
        stats[6] += 1

charGrid[0][17] = 10
charGrid[23][0] = 20

#game

running = True

while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        if evt.type == MOUSEBUTTONUP:
            if evt.button == 1:
                click = True
                if menu == "home":
                    if playRect.collidepoint(mx,my):
                        grid = gen(grid)
                        screen.blit(battlemenu,(0,0))
                        bMenuBack = screen.subsurface(Rect(120,755,740,30)).copy()
                        drawMap(grid)
                        menu = "battle"
                        stats[0] += 1
                    if instructionsRect.collidepoint(mx,my):
                        menu = "instructions"
                    if statsRect.collidepoint(mx,my):
                        menu = "stats"
                    if quitRect.collidepoint(mx,my):
                        running = False
                if menu in ["instructions","stats"]:
                    if backRect.collidepoint(mx,my):
                        menu = "home"
                    


    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    
    if menu == "home":
        screen.blit(home,(0,0))
        screen.blit(buttons,(500,250))
        if mb[0] == 1:
            if playRect.collidepoint(mx,my):
                screen.blit(playclick,(500,250))
            if instructionsRect.collidepoint(mx,my):
                screen.blit(instructionsclick,(500,310))
            if statsRect.collidepoint(mx,my):
                screen.blit(statsclick,(500,370))
            if quitRect.collidepoint(mx,my):
                screen.blit(quitclick,(500,430))



    if menu == "battle":
        treeGrow()
        

        screen.blit(bMenuBack,(120,755))
        screen.blit(cancelbutton,(10,600))
        screen.blit(nextTurnButton,(10,700))
        screen.blit(attackButton,(10,650))
        
        if turns%2 == 1:
            goldAmm = text.render(str(goldPlayerOne), True, (0,0,0))
        else:
            goldAmm = text.render(str(goldPlayerTwo), True, (0,0,0))
        screen.blit(goldAmm,(440,760))

        numturn = text.render(str(turns), True, (0,0,0))
        screen.blit(numturn,(590,757))           
        
        buyCharacter()
        drawMap(grid)
        drawCharacters(charGrid)
        cutTree(selectedPlayer[0],selectedPlayer[1],selectedPlayer[2])
        
        if 120<mx<120+24*40 and 0<my<40*18:
            if click == True and selectedPlayer[0] == 0:
                selectedPlayer = playerSelect(charGrid)
                click = False
            charMove(selectedPlayer[0],selectedPlayer[1],selectedPlayer[2])
        if attackFlag:
            attack(selectedPlayer[0],selectedPlayer[1],selectedPlayer[2])

        if mb[0] == 1:
            if cancelRect.collidepoint(mx,my):
                selectedPlayer=list(selectedPlayer)
                selectedPlayer[0] = 0
                attackFlag = False
                
            if attackRect.collidepoint(mx,my) and selectedPlayer[0] != 0:
                attackFlag = True
                    
        possibleMoves(selectedPlayer[0],selectedPlayer[1],selectedPlayer[2])
        draw.rect(screen,(255,0,0),(120 + selectedPlayer[1]*40, selectedPlayer[2]*40,40,40),1)

        if click == True and endTurnRect.collidepoint((mx,my)):
            turns +=1
            
            treeTurn = map(lambda x:x+1, treeTurn)
            teamOneAttackersMoves = map(lambda x:2, teamOneAttackersMoves)
            teamTwoAttackersMoves = map(lambda x:2, teamTwoAttackersMoves)
        
                
            selectedPlayer=list(selectedPlayer)
            selectedPlayer[0] = 0


        checkDeath()
        if running:
            draw.rect(screen,(255,10,20),(124,760,int(2.27 * (100 - teamOneAttackersHealth[0])),22))
            draw.rect(screen,(255,10,20),(856,760,int(2.27 * (100 - teamTwoAttackersHealth[0])),22))
         
    click = False
    display.flip()

    if menu == "instructions":
        screen.blit(instructionsscreen,(0,0))
        screen.blit(backButton,(900,100))
                    
    if menu == "stats": 
        screen.blit(statsscreen,(0,0))
        screen.blit(backButton,(900,100))
        statistics = ["Total Games Played: ", "Most Amount of Turns: ", "Team One Total Gold Collected: ", "Team Two Total Cash Collected: ", "Total Trees Cut: ", "Team Two Wins: ", "Team One Wins: "]
        statsFont = font.SysFont("Times New Roman", 40)
        for i in range(len(statistics)):
            line = statsFont.render(statistics[i] + str(stats[i]), True, (0,0,0))
            screen.blit(line,(350,200 + 50 * i))
        

if menu == "battle":    
    if stats[1]<turns:
        stats[1] = turns

    
updateStats()
    
quit()
