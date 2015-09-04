"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.conf import settings
from django.conf.urls.static import static
from datetime import datetime
from django.template import loader

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    fail()
    return render(request,
        'portfolio/home.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }))

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'portfolio/about.html',
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
        'portfolio/portfolio.html',
        context_instance = RequestContext(request,
        {
            'title':'My Portfolio',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }))
