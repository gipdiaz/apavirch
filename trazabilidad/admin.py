from django.contrib import admin
from django.db.models.loading import get_models

for model in get_models():
    try:
        admin.site.register(model)
    except:
        pass