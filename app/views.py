"""
Definition of views.
"""

import os
import uuid
import numpy as np
import json
import cv2
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse, HttpResponseServerError
from datetime import datetime
from app.models import HostedImage, ImageSet
from app.forms import UploadFileForm
import Alignment2D
import CVLoadFromURL

controlPanels = list([{ 'panelTemplate'  : 'app/Panels/selectPanel.js', 
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
          'content'        : Alignment2D.MaxDistanceRange()  }]) 

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    fail()
    return render(request,
        'app/home.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }))

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
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
    return render(request,
        'app/portfolio.html',
        context_instance = RequestContext(request,
        {
            'title':'My Portfolio',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }))



def merge(request):
    assert isinstance(request, HttpRequest)
    imageSetPK = request.GET['ImageSetPK']
    imageSet = ImageSet.objects.get(pk=imageSetPK)
    images = HostedImage.objects.filter(imageSet = imageSet)

    img1 = CVLoadFromURL.CVLoadFromURL(images[0].fullResImage.url)
    img2 = CVLoadFromURL.CVLoadFromURL(images[1].fullResImage.url)

    Canvas1 = mergeImages(img1, img2, **request.GET.dict())
    
    # Save the resulting image
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    filename = "%s.%s" % (uuid.uuid4(), 'jpg')
    ret = cv2.imwrite(os.path.join(settings.MEDIA_ROOT, filename), Canvas1)
    publicFilename = os.path.join(settings.MEDIA_URL, filename)
    response = JsonResponse({'mergedImageUrl': publicFilename})
    return response

    
def mergeImages(img1, img2, AlignMethod='', Jacobian='',  **kwargs):
   
    (kp1Matches, kp2Matches) = Alignment2D.ExtractFeatures(img1, img2, **kwargs)
  
    Transform = Alignment2D.AlignImages(kp1Matches, kp2Matches, AlignMethod, Jacobian) 

    #Overlay the two images, showing the detected feature.
    rows,cols,colours = img1.shape
    Canvas1 = np.zeros((rows * 2, cols * 2, colours) , img1.dtype)
    Canvas2 = np.copy(Canvas1)

    finalRows, finalCols, colours = Canvas1.shape
    tx = cols/2; # Translate to the center of the canvas
    ty = rows/2; 
    M = np.float32([[1,0,tx],[0,1,ty],[0,0,1]])

    img3 = cv2.drawKeypoints(img1, kp1Matches,color=(0,0,255))
    cv2.warpPerspective(img3, M, (finalCols, finalRows), Canvas1)
    
    finalTransform = np.dot(M, Transform) ; # Translate to the center of the canvas
    img2 = cv2.drawKeypoints(img2, kp2Matches,color=(255,0,0))
    cv2.warpPerspective(img2, finalTransform, (finalCols, finalRows), Canvas2, borderMode=cv2.BORDER_TRANSPARENT)

    alpha = 0.5
    beta = (1.0 - alpha)
    cv2.addWeighted(Canvas1, alpha, Canvas2, beta, 0.0, Canvas1)

    return Canvas1


def matchFeatures(request):
    """Renders the page."""
    assert isinstance(request, HttpRequest)
    defaultImageSetPK = 53
    imageSetPK = request.session.get('imageSetId', defaultImageSetPK)
   
    input_image_set = ImageSet.objects.get(pk=imageSetPK)
    images = HostedImage.objects.filter(imageSet = input_image_set)
    publicFilename = os.path.join(settings.MEDIA_URL, 'testImages/FitReferenceResult.jpg')

    return render(request,
        'app/featurematch.html',
        context_instance = RequestContext(request,
        {
            'merged_image_url': publicFilename,
            'imageSet'         : images, 
            'imageSetPK'       : imageSetPK,
            'control_panels'   :  controlPanels
        }))

def imageUpload(request):
    """Handles POST requests to upload an image to the server."""
    assert isinstance(request, HttpRequest)

    # A request to get a unique ID?
    if (request.path == '/imageUpload/GetId'):
        #Create a new entry in the ImageSet table
        set = ImageSet(user = 'Berthier')
        set.save()
        return JsonResponse({'uploadId': set.pk})

    # Handle the file upload request  
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        imageSetToUploadTo = ImageSet.objects.get(pk=form.cleaned_data['imageSetId'])
        img = HostedImage.objects.create_HostedImage(request.FILES['fileToUpload'], imageSetToUploadTo)
        img.save()
        return HttpResponse()
    else:
        form = UploadFileForm()
    return HttpResponseServerError()


def setSessionProperties(request):
    """Handles requests to change one or several session properties."""
    assert isinstance(request, HttpRequest)

    # Saves every items from the request's dictionary in the current session. (except the CSRF token)
    request.POST.pop('csrfmiddlewaretoken', None) 
    request.session.update(request.POST.dict())
    return HttpResponse()


def imageSelection(request):
    """Renders the select Image page."""
    assert isinstance(request, HttpRequest)
    
    imageSet = [
        {
            'tn': [ image.squareThumbnailImage.url for image in HostedImage.objects.filter(imageSet=set.pk) ],
            'pk': set.pk
        }
        for set in ImageSet.objects.all()]

    #Make sure each set always have at least 2 thumbnails, makes it easier to animate.
    #If set has only one image, duplicate it.
    for set in imageSet:
        if (len(set['tn']) == 1):
            set['tn'].append(set['tn'][0]);

    return render(request,
        'app/imageSelection.html',
        context_instance = RequestContext(request,
        {
           'imageSet' : json.dumps(imageSet) 
         }))



