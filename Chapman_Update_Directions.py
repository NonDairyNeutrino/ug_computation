# M/CS 435: Nonlinear Optimization
# Update Directions

# Nathan Chapman 3/5/2019

# Packages and Test Functions

import numpy as np

def testFunction(x):
    fval = (x[0] - 1)**4 + (x[1] - 2)**2 * (x[0] - 2)**2 + 2*(x[1] + 1)**2 * (x[2] - 1)**4 + x[0]**2 + 3*x[1]**2 + 2*x[2]**2
    fgrad = np.array([2*x[0] + 4*(-1+x[0])**3 + 2*(-2+x[0])*(-2+x[1])**2,6*x[1] + 2*(-2+x[1])*(-2+x[0])**2 + 4*(1+x[1])*(-1+x[2])**4,4*x[2] + 8*(1+x[1])**2 * (-1+x[2])**3])
    fhess = np.array([[2 + 12*(-1+x[0])**2 + 2*(-2+x[1])**2,4*(-2+x[0])*(-2+x[1]),0],[4*(-2+x[0])*(-2+x[1]),6 + 2*(-2+x[0])**2 + 4*(-1+x[2])**4,16*(1+x[1])*(-1+x[2])**3],[0,16*(1+x[1])*(-1+x[2])**3,4 + 24*(1+x[1])**2*(-1+x[2])**2]])
    return fval, fgrad, fhess

# Conjugate Gradient Descent Direction
# Here we implement the Fletcher-Reeves method for our conjugate gradient descent direction update.

def descentupdate(gradkp1, gradk, pk):

    #betak = np.dot(gradkp1, gradkp1 - gradk)/np.dot(gradk,gradk) # Here we use the dot product instead of the square of the norm to avoid errors due to square roots #PR
    betak = np.dot(gradkp1, gradkp1)/np.dot(gradk,gradk) #FR
    #betak = np.dot(gradkp1, gradkp1 - gradk)/np.dot(pk, gradkp1 - gradk) #HS

    pkp1 = -gradkp1 + betak * pk

    return pkp1

# Armijo Line Search

def Armijo(xk,fcn,pk,gradk,c,r):
    # Perform Armijo line search for the function fcn, from the point
    # xk, using the update direction pk.  We use gradk and c to check
    # the Armijo condition. We use r to determine the backtracking rate.
    # We assume the initial alpha=1 is used for the backtracking algorithm.

    alpha = 1
    fk = fcn(xk)
    fkp1 = fcn(xk + alpha*pk)
    numEvals = 2
    def DescCheck(step): return fk + c*step*np.dot(gradk,pk)
    
    while np.all(fkp1 > DescCheck(alpha)):
        alpha = r*alpha
        fkp1 = fcn(xk + alpha*pk)
        numEvals += 1

    return (xk, fk), (xk + alpha*pk, fkp1), numEvals

# Minimization Functions

def minimize(pt, data, method):
    
    fcn = lambda x: data(x)[0]
    def gradk(x): return data(x)[1]
    c = 10.**(-4)
    r = 0.5

    if method == "SD":
        def pk(x): return (lambda v: v/np.linalg.norm(v))(-1*data(x)[1]) #Steepest Descent

        xkp1, numEvals1 = (lambda x: (x[1][0], x[2]))(Armijo(pt, fcn, pk(pt), gradk(pt), c, r))

        xkp2, numEvals2 = (lambda x: (x[1][0], x[2]))(Armijo(xkp1, fcn, pk(xkp1), gradk(xkp1), c, r))

    elif method == "CG":
        
        p0 = (lambda v: v/np.linalg.norm(v))(-1*data(pt)[1]) #Initial descent direction determined by steepest descent

        xkp1, numEvals1 = (lambda x: (x[1][0], x[2]))(Armijo(pt, fcn, p0, gradk(pt), c, r))

        pkp1 = (lambda x: descentupdate(gradk(xkp1), x, -1*x))(gradk(pt)) #Since the previous descent direction was the negative gradient from steepest descent, we get to use it twice

        xkp2, numEvals2 = (lambda x: (x[1][0], x[2]))(Armijo(xkp1, fcn, pkp1, gradk(xkp1), c, r))
        
    return [(xkp1, xkp2), (fcn(xkp1), fcn(xkp2)), (np.linalg.norm(data(xkp1)[1]), np.linalg.norm(data(xkp2)[1])), (numEvals1, numEvals2)]

print("To perform two updates using steepest descent or conjugate gradient, via the Fletcher-Reeves method, from a given initial point using an Armijo line search, use minimization(initial_point, data, method).  Here data gives the value of a function, its gradient, and its hessian at a point as a list or tuple, and method is either 'SD' or 'CG'.  This returns [(first updated point, second updated point), (first updated value, second updated value), (norm of the first updated gradient, norm of the second updated gradient), (number of times the given function was evaluated in the first update, number of times the given function was evaluated in the second update)].")

##def main():
##    #for i in ["SD","CG"]:
##     #   print(i, minimize((0.,0.,0.), testFunction, i))
##
##if __name__ == '__main__':
##    main()
