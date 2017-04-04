#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
#
# playstate.py
#
#------------------------------------------------------------------------------

import pyglet
import math

import view
import infoconsole

#-------------------------------------------------------------------------------
class PlayState(object):

    #-------------------------------------------------------
    def __init__(self):

        self.initialized = False


    #-------------------------------------------------------
    def __del__(self):

        pass


    #-------------------------------------------------------
    def cleanup(self):

        pass

    #-------------------------------------------------------
    def on_select(self):
        pass


    #-------------------------------------------------------
    def init(self, win):

        # test if initialized, not draw before
        self.initialized = False

        # pause
        self.paused = False

        # show infoconsole
        self.infoOn = False

        # shift pressed
        self.lShift = False

        # alt pressed
        self.lAlt = False

        # mouse coordinates
        self.mouseX = 0
        self.mouseY = 0

        self.mouseViewX = 0
        self.mouseViewY = 0

        # scrolling
        self.scrollSpeed = 500
        self.scrollLeftRight = 0
        self.scrollUpDown = 0

        # dragging
        self.drag = False
        self.dragStartX = 0
        self.dragStartY = 0
        self.dragX = 0
        self.dragY = 0

        # view
        self.view = view.View(x=0, y=0, win=win, maxScale=10, minScale=1)

        # scale speed
        self.scaleSpeed = 0.1

        pyglet.gl.glClearColor(0.0, 0.0, 0.0, 1.0)

        self.batch = pyglet.graphics.Batch()
        self.batchUnits = pyglet.graphics.Batch()

        # info console
        self.info = infoconsole.InfoConsole("", x=10, y=win.height-25, width=300)

        self.gameObjects = []

        self.loadLevel()

        # now drawing is allowed
        self.initialized = True

    #-------------------------------------------------------
    def loadLevel(self, level=None):

        pass

    #-------------------------------------------------------
    def key_press(self, win, symbol, modifierers):

        # quit
        if symbol == pyglet.window.key.ESCAPE:
            win.cleanup()

        # toggle fps
        if symbol == pyglet.window.key.F:
            if win.fps:
                win.fps = False
            else:
                win.fps = True

        # toogle fullscreen
        if symbol == pyglet.window.key.F5:
            if win.fullscreen:
                win.set_fullscreen(False)
                self.resizeScreen(win)
            else:
                win.set_fullscreen(True)
                self.resizeScreen(win)

        # toggle pause
        if symbol == pyglet.window.key.P:
            if self.paused:
                self.paused = False
            else:
                self.paused = True

        # info on or off
        if symbol == pyglet.window.key.I:
            if self.infoOn:
                self.infoOn = False
            else:
                self.infoOn = True

        if self.paused:
            return

        # shift
        if symbol == pyglet.window.key.LSHIFT:
            self.lShift = True

        # alt
        if symbol == pyglet.window.key.LALT:
            self.lAlt = True

    #-------------------------------------------------------
    def key_release(self, win, symbol, modifierers):

        if self.paused:
            return

        # shift
        if symbol == pyglet.window.key.LSHIFT:
            self.lShift = False

        # alt
        if symbol == pyglet.window.key.LALT:
            self.lAlt = False

    #-------------------------------------------------------
    def mouse_motion(self, win, x, y, dx, dy):

        self.mouseX = x
        self.mouseY = y
        self.scrollLeftRight = 0
        self.scrollUpDown = 0

        if self.mouseX < 10:
            self.scrollLeftRight = -1

        if self.mouseX > win.width-10:
            self.scrollLeftRight = 1

        if self.mouseY < 10:
            self.scrollUpDown = -1

        if self.mouseY > win.height-10:
            self.scrollUpDown = 1

        self.mouseToViewCoord()

    #-------------------------------------------------------
    def mouse_press(self, win, x, y, button, modifiers):

        if self.paused:
            return

        self.mouseX = x
        self.mouseY = y

        self.mouseToViewCoord() # windowkoordinaten in viewkoordinaten umrechnen


        if button == pyglet.window.mouse.LEFT:

            #dragging
            self.dragStartX = self.mouseViewX
            self.dragStartY = self.mouseViewY

    #-------------------------------------------------------
    def mouse_release(self, win, x, y, button, modifiers):

        if button == pyglet.window.mouse.LEFT:

            self.drag = False
            self.dragStartX = 0
            self.dragStartY = 0
            self.dragX = 0
            self.dragY = 0


    #-------------------------------------------------------
    def mouse_scroll(self, win, x, y, scroll_x, scroll_y):

        if scroll_y < 0:
            self.view.addScale(-self.scaleSpeed)

        if scroll_y > 0:
            self.view.addScale(self.scaleSpeed)

    #------------------------------------------------------
    def mouse_drag(self, win, x, y, dx, dy, button, modifiers):

        if button == pyglet.window.mouse.LEFT:

            self.drag = True
            self.dragX, self.dragY = self.xyToViewCoord(x, y)

    #-------------------------------------------------------
    def update(self, win, dt):

        if not self.initialized:
            return

        # view.x berechnen und überprüfen, dass es noch zu sehen ist
        self.view.x += self.scrollLeftRight*self.scrollSpeed*dt

        '''if self.view.x > self.map.mapWidth:

            self.view.x = self.map.mapWidth

        if self.view.x < 0:

            self.view.x = 0'''

        # view.y berechnen und überprüfen, dass es noch zu sehen ist
        self.view.y += self.scrollUpDown*self.scrollSpeed*dt

        '''if self.view.y > self.map.mapHeight:

            self.view.y = self.map.mapHeight

        if self.view.y < 0:

            self.view.y = 0'''

        self.mouseToViewCoord()

        if self.infoOn:
            text = "Info"
            text += "\n"
            text += "\nKoordinaten: %d / %d" %(self.view.x, self.view.y)
            text += "\nMaxViewRect: %d %d %d %d" % self.view.getMaxViewRect()
            text += "\nScale: %f" % self.view.scale
            self.info.update(text)

        if self.paused:
            return

    #-------------------------------------------------------
    def resizeScreen(self, win):

        self.view.resize(win)
        tmpX, tmpY, tmpX2, tmpY2 = self.view.getMaxViewRect()
        self.info.label.y = win.height-25

    #-------------------------------------------------------
    def mouseToViewCoord(self):

        tmpX, tmpY = self.view.getBottomLeft()
        self.mouseViewX = self.mouseX * self.view.scale + tmpX
        self.mouseViewY = self.mouseY * self.view.scale + tmpY

    #------------------------------------------------------
    def xyToViewCoord(self, x, y):

        tmpX, tmpY = self.view.getBottomLeft()
        x2 = x * self.view.scale + tmpX
        y2 = y * self.view.scale + tmpY
        return x2, y2

    #-------------------------------------------------------
    def drawLine(self, x1, y1, x2, y2, color):

        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2f', (x1, y1, x2, y2)),
            ('c4B', (color[0], color[1], color[2], color[3], color[0], color[1], color[2], color[3]))
        )

    #-------------------------------------------------------
    def drawRect(self, x, y, x2, y2, color):

        self.drawLine(x, y, x2, y, color)
        self.drawLine(x2, y, x2, y2, color)
        self.drawLine(x2, y2, x, y2, color)
        self.drawLine(x, y2, x, y, color)


    #-------------------------------------------------------
    def draw(self, win):

        if not self.initialized:
            return

        win.clear()

        # setView, mit scaling und viewpoint
        self.view.camera()

        self.batch.draw()

        self.batchUnits.draw()

        if self.drag:
            self.drawRect(self.dragStartX, self.dragStartY, self.dragX, self.dragY, (255, 255, 0, 128))

        # resetView, für fps etc..
        self.view.reset()

        if self.infoOn:
            self.info.draw()

        # FPS ausgeben, wenn True
        if win.fps:
            win.fps_display.draw()

        # Pause
        if self.paused:
            self.spritePaused.draw()
