#!/usr/bin/env python
# -*- coding: utf-8 -*-

# helper.py
#
# some helper functions
#
#------------------------------------------------------------------------------

import pyglet
from pyglet.image import Animation, AnimationFrame


# this creates an animation sequence for an sprite
#
#------------------------------------------------------------------------------
def createAnimation(image=None, columns=0, rows=0, anchor_x=0, anchor_y=0, duration=0):
    #effect_seq = pyglet.image.ImageGrid(pyglet.image.load(image_name), rows, columns)
    effect_seq = pyglet.image.ImageGrid(image, rows, columns)
    effect_frames = []
    for row in range(rows, 0, -1):
        end = row * columns
        start = end - (columns -1) -1
        for effect_frame in effect_seq[start:end:1]:
            effect_frame.anchor_x = anchor_x
            effect_frame.anchor_y = anchor_y
            effect_frames.append(AnimationFrame(effect_frame, duration))

    #effect_frames[(rows * columns) -1].duration = None
    return Animation(effect_frames)


#------------------------------------------------------------------------------
def animationByList(image=None, aniList=[]):

    effect_frames=[]

    print aniList

    #for v in aniList:

        #print v#, f["y"], f["w"], f["h"], f["anchor_x"], f["anchor_y"], f["duration"]

#------------------------------------------------------------------------------
class unitsList(object):

    #------------------------------------------------------
    def __init__(self):

        self.imageList = []
        self.fileList = []
        self.units = []

    #------------------------------------------------------
    def loadFromXml(self, filename=None):

        # Prüfen, ob der Einheitentyp bereits früher geladen wurde.
        # Die Prüfung erfolgt aufgrund des Dateinamens
        # Falls nicht, laden, erstellen und Dateinamen in Liste eintragen
        if not filename in self.fileList:

            tmpUnit = basicUnit()

            self.fileList.append(filename) # Dateinamen in Liste eintragen

            # XML parsen
            tree = ET.parse(filename)
            root = tree.getroot()

            # Einheitentyp
            tmpType = root.get('type')
            tmpUnit.type = tmpType

            print tmpType

            # Einheitenname
            tmpName = root.get('name')
            tmpUnit.name = tmpName

            print tmpName

            # Lebenspunkte
            tmpLife = root.get('lifepoints')
            tmpUnit.lifepoints = tmpLife

            print tmpLife

            # Einheitenimage
            tmpImage = root.find('image').text
            tmpUnit.imageText = tmpImage

            # Animationen
            tmpAnimations= root.find('animations')

            # Animationsliste
            tmpAnimsList = []
            
            # einzelne Animationen
            for anim in tmpAnimations:
                print anim.get("name")
                print anim.get("frames")
                print anim.get("x")
                print anim.get("y")
                print anim.get("width")
                print anim.get("height")
                print anim.get("center_x")
                print anim.get("center_y")
                print anim.get("duration")

            tmpUnit.animations = tmpAnimations

            #Eigenschaften
            tmpProperties = root.find('properties')

            for prop in tmpProperties:
                print prop.get("name")
                
                if prop.get("possible") == "1":
                    print "possible"
                    print prop.get("speed")
                else:
                    print "not possible"

            # Angriff
            tmpAttack = root.find("weapon")
            print tmpAttack.get("name")

            

#------------------------------------------------------------------------------
class basicUnit(object):

    #------------------------------------------------------
    def __init__(self):

        self.type = ""
        self.name = ""
        self.lifepoints = 0
        self.imageText = ""

        self.animations = []

        self.wayPoints = []

        self.walking = False
        self.walkingSpeed = 0

        self.swimming = False
        self.swimmingSpeed = 0

        self.flying = False
        self.flyingSpeed = 0

        self.weapon = ""
        self.weaponDamage = 0

    #------------------------------------------------------
    def update(self, dt):

        pass

    #------------------------------------------------------
    def move(self):

        pass

    #------------------------------------------------------
    def attack(self):

        pass


#------------------------------------------------------------------------------
class unit(object):

    #------------------------------------------------------
    def __init__(self, unittype="", x=0, y=0, anims=[], batch=None, speed=0, swim=False, walk=False, drive=False, fly=False, health=0, attackOne=0, attackOneTime=0, attackTwo=0, attackTwoTime=0):

        self.type = unittype
        self.x = x
        self.y = y

        self.anims = anims

        self.sprite = pyglet.sprite.Sprite(anims[0], batch=batch, x=x, y=y)
        self.batch = batch

        self.wayPoints = []
        self.destination = destination

        self.speed = speed

        self.swim = swim
        self.walk = walk
        self.drive = drive
        self.fly = fly

        self.health = health

        self.attackOne = attackOne
        self.attackOneTime = attackOneTime
        
        self.attackTwo = attackTwo
        self.attackTwoTime = attackTwoTime