#This file is part of AwesomeTetris.
#AwesomeTetris is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#AwesomeTetris is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with AwesomeTetris. If not, see <http://www.gnu.org/licenses/>.
#By: James R. Benson

import pygame, random, time, sys, AwesomeTetrisVariables
from pygame.locals import *
from AwesomeTetrisVariables import *

#The "play()" function is the 'core' of the game, and every major method is handled within it
#during gameplay!
def play():
    #setting up tbe initial game elements before hitting the while loop
    playArea = clearGame()
    moveInterval = SuperTime()
    fallInterval = SuperTime()
    lvl = Determinelvl()
    fallingSpeed = FallingSpeed(lvl)
    itemInPlay = createNewShape()
    soonToBeboardItem = createNewShape()

    while (True):
        #If we have a shape on the board continue, otherwise create a new item :)
        if (itemInPlay == 0):
            itemInPlay = soonToBeboardItem
            soonToBeboardItem = createNewShape()
            fallInterval = SuperTime()
            
            #If the shape on the board is within the game bounds we're good!
            if (MoveCheck(itemInPlay, playArea, 0, 0) == 0):
                return
		#Always check to see with "isQuit()" if the player has hit ESC before continueing on with item movement or board logic!
        isQuit()
        boardItemMovement(playArea, itemInPlay)
        
        #If player presses the down arrow increment the shape's Y coordinate to move it down, and only if it is within the playArea!!!!
        if ((keyCheck == 'Down' and MoveCheck(itemInPlay, playArea, 0, 1) == 1)):
            itemInPlay['boardItemY'] += 1
            #Grabbing current time to store in the moveInterval so we're within the Clock cycle of the game.
            #This keeps the down movement of each piece in check.
            moveInterval = SuperTime()

        if ((SuperTime() - fallInterval) > fallingSpeed):
            if (MoveCheck(itemInPlay, playArea,0, 1) == 0):
                addToPlayArea(playArea, itemInPlay)
                global curScore
                curScore += finishLine(playArea)
                lvl = Determinelvl()
                fallingSpeed = FallingSpeed(lvl)
                itemInPlay = 0
            else:
                itemInPlay['boardItemY'] += 1
                fallInterval = SuperTime()
        
        #Here we paint all the shiny stuff on the board :).
        #Keep in mind that the background is a jpeg, so doing it in the wrong spot will cause a cpu strain issue!!
        PaintBackground()
        drawPlayArea(playArea)
        drawStatus(lvl)
        createNextboardItemText()
        createNextPlayBoardItem(soonToBeboardItem)
        drawInstructions()
        
        #As long as there is a shape in play, draw it. Otherwise we'd be trying to draw something that doesn't exist anymore.
        if (itemInPlay != 0):
            drawboardItem(itemInPlay)

        #refresh the screen display to show the changes made up to this point to the draw buffer.
        pygame.display.update()
        
        #This sets the overall cycle time of the game. Everything time based such as movement, and drawing speed, is connected to this.
        gameClock.tick(30)
        
#The "boardItemMovement" method handles shape movement logic on the board itself.
def boardItemMovement(playArea, itemInPlay):
    #This allows us to loop through any events currently being passed such as key presses etc.
    #With this we can get key presses :)!
    for event in pygame.event.get():
        #Keep in mind that key events are case sensitive, and trying to use them as lowercase won't work.
        
        #"KEYDOWN" is the event TYPE, which is the event type and not event key itself, is the initial depression of a key.
        #This means that once you let up on the key the event has ended, and "KEYUP" is fired.
        if (event.type == KEYDOWN):
            #when left arrow is pressed, move left
            if ((event.key == K_LEFT) and MoveCheck(itemInPlay, playArea, -1, 0) == 1):
                itemInPlay['boardItemX'] = itemInPlay['boardItemX'] - 1
            #when right arrow is pressed move right
            elif ((event.key == K_RIGHT) and MoveCheck(itemInPlay, playArea, 1, 0) == 1):
                itemInPlay['boardItemX'] = itemInPlay['boardItemX'] + 1
            #when up arrow is pressed flip shape, if it can be flipped
            elif (event.key == K_UP):
                itemInPlay['shape'] = (itemInPlay['shape'] + 1) % len(possibleShapes[itemInPlay['templateboardItem']])
                if (MoveCheck(itemInPlay, playArea, 0, 0) == 0):
                    itemInPlay['shape'] = (itemInPlay['shape'] - 1) % len(possibleShapes[itemInPlay['templateboardItem']])
            #when the down arrow is pressed we move the shape down the board adding onto the Y coordinate
            elif (event.key == K_DOWN):
                keyCheck = 'Down'
                if MoveCheck(itemInPlay, playArea, 0, 1) == 1:
                    itemInPlay['boardItemY'] = itemInPlay['boardItemY'] + 1
                moveInterval = SuperTime()
            #when spacebar is pressed when drop the piece onto the next empty space that can take a shape
            elif (event.key == K_SPACE):
                keyCheck = ''
                for i in range(1, 25):
                    if (MoveCheck(itemInPlay, playArea, 0, i) == 0):
                        break
                itemInPlay['boardItemY'] += i - 1
        #The "KEYUP" event type is when you RELEASE a key from being pressed. This is great for allowing events after the fact.
        #This allows us to fire something without interrupting it if we want it to break if another key is pressed, or if it
        #is pressed again. This means that if we put this on the "KEYDOWN" event it'd always break itself on-release
        #since the KEYUP event is a completely seperate fire. Meaning we'd never be able to pause the game if we used KEYDOWN, lol.
        elif (event.type == KEYUP):
            if (event.key == K_p):
                drawPauseScreen()
                Pause()

        
#Get the current CPU time.
def SuperTime():
    return time.time()
    
#Drawing the Background with my awesome images :D
def PaintBackground():
    gameDisplay.blit(myImage, myImageRect)
    
#Using a while loop to wait, which simulates a pause event.
#This is by far the most popular method to pause something in most languages.
#Notice we use the gameClock for this event.
def Pause():
    while PauseCheck() == 0:
        pygame.display.update()
        gameClock.tick()

#Drawing my silly pause screen that I cut up and redid based on a popular Simpsons background.
def drawPauseScreen():
    myImage = pygame.image.load("TetrisPause.jpg")
    myImageRect = myImage.get_rect()
    gameDisplay.fill(black)
    gameDisplay.blit(myImage, myImageRect)
    pygame.display.flip()
	
#Here we're checking for ANY key event to unpause the game.
def PauseCheck():
    #Check before doing any logic to see if someone hits ESC while the game is Paused.
    #Otherwise they're trapped until they unpause the game!
    isQuit()
    for event in pygame.event.get([KEYUP, KEYDOWN]):
        if (event.type == KEYDOWN):
            continue
        return 1
    return 0

#Here is the logic for checking on key events for ESC key
def isQuit():
    #This is pygame's method for checking to see if you hit the 'X' at the upper right.
    #All games made with PyGame should include both of these!
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    #AGain, looking for the esc key!
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
            
        pygame.event.post(event)
	
#Checking to see what level you're on based on the current Score.
def Determinelvl():
    global curScore
    lvl = int(curScore / 100)
    return lvl
	
#This is where the game determines a shape's falling speed.
#Notice that the higher level you're on, which is based on score, the faster the drop rate!
def FallingSpeed(lvl):
	speed = 0.50 - (lvl * 0.0125) #Roughly lvl 36 is when it gets almost impossible!
	return speed

#This is where we actually create the new shape, and then return it to be drawn.
#Please notice that "newBoardItem" is actually a dynamicObject that uses a "Key Value Pair" assignment.
#This allows you to ask for a "key" such as "shape" from the object, and have a value return.
#Also note that "Lists", or "Arrays", are actually dynamicArrays in Python. So this works out very well :)!
def createNewShape():
    newShape = random.choice(list(possibleShapes.keys()))
    newBoardItem = {'templateboardItem': newShape, 'shape': random.randint(0, len(possibleShapes[newShape]) - 1), 
				'boardItemX': int(15 / 2) - int(4 / 2), 'boardItemY': -2,'color': random.randint(0, len(colorArray)-1)} #Len gets the length of the array, and -1 since it starts from 0
    return newBoardItem

#Adding a shape to the playArea for collision logic
def addToPlayArea(playArea, itemToDraw):
    for x in range(4):
        for y in range(4):
            if possibleShapes[itemToDraw['templateboardItem']][itemToDraw['shape']][y][x] != '_':
                playArea[x + itemToDraw['boardItemX']][y + itemToDraw['boardItemY']] = itemToDraw['color']

#Clearing the playArea for a new game
def clearGame():
    playArea = []
    for i in range(15):
        playArea.append(['_'] * 25)
    return playArea

#Checking to see if a shape is within the bounds of the game's playArea
def isLegalArea(x, y):
    if (x > -1 and y < 25 and x < 15):
        return 0

#Checking to see if the shape's requested movement is a legal one.
def MoveCheck(boardItem, playArea, curX, curY):
    for x in range(4):
        for y in range(4): 
            boardItemCurrentX = x + boardItem['boardItemX'] + curX
            boardItemCurrentY = y + boardItem['boardItemY'] + curY
            if (boardItemCurrentY < 0 or possibleShapes[boardItem['templateboardItem']][boardItem['shape']][y][x] == '_'):
                continue
            if (isLegalArea(boardItemCurrentX, boardItemCurrentY) != 0):
                return 0
            if (playArea[boardItemCurrentX][boardItemCurrentY] != '_'):
                return 0
    return 1

#Here we're counting the blocks on the X axis to see if any are touching, and then checking to see if an entire X row in the game is full.
def checkForLines(blockY, playArea):
    for x in range(15):
        if (playArea[x][blockY] == '_'):
            return 'No'
    return 'Yes'
    
#using the number of lines destroyed to calculate a bonus score. Otherwise the player is rewarded with 10points for placing a shape.
def CalculateScore(lines):
    return (50 * lines) + 10

#Here we destroy a line if one is complete, and calculating score.
def finishLine(playArea):
    linesFound = 0
    blocksToCheck = 25 - 1
    curScoreCalculated = 0
    
    while (blocksToCheck > -1):
        if (checkForLines(blocksToCheck, playArea) == 'Yes'):
            for blocksToMove in range(blocksToCheck, 0, -1):
                for area in range(15):
                    playArea[area][blocksToMove] = playArea[area][blocksToMove-1]
            for area in range(15):
                playArea[area][0] = '_'
            linesFound += 1
        elif (checkForLines(blocksToCheck, playArea) == 'No'):
            blocksToCheck -= 1		
    curScoreCalculated = CalculateScore(linesFound)
    return curScoreCalculated

#Pygame needs coordinates to be converted into pixels so we can have a proper screen assignment for movement, drawing etc.
#Almost all pygames need this if you're moving stuff by hand on the green with keypresses, etc.
def pixelConvert(backGround_X, backGround_Y):
    xy = (245 + (backGround_X * 20)), (80 + (backGround_Y * 20))
    return xy

#Here we're drawing a shape to be used :)!
def createboardItem(color, pixelx=None, pixely=None):
    if (color == '_'):
        return
    pygame.draw.rect(gameDisplay, colorArray[color], (pixelx + 1, pixely + 1, 20 - 1, 20 - 1))
	
#Here we're actually drawing the background for the playArea itself
def createplayAreaBackGround(backGround_X, backGround_Y, color):
    if (color == '_'):
        return
    pixelx, pixely = pixelConvert(backGround_X, backGround_Y)
    pygame.draw.rect(gameDisplay, colorArray[color], (pixelx + 1, pixely + 1, 20 - 1, 20 - 1))

#Drawing the splash screen at start!
#Do you like the background of a Tetris Heart I found online that I cut up and recropped :)?
def drawTitleScreen():
    myImage = pygame.image.load("tetrisBG.jpg")
    myImageRect = myImage.get_rect()
    gameDisplay.fill(black)
    gameDisplay.blit(myImage, myImageRect)
    pygame.display.flip()
    drawTitleScreenText()

#Drawing the playArea itself for the game
def drawPlayArea(playArea):
    pygame.draw.rect(gameDisplay, (255,255,255), (241, 76, 307, 508), 6)
    pygame.draw.rect(gameDisplay, (0,0,0), (245, 80, 300, 501))
    for x in range(15):
        for y in range(25):
            createplayAreaBackGround(x, y, playArea[x][y])


#This is a helper method I wrote to draw the score and level information.
#Please note I did this quick & dirty just to get it down. 
#If i had time, i'd combine them all into one method.
def drawStatus(lvl):
    pygame.draw.rect(gameDisplay, (255,255,255), (28, 28, 163, 43), 2)
    pygame.draw.rect(gameDisplay, (0,0,0), (30, 30, 160, 40))
    global curScore
    
    curScoreTextLoc = (110, 50)
    drawcurScoreText(curScoreTextLoc, curScore)

    lvlTextLoc = (680, 50)
    drawlvlText(lvlTextLoc,lvl)

#This is where I added the "Awesome Tetris!!" text below the TetrisHeart on the splash screen.
#I'm essentially just drawing the background behind, and the text ontop with a fixed XY coordinate.
def drawTitleScreenText():
    titleScreenFont = pygame.font.Font('starcraft.ttf', 32)
    TitleScreenText = titleScreenFont.render('Awesome Tetris!', True, (255, 0, 0))
    titleRect = TitleScreenText.get_rect()
    titleRect.center = (410,460)
    gameDisplay.blit(TitleScreenText, titleRect)
    
#When the game ends, check the score, output a funny Dr.P quote, and make sure to reset the score for the next game ;)!
def drawGameOverText():
    text = 'Score: %s' % curScore
    if (curScore >= 2000):
        text = 'Fantastic Job People!'
    elif (curScore >= 1000):
        text = 'Getting Better People!'
    elif (curScore >= 0):
        text = 'Come On People, This Is Trivial!'
    titleScreenFont = pygame.font.Font('starcraft.ttf', 32)
    TitleScreenText = titleScreenFont.render(text, True, (255, 0, 0))
    titleRect = TitleScreenText.get_rect()
    titleRect.center = (410,300)
    gameDisplay.blit(TitleScreenText, titleRect)
    global curScore
    curScore = 0
	
#Just drawing the text itself concatinating the score's value with the text
def drawcurScoreText(curScoreLoc,curScore):
    mycurScore = gameDefaultFont.render('Score: %s' %curScore, True, (255, 255, 0))
    curScoreRect = mycurScore.get_rect()
    curScoreRect.center = curScoreLoc
    gameDisplay.blit(mycurScore, curScoreRect)
	
#Again, just drawing the text itself, and the rectangle to store it for drawing.
def drawlvlText(textLoc,lvl):
    lvlSurf = gameDefaultFont.render('lvl: %s' %lvl, True, (255, 255, 0))
    lvlRect = lvlSurf.get_rect()
    lvlRect.center = textLoc
    pygame.draw.rect(gameDisplay, (0,0,0), (605, 30, 138, 41))
    pygame.draw.rect(gameDisplay, (255,255,255), (605, 30, 140, 42), 2)
    gameDisplay.blit(lvlSurf, lvlRect)

#This is where we actually draw the shapes themselves calling the CreateBoardItem method.
def drawboardItem(boardItem): 
    itemX, itemY = pixelConvert(boardItem['boardItemX'], boardItem['boardItemY'])
    for x in range(4):
        for y in range(4):
            if (possibleShapes[boardItem['templateboardItem']][boardItem['shape']][y][x] != '_'):
                createboardItem(boardItem['color'], itemX + (x * 20), itemY + y * 20)

#Here we draw the "Next" piece to be drawn onto the board itself using the createBoardItem method.
def createNextPlayBoardItem(boardItem):
    for x in range(4):
        for y in range(4):
            if (possibleShapes[boardItem['templateboardItem']][boardItem['shape']][y][x] != '_'):
                createboardItem(boardItem['color'], 628 + (x * 20), (y * 20)+230)
    
#Text for the next shape :)
def createNextboardItemText():
    drawText = gameDefaultFont.render('Next Shape', True, (255, 255, 0))
    objectNext = drawText.get_rect()
    objectNext.center = (680, 210)
    pygame.draw.rect(gameDisplay, (0,0,0), (560, 190, 228, 161))
    pygame.draw.rect(gameDisplay, (255,255,255), (560, 190, 230, 162), 2)
    gameDisplay.blit(drawText, objectNext)
    
    
#Finally, this is just handling the text for the instructions on the left!
def drawInstructions():
    normalFont = pygame.font.Font('starcraft.ttf', 10)
    
    drawText = gameDefaultFont.render('Instructions', True, (255, 255, 0))
    newTextObject = drawText.get_rect()
    newTextObject.center = (120, 210)
    
    drawText1 = normalFont.render('Use Arrow Keys To Move', True, (255, 255, 255))
    newTextObject1 = drawText1.get_rect()
    newTextObject1.center = (110, 240)
    
    drawText2 = normalFont.render('Spacebar Drops The Shape', True, (255, 255, 255))
    newTextObject2 = drawText1.get_rect()
    newTextObject2.center = (110, 270)
    
    drawText3 = normalFont.render('Hit "P" to Pause', True, (255, 255, 255))
    newTextObject3 = drawText1.get_rect()
    newTextObject3.center = (110, 300)
    
    drawText4 = normalFont.render('Hit ESC to Exit', True, (255, 255, 255))
    newTextObject4 = drawText1.get_rect()
    newTextObject4.center = (110, 330)
    
    pygame.draw.rect(gameDisplay, (0,0,0), (10, 190, 213, 161))
    pygame.draw.rect(gameDisplay, (255,255,255), (10, 190, 215, 162), 2)
    gameDisplay.blit(drawText, newTextObject)
    gameDisplay.blit(drawText1, newTextObject1)
    gameDisplay.blit(drawText2, newTextObject2)
    gameDisplay.blit(drawText3, newTextObject3)
    gameDisplay.blit(drawText4, newTextObject4)
