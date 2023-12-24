#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 08:38:28 2023

@author: emmaallen

This class is a subclass of CelestialSystem
- only used for program mode one, the satellites experiment

The following methods are overridden ;
- updateTimestep

The following methods are additional
- distanceToTarget
- determineIntialVelocity

"""


import pandas as pd

from CelestialSystem import CelestialSystem


class CelestialSystemFour(CelestialSystem):  
    
    def __init__(self, bodies, niter, dt, programMode, integrationType):
        super().__init__(bodies, niter, dt, programMode, integrationType)
        
        """
        Constructor will intalise the same variables as CelestialSystem 
        
        Constructor will calculate the total number of satellites and determine the target planet as an object

        """     
        
        self.nameS = [] 
        self.dstOfClosestApproach = []
        self.intialVelocities = []
        
        self.numberOfVelocities = 0
        self.status = 1       
        
        for idx, body1 in enumerate(self.bodies):
            
            if self.bodies[idx].bodyType == 'Satellite':       
                self.numberOfVelocities += 1  
            
            for body2 in self.bodies:
                # set target Planet to be the correct object
                if body2.bodyType == 'Satellite':
                    if body1.name == body2.targetPlanet:
                        self.targetPlanet = body1

 
    def updateTimestep(self, i):
        """
        Method takes in timestep number and will complete the following
        - call energy calculations
        - call update position and velocity for each body in self.bodies
        - call orbital period calculations
        - determine if it is a new year - write energy to file if true
        
        dependent on program mode, the method will also 
        - 1 - determine and write to file the closest approach radii
        - 2 - update position and velocity for other integration method
        - 3 - call doomsday method

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
        # (i % x) - x can be changed to change the frequency of graphs and data written to graph
        if (i % 5000) == 0 and i > 10:
            
            self.plotEnergyGraph() 
            
            print(f'Graph of total energy has been displayed at Earth time: {self.time} seconds \n')
            
            with pd.ExcelWriter('PlanetData.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.df.to_excel(writer, sheet_name='Total Energy') 
            
            # write to excel sheet
            with pd.ExcelWriter('PlanetData.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.df1.to_excel(writer, sheet_name='Orbital Period') 
            
        # check if satellite successfully comes back to Earth
        for p in range(len(self.bodies)):
            if self.programMode == 6 and self.bodies[p].bodyType == 'Satellite':
                self.bodies[p].distanceToTarget(self.bodies[2], self.time)

  
    def distanceToTarget(self, j, i):
        """
        Method has input of body number (j) and targetPlanet object
        
        the distance between target planet and body is calculated. 
        if this distance is the closest distance possible then statement is printed and the name and distance are appended to
        seperate lists at the same index
        
        This method has no outputs
 
        """
        
        # calculate the distance between the satellite and planet
        self.bodies[j].distanceToTarget(self.bodies[3], self.time)
        
        # find the minimum distance that occured in one full orbit or in 4999 timesteps
        if i == 4999: 
            
            dstLst = self.bodies[j].lstOfClosestDst
            # find minimum distance that occured in one full orbit
            minDst = min(dstLst)
            minIndex = dstLst.index(minDst)
            minTime = self.bodies[j].timeLst[minIndex]

        
            # append values to lists to be written to a file later.
            self.nameS.append(self.bodies[j].name)
            self.intialVelocities.append(self.bodies[j].intialVelocity)
            self.dstOfClosestApproach.append(minDst)
            self.earthTime.append(minTime)
            
            print(f'The closest distance to Mars is {minDst} for {self.bodies[j].name}')
     
            
    def determineIntialVelocity(self, i):
        """
        Method takes input of timestep number and has no outputs 
        
        The method will call distanceToTarget to determine the best orbital radius. this value is written to the file
                    
        """
        # calculate the time 
        self.time = (i+1) * self.dt
        self.updatePositionAndVelocity(self.bodies)

        if self.status == 1:
            for idx, satellite in enumerate(self.bodies):
                if self.bodies[idx].bodyType == 'Satellite':        
                    
                    self.distanceToTarget(idx, i)
                    
                if len(self.dstOfClosestApproach) == self.numberOfVelocities:
                    
                    # save satellite name, intial velocity and closest approach distance into a dataframe and save in excel
                    df2 = pd.DataFrame(list(zip(self.nameS, self.intialVelocities, self.dstOfClosestApproach, self.earthTime)), columns=[('Satellite Name'), ('Initial Velocity'), ('Orbit with Closest Approach'), ('Time of closest Approach')])          
                    #print(df2)
                    with pd.ExcelWriter('PlanetData.xlsx', mode='a', if_sheet_exists='replace') as writer:
                        df2.to_excel(writer, sheet_name='Optimum Initial Velocity') 
                
                    # status set to zero to stop running after minimum velocity calculated once for each satellite
                    self.status = 0