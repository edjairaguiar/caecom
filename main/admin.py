from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Questao)
admin.site.register(models.Resposta)
admin.site.register(models.Poll)