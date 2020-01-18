import shelve
from django.shortcuts import render
from django.conf import settings
from books.models import *
from recommendation_sys.form import *
import random
from django.db.models import Q
from recommendation_sys.recommendations import *
import requests

# encoding:utf-8

# SISTEMA DE RECOMENDACIÓN COLABORATIVO BASADO EN ITEMS



def simulate_users_rating(request):  # populate para tener datos de puntuaciones para el sistema de recomendación
    """IMPORTANTE, AL EJECUTAR ESTA FUNCION SE ELIMINAN TODOS LOS USUARIOS EXCEPTO LOS ADMIN Y EL USUARIO AHORA
    CONECTADO"""
    Puntuacion.objects.filter(Q(usuario__is_superuser=False) and ~Q(usuario__username=request.user.username)).delete()
    User.objects.filter(Q(is_superuser=False) and ~Q(username=request.user.username)).delete()

    indiceLibro = 0
    lista_usuarios = []
    for x in range(1000):
        print("Insertando usuario: " + str(x))
        lista_usuarios.append(User(username=str(x), password=str(x)))
    User.objects.bulk_create(lista_usuarios)
    print("Usuarios simulados: " + str(User.objects.count()))

    primerIdLibro = Libro.objects.values_list('idLibro', flat=True).order_by('idLibro')[0]
    numero_libros = Libro.objects.count()
    lista_puntuaciones = []
    for user in User.objects.filter(~Q(username=request.user.username)):
        for _ in range(20):
            idLibro = random.randint(primerIdLibro, primerIdLibro + numero_libros - 1)
            print("Insertando puntuación al libroID: " + str(idLibro))
            lista_puntuaciones.append(Puntuacion(usuario=user, libro=Libro.objects.get(idLibro=idLibro),
                                                 puntuacion=random.randint(1, 6)))
    Puntuacion.objects.bulk_create(lista_puntuaciones)
    print("Puntuaciones simuladas: " + str(Puntuacion.objects.count()))

    msg = 'Se han añadido {} puntuaciones simuladas'.format(Puntuacion.objects.count())


    return render(request, 'message.html', {'message':msg, 'STATIC_URL': settings.STATIC_URL})

# HAY QUE HACER ESTO ANTES QUE NADA
def cargarRS(request):
    print("Cargando RS...")
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
    print("RS cargado")

    msg = 'Se ha cargado el Sistema de Recomendación'


    return render(request, 'message.html', {'message':msg, 'STATIC_URL': settings.STATIC_URL})


def libros_similares(request):
    if request.method == 'POST':
        formulario = libros_similaresForm(request.POST)
        if formulario.is_valid():
            shelf = shelve.open("dataRS.dat")
            prefs_transformed = shelf['ItemsPrefs']
            libro = Libro.objects.get(idLibro=formulario.cleaned_data['idLibro'])
            ranking = topMatches(prefs_transformed, int(formulario.cleaned_data['idLibro']), n=3)
            libros = []
            puntuaciones = []
            for re in ranking:
                libros.append(Libro.objects.get(idLibro=re[1]))
                puntuaciones.append(re[0])
            items = zip(libros, puntuaciones)
            return render(request, 'similarityBooks.html', {'libro': libro, 'items': items, 'STATIC_URL': settings.STATIC_URL})

    formulario = libros_similaresForm()
    return render(request, "similares.html",
                  {"formulario": formulario}, {'STATIC_URL': settings.STATIC_URL})

def recomendar_libro_al_usuario(request):
    top = None
    shelf = shelve.open("dataRS.dat")
    prefs = shelf['Prefs']
    itemsim = shelf['SimItems']
    ranking = getRecommendations(prefs, request.user.pk)
    top = ranking[0:2]
    libros = []
    scores = []
    for re in top:
        libros.append(Libro.objects.get(idLibro=re[1]))
        scores.append(re[0])
    items = zip(libros, scores)
    usuario = request.user
    return render(request, 'parati.html', {'usuario': usuario, 'items': items,'STATIC_URL': settings.STATIC_URL})
