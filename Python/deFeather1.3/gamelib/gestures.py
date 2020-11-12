from myconstants import *


class Gesture:
    no_wind_gesture_zone = 10

    def __init__(self):
        #variables to keep track of the direction of stroke
        self.start_xy = (-1, -1)
        self.end_xy = (-1, -1)
        self.length = 0
    
    def setStart(self, coord = (-1, -1)):
        self.start_xy = coord
    
    def setEnd(self, coord = (-1, -1)):
        self.end_xy = coord

    def isValidData(self):
        #verify if the currently available data is valid
        if(self.start_xy[0] < 0 or self.end_xy[0] < 0):
            return False
        return True

    def resetData(self):
        self.start_xy = (-1, -1)
        self.end_xy = (-1, -1)
        self.length = 0

    def getLength(self):
        return self.length

    def getGesture(self):
        #caliculate the gesture and reset the values.
        if(not(self.isValidData())):
            return GESTURE_NONE
        
        xdiff = self.end_xy[0] - self.start_xy[0]
        ydiff = self.end_xy[1] - self.start_xy[1]

        #check for various gestures
        if(abs(xdiff) > abs(ydiff)):#left or right gesture
            self.length = abs(xdiff)
            if abs(xdiff) < self.no_wind_gesture_zone:
                return GESTURE_PAINT
            if(xdiff < 0): #right to left motion of mouse
                return GESTURE_LEFT 
            else:
                return GESTURE_RIGHT
        else:
            self.length = abs(ydiff)
            if abs(ydiff) < self.no_wind_gesture_zone:
                return GESTURE_PAINT
            if(ydiff < 0): #down to up motion of mouse
                return GESTURE_UP
            else:
                return GESTURE_DOWN 
