# Django Rest
from  rest_framework import serializers

# Models
from .models import valores_sensores

class Sensores_serializer(serializers.Serializer):

    humedad_aire = serializers.FloatField()
    temperatura_aire = serializers.FloatField()
    humedad_suelo_1 = serializers.FloatField()
    humedad_suelo_2 = serializers.FloatField()
    humedad_suelo_3 = serializers.FloatField()
    humedad_suelo_4 = serializers.FloatField()
    luz = serializers.FloatField()

    Estado_riego = serializers.IntegerField()
    Estado_luz = serializers.IntegerField()

    modo_riego = serializers.IntegerField()
    modo_luz = serializers.IntegerField()

    def create(self, data):
        return valores_sensores.objects.create(**data)
