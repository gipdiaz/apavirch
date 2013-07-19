from django.http import HttpResponse, request
from django.shortcuts import render_to_response
from trazabilidad.models import *
from django.views.generic import DetailView, ListView
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
#from django import oldforms as forms
from django import forms 


@login_required
def index(prequest):
    return render_to_response('index.html',)

"""def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        data = request.POST.copy()
        errors = form.get_validation_errors(data)
        if not errors:
            new_user = form.save(data)
            return HttpResponseRedirect("/books/")
    else:
        data, errors = {}, {}

    return render_to_response("registration/register.html", {
        'form' : forms   FormWrapper(form, data, errors)
    })"""