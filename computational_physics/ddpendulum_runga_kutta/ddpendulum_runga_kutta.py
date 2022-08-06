#basic settings and imports
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
import math


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

#physical parameters for the problem

g=9.8         #Gravity
l=9.8         #The length of the pendulum is chosen in the book so that g/l == 1
damping=.5    #Damping coefficient as chosen in the book
omega_D=2./3. #Frequency of the driving force as in the book

#This is used to calculate omega and theta derivatives at any time or position
def calculate_derivatives(theta, omega, time, driving_force):

  d_theta = omega #Angle derivative from book

  d_omega = -(g/l)*np.sin(theta) - damping*d_theta + driving_force*np.sin(omega_D*time) #Angular speed derivative from book

  return d_theta, d_omega



#This is the intermediate step in RK2 that calculates the middle point for any
#position or time
def half_step(theta, omega, driving_force, time, time_step):

  #uses calculate derivatives to get the values
  d_theta, d_omega = calculate_derivatives(theta, omega, driving_force, time)

  #uses the RK2 method of calculating the midstep so the time step is /2
  half_theta_i= theta + d_theta * time_step/2
  half_omega_i= omega + d_omega * time_step/2


  return half_theta_i, half_omega_i


#The second part of RK2 takes the points from half_step and calculates the next values
def full_step(theta, half_theta, omega, half_omega, time, driving_force, time_step):

  #Calculating the derivative at the calculated mid point
  d_theta, d_omega = calculate_derivatives(half_theta,half_omega,time,driving_force)

  #RK2 adding of the midpoint derivative to the old values
  new_theta_i = theta + d_theta * time_step
  new_omega_i = omega + d_omega * time_step

  return new_theta_i,new_omega_i


#This is the RK2 implementation, first it calculates the intermediate step, then
#it uses that point to calculate the next theta and omega
def increment_stuff(theta_i, omega_i,  time_step, time, driving_force = 0):

  #this is the first midpoint calculation
  half_theta_i, half_omega_i = half_step(theta_i, omega_i, time, driving_force, time_step)

  #using the values calculated this finds the actual full step values
  new_theta_i , new_omega_i = full_step(theta_i, half_theta_i, omega_i, half_omega_i, time + time_step/2, driving_force, time_step)

  return new_theta_i, new_omega_i


#This runs the incrementation in a loop and stores the values in lists that are returned
def run_simulation(theta_i, omega_i, driving_force, time_step, total_time):

  #creating a list to the total time with incriment of the timestep
  times = np.arange(0., total_time, time_step)

  #initializing the list of values
  theta_list = [theta_i]
  omega_list = [omega_i]

  #each value in the time array
  for time in times:

    #for each of the timesteps we use our incrementstuff to find the next value
    new_theta_i, new_omega_i = increment_stuff(theta_list[-1], omega_list[-1], time_step, time, driving_force)

    #appending each of our lists
    theta_list.append(new_theta_i)
    omega_list.append(new_omega_i)

  #making our lists np arrays because they are more useful that way
  final_theta_list = np.array(theta_list)
  final_omega_list = np.array(omega_list)

  return theta_list,omega_list,times

#Angle_shift takes in a list of values and shifts points that are not within
#-pi to pi
def angle_shift(angle):

    #making any array an np array so that we can do the calculations
    new_angle = np.array(angle)

    #this loop will continue to run until every value is with the range we want
    while np.any(new_angle < -np.pi) or np.any(new_angle > np.pi):

        #This iterates through each value of our list
        for i in range(len(new_angle)):

            #if the value is under pi add 2 pi
            if new_angle[i] < -np.pi:
                new_angle[i] += +2*np.pi

            #if the value is over pi subtract 2 pi
            elif new_angle[i] > np.pi:
                new_angle[i] -= 2*np.pi

    return np.array(new_angle)

#This gets all the angles in the Poincare section/the angle of the pendulum after each driving period
def poincare_angle(initial_angle, initial_speed, driving_force, time_step, final_time):

	data = run_simulation(initial_angle, initial_speed, driving_force , time_step , final_time) #Get all the angles

	idx = get_poincare(data[-1]) #Get the indices of the time after each driving period

	periodic_angle_list = angle_shift(np.array(data[0])[idx]) #Shift the "period angles" into the interval [-pi,pi]

	return periodic_angle_list

#Here we choose some parameters to analyze the system
theta_i = 0.2       #Initial angle from book
omega_i = 0.        #Initial angular speed
driving_force = 1.2 #Amplitude of the driving force
time_step = 0.04    #Time step as in book
total_time = 60.    #Total time we let the pendulum move

theta_list, omega_list, times = run_simulation(theta_i , omega_i , driving_force , time_step , total_time) #Create the data once so we don't have to re-create it every time
#The above data is: list of angles throughout the run time, list of angular speeds thoughout the run time, list of times data was calculated

"""# Numerical analysis

To check the numerical accuracy of the code we performed two tests. First, we lowered $\Delta$T incrimentally to see how our routine was effected by different time steps. This first figure shows that lower $\Delta$T's converge farther along the time axis as we would expect. The chaotic behavior makes trajectories that diverge from each other very different at large values of time. The second test we used was comparing our trajectory to Dr. Covey's trajectory with the same $\Delta$T. We plot the difference between these trajectories over time and notice that the y-axis is on the order of $10^{-9}$ meaning the difference is very small between the solutions even at large values of time. These two test leads us to believe our routine is working as intended.
"""

#Here we make the analyze the (Left) angular evolution for different driving forces,
#(Center) angular evolution for a driving force of 1.2 of both the true values and with the shift,
#(Right) angular speed for different driving forces

#the size that look best on my computer
plt.figure(figsize=(20,6))

plt.suptitle('Figure 3.6',y=1.05,fontsize=34)

#We need 3 subplots, this is the first
plt.subplot(131)

#the 3 values of damping we're interested in
for driving_force_i in [0,.5,1.2]:

  #running each of the simulations for the left plot and then plotting them
  theta_list, omega_list, times = run_simulation(theta_i , omega_i , driving_force_i , time_step , total_time)
  plot_angles = angle_shift(theta_list[:-1]) - driving_force_i*6
# This angle data (plot_angles), up until the last point, is being shifted into the -[pi,pi] range to help with the physical analysis, and then shifted down again so that each graph is on the same plot.
  plt.plot(times, plot_angles, label = '$F_d$ = ' + str(driving_force_i))

plt.xlabel("time (s)")
plt.ylabel(r"$ \theta $  (radians)")
plt.legend()


#Second figure of the plots
plt.subplot(132)

#this is either shifting or not shifting the values to wrap them around
plt.plot(times, angle_shift(theta_list[:-1]), label = '$F_d$ = ' + str(driving_force_i), color = 'C2')
plt.plot(times, np.array(theta_list[:-1]) - np.pi*2, label = '$F_d$ = ' + str(driving_force_i), color = 'C2')

plt.xlabel("time (s)")
plt.ylabel(r" $\theta$ (radians)")


plt.subplot(133)

#we run 3 simulations again, Computationally inefficient (already calculated these)
#but this makes it easer to lay out the code in relevent sections
for driving_force_i in [0,.5,1.2]:
  theta_list, omega_list, times = run_simulation(theta_i , omega_i , driving_force_i , time_step , total_time)
  plt.plot(times,angle_shift(omega_list[:-1])-driving_force_i*6,label='$F_d$ = '+str(driving_force_i))


plt.xlabel("time (s)")
plt.ylabel(r"$\omega$ (radians/s)")

plt.legend()

'''
  FOR THIS TO WORK CORRECTLY YOU NEED TO UPLOAD THE CHECK FILE WITH
  THE NAME 'verify_Pendulum_HW3.txt' USING THE UPLOAD BUTTON HERE
'''

from google.colab import files
uploaded = files.upload()

#loading the txt in so we can compare
verify = np.loadtxt('verify_Pendulum_HW3.txt', skiprows=1)

#comparing various values of DELTA T to ours for convergence
for time_step_i in [.2,.1,.06,.04]:
  theta_list, omega_list, times = run_simulation(theta_i, omega_i, driving_force, time_step_i, total_time)
  plt.plot(times, theta_list[:-1], label = u'\u0394T = '+str(time_step_i))

plt.plot(verify[:,0], verify[:,1], 'k--', label = 'Coveys') #The "correct" data
plt.xlabel("time (s)")
plt.ylabel(r" $\theta$  (radians)")
plt.legend()

#Here we directly investigate the error between our data and the "correct" data by looking at an overlay and differences themselves

#again choosing the figure size that seems reasonable to me
plt.figure(figsize=(15,6))

#first plot is the the visual inspection for agreement
plt.subplot(121)

plt.scatter(times, theta_list[:-1], s=5, label='Ours')    #Our data
plt.plot(verify[:,0], verify[:,1], 'k--', label='Coveys') #Correct data

plt.xlabel("time (s)")
plt.ylabel(r" $\theta$  (radians)")
plt.legend()

#this plot is differnce between ours and Coveys calculation
plt.subplot(122)

differnce = verify[:,1] - np.array(theta_list[:-2]) #Difference between our data and the correct data
plt.plot(times[:-1], np.abs(differnce))

#this size scale of the differnces in 9 decimals
plt.ylim(-3*(10**-9), 3*(10**-9))
plt.xlabel("time (s)")
plt.ylabel(r"$|Covey-Ours|$ (radians)")

#Here we look at how the system behaves in the angle-angle_speed phase space for (Left) a non-chaotic driving force of 0.5, and (Right) a chaotic driving force of 1.2
#These plots and calculations were done for an evolution over 300 seconds

plt.figure(figsize=(15,6))
plt.suptitle('Figure 3.8',y=1.05,fontsize=34)

i=1
for driving_force_i in [0.5,1.2]:
  plt.subplot(1,2,i)
  theta_list, omega_list, times = run_simulation(theta_i, omega_i, driving_force_i, time_step, 300)
  plt.scatter(angle_shift(theta_list), omega_list, s = 5)
  i+=1

  plt.xlabel(r" $\theta$  (radians)")
  plt.ylabel(r"$\omega$ (radians/s)")

#Here we define a function where when you give it your array of times, it gives the indices of the times that are integer multiples of the driving period.
#This is done so that the corresponding data of angle and angular speed can be easily extracted with the same indices

def get_poincare(time):

  #initializing the values and lists we need
  idx = []
  last_time = time[-1]

  #omega_d*t/2 pi gives us N which with the last time will give us the total
  #N points satisfy the equation
  tot_points = int((omega_D*last_time)//(2*np.pi))


  for n in range(tot_points):
    distance_from = np.abs(time*omega_D-n*2*np.pi)
    idx.append(distance_from.argmin())

  return idx

#since we are using driving periods having pi in the timestep helps for accuracy
time_step=np.pi/100

#Here we get the Poincare section of the system with our standard parameters,
#but in this case, in order to get all the points needed to reproduce the figure in the book,
#the final time needs to be bumped up to 60,000 seconds

theta_list, omega_list, times = run_simulation(theta_i, omega_i, driving_force, time_step, 60000) #All the data

idx = get_poincare(times) #The indices of the driving periods


plt.scatter(
    np.array(angle_shift(theta_list))[idx], #The shifted angles at the driving periods
    np.array(omega_list)[idx],              #The angular speeds at the driving periods
    s=5                                     #Marker size
)

plt.title('Figure 3.9',fontsize=34)
plt.xlabel(r" $\theta$  (radians)")
plt.ylabel(r"$\omega$ (radians/s)")

#Creating the data for the different Poincare sections, and then the bifurcation diagram

poincare_angles, poincare_speeds, poincare_times = [], [], []

for driving_force in [1.4, 1.44, 1.465]:
    theta_list, omega_list, times = run_simulation(theta_i, omega_i, driving_force, time_step, 6*10**3)
    poincare_angles.append(theta_list)
    poincare_speeds.append(omega_list)
    poincare_times.append(times)

# print(poincare_angles)
# print(poincare_speeds)
# print(poincare_times)

#Here we look at the Poincare sections of the system for driving forces of (Top) 1.4, (Center) 1.44, (Bottom) 1.465 over the course of 6,000 seconds
plt.figure()
plt.suptitle('Problem 3.18',fontsize=34,y=1.05)

grid, subs = plt.subplots(3, sharex = True)

for i in range(len(poincare_times)):
    idx = get_poincare(poincare_times[i]) #Poincare indices
    subs[i].scatter(
        np.array(angle_shift(poincare_angles[i]))[idx[15:]], #period angles starting with i=15 (To remove transient behavior)
        np.array(poincare_speeds[i])[idx[15:]],              #period speeds starting with i=15 (To remove transient behavior)
        s=5
    )
plt.show()

#Here we create the data for the bifurcation diagram (i.e. the angle the pendulum is at every driving period as a function of the driving force)
#For each driving force, the data is created for simulation of 6,000 seconds and the standard parameters

#Initialization of the data arrays
driving_forces = np.array([])
poincare_thetas = np.array([])

idx = get_poincare(times) #Indices of the driving periods

for driving_force_i in np.arange(1.35, 1.5, 0.0005):
  theta_list, omega_list, times = run_simulation(theta_i, omega_i, driving_force_i, time_step, 6000)

  dummy_driving_i = np.full(
      len(idx[-500:]), #Length of the array of all but the first 10 Poincare indices to get rid of the transient behavior
      driving_force_i
  ) #This is an array of length len(idx[-500:]) and every element is driving_force_i.

  driving_forces = np.concatenate((driving_forces,dummy_driving_i)) #Final array of driving forces to be used as the x-axis in the bifurcation diagram

  dummy_theta     = np.array(theta_list)[idx[-500:]]               #Non-transient Poincare angles
  poincare_thetas = np.concatenate((poincare_thetas,dummy_theta)) #quasi-final array of Poincare angles for the different driving forces to be used in the birfurcation diagram

poincare_thetas = angle_shift(poincare_thetas) #After the shift of the angles into the interval [-pi, pi],
#this is the actual final array of Poincare angles for the different driving forces to be used in the birfurcation diagram

#Final plot of the bifurcation diagram for a driving force range of 1.35 to 1.5 in steps of 0.0005

plt.scatter(driving_forces, angle_shift(poincare_thetas), s=.1)
plt.ylim(.9,3)

plt.title('Bifurcation Diagram',fontsize=34)
plt.ylabel(r'$\omega$ (raidans)')
plt.xlabel('$F_D$')
