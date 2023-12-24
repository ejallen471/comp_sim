#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 09:11:36 2023

@author: emmaallen

Class is a subclass of CelestialSystem
- Run only for mode 5 (only considering the influence of the sun on the planet's orbits')

the following methods are overridden:
    - updatePositionAndVelocity

"""

from CelestialSystem import CelestialSystem


class CelestialSystemFive(CelestialSystem):  

    def updatePositionAndVelocity(self, bodies):
        """
        Method takes input of bodies list and body number (j). 
        
        The method will interate through the bodies list and update velocity and position, only considering the gravitational force of the central body
        
        Method has no outputs
        
        """
        # Loop through and update position for all bodies
        [bodies[j].updatePosition(self.dt) for j in range(len(bodies))]
        
        # Loop through and update velocity for all bodies, only including force from central body       
        [self.bodies[j].updateVelocity(self.dt, bodies[0]) for j in range(len(bodies)) if j != 0]

        