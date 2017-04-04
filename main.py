#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
#
# main.py
#
# This is the main.py. Most of it is an statemanager stack.
#
#------------------------------------------------------------------------------

import pyglet
import stack
import playstate

#-------------------------------------------------------------------------------
class MainWindow(pyglet.window.Window):

    #-------------------------------------------------------
    def __init__(self, caption="RTS", width=800, height=600):

        super(MainWindow, self).__init__(caption=caption, width=width, height=height, vsync=False)
        pyglet.clock.schedule_interval(self.update, 1./60)

        # fps anzeigen?
        self.fps = True
        self.fps_display = pyglet.clock.ClockDisplay()

        #pyglet.resource.path = [os.path.abspath('..')]
        pyglet.resource.reindex()
        self.stack = stack.Stack()
        #self.pushState(introstate.IntroState())
        self.pushState(playstate.PlayState())


    #-------------------------------------------------------
    def cleanup(self):

        while(not self.stack.empty()):
            self.stack.top().cleanup()
            self.stack.pop()

        self.close()

    #-------------------------------------------------------
    def changeState(self, state):

        if(not self.stack.empty()):
            self.stack.top().cleanup()
            self.stack.pop()

        self.stack.push(state)
        self.stack.top().init(self)

    #-------------------------------------------------------
    def pushState(self, state):

        if(not self.stack.empty()):
            self.stack.top().pause()

        self.stack.push(state)
        self.stack.top().init(self)

    #-------------------------------------------------------
    def popState(self):

        if(not self.stack.empty()):
            self.stack.top().cleanup()
            self.stack.pop()
            self.stack.top().resume()

        if(self.stack.empty()):
            self.stack.top().resume()

    #-------------------------------------------------------
    def top(self):

        return self.stack.top()

    #-------------------------------------------------------
    def on_draw(self):

        self.stack.top().draw(self)

    #-------------------------------------------------------
    def on_key_press(self, symbol, modifiers):

        self.stack.top().key_press(self, symbol, modifiers)

    #-------------------------------------------------------
    def on_key_release(self, symbol, modifiers):

        self.stack.top().key_release(self, symbol, modifiers)

    #-------------------------------------------------------
    def on_mouse_motion(self, x, y, dx, dy):

        self.stack.top().mouse_motion(self, x, y, dx, dy)

    #-------------------------------------------------------
    def on_mouse_press(self, x, y, button, modifiers):

        self.stack.top().mouse_press(self, x, y, button, modifiers)
    
    #------------------------------------------------------    
    def on_mouse_release(self, x, y, button, modifiers):
        
        self.stack.top().mouse_release(self, x, y, button, modifiers)

    #-------------------------------------------------------
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):

        self.stack.top().mouse_scroll(self, x, y, scroll_x, scroll_y)
    
    #-------------------------------------------------------
    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        
        self.stack.top().mouse_drag(self, x, y, dx, dy, button, modifiers)

    #-------------------------------------------------------
    def update(self, dt):

        if(not self.stack.empty()):
            self.stack.top().update(self, dt)

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    window = MainWindow()
    pyglet.app.run()

