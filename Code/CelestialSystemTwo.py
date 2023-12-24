#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 08:42:59 2023

@author: emmaallen

This class is a subclass of CelestialSystem. 

Class is  used for comparing the integration of Euler and beeman

the following methods are overridden:
    -updateTimestep
    -plotEnergyGraph
"""


import pandas as pd
import matplotlib.pyplot as plt

from CelestialBodyTwo import CelestialBodyTwo
from CelestialBody import CelestialBody
from CelestialSystem import CelestialSystem


class CelestialSystemTwo(CelestialSystem): 
    
    def __init__(self, bodies, niter, dt, programMode, integrationType):
        super().__init__(bodies, niter, dt, programMode, integrationType)
        
        """
        Constructor will intalise the same variables as CelestialSystem 
        
        a list of bodies using opposite integration to that selected by the user is made. 

        """ 
        
        planetData = pd.read_excel('PlanetData.xlsx', sheet_name='Planet Body Data')
        self.totalEnergyIntegrationTwo = []
        
        self.bodiesTwo = []          
                 
        if self.integrationType == 'Beeman':
            
            self.calculatedIntegrationType = 'Euler'
            # create seperate lists of bodies which will use Euler methods of integration to update position and velocity
            [self.bodiesTwo.append(CelestialBodyTwo(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Orbital Radius / m']))) for idx, row in planetData.iterrows()]               
            [self.bodiesTwo[i].initialise(self.bodies[0], self.programMode) for i in range(len(self.bodies))] 
        
        elif self.integrationType == 'Euler':
            
            self.calculatedIntegrationType = 'Beeman'
            # create seperate lists of bodies which will use Beeman methods of integration to update position and velocity
            [self.bodiesTwo.append(CelestialBody(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Orbital Radius / m']))) for idx, row in planetData.iterrows()]               
            [self.bodiesTwo[i].initialise(self.bodies[0], self.programMode) for i in range(len(self.bodies))]  
            
    
    def updateTimestep(self, i):
        """
        Method takes in timestep number and will complete the following
        - call energy calculations for both lists of bodies
        - call update position and velocity for each body in self.bodies and self.bodiesTwo
        - call orbital period calculations
        - determine if it is a new year - calculate the orbital period if so 
        
        """    
        # calculate time in seconds. (i + 1) to account for indexing
        self.time = (i+1) * self.dt   
        self.earthTime.append(self.time)
        
        # update position and velocity for both lists of bodies
        self.updatePositionAndVelocity(self.bodies)
        self.updatePositionAndVelocity(self.bodiesTwo)
        
        # calculate energy and append to list for bodies one 
        self.energyCalculation(self.bodies)    
        self.totalEnergyIntegrationOne.append(self.totalEnergyValue)  
        
        # calculate energy and append to list for bodies two 
        self.energyCalculation(self.bodiesTwo)  
        self.totalEnergyIntegrationTwo.append(self.totalEnergyValue)
        
        self.df = pd.DataFrame(list(zip(self.earthTime, self.totalEnergyIntegrationOne, self.totalEnergyIntegrationTwo)), columns=[('Time / seconds'), (f'Total Energy by {self.integrationType} / Joules'),  (f'Total Energy by {self.calculatedIntegrationType} / Joules')])  
     
        for j in range(0, len(self.bodies)):
            
            # Check if it is a new year, calculate orbital period accordingly
            if (self.bodies[j].determineNewYear(self.bodies[0], self.time)) and j != 0:
                  self.orbitalPeriod(j)
               
        # i > 100 to prevent graph shown at the start
        # (i % x) - x can be changed to change the frequency of graphs and data written to graph
        if (i % 5000) == 0 and i > 1:
            
            self.plotEnergyGraph() 
            
            print(f'Graph of total energy has been displayed at Earth time: {self.time} seconds \n')
            
            with pd.ExcelWriter('PlanetData.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.df.to_excel(writer, sheet_name='Total Energy') 
            
            # write to excel sheet
            with pd.ExcelWriter('PlanetData.xlsx', mode='a', if_sheet_exists='replace') as writer:
                self.df1.to_excel(writer, sheet_name='Orbital Period') 
            
    
    def plotEnergyGraph(self):
        """
        Method has no inputs or outputs 
        
         a graph of total energy against time is displayed with both integration methods 

        """   

        plt.figure()

        plt.plot(self.df['Time / seconds'], self.df['Total Energy by Beeman / Joules'], label = "Total Energy by Beeman / Joules")
        plt.plot(self.df['Time / seconds'], self.df['Total Energy by Euler / Joules'], label = "Total Energy by Euler / Joules")
        plt.xlabel("Time / Seconds")
        plt.ylabel("Total Energy / Joules")
        plt.title(('Total Energy against Time'))

        plt.legend()
        plt.show()


    