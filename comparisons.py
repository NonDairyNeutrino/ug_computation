#TRAJECTORIES FOR DIFFERENT TIME STEPS
initial_position = np.array([au, 0.]) #Earth distance from sun
initial_velocity = np.array([0., 2*np.pi*au/year]) #Earth average orbital speed
number_of_orbits = 10#int(np.ceil(1*(year/mercury_year)))
test_modifier = "GR" #Can be GR or Newtonian
scales = np.linspace(2, 20, 5)
i=0
fig = plt.figure()
ax = fig.add_subplot(111)

for time_scale in scales:
	test_position, test_velocity, test_periapsides, test_periapsides_angle, eccentricity = main(sun_mass, earth_mass, initial_position, initial_velocity, number_of_orbits, test_modifier, time_scale)
	np.savetxt(data_dir+'Earth'+test_modifier+str(number_of_orbits)+'_'+str(time_scale)+'positions.txt', test_position)
	np.savetxt(data_dir+'Earth'+test_modifier+str(number_of_orbits)+'_'+str(time_scale)+'periapsides.txt', test_periapsides)
	np.savetxt(data_dir+'Earth'+test_modifier+str(number_of_orbits)+'_'+str(time_scale)+'periapsides_angles.txt', test_periapsides_angle)

	ax.plot(test_position[:,0]/au, test_position[:,1]/au, linewidth = 1, label = str(time_scale))

ax.plot([0], [0], 'yo', markersize = 15)
ax.set_xlabel('x [au]')
ax.set_ylabel('y [au]')
ax.legend(loc = 'upper left')
ax.grid(True)
ax.set_title("Earth's orbit over "+str(number_of_orbits)+" Earth years")
ax.set_aspect('equal')
fig.savefig(vis_dir+'Earth_Trajectory_'+str(number_of_orbits)+'.pdf')
plt.show()

#PERIAPSIDES ANGLES FOR DIFFERENT TIME STEPS
initial_position = np.array([au, 0.]) #Earth distance from sun
initial_velocity = np.array([0., 2*np.pi*au/year]) #Earth average orbital speed
number_of_orbits = 10#int(np.ceil(1*(year/mercury_year)))
test_modifier = "GR" #Can be GR or Newtonian
scales = np.linspace(2, 20, 5)
i=0
fig = plt.figure()
ax = fig.add_subplot(111)

for time_scale in scales:
	test_position, test_velocity, test_periapsides, test_periapsides_angle, eccentricity = main(sun_mass, earth_mass, initial_position, initial_velocity, number_of_orbits, test_modifier, time_scale)
	np.savetxt(data_dir+'Earth'+test_modifier+str(number_of_orbits)+'_'+str(time_scale)+'positions.txt', test_position)
	np.savetxt(data_dir+'Earth'+test_modifier+str(number_of_orbits)+'_'+str(time_scale)+'periapsides.txt', test_periapsides)
	np.savetxt(data_dir+'Earth'+test_modifier+str(number_of_orbits)+'_'+str(time_scale)+'periapsides_angles.txt', test_periapsides_angle)

	ax.plot(test_position[:,0]/au, test_position[:,1]/au, linewidth = 1, label = str(time_scale))

ax.plot([0], [0], 'yo', markersize = 15)
ax.set_xlabel('x [au]')
ax.set_ylabel('y [au]')
ax.legend(loc = 'upper left')
ax.grid(True)
ax.set_title("Earth's orbit over "+str(number_of_orbits)+" Earth years")
ax.set_aspect('equal')
fig.savefig(vis_dir+'Earth_Trajectory_'+str(number_of_orbits)+'.pdf')
plt.show()

#RATE COMPARISON FOR DIFFERENT RUN TIMES
initial_position = np.array([46.*10.**9., 0.]) #start at perihelion
initial_velocity = np.array([0., (59*10**3)]) #speed at perihelion
test_modifier = "GR" #Can be GR or Newtonian
times = np.linspace(1, 100, 20)
rates = np.zeros(len(times))
i=0

for Earth_years in times:
	number_of_orbits = int(np.ceil(Earth_years*(year/mercury_year)))
	test_position, test_velocity, test_periapsides, test_periapsides_angle, eccentricity = main(sun_mass, mercury_mass, initial_position, initial_velocity, number_of_orbits, test_modifier)
	orbits = np.arange(0, number_of_orbits)*mercury_year/year
	rates[i] = precession_rate(orbits, test_periapsides_angle)
	i += 1

plt.plot(times, rates)
plt.xlabel('End Time (Earth years)')
plt.ylabel('Angle Precession (arcseconds/century)')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#plt.title('Precession rate: '+str(round(rate*100,0))+' arcseconds/century')#'Precession of Mercury over '+str(int(number_of_orbits*mercury_year/year))+" Earth years")
plt.tight_layout()
plt.savefig(vis_dir+'Precession_rate_Runtime_Comparison.pdf')
plt.show()
