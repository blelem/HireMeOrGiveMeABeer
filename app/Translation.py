"""
Similarity functions
"""
import numpy as np

def TranslationInitialEstimate(features1, features2):
    """ Calculates a rough estimate, good enough to start the recursive algo 
        parameters : 
           features1, features in the first image
           features2, features in the second image 
        returns  (tx, ty) """

    #For translation, tx=0, ty = 0 is a good starting point.
    
    return np.array([0,0])


def TranslationJacobian (feature, parameters = None):
    """ Return the Jacobian for the translation transform"""

    if feature is None:
        #Typically used to get the size of the Jacobian
        return (np.float32([ [0,0],
                             [0,0]] ))
                     
    J = np.float32([ [1,0],
                     [0,1]] )
    return J
        
def TranslationTransform (parameters):
    """ Return the translation transform 
        parameters: (tx,ty )"""

    (tx, ty) = list(parameters)
    T = np.float32([ [ 1, 0, tx],
                     [ 0, 1, ty],
                     [ 0, 0, 1 ] ])
    return T
                         


