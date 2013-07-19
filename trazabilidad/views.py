from django.http import HttpResponse, request
from django.shortcuts import render_to_response
from trazabilidad.models import *
from django.views.generic import DetailView, ListView
