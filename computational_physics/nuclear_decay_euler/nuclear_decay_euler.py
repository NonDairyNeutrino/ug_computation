##Packages
# First we import the neccesary packages that allow us to perform mathematical operations with arrays and plot our data.
#Import plotting and mathematical packages
import numpy as np
import matplotlib.pyplot as plt

"""
Physical Parameters
Here we define the physical parameters that govern the behavior of the system.
"""

tca = 10.      #time constant for nuclei A
tcb = 5.       #time constant for nuclei B
dt = tca/1000. #time step
it = 0         #initial time
tf = 10.0*tca  #final time
N_B0 = 0.      #Initial Value of type B nuclei
error = 0.05   #The error of each measurement

"""
Data Creation
Now we create the data corresponding to the population ratio following the the recurrence relation given by Euler's method.
"""

#Here we make the data for the exact values of p.r.

def poprat(decay_A, decay_B, time_step, initial_time, final_time, initial_value):

    times = np.arange(initial_time, final_time, time_step)/decay_A #Array of evaluation times nondimensionalized to be fractions of the time constant for the type A nuclei

    poprat_exact = np.zeros(len(times)) #Allocating space for the array of population ratios (without any error) so that is the same size as the times array
    poprat_exact[0] = initial_value     #Initial value of the population ratio

    #Create the recursive data for the population ratio
    for tn in range(1,len(poprat_exact)): #We begin the indices at 1 because we already have the initial value.
            poprat_exact[tn] = poprat_exact[tn-1] + (
                (1/decay_A) + ((1/decay_A) - (1/decay_B))*poprat_exact[tn-1] #Derivative of the populatin ratio
            )*time_step

    return poprat_exact

#Here we test our population ratio function
poprat(tca, tcb, dt, it, tf, N_B0)

#Here is the data corresponding to the analytic solution

def poprat_analytic(decay_A, decay_B, time_step, initial_time, final_time, initial_value):

    times = np.arange(initial_time, final_time, time_step)/decay_A #Array of evaluation times nondimensionalized to be fractions of the time constant for the type A nuclei

    poprat_analytic = np.zeros(len(times)) #Pre-allocation of analytic data
    poprat_analytic[0] = N_B0              #Analytic Initial

    for i in range(1, len(times)):
        if decay_A/decay_B == 1.: #Analytic form of N_B(t)/N_A(t) for tca/tcb == 1
            poprat_analytic[i] = (poprat_analytic[0] * np.exp(-times[i]) + times[i] * np.exp(-times[i]))/np.exp(-times[i])

        else: #Analytic form of N_B(t)/N_A(t) for tca/tcb != 1
            poprat_analytic[i] = (poprat_analytic[0] * np.exp(-(decay_A/decay_B)*times[i]) + (np.exp(-times[i]) - np.exp(-(decay_A/decay_B)*times[i]))/((decay_A/decay_B) - 1))/np.exp(-times[i])

    return poprat_analytic

#Here we compare the analytic function to the numerical method by finding the maximum difference between data points for different time steps
for time_step in 10.**np.arange(0.,-4,-1):
    print(max(np.abs(poprat_analytic(tca, tcb, time_step, it, tf, N_B0) - poprat(tca, tcb, time_step, it, tf, N_B0))))

"""
Testing and Plotting

Now that we have our data, we can plot it to see the overall behavior of the ratio of populations as a function of time.
"""

#Now we can look at how the data behaves for different ratios of time constants which we call gamma
times = np.arange(it, tf, dt)/tca

plt.plot(times, poprat(tca, 11., dt, it, tf, N_B0), 'r', linewidth = 6., label = 'gamma = 10./11.') #gamma == 10./11.
plt.plot(times, poprat(tca, 10., dt, it, tf, N_B0), 'b', linewidth = 6., label = 'gamma = 10./10.') #gamma == 10./10.
plt.plot(times, poprat(tca, 8.5, dt, it, tf, N_B0), 'g', linewidth = 6., label = 'gamma = 10./8.5') #gamma == 10./9.

plt.plot(times, poprat_analytic(tca, 11., dt, it, tf, N_B0), 'k--',
         times, poprat_analytic(tca, 10., dt, it, tf, N_B0), 'k--',
         times, poprat_analytic(tca, 8.5, dt, it, tf, N_B0), 'k--',
         label = "Analytic"
        ) #Analytic solution for the different gammas

plt.xlabel("t (in units of 1/tau_A)")
plt.ylabel("Population Ratio $N_B/N_A$")
plt.title("Nuclear Decay Population Ratio")
plt.legend(loc = 'upper left')

plt.show()

# #This is speculative code to see if the original algorithm is right compared to the method of finding the data for the individual species and then taking their ratio

# N_A = np.ones(len(times))
# N_B = data = np.zeros(len(times))

# for tn in range(1,len(times)):
#     N_A[tn] = N_A[tn - 1] - (N_A[tn - 1]/tca)*dt

# for tn in range(1,len(times)):
#     N_B[tn] = N_B[tn - 1] + (N_A[tn - 1]/tca - N_B[tn - 1]/tcb)*dt

# data = N_B/N_A

# print(max(np.abs(data - poprat_exact))) #Maximum difference between the different algorithms

# plt.plot(times, poprat_exact, 'r--', times, data, 'b--', times, poprat_analytic, 'g'); plt.show()
# #It looks like both algorithms converge to each other in the continuous limit

"""Getting the possible ages from the population ratio"""

#Here we define a function that takes in a population ratio
def age_range(pop, poprat_exact, error):

    #First test to see if the given population ratio is a viable candidate for the data/model e.g. if it is too big or negative
    if pop > max(poprat_exact):
        print("The population ratio is not acheived in the time range.")
        return None

    elif pop < 0:
        print("The population ratio can not be negative.")
        return None

    else:

        indices = range(len(times)) #Since the indexing set is a range of integers up the length of times, we just make it once for both searches through the error data

        exactdistance = np.abs(pop - poprat_exact) #Create an array of distances from the given population ratio to the data.
        closest_exact_match = min(exactdistance)   #Find the minimum distance between the given population ratio and the data
        #Find the index at which the given population ratio is closest to the data
        for i in indices:
            if exactdistance[i] == closest_exact_match:
                exact = times[i]

        lowerdistance = np.abs(pop*(1 - error) - poprat_exact) #Create an array of distances from the lower error bound of the given population ratio to the data.
        closest_lower_match = min(lowerdistance)               #Find the minimum distance between the lower error bound of the given population ratio and the data.
        #Find the index at which the lower error bound of the given population ratio is closest to the data.
        for i in indices:
            if lowerdistance[i] == closest_lower_match:
                youngest = times[i]

        upperdistance = np.abs(pop*(1 + error) - poprat_exact) #Create an array of distances from the upper error bound of the given population ratio to the data.
        closest_upper_match = min(upperdistance)               #Find the minimum distance between the upper error bound of the given population ratio and the data.
        #Find the index at which the upper error bound of the given population ratio is closest to the data.
        for i in indices:
            if upperdistance[i] == closest_upper_match:
                oldest = times[i]

        #Now we calculate the percent error on either side of the exact
        minus_percent_error = 100*(1 - youngest/exact)
        plus_percent_error = 100*(oldest/exact - 1)


    return minus_percent_error, exact, plus_percent_error

#Testing of the agerange function

data = poprat(tca, 10., dt, it, tf, N_B0)
for i in [10., -1., 0.2, 0.9, 0.99]:
    print(age_range(i, data, 0.49))

#Here we find the percent error in the age for a given population ratio up to 0.5% accuracy for different regimes of gamma
for decay_B in [11., 10., 8.5]:
    print([
        tca/decay_B,
        age_range(
            4., #Constant given population ratio of 4
            poprat(tca, decay_B, dt, it, tf, N_B0), #Calculate the data for the iterative type B decay constant
            error #The error associated with this population measurement.  Here error =
        )
    ])

#As we can see from the ouput, the percent error on either side of the point increases with gamma

#Data Table
#Here we export the data corresponding to gamma = 1.

np.savetxt(
    "pop_rat_data.txt",
    #The array of data for the nondimensionalized time and the population ratio at that time
    np.transpose(
        (
            times[:int(tca/dt)+2],       #Times up to one and one-thousandth of decay constant for type A nuclei
            poprat(tca, 10., dt, it, tf, N_B0)[:int(tca/dt)+2] #Population ratio up to the index corresponding to the above time
         )
    ),
    delimiter = "    ",
    header = "t/tau_A, N_B/N_A",
    comments = "#"
)

#print(open("pop_rat_data.txt").read()) #Here we make sure the data we just wrote is of the right form
