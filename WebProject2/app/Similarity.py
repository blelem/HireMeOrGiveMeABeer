"""
Similarity functions
"""
import numpy as np

def SimilarityInitialEstimate(features1, features2):
    """ Calculates a rough estimate, good enough to start the recursive algo 
        parameters : 
           features1, features in the first image
           features2, features in the second image 
        returns  (tx, ty, a, b) """

    #Find an estimate using two data points.
    x1      = features2[0][0]
    x1prime = features1[0][0]
    y1      = features2[0][1]
    y1prime = features1[0][1]
    x2      = features2[1][0]
    x2prime = features1[1][0]
    y2      = features2[1][1]
    y2prime = features1[1][1]

    A = np.float32([ [1,0, x1,-y1],
                     [1,0, x2,-y2],
                     [0,1, y1, x1],
                     [0,1, y2, x2]] )
    B = np.float32( [ x1prime - x1, x2prime - x2, y1prime - y1, y2prime - y2] )
    return np.linalg.solve(A,B)


def SimilarityJacobian (feature, parameters = None):
    """ Return the Jacobian for the Similarity transform"""

    if feature is None:
        #Typically used to get the size of the Jacobian
        return (np.float32([ [0,0,0,0],
                             [0,0,0,0]] ))
                     
    J = np.float32([ [1,0,feature[0], -feature[1]],
                     [0,1,feature[1], feature[0]]] )
    return J
        
def SimilarityTransform (parameters):
    """ Return the Similarity transform 
        parameters: (tx,ty,a,b )"""

    if parameters is None:
        parameters = (0,0,0,0)
        
    (tx, ty, a, b) = list(parameters)
    T = np.float32([ [ 1+a, -b,  tx],
                     [ b,   1+a, ty],
                     [ 0,    0,  1 ] ] )
    return T
                         


