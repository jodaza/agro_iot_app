from django.contrib import admin
from .models import valores_sensores, valores_sensores_hora

# Register your models here.

class Valores_sensores_hora_admin(admin.ModelAdmin):
    list_display = ( 'pk','sensor','sumatoria', 'minimo', 'maximo', 'registros','created')
    list_display_links = ('pk',)

class valores_sensores_admin(admin.ModelAdmin):
    list_display = ( 'pk','humedad_aire',
    'temperatura_aire',
    'humedad_suelo_1',
    'humedad_suelo_2',
    'humedad_suelo_3',
    'humedad_suelo_4',
    'luz',
    'Estado_riego',
    'Estado_luz',
    'modo_riego',
    'modo_luz',
    'created')
    list_display_links = ('pk',)


admin.site.register(valores_sensores, valores_sensores_admin)
admin.site.register(valores_sensores_hora, Valores_sensores_hora_admin)
