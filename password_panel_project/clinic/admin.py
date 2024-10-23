from django.contrib import admin
from .models import Clinic, Attendant

# Registrando os modelos para que possam ser gerenciados no admin
admin.site.register(Clinic)
admin.site.register(Attendant)
