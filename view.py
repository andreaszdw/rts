#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyglet.gl import *

#-------------------------------------------------------------------------------
class View(object):

    #-------------------------------------------------------
    def __init__(self, x, y, win, maxScale, minScale):

        # zentrum der ansicht
        self.x = x
        self.y = y

        # skalierungsfaktor
        self.scale = 1

        # skalierung min/max
        self.maxScale = maxScale
        self.minScale = minScale

        # für berechnungen damit die sicht schneller zentriert werden kann
        self.winWidth = win.width
        self.winHeight = win.height
        self.winWidthHalf = self.winWidth//2
        self.winHeightHalf = self.winHeight//2


    #-------------------------------------------------------
    def setXY(self, x, y):

        self.x = x
        self.y = y


    #-------------------------------------------------------
    def resize(self, win):

        # für berechnungen, damit die sicht schneller zentriert werden kann
        self.winWidth = win.width
        self.winHeight = win.height
        self.winWidthHalf = self.winWidth//2
        self.winHeightHalf = self.winHeight//2


    #-------------------------------------------------------
    def addScale(self, scale):

        self.scale += scale

        if self.scale < self.minScale:
            self.scale = self.minScale

        if self.scale > self.maxScale:
            self.scale = self.maxScale


    #-------------------------------------------------------
    def getViewRect(self):
        ''' liefert das aktuelle viewRect zurück'''

        return self.x-self.winWidthHalf*self.scale, self.y-self.winHeightHalf*self.scale, self.x+self.winWidthHalf*self.scale, self.y+self.winHeightHalf*self.scale

    #-------------------------------------------------------
    def getMaxViewRectSize(self):
        '''liefert die Größe des maximalen viewRect'''

        return self.winWidth*self.maxScale, self.winHeight*self.maxScale

    #-------------------------------------------------------
    def getMaxViewRect(self):
        '''liefert das maximale viewRect'''

        tmpMaxSizeX, tmpMaxSizeY = self.getMaxViewRectSize()
        tmpHalfMaxSizeX = tmpMaxSizeX//2
        tmpHalfMaxSizeY = tmpMaxSizeY//2
        return int(self.x-tmpHalfMaxSizeX), int(self.y-tmpHalfMaxSizeY), int(self.x+tmpHalfMaxSizeX), int(self.y+tmpHalfMaxSizeY)


    #-------------------------------------------------------
    def getBottomLeft(self):

        return self.x-self.winWidthHalf*self.scale, self.y-self.winHeightHalf*self.scale

    #-------------------------------------------------------
    def camera(self):

        #zoomen
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.winWidth*self.scale,
                   0, self.winHeight*self.scale)

        # auf view setzen
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.x-self.winWidthHalf*self.scale, self.y-self.winHeightHalf*self.scale, +1.0,
                  self.x-self.winWidthHalf*self.scale, self.y-self.winHeightHalf*self.scale, -1.0,
                  0.0, 1.0, 0.0)

    #-------------------------------------------------------
    def reset(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.winWidth, 0, self.winHeight)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
