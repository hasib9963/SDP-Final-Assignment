from django.contrib import admin
from . import models

admin.site.register(models.Pet)
admin.site.register(models.Review)