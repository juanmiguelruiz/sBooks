"""sbooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from books import views as views
from recommendation_sys import views as views_sys

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index', views.index),
    path('libros', views.libros),
    path('top', views.top),
    path('parati', views.parati),
    path('similares', views.similares),
    re_path(r'libro/(?P<id_libro>\d+)', views.libro),
    path('cargarBD/', views.populate_libros),
    path('cargarWhoosh/', views.indexWhoosh),
    path('simulateData/', views_sys.simulate_users_rating),


    path('signup', views.signup, name='signup'),
    path('', include("django.contrib.auth.urls")),

]
