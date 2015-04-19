# -*- coding: utf-8 -*-
"""
Created on Sun Feb 08 20:49:23 2015

@author: lemieux
"""
import numpy as np
import cv2
import Similarity
import Translation
import Homography
    
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
__HOMOGRAPHYJACOBIAN__ = 'homography'
__TRANSLATIONJACOBIAN__ = 'translation'

def JacobiansList():
   return dict ( [(  __SIMILARITYJACOBIAN__,  { 'description': 'similarity'}),
                  (  __HOMOGRAPHYJACOBIAN__,  { 'description': 'homography'}),
                  (  __TRANSLATIONJACOBIAN__, { 'description': 'translation'}),
                 ])


__LEVENBERG__ = 'levenberg'
__LLS__ = 'lls'

def AlignMethodList():
   return dict ( [(  __LEVENBERG__,  { 'description': 'levenberg'}),
                  (  __LLS__,        { 'description': 'LLS' })
                 ])

def AlignImages( featuresImage1, featuresImage2, method, jacobian):

    if jacobian ==__SIMILARITYJACOBIAN__:
        jacobianFct = Similarity.SimilarityJacobian
        transformFct = Similarity.SimilarityTransform
        initialEstimateFct = Similarity.SimilarityInitialEstimate
    elif jacobian ==__TRANSLATIONJACOBIAN__:
        jacobianFct =  Translation.TranslationJacobian
        transformFct = Translation.TranslationTransform
        initialEstimateFct = Translation.TranslationInitialEstimate
    elif jacobian == __HOMOGRAPHYJACOBIAN__:
        jacobianFct = Homography.HomographyJacobian
        transformFct = Homography.HomographyTransform
        initialEstimateFct = Homography.HomographyInitialEstimate
    else:
        raise NameError('Unsupported jacobian')

    if method==__LEVENBERG__:
        return Levenberg(featuresImage1, featuresImage2, jacobianFct, transformFct, initialEstimateFct)
    elif method==__LLS__:
        return LinearLeastSquare(featuresImage1, featuresImage2, jacobianFct, transformFct)
    else:
        raise NameError('Unsupported method')

def residualError( featuresImage1, featuresImage2, Transform):
    """Compute the residual error after Image2 is transformed to match Image1"""
          
    residualError = 0.0;
    for idx in range(0, np.size(featuresImage1,0)-1): 
        image1 =  featuresImage1[idx].T
        image2 = featuresImage2[idx].T 
        
        estimated = Transform.dot( image2 )
        estimated = estimated[0:2] / estimated[2] #Back to inhomogenous Cords
        residual =  image1[0:2] - estimated
        residualError = residualError + residual.T.dot(residual)

    return residualError

def LinearLeastSquare ( featuresImage1, featuresImage2 , jacobianFct, transformFct):
    """2D Alignment using Linear Least Square. """

    #Format the input vector 
    featuresCordsImage1 = [np.hstack((kp.pt, 1.0)) for kp in featuresImage1] 
    featuresCordsImage2 = [np.hstack((kp.pt, 1.0)) for kp in featuresImage2] 

    #Initalize Sums to zero.
    J = jacobianFct(None)  # Returns an empty null Jacobian of the right shape.
    SumA = J.T.dot(J)
    SumB = J.T.dot(np.array([0, 0]))

    deltax = np.subtract( featuresCordsImage1,featuresCordsImage2 )[:, 0:2]
    for idx in range(0, np.size(featuresCordsImage1,0)-1): 
        feature = featuresCordsImage2[idx]
        J = jacobianFct(feature)
        SumA = SumA + J.T.dot(J)
        SumB = SumB + J.T.dot(deltax[idx])
    
    EstimatedParameters = np.linalg.solve(SumA,SumB)
    Transform = transformFct(EstimatedParameters)

    error = residualError( featuresCordsImage1, featuresCordsImage2, Transform)
    print 'error = {0}'.format(str(error))
    return Transform;


def Levenberg( featuresImage1, featuresImage2 , jacobianFct, transformFct, initialEstimateFct):
    # Solve the system via the Iterative algorithm (Levenberg-)

    #Format the input vector 
    featuresCordsImage1 = [np.hstack((kp.pt, 1.0)) for kp in featuresImage1] # Homogeneous Cordinates
    featuresCordsImage2 = [np.hstack((kp.pt, 1.0)) for kp in featuresImage2] 

    #Initalize Sums to zero.
    J = jacobianFct(None)  # Returns an empty null Jacobian of the right shape.
    ParamsCount = J.shape[1]
    
    EstimatedParameters = initialEstimateFct(featuresCordsImage1, featuresCordsImage2)

    Transform = transformFct(EstimatedParameters)

    oldResidualError = float("inf")
    lambda_ = -1

    #Iterate
    for iteration in range(0,25): # Do 10 iterations. 
        
        SumA = np.zeros( (ParamsCount, ParamsCount) )
        SumB = np.zeros(ParamsCount);
      
        for idx in range(0, np.size(featuresCordsImage1,0)-1): 
            image1 =  featuresCordsImage1[idx].T
            image2 = featuresCordsImage2[idx].T 
        
            estimated = Transform.dot( image2 )
            estimated = estimated[0:2] / estimated[2] #Back to inhomogenous cords
            residual =  image1[0:2] - estimated
            J = jacobianFct(image1, EstimatedParameters)
            SumA = SumA + J.T.dot(J)
            SumB = SumB + J.T.dot(residual)
        
            
        if (lambda_ == -1):
           lambda_ = np.mean(np.diag(SumA)) * 0.000001

        SumA = SumA + (np.identity(ParamsCount) * lambda_)
        deltap = np.linalg.solve(SumA,SumB)
        EstimatedParameters = EstimatedParameters + deltap
        Transform = transformFct(EstimatedParameters)

        # Make sure we're converging.
        error = residualError( featuresCordsImage1, featuresCordsImage2, Transform)

        print 'Iteration {0} : error = {1} lambda= {2}'.format( str(iteration),str(error), str(  lambda_) )

        if (error > oldResidualError) : #We're not converging
            lambda_ = lambda_ * 10.0
            EstimatedParameters =  oldEstimatedParameters 
            Transform = transformFct(EstimatedParameters)
        else :                          #We're converging
            lambda_ = lambda_ / 10.0    
            oldResidualError = error
            oldEstimatedParameters = EstimatedParameters 
            
    return Transform;
    
