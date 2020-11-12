#!/usr/bin/env python
import os, pygame, operator, math
import operator
from copy import copy
from pygame.locals import *
from logging import debug as log_debug
from constants import *
from pygame.sprite import LayeredDirty

def vector_Sum(v1, v2):
    return [v1[0]+v2[0], v1[1]+v2[1]]

class Background_Manager:
    def set_screen(self, screen, background=None): #always background unless changing resolutions
        self.screen = screen
        if background:
            self.image = background
        self.rect = self.image.get_rect()
        self.offset = [0,0]
        self.dirty = 1
        self.newlyExposedArea = [None, None]
        screenRect = self.screen.get_rect()
        self.srcRect = Rect(self.offset[0], self.offset[1],
                            screenRect.width, screenRect.height)

    def BlitSelf(self, surface):
        self.srcRect.topleft =  self.offset[0], self.offset[1]
        surface.blit(self.image, (0,0), self.srcRect)

    def GetBgSurface(self, drawToSurface, dirtyRect):
        srcRect = dirtyRect.move(0,0)
        srcRect.topleft = vectorSum(srcRect.topleft, self.offset)
        drawToSurface.blit(self.image, dirtyRect, srcRect)

    def RectIsOutOfBounds(self, physRect):
        result = []
        if physRect.left > self.rect.right:
            result.append('right')
        if physRect.top > self.rect.bottom:
            result.append('bottom')
        if physRect.right < self.rect.left:
            result.append('left')
        if physRect.bottom < self.rect.top:
            result.append('top')
        return result

    def GetOffsetScreenRect(self):
        screenRect = self.screen.get_rect().move( self.offset[0],
                                                  self.offset[1] )
        return screenRect

    def GetDisplayCenter(self, physRect):
        return (physRect.centerx - self.offset[0], 
                physRect.centery - self.offset[1] )

    def SpriteIsVisible(self, physRect):
        screenRect = self.GetOffsetScreenRect()
        return screenRect.colliderect(physRect)

    def CalculateNewlyExposedArea(self, oldOffset):
        oScreenRect = self.GetOffsetScreenRect()
        xBlockWidth = abs(self.offset[0] - oldOffset[0])

        if oldOffset[0] < self.offset[0]:
            xPos = oScreenRect.right - xBlockWidth 
        else:
            xPos = self.offset[0]
        xBlock = Rect( xPos,
                       self.offset[1],
                       xBlockWidth,
                       oScreenRect.height )

        yBlockHeight = abs(self.offset[1] - oldOffset[1])

        if oldOffset[1] < self.offset[1]:
            yPos = oScreenRect.bottom - yBlockHeight
        else:
            yPos = self.offset[1]
        yBlock = Rect( self.offset[0],
                       yPos,
                       oScreenRect.width, 
                       yBlockHeight )

        self.newlyExposedArea = [xBlock, yBlock]

    def NotifyPlayerSpritePos(self, physRect):
        s_o = self.offset
        oldOffset = copy(s_o)

        oScreenRect = self.GetOffsetScreenRect()

        avatarLeft = int(physRect.left)
        avatarRight = int(physRect.right)
        avatarTop = int(physRect.top)
        avatarBottom = int(physRect.bottom)

        leftScrollTrig   = oScreenRect.centerx - 100
        rightScrollTrig  = oScreenRect.centerx + 100
        topScrollTrig    = oScreenRect.centery - 100
        bottomScrollTrig = oScreenRect.centery + 100

        minXOffset = 0
        maxXOffset = self.rect.right - oScreenRect.width
        minYOffset = 0
        maxYOffset = self.rect.bottom - oScreenRect.height

        if avatarRight > rightScrollTrig \
          and s_o[0] < maxXOffset:
            s_o[0] = min( maxXOffset,
                          s_o[0] + avatarRight - rightScrollTrig )
            self.dirty = 1

        elif avatarLeft < leftScrollTrig \
          and s_o[0] > minXOffset:
            s_o[0] = max( minXOffset,
                          s_o[0] + avatarLeft - leftScrollTrig )
            self.dirty = 1

        if avatarBottom > bottomScrollTrig \
          and s_o[1] < maxYOffset:
            s_o[1] = min( maxYOffset,
                          s_o[1] + avatarBottom-bottomScrollTrig )
            self.dirty = 1

        elif avatarTop < topScrollTrig \
          and s_o[1] > minYOffset:
            s_o[1] = max( minYOffset,
                          s_o[1] + avatarTop - topScrollTrig )
            self.dirty = 1

        if self.dirty:
            self.CalculateNewlyExposedArea(oldOffset)

        return self.GetDisplayCenter(physRect)
        
class Scroll_Group(LayeredDirty):
    def __init__(self, bgMangr):
        LayeredDirty.__init__(self)
        self.bgMangr = bgMangr
        self.displayRects = {}

    def add_internal(self, sprite, layer=None):
        LayeredDirty.add_internal(self, sprite, layer)
        center = self.bgMangr.GetDisplayCenter(sprite.rect)
        self.displayRects[sprite] = sprite.rect.move(0,0)
        self.displayRects[sprite].center = center

    def remove_internal(self, sprite):
        LayeredDirty.remove_internal(self, sprite)
        del self.displayRects[sprite]

    def update_helper(self, s):
        center = self.bgMangr.GetDisplayCenter(s.rect)
        self.displayRects[s].center = center
        bounds = self.bgMangr.RectIsOutOfBounds(s.rect)
        if bounds and hasattr(s, 'NotifyOutOfBounds'):
            s.NotifyOutOfBounds(bounds)
        if self.bgMangr.dirty and hasattr(s, 'NotifyDirtyScreen'):
            s.NotifyDirtyScreen(self.bgMangr)
    
    def update(self, *args, **kwargs):
        for s in self.spritedict.keys():
            self.displayRects[s] = s.rect.move(0,0)
            s.update(*args, **kwargs)
            self.update_helper(s)

    def clear(self, drawToSurface):
        if self.bgMangr.dirty:
            return
        LayeredDirty.clear(self, drawToSurface, 
                             self.bgMangr.GetBgSurface)

    def draw(self, surface):
        if self.bgMangr.dirty:
            self.bgMangr.BlitSelf(surface)
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append

        sorted_sprites = sorted(spritedict.items(), key=lambda x: x[0].depth)
        sorted_sprites = sorted(sorted_sprites, key=lambda x: x[0]._layer)
        sorted_sprites = sorted(sorted_sprites, key=lambda x: x[0].elevation)

        for s, r in iter(sorted_sprites):
            if s.visible == 1 and s.dirty:
                newrect = surface_blit(s.image, 
                                        self.displayRects[s])
                if r == 0:
                    dirty_append(newrect)
                else:
                    if newrect.colliderect(r):
                        dirty_append(newrect.union(r))
                    else:
                        dirty_append(newrect)
                        dirty_append(r)
                if s.dirty == 1: s.dirty = 0
                spritedict[s] = newrect
        if self.bgMangr.dirty:
            return [self.bgMangr.rect]
        else:
            return dirty

    def get_sprite(self, loc):
        spritedict = self.spritedict
        for each in spritedict:
            if each.pos == loc:
                return each
        return False