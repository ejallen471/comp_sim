SOLAR SYSTEM SIMULATION PROJECT:

This project will run an animation of the solar system. The exact simulation varies depending on which mode the user chooses to run 

PROJECT OVERVIEW:

The project contains three main python files - projectRun, CelestialSystem and CelestialBody and one excel file, planetData 
which all data is either read from or written to.
 - CelestialSystem has 4 sub classes - CelestialSystemTwo, CelestialSystemThree, CelestialSystemFour, CelestialSystemFive
 - CelestialBody has 2 sub classes - Satllite and CelestialBodyTwo

There are Five program modes, these are:

Program Mode One - Normal Animation:
- Beeman integration
- orbital period and total energy are written to file when a graph is displayed
- all planets in file are included
- graph of total energy is displayed 

Program Mode Two - Different Integration Methods(Beeman and Euler):
- user chooses which integration method to use to display the animation
- orbital period and total energy (for each integration) are written to file when a graph is displayed
- graph of total energy is displayed (with both integration methods)

Program Mode Three - Doomsday Alignment:
- Beeman integration
- orbital period and total energy are written to file when a graph is displayed
- graph of total energy is displayed 
- planets upto and including jupiter are included 

note this mode was included for interest and has not been fully tested with more than 3 planets 
this mode is NOT one of my selected additional experiments

Program Mode Four - Satellites:
- Beeman integration is used throughout
- the program will determine the best velocity (the one which gives gets the closest to the target planet) - note this takes time to run, be patient. 
- A normal animation will be displayed with the satellite which gets closest to Mars 
- the inital velocity is written to a file 

Program Mode Five - Normal Animation:
- Beeman integration
- the percentage difference between orbital period of planets moving with influence of all planets and only influence from the sun is 
  calculated and written to a file when a graph is displayed
- Total energy are written to file and a graph is displayed


HOW TO RUN PROJECT:

The project is ran through the projectRun file, user inputs will appear, then the correct program Mode will be displayed

- Sometimes when running first time an empty plot will appear for the animation, in this case the plot needs to be closed and re-run the project

- The following modules are used, these are all required to run the program:
    - numpy
    - pandas
    - math
    - scipy
    - matplotlib
    - sys
    
- all simulation and planet parameters are changed through the excel file. 


ADDITIONAL NOTES:

- This project only uses SI units. 
- When choosing the number of velocitites to test for a satellite, 1 to 5 is recommended as the actual number that are 
testing is this number cubed, Anything more is a long wait before the animation begins. 
- In the animation, due to the size of the satellite and planet patches they appear to collide however this would 
not be the case if the radius of the planet was considered when sizing the patches. 
