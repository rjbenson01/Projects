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

#These are pygame Data Structures that represent layers of a shape.
#Each underscore is an "empty" location. This means nothing is there when pygame determines how to draw a piece of the shape.
#An "x" represents an active filled piece of the shape. So putting an "x" somewhere will draw an active piece of a shape.
#Remember, the size is only 4x4 (8 total blocks if full)!
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~PyGame Template Section#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
t = [['____','__x_','_xxx','____'],['____','__x_','__xx','__x_'],['____','____','_xxx','__x_'],['____','__x_','_xx_','__x_']]
s = [['____','____','__xx','_xx_'],['____','__x_','__xx','___x']]
z =	[['____','____','_xx_','__xx'],['____','__x_','_xx_','_x__']]
box = [['____','____','_xx_','_xx_']]
j =	[['____','_x__','_xxx','____'],['____','__xx','__x_','__x_'],['____','____','_xxx','___x'],['____','__x_','__x_','_xx_']]
L =	[['____','___x','_xxx','____'],['____','__x_','__x_','__xx'],['____','____','_xxx','_x__'],['____','_xx_','__x_','__x_']]
line = [['__x_','__x_','__x_','__x_'],['____','____','xxxx','____']]

possibleShapes = {'Tee': t, 'Snake': s,'Lemon': L,'Box': box, 'Zed': z,'Jay': j,'Line': line}
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~PyGame Template Section#~~~~~~~~~~~~~~~~~~~~~~~~~~~~
