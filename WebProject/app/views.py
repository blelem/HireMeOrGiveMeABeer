"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from datetime import datetime
from app.models import InputImages 

import Alignment2D
import cv2
import os
import uuid
import numpy as np

controlPanels = list( [
        { 'panelTemplate'  : 'app/Panels/selectPanel.js', 
          'displayName'    : 'Alignment Algo', 
          'panelId'        : 'AlignmentAlgoPanel',
          'jsonName'       :  'AlignMethod',
          'content'        :  Alignment2D.AlignMethodList() },

        { 'panelTemplate'  : 'app/Panels/selectPanel.js', 
          'displayName'    : 'Jacobian', 
          'panelId'        : 'JacobianPanel',
          'jsonName'       :  'Jacobian',
          'content'        :  Alignment2D.JacobiansList()   },
          
        { 'panelTemplate'  : 'app/Panels/sliderPanel.js', 
          'displayName'    : 'Max distance', 
          'panelId'        : 'MaxDistancePanel',
          'jsonName'       : 'MaxDistance',
          'content'        : Alignment2D.MaxDistanceRange()  }
         ] ); 

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    fail()
    return render(
        request,
        'app/home.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }))

def portfolio(request):
    """Renders the portfolio page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/portfolio.html',
        context_instance = RequestContext(request,
        {
            'title':'My Portfolio',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }))



def merge(request):
    assert isinstance(request, HttpRequest)
    filePk = request.GET['inputImagesSelected']

    file = InputImages.objects.get(pk=filePk)
    img1 = cv2.imread(file.image_1.path, cv2.CV_LOAD_IMAGE_COLOR)
    img2 = cv2.imread(file.image_2.path, cv2.CV_LOAD_IMAGE_COLOR)

    Canvas1 = mergeImages(img1, img2, **request.GET.dict())
    
    # Save the resulting image
    if not os.path.exists(settings.MEDIA_ROOT):
	    os.makedirs(settings.MEDIA_ROOT)

    filename = "%s.%s" % (uuid.uuid4(), 'jpg')
    ret = cv2.imwrite(os.path.join(settings.MEDIA_ROOT, filename), Canvas1)
    publicFilename = os.path.join(settings.MEDIA_URL, filename)
    response = JsonResponse({'mergedImageUrl': publicFilename})
    return response

    
def mergeImages(img1, img2, AlignMethod = '', Jacobian = '',  **kwargs):
   
    (kp1Matches, kp2Matches) = Alignment2D.ExtractFeatures(img1, img2, **kwargs)
  
    Transform =  Alignment2D.AlignImages(kp1Matches, kp2Matches, AlignMethod, Jacobian) 

    #Overlay the two images, showing the detected feature.
    rows,cols,colours = img1.shape
    Canvas1 = np.zeros((rows * 2, cols * 2, colours) , img1.dtype)
    Canvas2 = np.copy(Canvas1)

    finalRows, finalCols, colours = Canvas1.shape
    M = np.float32([[1,0,0],[0,1,0],[0,0,1]])

    img3 = cv2.drawKeypoints(img1, kp1Matches,color=(0,0,255))
    cv2.warpPerspective(img3, M,(finalCols, finalRows), Canvas1)

    img2 = cv2.drawKeypoints(img2, kp2Matches,color=(255,0,0))
    cv2.warpPerspective(img2, Transform,(finalCols, finalRows), Canvas2, borderMode=cv2.BORDER_TRANSPARENT)

    alpha = 0.5
    beta = (1.0 - alpha)
    cv2.addWeighted(Canvas1, alpha, Canvas2, beta, 0.0, Canvas1)

    return Canvas1


def matchFeatures(request):
    """Renders the page."""
    assert isinstance(request, HttpRequest)

    input_image_set = InputImages.objects.get(set_name='DefaultFit')
    publicFilename = os.path.join(settings.MEDIA_URL, 'testImages/FitReferenceResult.jpg')

    return render(request,
        'app/featurematch.html',
        context_instance = RequestContext(request,
        {
            'merged_image_url': publicFilename,
            'input_image_list' : InputImages.objects.all(), 
            'selected_input_image' : input_image_set,
            'control_panels'   :  controlPanels
        }))



