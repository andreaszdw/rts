#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
#
# stack.py
#
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
class Stack:
    def __init__(self):
        self.data = []

    #------------------------------------------------------
    # This method pushes a state onto the stack, making it the top and the method top()
    # will return this on the next call.
    #------------------------------------------------------
    def push(self, data_):
        self.data.append(data_)

    #------------------------------------------------------
    # This method removes the current state from the top of the stack. The state below it
    # will automaticly be returned by the next call to the top() method.
    #------------------------------------------------------
    def pop(self):
        if len(self.data) == 0:
            return 0
        
        data = self.top()
        self.data.pop(-1)
        return data

    #------------------------------------------------------
    # returns the top state in the stack (the active one)
    #------------------------------------------------------
    def top(self):
        if len(self.data) == 0:
            return 0
        else:
            return self.data[-1]

    #------------------------------------------------------
    def empty(self):
        if len(self.data) == 0:
            return True
        else:
            return False

    #------------------------------------------------------
    def __del__(self):
        pass
