#!/usr/bin/env python
# -*- coding: utf-8 -*-

# base class for gameoebjects
# every object inherits from this class
# every object has an __init__, an update and a paused funcition
# maybe some are never used, but who knows
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
class GameObject(object):

    #------------------------------------------------------
    def __init__(self, batch):

        self.batch = batch  # batch for rendering

    #------------------------------------------------------
    def update(dt):
        pass

    #------------------------------------------------------
    def paused():
        pass