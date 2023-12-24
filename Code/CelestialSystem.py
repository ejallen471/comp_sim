#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 13:35:07 2023

@author: emmaallen

This file contains the Celestial System Class. 

The methods of this class are 

- updateTimestep
- updatePositionAndVelocity
- orbitalPeriod
- percentageDiff
- calculatedOrbitalPeriod
- energyCalculation
- plotEnergyGraph
- animate
- runAnimation

"""

import pandas as pd
from numpy.linalg import norm
from scipy import constants as const

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class CelestialSystem():  

    def __init__(self, bodies, niter, dt, programMode, integrationType):
        """
        Method will create variables based on inputs (bodies, niter, dt, programMode, integrationType) 
        
        and intialise empty lists for later use

        """
        
        self.niter = niter
        self.dt = dt
        self.programMode = programMode
        self.bodies = bodies
        self.integrationType = integrationType

        # intalise empty lists for later use
        self.earthTime = []
        self.totalEnergyIntegrationOne = []
        self.simulationTimePeriodOne = []
        self.timePeriodDifference = []
        self.calculatedOrbtialPeriodLst = []
        self.periodPercentageDiff = []
        self.planetNames = []
   
         
    def updateTimestep(self, i):
        """
        Method takes in timestep number and will complete the following
        - call energy calculations
        - call update position and velocity for each body in self.bodies
        - call orbital period calculations
        - write energy and orbital period to file if true

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
                
    
    
    def updatePositionAndVelocity(self, bodies):
        """
        Method takes input of bodies list and body number (j). 
        
        The method will interate through the bodies list and update velocity and position
        
        Method has no outputs
    
        """
        # Loop through and update position for all bodies
        [bodies[j].updatePosition(self.dt) for j in range(len(bodies))]
        
        # Loop through all and update velocity for all bodies, this takes into account the inter-body force (as well as force from central body)
        [bodies[j].updateVelocity(self.dt, bodies[k]) for j in range(len(bodies)) for k in range(len(bodies)) if  j != k]
                      
                 
    def orbitalPeriod(self, j):
        """
        Method takes input of body number
        
        Method calculates 
        - the Time period and appends to list (simulatedTimePeriod)
        - percentage difference between simulated and calculated value. Value is appended to list (timePeriodDifference)
        
        then these lists, along with the planet name and calculated value are made into a pandas dataframe
        
        Method has no outputs
        """

        try:      
            self.simulationTimePeriodOne.append(self.bodies[j].orbitalPeriod)
            self.planetNames.append(self.bodies[j].name)
            
            timePeriod = self.bodies[j].calculateTimePeriod(self.bodies[0])
            self.calculatedOrbtialPeriodLst.append(timePeriod)
            self.percentageDiff(self.simulationTimePeriodOne[j], self.calculatedOrbtialPeriodLst[j])
            
            columns =['Planet Name', 'Calculated Orbital Period / seconds', 'Simulation Orbital Period /  seconds', 'Orbital Period Difference / seconds', 'Orbital Period Percentage Difference']
            # create data frame with planet name, calculated and simulated orbital period, period difference and percentage difference
            self.df1 = pd.DataFrame(zip(self.planetNames, self.calculatedOrbtialPeriodLst, self.simulationTimePeriodOne, self.timePeriodDifference, self.periodPercentageDiff), columns=columns) 
        
        except IndexError:
            pass
        
                
    def percentageDiff(self, valueOne, valueTwo):
        """
        Method takes input of two values (type float)
        
        the percentage difference between the the two values and is appended to a list
        
        there are no outputs 

        """
        
        percentageDiff = 100 * (abs(valueOne - valueTwo) / valueOne)
        
        self.timePeriodDifference.append(abs(valueOne-valueTwo))
        self.periodPercentageDiff.append(percentageDiff)
          
       
    def energyCalculation(self, bodies):  
        """
        Method input of bodies list 
        
        Method will calculate the total energy and append to list. the corresponding earth time (in seconds) is appended to a 
        seperate list with the same index
        
        Method has no outputs

        """
        kineticEnergy = 0
        potentialEnergy = 0
     
        for j in range(len(bodies)):
            kineticEnergy += (1/2) * bodies[j].m * (norm(bodies[j].v))**2
     
            for k in range(len(bodies)):
                if (k != j): 
                    potentialEnergy -= (const.G * bodies[j].m * bodies[k].m) / (norm(bodies[j].r - bodies[k].r))         
                          
        # divide potential energy by two to avoid double counting
        self.totalEnergyValue = (kineticEnergy + (potentialEnergy / 2))

            
    def plotEnergyGraph(self):
        """
        Method has no inputs or outputs 
        
        Dependent on program mode, a graph of total energy against time is displayed

        """   

        # plot one energy on the graph
        ax = self.df.plot(x='Time / seconds', y='Total Energy / Joules', colormap='jet')
        ax.set_xlabel("Time / Seconds")
        ax.set_ylabel("Total Energy / Joules")
        plt.title((f'Total Energy against Time with {self.integrationType} integration'))
                      
    
    def animate(self, i):     
        """
        Method has input of timestep number 
        
        Method calls the updateTimestep method and return self.patches
        
        Method has no outputs 
        
        """

        self.updateTimestep(i)
        
        for j in range(len(self.bodies)):
            self.patches[j].center = self.bodies[j].r 
                                                            
        return self.patches 

    
    def runAnimation(self):
        """
        Method will create a patch for each planet and run the animation

        """  
 
        self.patches = []
        img = plt.imread("Stars.jpg")
        fig, ax = plt.subplots()
        ax.imshow(img, extent=[-1e12, 1e12, -1e12, 1e12])
        ax.set_xlabel("Distance / m")
        ax.set_ylabel("Distance / m ")
        plt.title('Animation of the Solar System')

        [self.patches.append(ax.add_patch(plt.Circle(body.r, 1e9*body.planetRadius, color=body.colour, animated=True))) for idx, body in enumerate(self.bodies)]
 
        # lim = 1e12 # math.sqrt(np.dot(self.bodies[-1].r, self.bodies[-1].r)) 
        ax.axis('scaled')
                
        self.anim = FuncAnimation(fig, self.animate, frames=self.niter, repeat=True, interval=1, blit=True)
        plt.show()