from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    #path('service_path', service_view, name="service_name"),


]

urlpatterns = format_suffix_patterns(urlpatterns)