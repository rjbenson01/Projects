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

import pygame, random, time, sys, AwesomeTetrisTemplates
from pygame.locals import *
from random import randint, uniform
from AwesomeTetrisTemplates import *
from colorsys import hsv_to_rgb

#init Pygame so we can use pygame specific methods!
pygame.init()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~Colors Section!~~~~~~~~~~~~~~~~~~~~~~~~~~~~
black = (0, 0, 0)
colorArray = []
for x in range(50):
    # Select random color
    h = uniform(1, 380) 
    s = uniform(1, 1)
    v = uniform(1, 1)

    r, g, b = hsv_to_rgb(h, s, v)

    # Convert to 0-1 range for HTML output
    r, g, b = [x*255 for x in (r, g, b)]
    newColor = (r, g, b)
    colorArray.append(newColor)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~Colors Section!~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~Variables Section!~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#game specific stuff
gameDisplay = pygame.display.set_mode((800, 600))
gameClock = pygame.time.Clock()
myImage = pygame.image.load("boardBG.jpg")
myImageRect = myImage.get_rect()
gameDefaultFont = pygame.font.Font('starcraft.ttf', 18)
screenFont = pygame.font.Font('starcraft.ttf', 30)
curScore = 0
keyCheck = ''