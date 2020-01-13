from django.shortcuts import render
import shelve
from builtins import type

from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, render, HttpResponseRedirect, redirect
from django.conf import settings
from django.views.generic import ListView

from books.forms import *
from books.models import *
from bs4 import BeautifulSoup
import os.path
from whoosh import sorting
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser, OrGroup, QueryParser
from whoosh.query import Or, Term, Query, And
from books.models import *
from books.forms import *
import requests
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
from faker import Faker
from django.db.models import Q
from math import sqrt
from recommendation_sys.recommendations import *

# encoding:utf-8

# SISTEMA DE RECOMENDACIÓN COLABORATIVO BASADO EN ITEMS
fake = Faker()


def simulate_users_rating(request):  # populate para tener datos de puntuaciones para el sistema de recomendación
    """IMPORTANTE, AL EJECUTAR ESTA FUNCION SE ELIMINAN TODOS LOS USUARIOS EXCEPTO LOS ADMIN Y EL USUARIO AHORA
    CONECTADO"""
    Puntuacion.objects.filter(Q(usuario__is_superuser=False) and ~Q(usuario__username=request.user.username)).delete()
    User.objects.filter(Q(is_superuser=False) and ~Q(username=request.user.username)).delete()

    indiceLibro = 0
    lista_usuarios = []
    for _ in range(100):
        username = fake.name()
        print("Insertando usuario: " + username)
        try:
            User.objects.create(username=username, password=username)
        except:
            continue
    print("Usuarios simulados: " + str(User.objects.count()))

    primerIdLibro = Libro.objects.values_list('idLibro', flat=True).order_by('idLibro')[0]
    numero_libros = Libro.objects.count()
    lista_puntuaciones = []
    for user in User.objects.filter(Q(is_superuser=False) and ~Q(username=request.user.username)):
        for _ in range(5):
            idLibro = random.randint(primerIdLibro, primerIdLibro + numero_libros - 1)
            print("Insertando puntuación al libroID: " + str(idLibro))
            lista_puntuaciones.append(Puntuacion(usuario=user, libro=Libro.objects.get(idLibro=idLibro),
                                                 puntuacion=random.randint(1, 6)))
    Puntuacion.objects.bulk_create(lista_puntuaciones)
    print("Puntuaciones simuladas: " + str(Puntuacion.objects.count()))

    return render(request, 'index_sys.html')


def cargarRS():
    Prefs = {}
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.usuario.pk)
        itemid = int(ra.libro.idLibro)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs'] = Prefs
    shelf['ItemsPrefs'] = transformPrefs(Prefs)
    shelf['SimItems'] = calculateSimilarItems(Prefs, n=10)
    shelf.close()
