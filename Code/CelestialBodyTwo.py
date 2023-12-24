#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 14:50:08 2023

@author: emmaallen

This body class is a subclass of CelestialBody, it uses Direct Euler or Forward Euler integration methods. 

2 methods are overridden from celestialBody, these are:
    
    - updatePosition
    - updateVelocity
"""


from CelestialBody import CelestialBody


class CelestialBodyTwo(CelestialBody):  
    
    def updatePosition(self, dt):
        """
        Method takes an input of timestep (dt) and will calculate the new position using direct Euler method
        
        Method has no outputs

        """
        # previous position stored to be used to determine the new year
        self.r_previous = self.r      
        self.r = self.r + (self.previousV * dt)
         

    def updateVelocity(self, dt, bodyi):
        """
        Method takes an input of timestep (dt) and body object (bodyi)
        
        The method will calculate the new velocity using direct Euler method and call accleration method
        
        Method has no outputs

        """
               
        self.a = self.updateAcceleration(bodyi) 
        self.previousV = self.v
              
        self.v = self.previousV + (self.a * dt)
        
        


