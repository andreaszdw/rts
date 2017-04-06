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
    def __init__(self):

        self.bgImage = None
        self.bgSprite = None
        
        self.xTiles = 0
        self.yTiles = 0
        self.tileWidth = 0
        self.tileHeight = 0

        self.mapWidth = 0
        self.mapHeight = 0

        self.tiles = []
        self.tileSet = []

    #------------------------------------------------------
    def loadFile(self, filename, batch):

        # open the file and load the json
        f = open(filename).read()
        tmpData = json.loads(f)

        # load the bg image
        self.bgImage = pyglet.image.load(tmpData["layers"][0]["image"])
        self.bgSprite = pyglet.sprite.Sprite(self.bgImage, batch=batch)
        
        # load the number of tiles
        self.xTiles = tmpData["layers"][1]["height"]
        self.yTiles = tmpData["layers"][1]["width"]

        # load the size of the tiles
        self.tileWidth = tmpData["tilewidth"]
        self.tileHeight = tmpData["tileheight"]

        # calculate the size of the map
        self.mapWidth = self.xTiles * self.tileWidth
        self.mapHeight = self.yTiles * self.tileHeight

        # load the tile data
        self.tiles = tmpData["layers"][1]["data"]

        # load the single tile infos
        for i in range(len(tmpData["tilesets"][0]["tileproperties"])):

            tmpId = i+1
            self.tileSet.append(TileUnit(name=tmpData["tilesets"][0]["tileproperties"][str(i)]["type"], id=tmpId))

    #------------------------------------------------------
    # returns the tile in x, y from coordinates
    #------------------------------------------------------
    def xyToMapTile(self, x, y):

        if self.tileWidth and self.tileHeight:

            tileX = int(x // self.tileWidth)
            tileY = int(y // self.tileHeight)

        else:

            return None, None

        return tileX, tileY

    #------------------------------------------------------
    # returns the value of the tile form coordinates
    #------------------------------------------------------
    def getTileFromXY(self, x, y):

        tileX, tileY = self.xyToMapTile(x, y)
        
        if (tileX != None) and (tileY != None):

            if tileX < 0: return False, False
            if tileY < 0: return False, False
            if tileX > self.xTiles - 1: return False, False
            if tileY > self.yTiles - 1: return False, False

            tmpTile = self.tiles[tileX+(self.yTiles-1-tileY)*self.yTiles]

            return tmpTile