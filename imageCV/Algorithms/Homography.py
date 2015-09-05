"""
Homography functions
"""
import numpy as np

def HomographyInitialEstimate(features1, features2):
    """ Calculates a rough estimate, good enough to start the recursive algo 
        parameters : 
           features1, features in the first image
           features2, features in the second image 
        returns  (h00, h01, h02, h10, h11, h12, h20, h21) """


    #Use four points to get a good estimate
    nbFeatures = np.size(features1,0)
    A = np.zeros(shape=(nbFeatures*2, 9))
    # for iteration in range(0,4): 
    for iteration in range(0, nbFeatures-1): 
       x1      = features2[iteration][0]
       x1prime = features1[iteration][0]
       y1      = features2[iteration][1]
       y1prime = features1[iteration][1]
       A[iteration*2]   = np.float32([0,   0, 0, -x1, -y1, -1,  y1prime*x1,  y1prime*y1,  y1prime] )
       A[iteration*2+1] = np.float32([x1, y1, 1,   0,   0,  0, -x1prime*x1, -x1prime*y1, -x1prime] )

    #Solve, find the nullspace of the homogeneous matrix

    u, s, vh = np.linalg.svd(A)
    null_space = vh[8]
    params = np.transpose(null_space)
    params = params / params[8]
    return params[0:8]

def HomographyJacobian (feature, parameters = None):
    """ Return the Jacobian for the Homography transform"""

    if feature is None:
        #Typically used to get the size of the Jacobian
        return (np.float32([ [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0]] ))
    if parameters is None:
        parameters = (0,0,0,0,0,0,0,0)
    (x, y, z) = list(feature)
    (h00, h01, h02, h10, h11, h12, h20, h21) = list(parameters)
    xprime = (1 + h00)*x + h01*y + h02
    yprime = h10*x + (1 + h11)*y + h12
    D = h20*x + h21*y + 1

    J = np.float32([ [x, y, 1, 0, 0, 0, -xprime*x/D, -xprime*y/D],
                     [0, 0, 0, x, y, 1, -yprime*x/D, -yprime*y/D]] ) /D;
    return J
        
def HomographyTransform(parameters):
    """ Return the Homography transform 
        parameters: (h00, h01, h02, h10, h11, h12, h20, h21 )"""

    if parameters is None:
        parameters = (0,0,0,0,0,0,0,0)
        
    (h00, h01, h02, h10, h11, h12, h20, h21) = list(parameters)
    T = np.float32([ [ h00, h01, h02],
                     [ h10, h11, h12],
                     [ h20, h21, 1] ] )
    return T


