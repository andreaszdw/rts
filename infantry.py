#!/usr/bin/env python
# -*- coding: utf-8 -*-

# infantry.py
#
# animated infantry class
#------------------------------------------------------------------------------

import json
import pyglet

import gameobject
import helper

#------------------------------------------------------------------------------
class Infantry(gameobject.GameObject):

    #------------------------------------------------------
    def __init__(self, batch, jsonFile):

        self.batch = batch  # batch for rendering

        self.name = ""
        self.animations = []

        self.loadFromJson(jsonFile)

    #------------------------------------------------------
    def loadFromJson(self, jsonFile):

        # open the file and load the json
        f = open(jsonFile).read()
        tmpData = json.loads(f)

        # load the image, here I need some resource manager, so
        # I could not load the same image multiple
        self.image = pyglet.image.load(tmpData["image"])

        for a in tmpData["animations"]:

            print a["name"]
            self.animations.append(
            helper.animationByList(self.image, a["frames"]))



            '''self.animations.append(helper.createAnimation(self.image,a["frames"], 1, 
                                                          a["anchor_x"], 
                                                          a["anchor_y"],
                                                          a["duration"]))'''


        '''self.animations.append(helper.createAnimation(self.image,tmpData["animations"][0]["frames"], 1, 
                                                      tmpData["animations"][0]["anchor_x"], 
                                                      tmpData["animations"][0]["anchor_y"],
                                                      tmpData["animations"][0]["duration"]))'''

        self.sprite = pyglet.sprite.Sprite(self.animations[0], batch=self.batch, x=2560//2, y=2560//2)
        #self.sprite = pyglet.sprite.Sprite(self.image, batch=self.batch, x=2560//2, y=2560//2)

    #------------------------------------------------------
    def update(dt):
        pass

    #------------------------------------------------------
    def paused():
        pass