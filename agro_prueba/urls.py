from django.contrib import admin
from django.urls import path

# get sensor views
from get_sensor_values.views import  indroduce_object
#, prueba_api
# control app
from control.views import Send_all_control, send_values_vue, curl_timer_values, curl_automatic_values
# interface app
from interface.views import MainInterface, sensorviews, logouts, controlviews, historyviews, documentationviews, last_values, send_intervalos_luz
# rest 
from rest_framework.authtoken import views


urlpatterns = [
    path('api_generate_token/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
    path('gets/', indroduce_object().as_view() ),
    # control app
    path('send_all/', Send_all_control().get, name="EnviarTodo"),
    # interface app
    path('showsensor/', sensorviews, name ="sensorview"),
    path('showcontrol/', controlviews, name ="controlview"),
    path('showhistory/<str:types>/<str:sensors>/<str:years>/<str:months>/<str:days>/', historyviews),
    path('showhistory/', historyviews, name ="historyview"),
    path('documentation/', documentationviews, name ="documentationviews"),
    # AJAX REQUESTS
    path('send_last_values/', last_values, name ="last_values"),
    path('send_last_times_luz/', send_intervalos_luz, name ="last_values_luz"),
    # Vue Apis
    path('send_values_vue/<str:pk>', send_values_vue.as_view(), name = 'send_values_vue'),
    path('curl_timer/<str:accionador>', curl_timer_values.as_view(), name = 'curl_timer'),
    path('curl_auto/<str:pk>', curl_automatic_values.as_view(), name = 'curl_auto'),
    # user auth
    path('login/', MainInterface().logins, name = "login"),
    path('logout/', logouts, name = "logout"),
]