from django.shortcuts import render

# importando modelos de la app control
from .models import Timer_mode_riego, Timer_mode_luz, ValueChange, Automatic_mode

from django.http import JsonResponse
# REST
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

# rest
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from .serializers import Control_values_serializer, Timer_mode_luz_serializer, Timer_mode_riego_serializer, Automatic_mode_serializer


# login miss
class Send_all_control():
    def get(self,request):
        intervalos_riego = Timer_mode_riego.objects.all()
        intervalos_riego_segundos = []
        # Modificando los intervalos a s, y en orden:
        for intervalo in intervalos_riego:
            intervalos_riego_segundos.append([(intervalo.encender_time.hour*3600+intervalo.encender_time.minute*60),(intervalo.apagar_time.hour*3600+intervalo.apagar_time.minute*60)])
        intervalos_riego_segundos.sort()
        # Intervalos de iluminacion del modo programado
        intervalos_luz = Timer_mode_luz.objects.all()
        intervalos_luz_segundos = []
        for intervalo in intervalos_luz:
            intervalos_luz_segundos.append([(intervalo.encender_time.hour*3600+intervalo.encender_time.minute*60),(intervalo.apagar_time.hour*3600+intervalo.apagar_time.minute*60)])
        intervalos_luz_segundos.sort()
        # Parametros del modo automatico
        parametros = Automatic_mode.objects.all()
        lista_parametros = []
        for parametro in parametros:
            lista_parametros.append([parametro.minimo,parametro.maximo])
        # estado
        riego_change = ValueChange.objects.get(activador="riego")
        luz_change = ValueChange.objects.get(activador="luz")
        
        return JsonResponse([['parametros_riego',lista_parametros], ['intervalos_riego',intervalos_riego_segundos],['intervalos_luz',intervalos_luz_segundos],[riego_change.change_status,luz_change.change_status]], safe=False)

 # FRONTEND APIS

class send_values_vue(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Get Request
    def get(self, request, pk ='riego'):
        values = ValueChange.objects.all()
        serializer =  Control_values_serializer(values, many=True)
        return Response(serializer.data)
    def put(self, request, pk='riego'):
        if pk == 'iluminacion':
            pk = 'luz'
        accionador = ValueChange.objects.get(pk=pk)
        serializer = Control_values_serializer(accionador, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class curl_timer_values(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Get Request
    def get(self, request, accionador):
        if accionador == 'riego':
            values = Timer_mode_riego.objects.all()
            serializer =  Timer_mode_riego_serializer(values, many=True)
            return Response(serializer.data)
        elif accionador == 'iluminacion':
            values = Timer_mode_luz.objects.all()
            serializer =  Timer_mode_luz_serializer(values, many=True)
            return Response(serializer.data)
    # POST 
    def post(self, request, accionador):
        if accionador == 'riego':
            serializer = Timer_mode_riego_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            timer_riego = serializer.save()
            return JsonResponse([0], safe=False)
        elif accionador == 'iluminacion':
            serializer = Timer_mode_luz_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            timer_luz = serializer.save()
            return JsonResponse([0], safe=False)
    # DELETE
    def delete(self,request, accionador, pk):
        if accionador == 'riego':
            if pk == 'all':
                intervalo = Timer_mode_riego.objects.all()
                intervalo.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                intervalo = Timer_mode_riego.objects.get(pk=pk)
                intervalo.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        if accionador == 'iluminacion':
            if pk == 'all':
                intervalo = Timer_mode_luz.objects.all()
                intervalo.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                intervalo = Timer_mode_luz.objects.get(pk=pk)
                intervalo.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

class curl_automatic_values(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # Get Request
    def get(self, request, pk = 'temperatura'):
        values = Automatic_mode.objects.all()
        serializer =  Automatic_mode_serializer(values, many=True)
        return Response(serializer.data)
    # POST 
    def put(self, request, pk):
        if pk == 'iluminacion':
            pk = 'luz'
        sensor = Automatic_mode.objects.get(pk=pk)
        serializer = Automatic_mode_serializer(sensor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)