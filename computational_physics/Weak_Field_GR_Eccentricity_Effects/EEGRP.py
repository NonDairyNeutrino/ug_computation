"""
Physics 486: Computational Physics Final Projet
Title: Effects of Eccentricity on General Relativistic Precession
Author: Nathan Chapman
"""

"""
Project Psuedocode

> initialize position of planet/distance from central body, planet velocity vector, planet mass, orbital eccentricity
> use modified gravity to find acceleration a(t) of the planet
> update position with energy conserving method like Runge-Kutta, Euler-Cromer, or Verlet
> update velocity with energy conserving method as above
> update time with t -> t + dt
> repeat above until the planet reaches periapsis, and record the position to find the angle that the periapsis has moved by
> repeat above for several orbits
> find line of best fit for the periapsis angles as a function of time
> find and record slope of the best fit line/rate of precession for that eccentricity

Gravitational Interaction

> initialize position/distance from Sun, scaling parameters
(planet mass, star mass, eccentricity, Gravitational constant, speed of light)
> update the acceleration a(t) between the Sun and the planet via
the modified/perturbed Newtonian gravity with the previous position
> return acceleration at the next time step
"""

"Packages"
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import multiprocessing as mp

"Global/Physical Constants"
light_speed = 3.*10**8 #m/s
Newton_G = 6.67 * 10**(-11) #m^3 kg^-1 s^-2
sun_mass = 1.99*10**30 #kg
earth_mass = 5.97*10**24 #kg
earth_radius = 6.37*10**6 #meters
earth_eccentricity = 0.0167
au = 1.496*10**(11) #1 astronomical unit in meters
year = 3.154*10**(7) #1 year in seconds
mercury_year = 7.6*10**6 #seconds
mercury_distance = 0.31*au
mercury_mass = 3.33*10**(25) #kg
mercury_eccentricity = 0.205
mercury_orbital_velocity = 4.74*10**4 #m/s

data_dir = 'Data/'
vis_dir = 'Visualizations/'

"Functions"
#Schwarzchild radius
#Input: scalar mass of central body e.g. the Sun
#Output: Schwarzchild radius for given mass
def schwarz_radius(mass):
	r_s = 2 * Newton_G * mass / (light_speed**2)
	return r_s

#r_L from paper
#Input: 2D vectors of position and velocity
#Output: Scalar (? this might not be right) angular momentum radius
def ang_mom_radius_squared(position, velocity):
	r_L2  = np.sum(np.cross(position, velocity)**2) / (light_speed**2)
	return r_L2

#Modified gravity from paper
#Input: scalar mass of central body, vector position of planet, vector velocity of planet
#Output: vector acceleration due to modified gravity of the central body at that position
def gravity(mass, position, velocity, modifier):
	distance = LA.norm(position) #This implicitly defines the sun as the origin
	if modifier == "GR":
		acceleration = -0.5 * light_speed**2 * schwarz_radius(mass) * (1 + 3 * ang_mom_radius_squared(position, velocity) / distance**2) * position / (distance**3)
		#print(acceleration*year**2/au)
	elif modifier == "Newtonian":
		acceleration = -1*Newton_G*mass*position / distance**3
		#print(acceleration*year**2/au)
	else:
		print('no')
		quit()
	return acceleration

#Verlet method
#Input: current point, previous point, current second derivative, time step
#Output: the next point
def verlet(y_i, y_im1, current_second_derivative, time_step):
	y_ip1 = 2.*y_i - y_im1 + current_second_derivative*time_step**2
	return y_ip1

#Function that steps the simulation forward by one iteration
#Input: mass of central body, position array with at least 2 elements, velocity array
#Output: next position, next velocity
def step(mass, position, velocity, time_step, modifier):
	a_i   = gravity(mass, position[-1], velocity[-1], modifier)          #acceleration due to modified gravity
	r_ip1 = verlet(position[-1], position[-2], a_i, time_step) #verlet iteration of position
	v_ip1 = 0.5*(r_ip1 - position[-2])/time_step               #velocity iteration from centered difference
	return r_ip1, v_ip1

#Function to determine the first point after the initial value via Euler-Cromer method
#Input: mass of central body, scalar initial position,
#Output: first position, first velocity
def first_step(central_mass, initial_position, initial_velocity, modifier, time_scale):
	acceleration = gravity(central_mass, initial_position, initial_velocity, modifier)
	time_step = 2*LA.norm(initial_velocity)/LA.norm(acceleration)/time_scale #to make sure the time step is small enough for the evolution below
	#print(time_step/60)
	next_velocity = initial_velocity + acceleration * time_step
	next_position = initial_position + next_velocity * time_step
	return next_position, next_velocity, time_step

#Find the angle of a vector in Cartesian coordinates
#Input: a 2D vector
#Output: the principal angle the vector makes with the x-axis
def vector_angle(vector):
	angle = np.arctan2(vector[1], vector[0])
	#This gives the counterclockwise angle from the x-axis
	# if vector[1] >= 0:
	# 	angle = np.arctan2(vector[1], vector[0])
	# else:
	# 	angle = 2*np.pi + np.arctan2(vector[1], vector[0])
	return angle

#Loop step through one orbit/till it gets back to periapsis
#Input: mass of central body, array of previous two positions, array of previous two velocities, eccentricity, time step
#Output: array of positions for this orbit, array of velocities for this orbit
def orbit(central_mass, orbit_mass, position_array, velocity_array, time_step, modifier):
	angular_momentum = orbit_mass * np.cross(position_array[-1], velocity_array[-1]) #ASSUMING CENTRAL BODY IS FIXED
	reduced_mass = central_mass * orbit_mass / (central_mass + orbit_mass)
	pop = LA.norm(angular_momentum)**2 / (Newton_G * central_mass * orbit_mass * reduced_mass) #Principal Orbital Parameter (c in Taylor), NOT SPEED OF LIGHT
	eccentricity = (pop / LA.norm(position_array[0])) - 1
	semi_major_axis = pop/(1 - eccentricity**2)
	period = np.sqrt(4*np.pi**2 * semi_major_axis**3 * reduced_mass / (Newton_G * central_mass * orbit_mass)) #Orbital period
	#print(period/60/60/24) #Earth days
	position, velocity = (position_array, velocity_array) #Initialize position and velocity

	for time in np.arange(0., period, time_step):
		next_position, next_velocity = step(central_mass, position, velocity, time_step, modifier)
		position = np.append(position, [next_position], axis = 0)
		velocity = np.append(velocity, [next_velocity], axis = 0)

	#Now position is the array of positions for this orbit plus the last two positions from the previous orbit

	#Find the periapsis of the orbit
	distances = LA.norm(position[2:], axis = 1) #array of distances of this orbit
	index_of_periapsis = np.argmin(distances) #index_of_periapsis of this orbit
	#print(index_of_periapsis)
	periapsis = (position[2:])[index_of_periapsis] #periapsis of this orbit
	periapsis_angle = vector_angle(periapsis)*(180/np.pi)*3600 #convert from radians to arcseconds #angle of periapsis of this orbit

	return position[2:], velocity[2:], periapsis, periapsis_angle, eccentricity

#Loop orbit
#Input: mass of central body, array of previous two positions, array of previous two velocities, eccentricity, time step, number of orbits
#Output: array of positions for whole time, array of velocities for whole time, array of positions of periapsides for whole time, array of angles of periapsides for whole time, array of distances for whole time
def multiple_orbits(central_mass, orbit_mass, position_array, velocity_array, time_step, number_of_orbits, modifier):
	position, velocity = (position_array, velocity_array) #Initialize multiple orbit position and velocity arrays
	periapsides = np.zeros(len(position_array[0])*number_of_orbits).reshape(number_of_orbits, len(position_array[0])) #pre-allocate periapsides array
	periapsides_angle = np.zeros(number_of_orbits) #pre-allocate periapsides array

	#Force the first periapsis to be the first element of the position array because WE'RE STARTING AT PERIAPSIS
	periapsides[0] = position[0]
	periapsides_angle[0] = vector_angle(position[0])

	for i in range(1, number_of_orbits):
		orbit_position, orbit_velocity, orbit_periapsis, orbit_periapsis_angle, orbit_eccentricity = orbit(central_mass, orbit_mass, position[-2:], velocity[-2:], time_step, modifier)
		if i == 1:
			position = np.append(position, orbit_position, axis = 0)
			velocity = np.append(velocity, orbit_velocity, axis = 0)
			periapsides[i] = orbit_periapsis
			periapsides_angle[i] = orbit_periapsis_angle
			eccentricity = orbit_eccentricity
			#distances_array = np.append(LA.norm(position_array, axis = 1), orbit_distances)
		else:
			position = np.append(position, orbit_position, axis = 0)
			velocity = np.append(velocity, orbit_velocity, axis = 0)
			periapsides[i] = orbit_periapsis
			periapsides_angle[i] = orbit_periapsis_angle
			#distances_array = np.append(distances_array, orbit_distances)

	return position, velocity, periapsides, periapsides_angle, orbit_eccentricity

#Best fit line for periapsis angles
#Input: array of times, array of periapsides angles
#Output: slope/rate of angular precession
def precession_rate(times, angles):
	rate = np.polyfit(times, angles, 1)[0]
	return rate

#MAIN ROUTINE
#Input:
#Output:
def main(central_mass, orbit_mass, initial_position, initial_velocity, number_of_orbits, modifier, time_scale):
	first_position, first_velocity, time_step = first_step(central_mass, initial_position, initial_velocity, modifier, time_scale)
	position, velocity = (np.array([initial_position, first_position]), np.array([initial_velocity, first_velocity]))
	position, velocity, periapsides, periapsides_angle, eccentricity = multiple_orbits(central_mass, orbit_mass, position, velocity, time_step, number_of_orbits, modifier)

	return position, velocity, periapsides, periapsides_angle, eccentricity

#Trajectory plot
#Input:
#Output:
def trajectory_plot(positions):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(positions[:,0]/au, positions[:,1]/au, linewidth = 2)
	ax.plot([0], [0], 'yo', markersize = 15)
	ax.set_xlabel('x [au]')
	ax.set_ylabel('y [au]')
	ax.grid(True)
	ax.set_title("Mercury's orbit over "+str(int(number_of_orbits*mercury_year/year))+" Earth years")
	ax.set_aspect('equal')
	fig.savefig(vis_dir+'Trajectory_'+str(int(number_of_orbits*mercury_year/year))+'.pdf')
	plt.show()

#
#Input:
#Output:
def periapsis_angle_plot(times, periapsides_angles):
	rate = precession_rate(times, periapsides_angles)
	plt.plot(times, periapsides_angles, times, rate*times + periapsides_angles[0])
	plt.xlabel('Time (Earth years)')
	plt.ylabel('Periapsis angle (arcseconds)')
	plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	plt.title('Precession rate: '+str(round(rate*100,0))+' arcseconds/century')#'Precession of Mercury over '+str(int(number_of_orbits*mercury_year/year))+" Earth years")
	plt.tight_layout()
	plt.savefig(vis_dir+'Precession_Angle_'+str(int(number_of_orbits*mercury_year/year))+'.pdf')
	plt.show()

#Distance plot
#Input:
#Output:
def distance_plot(times, distances):
	plt.plot(times, distances/au)#*mercury_year/year
	plt.xlabel('Time (Earth years)')
	plt.ylabel('Distance from Sun (Au)')
	plt.tight_layout()
	#plt.title(str(int(number_of_orbits))+" Earth years")
	#plt.savefig(vis_dir+'Distance_'+str(int(number_of_orbits))+'.pdf')
	plt.show()

#Comparing Newtonian to GR
#Input: distance lower bound, distance upper bound, mass of central object, velocity vector of object
#Output: plot of difference between Newtonian gravity and GR
def gravity_comparison(lower_distance, upper_distance, mass, velocity):
	distances = np.linspace(lower_distance, upper_distance, 100)*au
	newton = np.array([LA.norm(gravity(mass, np.array([r, 0.]), velocity, "Newtonian")) for r in distances]) #np.array([0, 2*np.pi*au/year])
	GR = np.array([LA.norm(gravity(mass, np.array([r, 0.]), velocity, "GR")) for r in distances])

	plt.plot(distances/au, np.abs(newton - GR))
	plt.plot([0.31, 0.31], [np.abs(newton - GR)[-1], np.abs(newton - GR)[0]], 'k--') #Mercury's perihelion
	plt.plot([0.47, 0.47], [np.abs(newton - GR)[-1], np.abs(newton - GR)[0]], 'k--') #Mercury's aphelion
	plt.xlabel("Distance (au)")
	plt.ylabel("Acceleration (m/s^2)")
	plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
	#plt.title("Newtonian-GR Comparison")
	plt.tight_layout()
	#plt.savefig(vis_dir+'Newton_GR_Comp_Mercury.pdf')
	plt.show()

#PRECESSION RATE VS ECCENTRICITY
number_of_factors = 10
initial_position = np.array([46.*10.**9., 0.]) #start at perihelion
number_of_orbits = int(np.ceil(20*(year/mercury_year)))
test_modifier = "GR" #Can be GR or Newtonian
orbits = np.arange(0, number_of_orbits)*mercury_year/year

def foo(factor):
	initial_velocity = np.array([0., (59*10**3)*factor]) #speed at perihelion
	test_position, test_velocity, test_periapsides, test_periapsides_angle, eccentricity = main(sun_mass, mercury_mass, initial_position, initial_velocity, number_of_orbits, test_modifier, 2000)
	rate = precession_rate(orbits, test_periapsides_angle)*100

	return eccentricity, rate

if __name__ == '__main__':
	pool = mp.Pool(mp.cpu_count()-1)
	results = np.transpose(pool.map(foo, np.linspace(0.915, 1.2, number_of_factors))) #1.285 gives an eccentricity of about 0.99
	pool.close()
	plt.plot(results[0], results[1])
	plt.xlabel('Eccentricity')
	plt.ylabel('Precession Rate (arcseconds/century)')
	plt.tight_layout()
	plt.savefig(vis_dir+'rate_v_eccentricity_final.pdf')
	plt.show()

# i = 0
# number_of_factors = 2
# initial_position = np.array([46.*10.**9., 0.]) #start at perihelion
# number_of_orbits = int(np.ceil(100*(year/mercury_year)))
# test_modifier = "GR" #Can be GR or Newtonian
# orbits = np.arange(0, number_of_orbits)*mercury_year/year
#
# eccentricities = np.zeros(number_of_factors)
# rates = np.zeros(number_of_factors)
#
# for factor in [1.2]: #np.linspace(0.915, 1.285, number_of_factors): #Starting and stopping points are hard coded because I just manually found the factors that gave eccentricities close to 0 and 1
# 	initial_velocity = np.array([0., (59*10**3)*factor]) #speed at perihelion
# 	test_position, test_velocity, test_periapsides, test_periapsides_angle, eccentricity = main(sun_mass, mercury_mass, initial_position, initial_velocity, number_of_orbits, test_modifier)
# 	eccentricities[i] = eccentricity
# 	rates[i] = precession_rate(orbits, test_periapsides_angle)*100
# 	i += 1
#
# plt.plot(eccentricities, rates)
# plt.xlabel('Eccentricity')
# plt.ylabel('Precession Rate (arcseconds/century)')
# plt.show()

# COMPARISON BETWEEN NEWTONIAN GRAVITY AND GR FOR INTERESTING REGIMES
# gravity_comparison(0.3, 0.48, sun_mass, np.array([0, mercury_orbital_velocity]))

#3D PLOT OF ORBIT
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(test_position[0]/au, test_position[1]/au, test_position[2]/au)
# plt.show()
