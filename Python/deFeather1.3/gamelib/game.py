import pygame
import random
import ConfigParser
from pygame.locals import *

from myconstants import *
import gestures
import gamelib
import renderer
import data
import menu
from feather import *
from building import *

class Enemy:
    WALKING = 0
    SHOOTING = 1    
    walkSpeed = 4
    def __init__(self, pos = (0, 0), vel = (0, 0), color = (255, 255, 255)):
        self.x = pos[0] 
        self.y = pos[1]
        self.vx = vel[0]
        self.vy = vel[1]
        self.mode = Enemy.WALKING
        self.color = color
        self.curframe = 0
        size = gamelib.vwalk[0].get_size()
        #magic number 2 to get rid of the artifact at bottom caused due to diff in sizes of images
        self.colorplane = pygame.surface.Surface((size[0], size[1]-2), 0, gamelib.vwalk[0])
        self.images = gamelib.vwalk
        self.kill = False

    def update(self):
        if self.mode == Enemy.WALKING:
            self.x += self.vx
            self.y += self.vy
            if self.x < 0 or self.x+self.images[0].get_size()[0] > renderer.getWidth():
                self.vx = -self.vx
            if abs(self.vx) > 0:
                self.curframe += 1
                self.curframe %= len(self.images)

    def setMode(self, mode):
        if self.mode == mode:
            return
        self.mode = mode
        if mode == Enemy.SHOOTING:
            self.colorplane = pygame.surface.Surface(gamelib.vshoot[0].get_size(), 0, gamelib.vshoot[0])
            self.images = gamelib.vshoot
            self.curframe = 0
        elif mode == Enemy.WALKING:
            self.vx = Enemy.walkSpeed 
            size = gamelib.vwalk[0].get_size()
            self.colorplane = pygame.surface.Surface((size[0], size[1]-2), 0, gamelib.vwalk[0])
            self.images = gamelib.vwalk
            self.curframe = 0
                    
    def render(self):
#        if self.mode == Enemy.WALKING:
        tmp = self.images[self.curframe]
        if self.vx < 0:
            tmp = pygame.transform.flip(self.images[self.curframe], 1, 0)
        self.colorplane.fill(self.color)
        self.colorplane.blit(tmp, (0, 0), None, BLEND_RGBA_MULT)
        renderer.drawImage(self.colorplane, (self.x, self.y))
        
class FlyingEnemy(Enemy):
    def __init__(self, pos, vel=(5, 0)):
        Enemy.__init__(self, pos, vel)
        self.images = gamelib.vfly
        size = self.images[0].get_size()
        self.colorplane = pygame.surface.Surface(size, 0, self.images[0])

#render a splash of color on screen
class Splash(Enemy):
    def __init__(self, pos, color):
        Enemy.__init__(self, pos, (0, 0), color)
        self.images = gamelib.splash_imgs
        size = self.images[0].get_size()
        self.x = self.x - size[0]/2
        self.y = self.y - size[1]/2
        self.colorplane = pygame.surface.Surface(size, 0, self.images[0])

    def update(self):
        self.curframe += 1
        if self.curframe > 2:
            self.kill = True
        self.curframe %= len(self.images)

#wind trails class since we have only 3 frames for wind as well we don't have to change the update method
class WindStrokes(Splash):
    def __init__(self, pos, gesture_dir):
        Splash.__init__(self, pos, (255, 255, 255))
        self.images = gamelib.wind_imgs
        size = self.images[0].get_size()
        self.x = pos[0] - size[0]/2
        self.y = pos[1] - size[1]/2
        self.angle = 0
#        self.colorplane = pygame.surface.Surface(size, 0, self.images[0])
        if gesture_dir == GESTURE_LEFT:
            self.angle = 180
        elif gesture_dir == GESTURE_UP:
            self.angle = 90
        elif gesture_dir == GESTURE_DOWN:
            self.angle = 270

    def render(self):
        renderer.drawImage(pygame.transform.rotate(self.images[self.curframe], self.angle), (self.x, self.y))

class Game:
    updateInterval = 100 #milli secs
    timeLimit = 120 #* 1000/updateInterval #seconds * 1000/#millisecs
    hudFont = None
    def __init__(self):
        self.gesture = gestures.Gesture()
        self.isDone = False
        self.graphics = renderer.init((800, 600))
        self.feather = Feather()
        self.menu = menu.Menu()
        self.parser = None
        #level specific
        self.time = 0
        self.buildings = []
        self.enemies = []
        self.flyenemies = []
        self.splashes = []
        self.windstrokes = []
        self.level = '' 
        self.score = 0
        self.isLevelOver = False
        sz = gamelib.grass_img.get_size()
        self.grassCP = pygame.surface.Surface(sz, 0, gamelib.grass_img)
        self.skyColor = (123, 123, 123)
        Game.hudFont = pygame.font.Font(pygame.font.get_default_font(), 30)

        pygame.time.set_timer(USEREVENT+1, Game.updateInterval)

    def loadLevel(self, fname):
        #clear the lists of buildings and enemies
        del self.buildings[:]
        del self.enemies[:]
        del self.flyenemies[:]
        del self.splashes[:]
        del self.feather
        del self.windstrokes[:]

        self.skyColor = (123, 123, 123)
        self.grassCP.fill((255, 255, 255))
        self.grassCP.blit(gamelib.grass_img, (0, 0), None, BLEND_RGBA_MULT)
        self.feather = Feather()
        #reset these values
        self.time = 0
        self.level = fname
        self.score = 0
        self.isLevelOver = False
        self.feather.addColor((255, 255, 255))
        #start parsing the file
        self.parser = ConfigParser.ConfigParser()
        fp = open(data.filepath(fname))
        self.parser.readfp(fp)
        fp.close()
        if self.parser.has_section('b2'):
            xcoords = self.parser.get('b2', 'x').split(',')
            for x in xcoords:
                self.buildings.append(Building(int(x), 0))

        if self.parser.has_section('b4'):
            xcoords = self.parser.get('b4', 'x').split(',')
            for x in xcoords:
                self.buildings.append(Building(int(x), 2))

        if self.parser.has_section('b3'):
            xcoords = self.parser.get('b3', 'x').split(',')
            for x in xcoords:
                self.buildings.append(Building(int(x), 1))

        if self.parser.has_section('b5'):
            xcoords = self.parser.get('b5', 'x').split(',')
            for x in xcoords:
                self.buildings.append(Building(int(x), 3))

        #load the enemies at diff locations
        enemy_y = Building.baseLine - gamelib.vwalk[0].get_size()[1]
        enemy_vx = self.parser.getint('walkenemy', 'vx')
        for i in xrange(self.parser.getint('walkenemy', 'num')):
            enemy_x = random.randint(0, renderer.getWidth()-gamelib.vwalk[0].get_size()[0])
            self.enemies.append(Enemy((enemy_x, enemy_y), (enemy_vx, 0), random.choice(gamelib.colors)))
        
        enemy_vx = self.parser.getint('flyingenemy', 'vx')
        for i in xrange(self.parser.getint('flyingenemy', 'num')):
            enemy_y = random.randint(0, renderer.getHeight()/2-gamelib.vfly[0].get_size()[1])
            enemy_x = random.randint(0, renderer.getWidth()-gamelib.vfly[0].get_size()[0])
            self.flyenemies.append(FlyingEnemy((enemy_x, enemy_y), (enemy_vx, 0)))

        if gamelib.hasSounds:            
            pygame.mixer.music.play()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == USEREVENT+1:
                self.time += 1
                self.updateState()
            if event.type == MOUSEBUTTONDOWN:
                self.gesture.setStart(pygame.mouse.get_pos())
            elif event.type == MOUSEBUTTONUP:
                self.gesture.setEnd(pygame.mouse.get_pos())
                #find out what the gesture is only after setting the end
                if self.gesture.isValidData():
                    gesture_direction = self.gesture.getGesture()
                    if gesture_direction == GESTURE_NONE:
                        pass
                    elif gesture_direction == GESTURE_PAINT:
                        #find the location of mouse
                        #find if building in that location overlaps with the  feather.
                        if self.feather.isPointOver(self.gesture.end_xy):
                            self.splashes.append(Splash(pygame.mouse.get_pos(), self.feather.color))
                            #do a reverse looping to avoid the z problem.
                            num_builds = len(self.buildings)
                            while num_builds > 0:
                                building = self.buildings[num_builds-1]
                                if building.isPointOver(self.gesture.end_xy):
                                    self.score += building.updateColor(self.feather.color, self.gesture.end_xy)
                                    self.skyColor = (0, 0, 123)
                                    if gamelib.hasSounds:
                                        gamelib.seffects['squish'].play()
                                    break;
                                num_builds -= 1
                    else:
                        self.feather.setState(gesture_direction, self.gesture.getLength())
                        self.windstrokes.append(WindStrokes(self.gesture.end_xy, gesture_direction))
                        if gamelib.hasSounds:
                            gamelib.seffects['wind'].play()
                    self.gesture.resetData()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    retVal = menu.MessageBox()
                    if retVal == 'newlvl':
                        #self.menu.isDone = False
                        self.menu = menu.Menu()
            elif event.type == QUIT:
                self.isDone = True

    def updateState(self):
        self.feather.update()            

        new_list = []
        for stroke in self.windstrokes:
            stroke.update()
            if not(stroke.kill):
                new_list.append(stroke)
        self.windstrokes = new_list

        
        enemy_size = gamelib.vwalk[0].get_size()
        new_list = []
        for splash in self.splashes:
            splash.update()
            if not(splash.kill):
                new_list.append(splash)
        self.splashes = new_list

        for enemy in self.flyenemies:
            enemy.update()
            size = enemy.colorplane.get_size()
            #lower left point
            x1 = enemy.x
            y1 = enemy.y + size[1]
            x2 = enemy.x + size[0]
            erect = pygame.rect.Rect(enemy.x, enemy.y+3*size[1]/4, size[0], size[1]/4)
            frect = self.feather.getRect() 
            f = self.feather
            #if f.isPointOver((x1,y1)) or f.isPointOver((x2, y1)):
            if frect.colliderect(erect): 
                #show message box for time up
                retVal = menu.MessageBox('Game Over', ['Feather Destroyed', '', '', 'Esc to Main Menu', 'Enter to Restart Level'], (255, 0, 0))
                if retVal == 'continue':
                    #self.menu.isDone = False
                    self.menu = menu.Menu()
                elif retVal == 'newlvl':
                    self.loadLevel(self.level) 


        new_list = []
        for enemy in self.enemies:
            enemy.update()
            #code for handling the feather crushing enemies.
            size = enemy.colorplane.get_size()
            x = enemy.x + size[0]/2
            y = enemy.y + size[1]/2
            erect = pygame.rect.Rect(enemy.x, enemy.y, size[0], size[1])
            frect = self.feather.getRect()
            if frect.colliderect(erect):
            #if self.feather.isPointOver((x, y)) or self.feather.isPointOver((enemy.x, enemy.y)) or self.feather.isPointOver((x+size[0], enemy.y)):
                if self.feather.vy > 0:
                    #self.feather.color = enemy.color
                    self.feather.addColor(enemy.color)
                    enemy.kill = True
                    y = enemy.y + size[1]
                    self.splashes.append(Splash((x, y), enemy.color))
                    #fill grass color (can optimize but light)
                    self.grassCP.fill((0, 255, 0))
                    self.grassCP.blit(gamelib.grass_img, (0, 0), None, BLEND_RGBA_MULT)
                    if gamelib.hasSounds:
                        gamelib.seffects['squish'].play()
                else:
                    self.feather.addColor((255, 255, 255))
            if enemy.kill == True:
                continue
            #code for handling enemy draining color                    
            for building in self.buildings:
                if building.isPointOver((enemy.x+enemy_size[0]/2, enemy.y)):
                    #check if the color is sane as per enemy
                    if not(building.color == (255, 255, 255)):
                        enemy.setMode(Enemy.SHOOTING)
                        enemy.color = building.color 
                        building.updateColor((255, 255, 255), (enemy.x, enemy.y))
                        if gamelib.hasSounds:
                            gamelib.seffects['gulp'].play()
                    else:
                        if not(building.colorPercent < 1):
                            enemy.setMode(Enemy.WALKING)
            new_list.append(enemy)
        self.enemies = new_list

        #the value for tracking the game type
        flag = True
        for building in self.buildings:
            building.update()                                   
            if building.color == (255, 255, 255) or building.colorPercent < 1: 
                flag = False
        
        timeval = self.time * Game.updateInterval / 1000
        if timeval >= self.timeLimit:
           #show message box for time up
           retVal = menu.MessageBox('Game Over', ['Time Up', '', '', 'Esc to Main Menu', 'Enter to Restart Level'], (255, 0, 0))
           if retVal == 'continue':
               #self.menu.isDone = False
               self.menu = menu.Menu()
           elif retVal == 'newlvl':
               self.loadLevel(self.level) 

        if flag and len(self.enemies) == 0:
            self.isLevelOver = True
            ##calculate the score and time
            #show the score and time store them
            #progress to next level
            retVal = menu.MessageBox('Level Cleared', ['Time: '+timeval.__str__()+' sec', \
                        'Score: '+self.score.__str__(), 'Esc to Main Menu', 'Enter to Next Level'], (0, 255, 0))
            self.saveData()
            if retVal == 'continue':
                #self.menu.isDone = False
                self.menu = menu.Menu()
            elif retVal == 'newlvl':
                for i in xrange(len(menu.Menu.levels)):
                    if menu.Menu.levels[i] == self.level:
                        self.loadLevel(menu.Menu.levels[i+1]) 
                        break
                    i += 1

    def saveData(self):
        print "Saving data...", self.time, self.score
        fp = open(data.filepath(self.level), 'w')
        prev_best = self.parser.getint('score', 'maxscore')
        if self.score > prev_best:
            self.parser.set('score', 'maxscore', self.score) 
        prev_time = self.parser.getint('time', 'best')
        timeval = self.time * Game.updateInterval / 1000 #caliculating time in seconds
        if timeval < prev_time:
            self.parser.set('time', 'best', timeval)
        self.parser.write(fp)
        fp.close()

    def renderState(self):
        self.graphics.fill(self.skyColor)
        renderer.drawImage(self.grassCP, (0, Building.baseLine-gamelib.grass_img.get_size()[1]))
        for building in self.buildings:
            building.render()

        for enemy in self.enemies:
            enemy.render()

        for enemy in self.flyenemies:
            enemy.render()

        for splash in self.splashes:
            splash.render()


        self.feather.render() 
        renderer.drawImage(gamelib.grnd_img, (0, renderer.getHeight()-gamelib.grnd_img.get_size()[1]))

        for stroke in self.windstrokes:
            stroke.render()

        renderer.drawImage(Game.hudFont.render('Score: ' + self.score.__str__(), True, (255, 255, 255), (0, 0, 0)), (0, Building.baseLine + 10))
        timeval = self.time * Game.updateInterval / 1000
        renderer.drawImage(Game.hudFont.render('Time: ' + timeval.__str__(), True, (255, 255, 255), (0, 0, 0)), (0, Building.baseLine + 40))
        pygame.display.flip()

    def run(self):
        while not(self.isDone):
            if self.menu.isDone: #main menu done or not?
                self.handleEvents()
                self.renderState()
            else:
                retVal = self.menu.show() #control goes to menu class where event/others are handled
                if retVal == 'exit':
                    self.isDone = True
                elif retVal.endswith('.txt'):
                    self.loadLevel(retVal)

