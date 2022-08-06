"Function Tests"
print(schwarz_radius(sun_mass)) #Should equal 2.95 km or about 2950 m in SI
print(
	gravity(
		5.97*10**24, #Earth mass
		np.array([0., 6.37*10**6]), #Earth radius
		np.array([0.,0.]),
		"GR"
	) #test for the gravity at the surface of the Earth
) #Since the GR effects of Earth are negligible, this should be about -9.8 m/s^2
print(verlet(1., 0., 0., 1.)) #Should be 2
print(verlet(1., 0., 2., 1.)) #Should be 4
print(step(
	5.97*10**24, #Earth mass
	np.array([[0., 6.37*10**6],[0., 6.37*10**6 - 9.8/2]]), #Earth radius
	np.array([[0.,0.],[0,-9.8]]),
	1.
))
first_position, first_velocity, test_time_step = first_step(sun_mass, initial_position, initial_velocity)
position, velocity = (np.array([initial_position, first_position]), np.array([initial_velocity, first_velocity]))
# test_position, test_velocity = orbit(sun_mass, mercury_mass, position, velocity, mercury_eccentricity, test_time_step)
test_position, test_velocity, test_periapsides, test_periapsides_angle, test_distances_array = multiple_orbits(sun_mass, mercury_mass, position, velocity, mercury_eccentricity, test_time_step, number_of_orbits)

test_time_step = mercury_year / 100
initial_position = np.array([46.*10.**9., 0.]) #start at perihelion
initial_velocity = np.array([0., (59*10**3)]) #speed at perihelion
number_of_orbits = int(np.ceil(100*(year/mercury_year)))
test_modifier = "GR" #Can be GR or Newtonian

test_position, test_velocity, test_periapsides, test_periapsides_angle, eccentricity = main(sun_mass, mercury_mass, initial_position, initial_velocity, number_of_orbits, test_modifier, 2000)

"Method tests"
# SAVE JUST COMPUTED DATA
np.savetxt(data_dir+test_modifier+str(int(number_of_orbits*mercury_year/year))+'positions.txt', test_position)
np.savetxt(data_dir+test_modifier+str(int(number_of_orbits*mercury_year/year))+'periapsides.txt', test_periapsides)
np.savetxt(data_dir+test_modifier+str(int(number_of_orbits*mercury_year/year))+'periapsides_angles.txt', test_periapsides_angle)

np.savetxt(data_dir+test_modifier+'distances_'+str(int(number_of_orbits*mercury_year/year))+'.txt', test_distances_array)

# USE ALREADY COMPUTED DATA
test_position = np.loadtxt(data_dir+test_modifier+str(int(number_of_orbits*mercury_year/year))+'positions.txt')
test_periapsides = np.loadtxt(data_dir+test_modifier+str(int(number_of_orbits*mercury_year/year))+'periapsides.txt')
test_periapsides_angle = np.loadtxt(data_dir+test_modifier+str(int(number_of_orbits*mercury_year/year))+'periapsides_angles.txt')

test_distances_array = np.loadtxt(data_dir+'distances_'+str(int(number_of_orbits*mercury_year/year))+'.txt')

orbits = np.arange(0, number_of_orbits)*mercury_year/year

trajectory_plot(test_position)
periapsis_angle_plot(orbits, test_periapsides_angle)
distance_plot(np.linspace(0., number_of_orbits, len(test_distances_array)), test_distances_array)
