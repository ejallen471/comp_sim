#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 08:45:48 2023

@author: emmaallen

This class is a subclass of CelestialSystem. 
- it is only used for program mode three - doomsday Planetary Alignment 

The following methods are overridden ;
- updateTimestep

The following methods are additional
- doomsdayPlanetaryAlignment

"""

import pandas as pd

from CelestialSystem import CelestialSystem

class CelestialSystemThree(CelestialSystem): 
    
    def updateTimestep(self, i):
        """
        Method takes in timestep number and will complete the following
        - call energy calculations
        - call update position and velocity for each body in self.bodies
        - call orbital period calculations
        - write energy and orbital period to file if true
        - call doomsday alignment function
        """    
        # calculate time in seconds. (i + 1) to account for indexing
        self.time = (i+1) * self.dt   
        self.earthTime.append(self.time)
        
        self.updatePositionAndVelocity(self.bodies)
        
        self.energyCalculation(self.bodies)    
        self.totalEnergyIntegrationOne.append(self.totalEnergyValue)    
        
        for j in range(0, len(self.bodies)):
            
            # Check if it is a new year, calculate orbital period accordingly
            if (self.bodies[j].determineNewYear(self.bodies[0], self.time)) and j != 0:
                  self.orbitalPeriod(j)
            
        self.df = pd.DataFrame(list(zip(self.earthTime, self.totalEnergyIntegrationOne)), columns=['Time / seconds', 'Total Energy / Joules'])
           
        # i > 100 to prevent graph shown at the start
        # (i % x) - x can be changed to change the frequency of graphs
        if (i % 5000) == 0 and i > 10:
            
            self.plotEnergyGraph() 
            
            print(f'Graph of total energy has been displayed at time: {self.time} seconds \n')

        # write to file at specific timestep - different to graph timestep to minimise lag 
        # (i % x) - x can be changed to change when data is written to file
        elif (i % 2000) == 0 and i > 10:
            
            with pd.ExcelWriter('PlanetData.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.df1.to_excel(writer, sheet_name='Orbital Period') 
            
            with pd.ExcelWriter('PlanetData.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.df.to_excel(writer, sheet_name='Total Energy') 
            
            print(f'Total Energy and orbtial period data has been written to file at time: {self.time} seconds \n')
                    
        self.doomsdayPlanetaryAlignment()
        
        
        
    def doomsdayPlanetaryAlignment(self):
        """
        Method has no inputs or outputs 
        
        the angle between the sun's horizontal line (to account for sun drifting) and the line direct to the planet
        is calculated 
        
        if angles are aligned, a statement is printed. 
 
        """
              
        thetaLst = []   
        # calculate the angle from x axis for all planets
        [body.angleOfX() for body in self.bodies]
        # append angle to a seperate list 
        [thetaLst.append(body.theta) for body in self.bodies] 

        # compare all angles to the angle of first planet (not sun). result is true or false
        res =  all(map(lambda i: i <= (thetaLst[1] + 5) and i >= (thetaLst[1] - 5), thetaLst))

        if res == True:
            print(f'Doomsday at time {self.time} seconds \n')