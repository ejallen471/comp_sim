#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:02:50 2023

@author: emmaallen

This class contains the following methods:

- initialise
- updatePosition
- updateVelocity
- updateAcceleration
- determineNewYear
- calculateTimePeriod
- kineticEnergy
- angleOfX
- distanceToTarget

"""

import numpy as np
from numpy.linalg import norm
import math



from scipy import constants as const

class CelestialBody():   
    
    def __init__(self, bodyType, name, planetRadius, colour, mass, startingPosition):
        
        """
        Constructor will take inputs of bodyType, name, planetRadius, colour, mass, startingPosition and create variables for later use

        """  

        self.bodyType = bodyType
        self.name = name
        self.planetRadius = planetRadius
        self.colour = colour
        
        self.m = mass        
        self.orbitRadius = startingPosition 
        
        self.numberOfOrbits = 1
        self.lstOfClosestDst = []
        self.timeLst = []

    def initialise(self, bodyi, programMode):
        
        """
        Method takes an input of body object which the self.body object is orbitting. Final input is the programMode
        
        the starting velocity, position and acceleration are calculated and previous velocity and acceleration variables are set
        
        to begin the integration.

        """               
            
        try:    
            self.r = np.array((self.orbitRadius, 0.0), dtype=float)
            self.v = np.array([0, math.sqrt((const.G * bodyi.m) / self.orbitRadius)], dtype=float) 
            self.a = self.updateAcceleration(bodyi) 
      
        # To catch Sun case where orbitRadius = 0
        except ZeroDivisionError:
            self.v = np.array([0,0], dtype=float)
            self.r = np.array([0,0], dtype=float)
            self.a = np.array([0,0], dtype=float)
              
        # intialise acceleration to begin integration 
        self.previousA = self.a  
        self.previousR = self.r
        self.previousV = self.v


    def updatePosition(self, dt):
        """
        Method takes an input of timestep (dt) and will calculate the new position using Beeman integration
        
        Method has no outputs
        
        """
        # save previous position to check for year
        self.previousR = self.r
    
        self.r = self.r + self.v * dt + ((4*self.a - self.previousA)* dt**2) / 6
        

    def updateVelocity(self, dt, bodyi):
        """
        Method takes an input of timestep (dt) and body object (bodyi)
        
        The method will calculate the new velocity using Beeman integration and call accleration method
        
        Method has no outputs
        
        """

        futureA = self.updateAcceleration(bodyi)
        
        self.v = self.v + ((2*futureA + 5*self.a - self.previousA) * dt) / 6
        
        # update acceleration for next iteration
        self.previousA = self.a
        self.a = futureA
        
        
    def updateAcceleration(self, bodyi):
        """
        Method has input of body object
        
        Method will calculate and return the acceleration
        
        """

        rij = self.r - bodyi.r
        a = - (const.G * bodyi.m * rij) / norm(rij)**3
        return a
    

    def determineNewYear(self, centralBody, t):
        """
        Method takes an input of celestial body object (coded to always be the sun) and time (t)
        
        previous and current position are compared with the y position of the sun to determine whether a new year has passed
        
        True or False is returned accordingly
        
        """       
        # update the year when the planet passes the line of the sun (to account for sun drift)
        if (self.previousR[1] < centralBody.r[1] and self.r[1] >= centralBody.r[1]):
            
            self.orbitalPeriod = t  / self.numberOfOrbits
            self.numberOfOrbits += 1
            
            return True
        else:
            return False
    

    def calculateTimePeriod(self, centralBody):
        """
        Method takes input of celestial body object and will calculate the time to orbit (in seconds) based upon Keplers Laws 
        
        This value is returned

        """
        
        timePeriod = 2 * math.pi * math.sqrt((self.orbitRadius)**3 / (const.G * centralBody.m))
        
        return timePeriod          
      

    def angleOfX(self):
        """
        Method has no inputs and outputs
        
        The angle of the body is calculated in degrees

        """
            
        y = self.r[1]
        x = self.r[0]

        self.theta = abs(math.degrees(math.atan(y/x)))
        

    def distanceToTarget(self, targetPlanet, time): 
        """
        Method takes input of the target planet 
        
        The distance between the satellite and target planet is calculated and dst lst is updated.
        
        
        """
        rij = targetPlanet.r - self.r
        
        dst = norm(rij) - (3.40E+06 + 1.74E+06)

        if dst < 3.40E+06 and targetPlanet.name == 'Mars':
            print(f'Satellite has collided with Mars at distance {dst} at {time} seconds')
        
        elif dst < 1.74E+06 and targetPlanet.name == 'Earth':
            print('Satellite has sucessfully made it to Earth at {time} seconds')
        
        else:
            self.lstOfClosestDst.append(dst)
            self.timeLst.append(time)
        
        
        
    

        

        
        
        
        


            
        
        
        
        
