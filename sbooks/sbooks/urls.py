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
from django.urls import path
from books import views as bviews
from users import views as uviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bviews.index),
    path('index', bviews.index),
    path('libros', bviews.libros),
    path('top', bviews.top),
    path('parati', bviews.parati),
    path('similares', bviews.similares),
    path('libro', bviews.libro),
    path('cargarBD/', bviews.populate_libros),

    path('login', uviews.LoginUser.as_view()),
    path('login1', uviews.login),

]
