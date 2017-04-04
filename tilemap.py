#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
#
# map.py
#
#------------------------------------------------------------------------------

import json
import pyglet
from heapq import *

#------------------------------------------------------------------------------
class TileUnit(object):

    #------------------------------------------------------
    def __init__(self, name="", id=0):

        self.name = name
        self.id = id

#------------------------------------------------------------------------------
class Map(object):

    #------------------------------------------------------
    def __init__(self, fileName="", backgroundImage="", xTiles="", yTiles="", tileWidth="", tileHeight=""):

        self.fileName = fileName
        self.backgroundImage = backgroundImage
        self.xTiles = xTiles
        self.yTiles = yTiles
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight

        self.tiles = []
        self.tileSet = []

        self.loadFile(self.fileName)

    #------------------------------------------------------
    def loadFile(self, file):

        f = open(self.fileName).read()
        tmpData = json.loads(f)
        
        self.backgroundImage = tmpData["layers"][0]["image"]
        print self.backgroundImage

        self.xTiles = tmpData["layers"][1]["height"]
        self.yTiles = tmpData["layers"][1]["width"]

        print "%d x %d tiles" % (self.xTiles, self.yTiles)

        self.tileWidth = tmpData["tilewidth"]
        self.tileHeight = tmpData["tileheight"]
        print "%d x %d tilesize" % (self.tileWidth, self.tileHeight)

        self.tiles = tmpData["layers"][1]["data"]
        #print self.tiles

        for i in range(len(tmpData["tilesets"][0]["tileproperties"])):

            tmpId = i+1
            self.tileSet.append(TileUnit(name=tmpData["tilesets"][0]["tileproperties"][str(i)]["type"], id=tmpId))

            print self.tileSet[i].name, self.tileSet[i].id