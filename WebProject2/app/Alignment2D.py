# -*- coding: utf-8 -*-
"""
Created on Sun Feb 08 20:49:23 2015

@author: lemieux
"""
import numpy as np
import cv2
    
def SetupTheStuff(img1, img2):
    """ Find descriptors and match descriptors 
        (kp1Matches, kp2Matches) = Alignment2D.SetupTheStuff(image1, image2) """

    fd = cv2.FeatureDetector_create('SIFT')
    keypoints1 = fd.detect(img1)
    keypoints2 = fd.detect(img2)

    maxfeatures = 100;
    keypoints1 = sorted(keypoints1, key=lambda pts: pts.size,reverse=True)[0:maxfeatures]
    keypoints2 = sorted(keypoints2, key=lambda pts: pts.size,reverse=True)[0:maxfeatures]

    de = cv2.DescriptorExtractor_create('SIFT')
    (kp1, desc1) = de.compute(img1, keypoints1)
    (kp2, desc2) = de.compute(img2, keypoints2)

    dm = cv2.DescriptorMatcher_create('BruteForce')
    matches = dm.match(desc1, desc2)

    bestMatches = filter(lambda items: items.distance<100, matches)
    kp1Matches = [ kp1[idx] for idx in [x.queryIdx for x in bestMatches]]
    kp2Matches = [ kp2[idx] for idx in [x.trainIdx for x in bestMatches]]
    
    return kp1Matches, kp2Matches


__SIMILARITYJACOBIAN__ = 'similarity'
__HOMOGRAPHYJACOBIAN__ = 'homograpy'
__TRANSLATIONJACOBIAN__ = 'translation'

def JacobiansList():
   return dict ( [(  __SIMILARITYJACOBIAN__,  { 'description': 'similarity'}),
                  (  __HOMOGRAPHYJACOBIAN__,  { 'description': 'homography'}),
                  (  __TRANSLATIONJACOBIAN__, { 'description': 'translation'}),
                 ])

    
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
                         
def HomographyJacobian (feature, parameters = None):
    """ Return the Jacobian for the Homography transform"""

    if feature is None:
        #Typically used to get the size of the Jacobian
        return (np.float32([ [0,0,0,0,0,0,0,0],
                             [0,0,0,0,0,0,0,0]] ))
    (x, y) = list(feature)
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

    if parameters is None:
        parameters = (0,0,0,0)
        
    (tx, ty) = list(parameters)
    T = np.float32([ [ 1, 0, tx],
                     [ 0, 1, ty],
                     [ 0, 0, 1 ] ])
    return T
                         


__LEVENBERG__ = 'levenberg'
__LLS__ = 'lls'

def AlignMethodList():
   return dict ( [(  __LEVENBERG__,  { 'description': 'levenberg'}),
                  (  __LLS__,        { 'description': 'LLS' })
                 ])

def AlignImages( featuresImage1, featuresImage2, method, jacobian):

    if jacobian ==__SIMILARITYJACOBIAN__:
        jacobianFct = SimilarityJacobian
        transformFct = SimilarityTransform
    elif jacobian ==__TRANSLATIONJACOBIAN__:
        jacobianFct =  TranslationJacobian
        transformFct = TranslationTransform
    elif jacobian == __HOMOGRAPHYJACOBIAN__:
        jacobianFct = HomographyJacobian
        transformFct = HomographyTransform
    else:
        raise NameError('Unsupported jacobian')

    if method==__LEVENBERG__:
        return Levenberg(featuresImage1, featuresImage2, jacobianFct, transformFct)
    elif method==__LLS__:
        return LinearLeastSquare(featuresImage1, featuresImage2, jacobianFct, transformFct)
    else:
        raise NameError('Unsupported method')

def LinearLeastSquare ( featuresImage1, featuresImage2 , jacobianFct, transformFct):
    """2D Alignment using Linear Least Square. """

    #Format the input vector 
    featureCoordsImage1 = [kp.pt for kp in featuresImage1] 
    featureCoordsImage2 = [kp.pt for kp in featuresImage2] 

    #Initalize Sums to zero.
    J = jacobianFct(None)  # Returns an empty null Jacobian of the right shape.
    SumA = J.T.dot(J)
    SumB = J.T.dot(np.array([0, 0]))

    deltax = np.subtract( featureCoordsImage1,featureCoordsImage2 )
    for idx in range(0, np.size(featureCoordsImage1,0)-1): 
        feature = featureCoordsImage2[idx]
        J = jacobianFct(feature)
        SumA = SumA + J.T.dot(J)
        SumB = SumB + J.T.dot(deltax[idx])
    
    EstimatedParameters = np.linalg.solve(SumA,SumB)
    Transform = transformFct(EstimatedParameters)

    return Transform;


def Levenberg( featuresImage1, featuresImage2 , jacobianFct, transformFct):
    # Solve the system via the Iterative algorithm (Levenberg-)

    #Format the input vector 
    featureCoordsImage1 = [np.hstack((kp.pt, 1.0)) for kp in featuresImage2] # Homogeneous coordinates
    featureCoordsImage2 = [np.array(kp.pt) for kp in featuresImage1] 

    #Initalize Sums to zero.
    J = jacobianFct(None)  # Returns an empty null Jacobian of the right shape.
    ParamsCount = J.shape[1]
    
    EstimatedParameters = np.zeros(ParamsCount);
    Transform = transformFct(EstimatedParameters)

    #Iterate
    for iteration in range(0,10): # Do 10 iterations, or until the residual is small enough. 
        
        SumA = np.zeros( (ParamsCount, ParamsCount) )
        SumB = np.zeros(ParamsCount);
        for idx in range(0, np.size(featureCoordsImage1,0)-1): 
            reference =  featureCoordsImage1[idx].T
            measured = featureCoordsImage2[idx].T 
        
            estimated = Transform.dot( reference )
            estimated = estimated[0:2] / estimated[2] #Back to inhomogenous coords
            residual =  measured - estimated
            J = jacobianFct(measured, EstimatedParameters)
            SumA = SumA + J.T.dot(J)
            SumB = SumB.T + J.T.dot(residual)

        deltap = np.linalg.solve(SumA,SumB)
        EstimatedParameters = EstimatedParameters + np.asarray(deltap)
        Transform = transformFct(EstimatedParameters)
    
    return Transform;
    
