# M/CS 435: Nonlinear Optimization
#Line Search Methods

#Packages and Test Functions

import numpy as np
import matplotlib.pyplot as plt

# Test functions

def testFunction1(x):
    
    fval = x**16-x**2+x-1
    fgrad = 16*x**15-2*x+1
    fHess = (16*15)*x**14-2
    
    return fval,fgrad,fHess
    
def testFunction2(x): #If x is small, then this will give problems
    
    fval = .01*(x**6-30*x**4+19*x**2+7*x**3)
    fgrad = .01*(6*x**5-120*x**3+2*x+21*x**2)
    fHess = .01*(30*x**4-360*x**2+42*x)
    
    return fval,fgrad,fHess

#First we plot our testFunctions to graphically determine the local minima, and then compare to the result of the algorithm.

# pts = []; dom = np.arange(-1.1,1.1,0.05);
# for i in dom: pts.append(testFunction1(i))
# pts = np.transpose(pts)
# plt.plot(dom, pts[0])
# plt.show()

# pts = []; dom = np.arange(-6., 6., 0.25);
# for i in dom: pts.append(testFunction2(i))
# pts = np.transpose(pts)

# plt.plot(dom, pts[0])
# plt.show()

# Armijo

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

# A single steepest descent update using an Armijo line search.
# Input: Initial point, function that gives (fval,fgrad,fHess) i.e. f: x -> (fval(x), fgrad(x), fHess(x))
# Output: ((Initial point, value of fval at the initial point), (the updated point, the value of fval at the updated point), the numer of times fval was evaluated)

def ArmijoMini(pt, data):
    
    fcn = lambda x: data(x)[0]
    pk = (lambda v: v/np.linalg.norm(v))(-1*data(pt)[1])
    gradk = data(pt)[1]
    c = 10.**(-4)
    r = 0.5
    
    return Armijo(pt, fcn, pk, gradk, c, r)

# Armijo Tests

#print('Testing testFunction1 over a range of points')
#for i in np.arange(-1.,1.25,0.25): print(ArmijoMini(i, testFunction1))

#Testing testFunction2 over a range of points
#for i in np.arange(-5., 7.5, 2.5): print(ArmijoMini(i, testFunction2))

#Vector domain
#print(ArmijoMini(np.array([-1.,1.]),testFunction1))
#print(ArmijoMini(np.array([-5.,5.]),testFunction2))

# Newton

def Newton(xk,fcn,grad,hess,pk,c,ctilde,tol):
    # Perform a Newton line search for the function fcn, whose gradient is given
    # by the function grad, and whose Hessian is given by the function hess.
    # pk is the update direction and gradk, c, ctilde are used for the curvature
    # condition and Armijo conditions.
    # The search terminates when consecutive updates to alpha are less than tol.

    alpha = 1
    fk = fcn(xk)
    fkp1 = fcn(xk + alpha*pk)
    numEvals = 2
    gradk = grad(xk)
    def DescCheck(step): return fk + c*step*np.dot(gradk,pk)
    #CurvCheck = ctilde*np.abs(np.dot(gradk,pk))
    
    def derrat(step):
        first = np.dot(grad(xk + step*pk), pk) #First derivative of psi
        hesspk = np.dot(hess(xk + step*pk), pk) #If hess is not a matrix, then this won't work i.e. if hess is a vector, then this will be a scalar.  Then the next step will produce a vector, when we want a scalar.
        second = np.dot(pk, hesspk) #Second derivative of psi
        return first/second #ratio of the first and second derivatives of psi at alpha
    
    while np.all(fkp1 > DescCheck(alpha)) or np.abs(derrat(alpha)) > tol:
        alpha = alpha - derrat(alpha)
        fkp1 = fcn(xk + alpha*pk)
        numEvals += 1
        if numEvals > 49:
            break

    return (xk, fk), (xk + alpha*pk, fkp1), numEvals

# A single steepest descent update using a Newton line search.
# Input: Initial point, function that gives (fval,fgrad,fHess) i.e. f: x -> (fval(x), fgrad(x), fHess(x))
# Output: ((Initial point, value of fval at the initial point), (the updated point, the value of fval at the updated point), the numer of times fval was evaluated)

def NewtonMini(pt, data):
    
    fcn = lambda x: data(x)[0]
    grad = lambda x: data(x)[1]
    hess = lambda x: data(x)[2]
    pk = (lambda v: v/np.linalg.norm(v))(-1*data(pt)[1])
    c = 10**(-4)
    ctilde = 10**(-4)
    tol = 10**(-8)
    
    return Newton(pt, fcn, grad, hess, pk, c, ctilde, tol)

## Tests

#Testing testFunction1 over a range of points
#for i in np.arange(-1., 1.25, 0.25): print(NewtonMini(i, testFunction1))

#Testing testFunction2 over a range of points
#for i in np.arange(-5., 7.5, 2.5): print(NewtonMini(i, testFunction2))

#Vector domain
# print(NewtonMini(np.array([-0.5,1.]),testFunction1))
# print(NewtonMini(np.array([-5.,5.]),testFunction2))
#This doesn't work if the hessian given by the function is not a matrix.

print('To perform a single steepest descent update from an initial point using an Armijo or Newton line search, use ArmijoMini(initial_point, data) or NewtonMini(initial_point, data), respectively.  Where data gives the value of a function, its gradient, and its hessian as a list or tuple.  Both of these return ((initial point, initial value), (updated point, updated value), number of times the given function was evaluated).')