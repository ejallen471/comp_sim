#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 21:37:48 2023

@author: emmaallen

REMEMEBER THE WHILE FALSE NEEED TO BE CHANGED TO WHILE TRUE TO GET USER INPUT

File contains:

- RunProject class which will ask for user inputs and run simulation accordingly.
Methods of this class are:
    - beginSimulation 
    - programModeOne
    - programModeTwo
    - programModeThree
    - programModeFour
    - programeModeFive

- main function which calls the beginSimulation Method 

"""

import pandas as pd
import numpy as np
import sys

from CelestialSystem import CelestialSystem
from CelestialSystemTwo import CelestialSystemTwo
from CelestialSystemThree import CelestialSystemThree
from CelestialSystemFive import CelestialSystemFive
from CelestialSystemFour import CelestialSystemFour

from CelestialBody import CelestialBody
from CelestialBodyTwo import CelestialBodyTwo
from Satellite import Satellite


class RunProject():
    
    def __init__(self):
        """
        Constructor will read in data from excel file and intialise the simulation parameters 


        """
        
        # read information from excel file 
        self.planetData = pd.read_excel('PlanetData.xlsx', sheet_name='Planet Body Data')
        self.satelliteData = pd.read_excel('PlanetData.xlsx', sheet_name='Satellite Data')
        self.simulationParameters = pd.read_excel('PlanetData.xlsx', sheet_name='Simulation Parameters')
        
        # Intialise list of bodies to be empty
        self.bodies = []
        
        # Integration Type set as Beeman
        self.integrationType = 'Beeman'
        
        for index, row in self.simulationParameters.iterrows():
            # Number of iterations 
            self.niter = int(row['Number of Iterations'])
            # Number of timesteps       
            self.dt = float(row['Timesteps / s'])  

    
    def beginSimulation(self):       
        """
        This method has no inputs and no outputs 
        
        The method asks for a user input to decide the programMode. 
        The correct programMode function is called, dependent on the user input. 
        
        If an incorrect mode is choosen the program will stop
        """
              
        # Asking for user input to choose mode of running program
        while True:
            try:              
                self.programMode = int(input("Please Choose Program Mode: \n 1. No Experiment - Normal Animation  \n 2. Experiment 1 - Integrating with Direct Euler in Comparision with Beeman \n 3. Experiment 2 - Doomsday Planetary Alignment  \n 4. Experiment 3 - Satellite flyby of Mars \n 5. Experiment 4 - Only the Sun's Influence of the planets\n"))
                
                if self.programMode > 5 or self.programMode < 1:
                    raise ValueError
                    
            except ValueError:
                print("Invalid input! Please enter a number between 1 and 5\n")
                continue
            else:
                break  
        
        print(f'Selected program mode is {self.programMode}\n')
        
        # Normal Animation
        if self.programMode == 1:
            self.programModeOne()
            
        # Different Integrations    
        elif self.programMode == 2:
            self.programModeTwo()
            
        # Doomsday    
        elif self.programMode == 3:  
            self.programModeThree()
            
        # Satellites - flyby of Mars 
        elif self.programMode == 4:     
            self.programModeFour()
        
        # Only including the Sun's influence 
        elif self.programMode == 5:
            self.programModeFive()
        
        else:
            sys.exit('Unrecognised program mode. Program has stopped \n')
            
          
    def programModeOne(self):
        
        """
        This method corresponds to normal animation (no experiments)
        
        The method has no inputs of outputs
        
        A list of body objects is created and then intalised. 
        
        Then the animation is run 
        """
        
        # create all bodies
        [self.bodies.append(CelestialBody(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Orbital Radius / m']))) for idx, row in self.planetData.iterrows()]               
    
        # intialise velocity, position and acceleration
        [self.bodies[i].initialise(self.bodies[0], self.programMode) for i in range(len(self.bodies))]            
        universe = CelestialSystem(self.bodies, self.niter, self.dt, self.programMode, self.integrationType)        
        universe.runAnimation()

    
    def programModeTwo(self):      
        """
        This method corresponds to integration of Euler and Beeman comparision
        
        The method has no inputs or outputs. 
        
        The user is asked which integration type should be displayed, then the animation is started accordingly

        """
           
        # User input for the type of animation to be seen.
        while True:
            animationToSee = (input("\nPlease Choose which integration you would like to see on the animation: Euler or Beeman \n"))
            animationToSee = animationToSee.lower()
            
            if animationToSee == 'euler' or animationToSee == 'beeman':
                print(f'\nChoosen animation is {animationToSee} integration\n')
                break
            else:
                print("\nInvalid input! Please enter Euler or Beeman\n")
                continue
   
        
        if animationToSee == 'beeman':     
            # intialise all bodies, with velocity, position and acceleration - Beeman
            [self.bodies.append(CelestialBody(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Orbital Radius / m']))) for idx, row in self.planetData.iterrows()]               
            [self.bodies[i].initialise(self.bodies[0], self.programMode) for i in range(len(self.bodies))] 
            
            # Intialise system with - Beeman
            universe = CelestialSystemTwo(self.bodies, self.niter, self.dt, self.programMode, self.integrationType)
            universe.runAnimation()
         
        elif animationToSee == 'euler':
        
            self.integrationType = 'Euler'
            # intialise all bodies, with velocity, position and acceleration - Beeman
            [self.bodies.append(CelestialBodyTwo(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Orbital Radius / m']))) for idx, row in self.planetData.iterrows()]               
            [self.bodies[i].initialise(self.bodies[0], self.programMode) for i in range(len(self.bodies))] 
            
            # Intialise system with - Beeman
            universe = CelestialSystemTwo(self.bodies, self.niter, self.dt, self.programMode, self.integrationType)
            universe.runAnimation()
        
        else:
            sys.exit('Unrecognised integration type. Program has stopped')
    
    def programModeThree(self):
        """
        This method corresponds to doomsday plantary alignment
        
        The method has no inputs or outputs
        
        A list of body objects is created, then planets further out than jupiter are discounted. 
        The animation is then run 

        """    
        # intialise all bodies
        [self.bodies.append(CelestialBody(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Orbital Radius / m']))) for idx, row in self.planetData.iterrows()]               
    

        # intialise velocity, position and acceleration
        [self.bodies[i].initialise(self.bodies[0], self.programMode) for i in range(len(self.bodies))]
        universe = CelestialSystemThree(self.bodies, self.niter, self.dt, self.programMode, self.integrationType)
        universe.runAnimation()
    
    def programModeFour(self):  
                
        """
        This method corresponds to satellite mode
        
        Method has no inputs or outputs 
        
        Satellites objects are intialised and the simulation is ran (without animation showing) to determine the best orbit radii 
        
        The animation and simulation are run with the satellite object intialised with this orbit radius

        """
        
        # Intialise planets
        [self.bodies.append(CelestialBody(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Orbital Radius / m']))) for idx, row in self.planetData.iterrows()]               
          
        xValues = []
        yValues = []
        i = 0

        numberOfTestSatellites = 1
        
        for index, row in self.satelliteData.iterrows():
            
            # determine the velocities to test
            x1 = row['Min intial X velocity / ms^-1']
            x2 = row['Max intial X velocity / ms^-1']             
            # make y component of velocity with respect to the Earth
            y1 = row['Min intial Y velocity / ms^-1']
            y2 = row['Max intial Y velocity / ms^-1'] 
                     
            xValues = np.linspace(x1,x2,2)
            yValues = np.linspace(y1,y2,2)
            
            # To vary the starting angle, change the pairs of x and y positions
            for x in xValues: 
                for y in yValues:    
                      
                    velocity = np.array([x,y], dtype = float)
                    velocity2 = np.array([-x,y], dtype = float)
                    
                    print(f'starting velocity {numberOfTestSatellites} is {velocity}')
                    print(f'starting velocity {numberOfTestSatellites + 1} is {velocity2}')
                    
                    # create a satellite object for each velocity               
                    self.bodies.append(Satellite('Satellite', (f'Satellite {numberOfTestSatellites}'), row['Relative size'], row['Colour'], float(row['Mass / kg']), (float(row['Starting Position / m']) + (numberOfTestSatellites)), velocity, row['Target Planet']))   
                    self.bodies.append(Satellite('Satellite', (f'Satellite {numberOfTestSatellites + 1}'), row['Relative size'], row['Colour'], float(row['Mass / kg']), (float(row['Starting Position / m']) + (numberOfTestSatellites + 1)), velocity2, row['Target Planet']))              
                    
                    numberOfTestSatellites += 2
                
                    
        [self.bodies[i].initialise(self.bodies[0], self.programMode) for i in range(len(self.bodies))] 

        universe = CelestialSystemFour(self.bodies, self.niter, self.dt, self.programMode, self.integrationType)
        
        # run simulation to find the minimum radius in the given in
        for i in range(5000):   
            universe.determineIntialVelocity(i)
            
        
        # read in data for minimum radius
        velocityData = pd.read_excel('PlanetData.xlsx', sheet_name='Optimum Initial Velocity')
        
        vDstDictionary = {}
        self.bodies = []
        self.programMode = 1
            
        for index, row in velocityData.iterrows():
            
            intialV = row['Initial Velocity']
            intialVStr = intialV.replace('[','').replace(']','').split()
            intialVnp = np.array(intialVStr, dtype=float)
            intialV = tuple(intialVnp)
            
            # Append to dictionary with key is velocity tuple and value is orbit with closest approach
            vDstDictionary[intialV] = row['Orbit with Closest Approach']
        
        # get key of the minimum distance value
        minV = min(vDstDictionary, key=vDstDictionary.get)
        minV = np.array([minV[0], minV[1]], dtype = float) 
        
        print(f'\nThe optimum starting velocity is {minV}. The animation will now run\n')
  
        # create planets and satellite with minimum radius 
        [self.bodies.append(CelestialBody(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Starting Position / m']))) for idx, row in self.planetData.iterrows()]       
        [self.bodies.append(Satellite(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Starting Position / m']), minV, row['Target Planet'])) for idx, row in self.satelliteData.iterrows()]     
        
        # Intialise all bodies
        [self.bodies[i].initialise(self.bodies[0], self.programMode) for i in range(len(self.bodies))]    
        
        # Run animation
        universe = CelestialSystemFour(self.bodies, self.niter, self.dt, self.programMode, self.integrationType)
        universe.runAnimation()
    

    
    def programModeFive(self):
        """
        This method corresponds to where the planets will only feel a force from the sun
        
        The method has no inputs of outputs
        
        A list of body objects is created and then intalised. 
        
        Then the animation is run 
        """
        
        # create all bodies
        [self.bodies.append(CelestialBody(row['Body Type'], row['Body Name'], row['Relative size'], row['Colour'], float(row['Mass / kg']), float(row['Orbital Radius / m']))) for idx, row in self.planetData.iterrows()]               
        
        # intialise velocity, position and acceleration
        [self.bodies[i].initialise(self.bodies[0], self.programMode) for i in range(len(self.bodies))]        
        universe = CelestialSystemFive(self.bodies, self.niter, self.dt, self.programMode, self.integrationType)
        universe.runAnimation()
        
        

def main():
    
    runProject = RunProject()  
    runProject.beginSimulation()


main()

