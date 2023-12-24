#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 14:32:51 2023

@author: emmaallen

class is a subclass of CelestialBody with the following methods overridden:
    - Initialise

class also has addition attributes of intialVelocity and targetPlanet
"""

import numpy as np
import pandas as pd
import math
from scipy import constants as const

 

from CelestialBody import CelestialBody

class Satellite(CelestialBody):
    

    def __init__(self, bodyType, name, planetRadius, colour, mass, orbitRadius, intialVelocity, targetPlanet):
        super().__init__(bodyType, name, planetRadius, colour, mass, orbitRadius)
        
        """
        Constructor will intalise the same variables as CelestialBody (bodyType, name, planetRadius, colour, mass, orbitRadius)
        
        in addition, the constructor will intalise intialVelocity, targetPlanet

        """
        self.intialVelocity = intialVelocity
        self.targetPlanet = targetPlanet
        self.intialPosition = orbitRadius

    def initialise(self, bodyi, programMode):
        
        """
        Method takes an input of body object which the self.body object is orbitting. Final input is the programMode
        
        the starting velocity, position and acceleration are calculated and previous velocity and acceleration variables are set
        
        to begin the integration.

        """
        
        try:    
            self.r = np.array((self.intialPosition, 0.0), dtype=float)
            # adding the intial velocity of Earth
            self.v = self.intialVelocity + np.array([0, math.sqrt((const.G * 1.99E+30) / 1.50E+11)], dtype=float)
            self.a = self.updateAcceleration(bodyi) 
            
            if programMode != 4 and self.bodyType == 'Satellite':
                
                # write final initial velocity to file
                print(f'The Intial velocity of the satellite is {self.v} \n')
             
                d = {'Satellite Name': [self.name], 'Intial Velocity x / ms^1': [self.v[0]], 'Intial Velocity y / ms^1': [self.v[1]]}                
                df2 = pd.DataFrame(data=d)
               
                with pd.ExcelWriter('PlanetData.xlsx', mode='a', if_sheet_exists='replace') as writer:
                    df2.to_excel(writer, sheet_name='Satellite Initial Velocity')
      
        # To catch Sun case where orbitRadius = 0
        except ZeroDivisionError:
            self.v = np.array([0,0], dtype=float)
            self.r = np.array([0,0], dtype=float)
            self.a = np.array([0,0], dtype=float)         
        
        # intialise acceleration to begin integration 
        self.previousA = self.a  
        self.previousR = self.r


        
        
        
        
        
        
        
        
        
        
        
        