from django.http import HttpResponse, request
from django.shortcuts import render_to_response
from trazabilidad.models import *
from django.views.generic import DetailView, ListView
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.template import RequestContext, Template, Context

@login_required
def index(request):
    return render_to_response('index.html',context_instance=RequestContext(request))