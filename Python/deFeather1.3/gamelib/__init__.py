import pygame
import sys
from pygame.locals import *

import data

hasSounds = True

pygame.init() #initialize this some where else?
try :
    pygame.font.init() #initilize the font module
except:
    print "Could not initialize fonts"
    sys.exit(0)
try :
    pygame.mixer.init() #initialize the sounds
except:
    print "Could not initialize sounds. Continueing without them"
    hasSounds = False

seffects = {}
if hasSounds:
    seffects['squish'] = pygame.mixer.Sound(data.filepath('squish.ogg'))
    seffects['wind'] = pygame.mixer.Sound(data.filepath('wind.ogg'))
    seffects['gulp'] = pygame.mixer.Sound(data.filepath('gulp.ogg'))
    pygame.mixer.music.load(data.filepath('background.ogg')) 
    pygame.mixer.music.set_volume(0.5)

amb_imgs = []
amb_imgs.append(data.loadImage("building2_amb.png"))
amb_imgs.append(data.loadImage("building3_amb.png"))
amb_imgs.append(data.loadImage("building4_amb.png"))
amb_imgs.append(data.loadImage("building5_amb.png"))

det_imgs = []
det_imgs.append(data.loadImage("building2_det.png"))
det_imgs.append(data.loadImage("building3_det.png"))
det_imgs.append(data.loadImage("building4_det.png"))
det_imgs.append(data.loadImage("building5_det.png"))

feather_img = []
feather_img.append(data.loadImage("feather0.png"))
feather_img.append(data.loadImage("feather1.png"))
feather_img.append(data.loadImage("feather2.png"))
feather_img.append(data.loadImage("feather1.png"))
feather_img.append(feather_img[0])
feather_img.append(data.loadImage("feather3.png"))
feather_img.append(data.loadImage("feather4.png"))
feather_img.append(data.loadImage("feather3.png"))

grnd_img = data.loadImage("ground.png")
grass_img = data.loadImage("grass_amb.png")

vwalk = []
vwalk.append(data.loadImage("walk2.png"))
vwalk.append(data.loadImage("walk1.png"))
vwalk.append(vwalk[0])
vwalk.append(data.loadImage("walk3.png"))

vshoot = []
vshoot.append(data.loadImage("shoot1.png"))

vfly = []
vfly.append(data.loadImage("flyenemy.png"))

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

splash_imgs = []
splash_imgs.append(data.loadImage("splash1.png"))
splash_imgs.append(data.loadImage("splash2.png"))
splash_imgs.append(data.loadImage("splash3.png"))

wind_imgs = []
wind_imgs.append(data.loadImage("wind1.png"))
wind_imgs.append(data.loadImage("wind2.png"))
wind_imgs.append(data.loadImage("wind3.png"))
