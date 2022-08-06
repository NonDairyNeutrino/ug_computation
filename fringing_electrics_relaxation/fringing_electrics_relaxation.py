#basic settings and imports
import matplotlib
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
import numpy as np
from numpy import linalg as LA
#import pandas as pd
#import math


#this 'magic' matplotlib command tells iPython to show any figures in this notebook,
#rather than a separate window or saving them in separate files.
# %matplotlib inline

#These commands help python remember how to format my figures so that they look nice
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('pdf', 'png')
plt.rcParams['savefig.dpi'] = 200
plt.rcParams['figure.autolayout'] = True
plt.rcParams['figure.figsize'] = 10, 6
plt.rcParams['axes.labelsize'] = 18
plt.rcParams['axes.titlesize'] = 20
plt.rcParams['font.size'] = 16
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['lines.markersize'] = 8
plt.rcParams['legend.fontsize'] = 14

matplotlib.rcParams['xtick.direction'] = 'in'
matplotlib.rcParams['ytick.direction'] = 'in'

"""# Defining the Capacitor and Region of Interest"""

#Here we define a function that outputs the regions the capacitors occupy for a given capacitor length, seperation, number cells on a side of the system, and the size of the system.

def capacitor_data(capacitor_length, capacitor_separation, cell_number, system_size):

    center_of_system = cell_number/2 #Define the center of the grid/system in "units" of cells

    Delta_x = system_size/cell_number #Define the 'cell size'

    #The location of the top and bottom of the capacitor in number of cells
    capacitor_y_bot = int(center_of_system + capacitor_length/(2*Delta_x))
    capacitor_y_top = int(center_of_system - capacitor_length/(2*Delta_x))

    #The horizontal location of the capacitors
    capacitor_left_x = int(center_of_system - capacitor_separation/(2*Delta_x))
    capacitor_right_x = int(center_of_system + capacitor_separation/(2*Delta_x))

    return capacitor_y_bot, capacitor_y_top, capacitor_left_x, capacitor_right_x

#Define a grid using best-guess values, boundary conditions, and the number of cells.
#NOTE when defining cell_number use an odd number so that capacitors can be made to be centered within our range

def grid(cell_size, system_size, best_guess, bc_x_left, bc_x_right, bc_y_bot, bc_y_top, bc_left_capacitor, bc_right_capacitor, capacitor_length, capacitor_separation):
    cell_number = int(system_size / cell_size) #Number of cells on a side of the system
    system = np.full((cell_number, cell_number), best_guess) #define the array and populate with the best guess

    #use boundary conditions to define values at the top and bottom row
    system[0] = np.full(cell_number, bc_y_top)
    system[-1] = np.full(cell_number, bc_y_bot)

    #use boundary conditions to define values at the left and right column
    system[:,0] = np.full(cell_number, bc_x_left)
    system[:,-1] = np.full(cell_number, bc_x_left)

    #define rows and columns of capacitors
    capacitor_y_bot, capacitor_y_top, capacitor_left_x, capacitor_right_x = capacitor_data(capacitor_length, capacitor_separation, cell_number, system_size)

    #use boundary conditions and values found when calling capacitor_data to define the capacitors in the array
    system[capacitor_y_top : capacitor_y_bot, capacitor_left_x] = bc_left_capacitor
    system[capacitor_y_top : capacitor_y_bot, capacitor_right_x] = bc_right_capacitor

    return system, capacitor_y_bot, capacitor_y_top, capacitor_left_x, capacitor_right_x, system_size

"""# Create the Gauss-Seidel with Simultaneous Over-Relaxation Function"""

#Here we make define the Gauss-Seidel method with simultaneous over-relaxation

def GS(system_grid):

    system, capacitor_y_bot, capacitor_y_top, capacitor_left_x, capacitor_right_x, system_size = system_grid #import system properties

    dummy = np.copy(system)                       #initialize dummy as whatever system is right now, and not link to whatever it is later
    deltaV = np.zeros((len(system), len(system))) #Simultaneous over relaxation
    alpha = 2/(1 + np.pi/system_size)             #over relaxation parameter

    for i in range(1, len(system)-1): #Don't reset the boundaries
        for j in range(1, len(system) - 1): #Don't reset the other boundaries
            if (j == capacitor_left_x or j == capacitor_right_x) and capacitor_y_top <= i < capacitor_y_bot: #Don't reset the capacitor values
                continue
            else:
                dummy[i,j]   = 0.25*(system[i+1, j] + dummy[i-1, j] + system[i, j+1] + dummy[i, j-1]) #Gauss-Seidel
                deltaV[i, j] = dummy[i,j] - system[i, j]  #How much the system changes after a single averaging loop
                dummy[i,j] = alpha*deltaV[i,j] + system[i, j] #Update the system

    return dummy, deltaV

"""# Create a Function that Carries Out the Relaxation Method"""

#Here make a function that loops GS until the specified convergence criterion
#grid_output is the output of grid
def relax(grid_output, convergence): #Don't do it, till you want to get too it

    initial_system, capacitor_y_bot, capacitor_y_top, capacitor_left_x, capacitor_right_x, system_size = grid_output

    deltaV = np.full((len(initial_system), len(initial_system)), 10.) #Initialize the change array to later be overwritten
    system = initial_system #Initialize system
    i=0 #Initialize run count
    while np.abs(np.amax(deltaV)) > convergence:
        system, deltaV = GS((system, capacitor_y_bot, capacitor_y_top, capacitor_left_x, capacitor_right_x, system_size))
        i=i+1
    print("Number of averaging runs:", i)

    return system

"""# Create a Function To Calculate The Electric Feild in Each Cell"""

#Here we define a function to find the electric field given a potential distribution
#potential is the output of relax
def electric_field(potential, cell_size):
    x, y = potential.shape    #Set the length of the horizontal and vertical ranges to be the dimensions of the potential array
    field = np.zeros((x,y,2)) #Initialize the electic field array as an array of 2D vectors
    for i in range(y-1):
        for j in range(x-1):
            #x and y components of the electic field at i,j
            field[i, j, 0] = -0.5*(potential[i+1, j] - potential[i-1, j]) / cell_size #x component
            field[i, j, 1] = -0.5*(potential[i, j+1] - potential[i, j-1]) / cell_size #y component

    return field

"""# Define the Data that will be Plotted and Plot it Multiple Ways"""

#Here we define a test parameters to use in grid and test if our functions are working at all, and as they should be
test_cell_size = 1/50
test_system_size = 1.
test_best_guess = 0. #THINGS GET WEIRD WHEN OUR BEST GUESS IS CLOSE TO ONE OF THE CAPACITORS VALUES
test_bc_x_left = test_bc_x_right = test_bc_y_bot = test_bc_y_top = 0.
test_bc_left_capacitor = 1.
test_bc_right_capacitor = -1.
test_capacitor_length = test_system_size/2.
test_capacitor_separation = 0.4 #test_system_size/2.
test_convergence = 10.**(-5.)

#Test data of original grid to be relaxed
data = grid(test_cell_size, test_system_size, test_best_guess,             #Test system properties
            test_bc_x_left, test_bc_x_right, test_bc_y_bot, test_bc_y_top, #Test boundary conditions
            test_bc_left_capacitor, test_bc_right_capacitor, test_capacitor_length, test_capacitor_separation #Test capacitor properties
           )

potential = relax(data, test_convergence) #Test potential field through relaxation method

"""## Plot the potential"""

#The potential field around the capacitor
plt.imshow(potential,extent=[0, test_system_size, 0, test_system_size], origin='lower') #color plot of potential
plt.xlabel("x (a.u.)") #axis labels
plt.ylabel("y (a.u.)")
plt.title("Electric Potential")
cbar = plt.colorbar()
cbar.set_label('Volts', rotation=270)
plt.show()

#Here we make a contour plot of the potential around the capacitor
x, y = potential.shape #The dimensions of the potential grid
x_grid, y_grid = np.meshgrid(np.linspace(0, test_system_size, x), np.linspace(0, test_system_size, y)) #Get the horizontal and vertical domains in the right form for the contour function
contours = plt.contour(x_grid, y_grid, potential) #Make the contour plot
plt.clabel(contours, inline=True, fontsize=8) #Label the contours with their potentials
plt.imshow(potential, extent=[0, test_system_size, 0, test_system_size], origin='lower', alpha=0.4) #Overlay the potential distribution from above
cbar = plt.colorbar() #Add a legend
plt.xlabel("x (a.u.)")
plt.ylabel("y (a.u.)")
plt.title("Electric Potential")
cbar.set_label('Volts', rotation=270)
plt.show()

"""## Plot the electric field"""

#Here we plot the electric (vector) field around the capacitor
field = electric_field(potential, test_cell_size)      #Define the electric field from the potential distribution
plt.quiver(x_grid, y_grid, field[:,:,1], field[:,:,0]) #Vector field plot
plt.axes().set_aspect('equal')    #Set the aspect ratio to be square/equal
plt.xlabel("x (a.u.)")
plt.ylabel("y (a.u.)")

#Here we overlay all the plots on top of each other to get a full description of the physics in a single plot
field = electric_field(potential, test_cell_size)
x, y = np.meshgrid(np.linspace(0, 1, len(potential)), np.linspace(0, 1, len(potential)))
contours = plt.contour(x, y, potential) #create potential contours
plt.quiver(x, y, field[:,:,1], field[:,:,0])
plt.axes().set_aspect('equal')
plt.clabel(contours, inline=True, fontsize=8) #add potential contours
plt.imshow(potential, extent=[0, test_system_size, 0, test_system_size], origin='lower', alpha=0.6) #add in potential colormap
cbar = plt.colorbar()
plt.xlabel("x (a.u.)")
plt.ylabel("y (a.u.)")
cbar.set_label('Volts', rotation=270)
plt.show()

#Here we investigate the distribution of the electic field magnitude
field_mag = LA.norm(electric_field(potential, test_cell_size), axis = 2) #Electric field magnitude
x, y = np.meshgrid(np.linspace(0, 1, len(field_mag)), np.linspace(0, 1, len(field_mag)))
contours = plt.contour(x, y, field_mag)
plt.clabel(contours, inline=True, fontsize=8)
plt.imshow(field_mag, extent=[0, 1, 0, 1], origin='lower', alpha=0.6)
cbar = plt.colorbar()
plt.quiver(x_grid, y_grid, field[:,:,1], field[:,:,0]) #Vector field plot
plt.xlabel("x (a.u.)")
plt.ylabel("y (a.u.)")
cbar.set_label('Volts/cell size', rotation=270)
plt.show()

plt.plot(np.arange(0., 1., test_cell_size), LA.norm(electric_field(potential, test_cell_size), axis = 2)[int(test_system_size/test_cell_size/2)])
plt.xlabel("x (a.u.)")
plt.ylabel("Electric Field Magnitude (V/cell size)")
plt.title("y = 0.5")
#plt.legend(loc = "upper right")
plt.show()

"""## Electric Field as a function of plate seperation"""

#Define a function to calcualte the electric feild magnitudes at a chosen point for varying seperations of the capacitors
def electric_feild_magnitudes(point_x_position,point_y_position):
    point = [point_y_position,point_x_position] #define a point in the area of interest that we will focus on
    seperations = np.arange(0.1, 1.0, 0.1) #define the range of seperations and the steps we are observing
    magnitudes = np.zeros(len(seperations)) #make an empty array for the magnitudes
    i = 0 #initialize i
    for sep in seperations:
        data = grid(test_cell_size, test_system_size, test_best_guess,         #Test system properties
                test_bc_x_left, test_bc_x_right, test_bc_y_bot, test_bc_y_top, #Test boundary conditions
                test_bc_left_capacitor, test_bc_right_capacitor, test_capacitor_length, sep #Test capacitor properties
               )
        potential = relax(data, test_convergence) #find the potential data of the space
        field_mag = LA.norm(electric_field(potential, test_cell_size), axis = 2) #find the magnitude of the electric field at each point
        magnitudes[i] = field_mag[point[0],point[1]] #pull out the magnitude that corresponds to the point of interest we defined
        i+=1 #move on to next part of the array

    return magnitudes, seperations

#Here we investigate how the magnitude of the electric field at a point varies as a function of plate seperation

magnitudes, seperations = electric_feild_magnitudes(int(test_system_size/test_cell_size/2), int(test_system_size/test_cell_size/5))

magnitudes

plt.plot(seperations, magnitudes, 'k', label = "[0.5, 0.8]")
plt.xlabel("Plate Seperation (a.u.)")
plt.ylabel("Electric Field Magnitude (V/cell size)")
plt.legend(loc = "upper right")
plt.show()

#Here we investigate how the magnitude of the electric field at the center point as a function of plate seperation
magnitudes_center, seperations = electric_feild_magnitudes(int(test_system_size/test_cell_size//2),int(test_system_size/test_cell_size//2))

#Now we'll find the analytic solution at the center between the two plates to compare to our numerical solution
calculated_E = np.zeros(len(magnitudes_center)) #create an array to store our analytically calculated electric field in
for i in range(0,len(calculated_E)): #calculate the electric field with the equation for the electric field between a capacitor
    calculated_E[i]=abs((test_bc_right_capacitor-test_bc_left_capacitor))/seperations[i]

plt.plot(seperations, magnitudes_center, 'k', label = "Numerical")
plt.plot(seperations, calculated_E, label = "Analytic")
plt.xlabel("Plate Seperation (a.u.)")
plt.ylabel("Electric Field Magnitude (V/cell size)")
plt.legend(loc = "upper right")
plt.show()

difference_between_solutions = abs(magnitudes_center-calculated_E) #find the difference between the solutions
percent_error = difference_between_solutions/calculated_E #use the difference to find the percent error
plt.plot(seperations, percent_error) #plot percent error
plt.xlabel("Plate Seperation (a.u.)")
plt.ylabel("Percent Error in Electric Field Magnitude")

"""## Accuracy as a function of cell size"""

def varying_cell_size():
    cell_sizes = 1/(np.arange(10,55,5))
    sep = 0.25
    magnitudes = np.zeros(len(cell_sizes))
    difference_in_magnitudes = np.zeros(len(cell_sizes))
    percent_error = np.zeros(len(cell_sizes))

    #define a reference point/assumed (very close to) correct answer to compare our values for different cell sizes for.
    point_accurate = [int((test_system_size*100)/10),int((test_system_size*100)/4)] #define the point we will be looking at
                        #(the point in space will be the same, but as cell size is changing, the number of cells in is also changing and needs to be reevaluated)
    data_accurate = grid(1/100, test_system_size, test_best_guess,         #Test system properties
                test_bc_x_left, test_bc_x_right, test_bc_y_bot, test_bc_y_top, #Test boundary conditions
                test_bc_left_capacitor, test_bc_right_capacitor, test_capacitor_length, sep #Test capacitor properties
               )
    potential_accurate = relax(data_accurate, test_convergence) #potential for our reference system
    field_mag_accurate = LA.norm(electric_field(potential_accurate, 1/100), axis = 2) #magnitude of the electric field for our reference system
    accurate_magnitudes = field_mag_accurate[point_accurate[0],point_accurate[1]] #the magnitude of the electric field at our point of interest for our reference system

    i = 0
    for size in cell_sizes: #run through the cell sizes
        point = [int(test_system_size/size/10),int(test_system_size/size/4)] #define location based on cells
        data = grid(size, test_system_size, test_best_guess,         #Test system properties
                test_bc_x_left, test_bc_x_right, test_bc_y_bot, test_bc_y_top, #Test boundary conditions
                test_bc_left_capacitor, test_bc_right_capacitor, test_capacitor_length, sep #Test capacitor properties
               )
        potential = relax(data, test_convergence) #calculate the potential of the field
        field_mag = LA.norm(electric_field(potential, size), axis = 2) #calculate the magnitude of the field
        magnitudes[i] = field_mag[point[0],point[1]] #select magnitude that corresponds to our point
        difference_in_magnitudes[i] = abs(magnitudes[i]-accurate_magnitudes) #find the difference in the electric field magnitudes at the same point for different cell sizes
        percent_error[i] = difference_in_magnitudes[i]/accurate_magnitudes #convert difference to percent error
        i+=1

    return difference_in_magnitudes, cell_sizes, percent_error

differences, cell_size, percent = varying_cell_size()

#plt.plot(cell_size, differences)
plt.plot(cell_size, percent)
plt.xlabel("Cell Size")
plt.ylabel("Percent Error in Electric Field Magnitude")
