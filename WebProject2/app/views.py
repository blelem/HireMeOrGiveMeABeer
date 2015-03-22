"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import Alignment2D
# Imports for test code, simulating saving an image to the server's media content.d
import cv2
import os
from django.conf import settings
# End of test code imports.
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)

    #Test code, simulates saving an image to the server's media content.
    img = cv2.imread('app/static/app/testImages/fit01.jpg', cv2.CV_LOAD_IMAGE_COLOR)
    if not os.path.exists(settings.MEDIA_ROOT):
		os.makedirs(settings.MEDIA_ROOT)
    ret = cv2.imwrite('{0}{1}'.format(settings.MEDIA_ROOT, 'abracadabra.jpg'), img)
	
    #End of test code
    (kp1Matches, kp2Matches) = Alignment2D.SetupTheStuff()
    Transform = Alignment2D.LinearLeastSquare ( kp1Matches, kp2Matches ) 
	#Alignment2D.Levenberg(kp1Matches, kp2Matches) 

    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title': Transform,
            'message':'Your contact page.',
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
        })
    )
