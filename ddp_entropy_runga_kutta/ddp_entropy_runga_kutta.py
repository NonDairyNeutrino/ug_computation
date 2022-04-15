#import packages that we'll use often.
#from astropy.table import Table, Column
import numpy as np
#import scipy as sp
#from scipy.interpolate import interp1d
#import matplotlib.pylab as pl

import math
# from astropy.io import ascii
#
# import matplotlib as mpl
import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# import matplotlib.mlab as mlab
# import matplotlib.colorbar as cb
# import matplotlib.style
# #Setting new default figure parameters
# mpl.rcParams['figure.figsize'] = [8.0, 6.0]
# mpl.rcParams['figure.dpi'] = 200
# mpl.rcParams['savefig.dpi'] = 200
#
# mpl.rcParams['font.size'] = 12
# mpl.rcParams['legend.fontsize'] = 'large'
# mpl.rcParams['figure.titlesize'] = 'medium'

# %matplotlib inline

# from google.colab import files

#Define Global variables

g = 9.8 #gravity, m/s^2

l = 9.8 #length of pedlum

q = 0.5 #damping constant

drivFreq = 2/3 #Driving frequency

#Function to calculate derivatives
def update_deriv(theta_t0, w_t0, t0, drive_force):

  dtheta_dt = w_t0
  dw_dt = -g/l * math.sin(theta_t0) - q*dtheta_dt + drive_force * math.sin(drivFreq * t0)

  return dtheta_dt, dw_dt

#Function to step values forward based off time step
def step(theta_t0, w_t0, dtheta_dt, dw_dt, timeStep):

  theta = theta_t0 + dtheta_dt * timeStep
  w = w_t0 + dw_dt * timeStep

  return theta, w

#Function that runs RK-2 method
def RK_2(thetaInitial, wInitial, timeStep, drive_force, correction, timeSpan):

  #Create arrays to save info
  arraySize = math.ceil(timeSpan / timeStep)

  timeArray = np.empty(arraySize)
  energyArray = np.empty(arraySize)
  thetaArray = np.empty(arraySize)
  wArray = np.empty(arraySize)

  #Set initial values
  thetaArray[0] = thetaInitial
  wArray[0] = wInitial
  timeArray[0] = 0


  #loop to fill arrays
  for i in range(0, arraySize-1):

    #Derivatives
    dtheta_dt, dw_dt = update_deriv(thetaArray[i], wArray[i], timeArray[i], drive_force)

    #Take half step
    half_theta, half_w = step(thetaArray[i], wArray[i], dtheta_dt, dw_dt, timeStep/2)

    #Take half step derivative
    half_dtheta, half_dw = update_deriv( half_theta, half_w, timeArray[i] + timeStep/2, drive_force)

    #Take full step
    thetaArray[i+1], wArray[i+1] = step(thetaArray[i], wArray[i], half_dtheta, half_dw, timeStep)

    #Correct for into range of -pi to pi if wanted
    if correction == 0:
      if thetaArray[i+1] >= math.pi:
        thetaArray[i+1] = thetaArray[i+1] - (2 * math.pi)
      elif thetaArray[i+1] <= (-1 * math.pi):
        thetaArray[i+1] = thetaArray[i+1] + (2 * math.pi)

    #Increment time step
    timeArray[i+1] = timeArray[i] + timeStep

  return thetaArray, wArray, timeArray

#Function to sample theta and omega in phase with the driving frequency
def getPoincarePlot(driveFreq,thetaInitial, wInitial, timeStep, drive_force, correction, timeSpan):

  thetaArrayP, wArrayP, timeArrayP = RK_2(thetaInitial, wInitial, timeStep, drive_force, correction, timeSpan)

  thetaPhase = []
  wPhase = []
  timePhase = []



  for x in range(2826, len(timeArrayP)):
    n = timeArrayP[x] // (3*math.pi)
    if(abs(timeArrayP[x]-(3*math.pi*n)) < (timeStep)):
      thetaPhase.append(thetaArrayP[x])
      wPhase.append(wArrayP[x])
      timePhase.append(timeArrayP[x])


  return thetaPhase, wPhase, timePhase

#function used to create an array of possible theta values then look at the
#populate each bin with how many theta values from our array fall within the bin
#value size
def populateBins(thetaArray, binSize):

  #arrays to hold occurances and the range of values

  possibleThetas = np.arange(-math.pi, math.pi + binSize, binSize)
  populationArray = np.zeros(len(possibleThetas))
  #loop through each theta array and find the bin it belongs to and increment
  #the poplulation
  for theta in thetaArray:
    for i in range(len(possibleThetas)-1):
      if theta <= -math.pi + (i * binSize):
        populationArray[i] += 1
        break
      else:
        continue

  return populationArray, possibleThetas

#Function that returns the probability of a measurement going into a specific
#range of theta values into each bin
def binProbability(thetaArray, binSize):

  populationArray, possibleThetas = populateBins(thetaArray, binSize)
  probabilityArray = populationArray/len(thetaArray)

  return probabilityArray, possibleThetas

#function used to calculate the entropy of the system by summing the negative probability of
#each state times the nat. log of the probability.
def entropy(probabilityArray):


  result = 0;
  for probability in probabilityArray:
    if probability != 0:
     result += probability*np.log(probability)
    else:
      continue

  return -1*result

#ONLY RUN ONCE, GET ALL THETA VALUES

forceArray = np.linspace(1.4, 1.5, 1000)

for force in forceArray:
  testTheta, omega, time = getPoincarePlot(2/3, 0.2, 0, 3*math.pi/800, force, 0, 20000)
  #print(testTheta)
  np.savetxt(str(force)+'.txt', np.array([testTheta]))

#HOW TO LOAD OUR THETA VALUES
#print(np.loadtxt('1.4.txt'))

# #Make probability distributions
#
# forceArray = np.arange(1.4, 1.5, 0.02)
#
#
# for force in forceArray:
#   testtheta, omega, time = getPoincarePlot(2/3, 0.2, 0, 3*math.pi/800, force, 0, 20000)
#   probabilityArray, possibleThetas = binProbability(testtheta, 2*math.pi/75)
#   plt.plot(possibleThetas, probabilityArray, label = str(force))
#
# plt.xlabel('$\Theta$')
# plt.ylabel('Probability')
# plt.legend(loc = 'upper left')
# plt.show()
#
# binSizes = [2*math.pi/1000, 2*math.pi/75, 2*math.pi/10, 2*math.pi/5]
#
#
# for binSize in binSizes:
#   testtheta, omega, time = getPoincarePlot(2/3, 0.2, 0, 3*math.pi/800, 1.4, 0, 20000)
#   probabilityArray, possibleThetas = binProbability(testtheta, binSize)
#   plt.plot(possibleThetas, probabilityArray, label = str(binSize)[:5])
#
# plt.xlabel('$\Theta$')
# plt.ylabel('Probability')
# plt.legend(loc = 'upper left')
# plt.xlim(0,math.pi)
# plt.show()
#
# #function that calculates entropy for a force that is input by user
# def entropyOverForce(force):
#
#   getTheta, omega, time = getPoincarePlot(2/3, 0.2, 0, 3*math.pi/800, force, 0, 20000)
#   probabilityArray, possibleThetas = binProbability(getTheta, 2*math.pi/75)
#
#   entropyValue = entropy(probabilityArray)
#
#   return entropyValue
#
# #test code block for entropy over forces
#
# forceArray = np.arange(1.4, 1.5, 0.01)
# entropyArray = []
#
# for force in forceArray:
#   entropyArray = np.append(entropyArray, entropyOverForce(force))
#
# plt.scatter(forceArray, entropyArray)
# plt.xlabel('Driving force')
# plt.ylabel('Entropy')
# plt.show()
#
# #Funciton used for convergence test to show how entropy increases when we increase
# #the number of possible states our system can be in
# def plotEntropyvsBinNumber(driveFreq,thetaInitial, wInitial, timeStep, drive_force, correction, timeSpan):
#
#   theta, omega, time = getPoincarePlot(driveFreq,thetaInitial, wInitial, timeStep, drive_force, correction, timeSpan)
#   entropyArray = []
#   binSizes = np.arange(math.pi/1000, math.pi, math.pi/1000)
#
#   for x in binSizes:
#     testProbabilityArray, testPossibleThetas = binProbability(theta, x)
#     entropyArray = np.append(entropyArray, entropy(testProbabilityArray))
#
#
#   return entropyArray, binSizes
#
# #test code block
#
# #theta, omega, time = getPoincarePlot(2/3, 0.2, 0, 3*math.pi/300, 1.39, 0, 20000)
#
#
# #print(theta)
# #testProbabilityArray, testPossibleThetas = binProbability(theta, math.pi/5)
#
# #print(testProbabilityArray)
#
# #print(entropy(testProbabilityArray))
#
# #plot entropy vs bin sizes
# entropyArray, binNumbers = plotEntropyvsBinNumber(2/3, 0.2, 0, 3*math.pi/100, 1.4, 0, 20000)
#
# plt.scatter(binNumbers, entropyArray)
