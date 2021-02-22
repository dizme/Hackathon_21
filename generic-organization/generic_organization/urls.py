"""generic_organization URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.http import HttpResponse
from generic_organization.settings import DESCRIPTION_APP, DESCRIPTION_VERSION, DESCRIPTION_TYPE, \
    DESCRIPTION_ORGANIZATION
from generic_organization.settings import TEMPLATE_FOLDER_LIST, BASE_CODE_FOLDER
import json
import os
body_health_json = None


def healthz(request):
    global body_health_json

    if not body_health_json:
        body_health = dict()
        body_health["name"] = DESCRIPTION_APP
        body_health["status"] = "OK"
        body_health["version"] = DESCRIPTION_VERSION
        body_health["type"] = DESCRIPTION_TYPE
        body_health["organization"] = DESCRIPTION_ORGANIZATION
        body_health_json = json.dumps(body_health)
    
    return HttpResponse(body_health_json, status=200,  content_type="application/json")


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('health/', healthz, name="healthz probe"),
    re_path('api/(?P<version>(v1|v2))/', include('generic_organization_service.urls'))
]

for root, dirs, files in os.walk(BASE_CODE_FOLDER, topdown=False, followlinks=False):
    if os.path.exists(os.path.join(root, "urls.py")) and os.path.basename(root) not in TEMPLATE_FOLDER_LIST:
        urlpatterns.append(
            re_path('api/(?P<version>(v1|v2))/', include(os.path.basename(root) + ".urls"))
        )