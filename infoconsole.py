#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet

#-------------------------------------------------------------------------------
class InfoConsole(object):

    #-------------------------------------------------------
    def __init__(self, text, x=0, y=0, width=0, batch=None):
        
        pyglet.font.add_file("fonts/Consolas.ttf")
        self.batch=pyglet.graphics.Batch()
        self.label=pyglet.text.Label(text, font_name = "Consolas",
                                     font_size=9,
                                     x=x, y=y,
                                     multiline=True,
                                     width=width,
                                     batch=self.batch)
        
    #-------------------------------------------------------
    def update(self, text):
        
        self.label.text = text

    #-------------------------------------------------------
    def draw(self):
        
        self.batch.draw()
