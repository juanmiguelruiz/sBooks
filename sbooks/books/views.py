from django.shortcuts import render_to_response, get_object_or_404, HttpResponse, render, HttpResponseRedirect
from django.conf import settings
from books.models import *
from bs4 import BeautifulSoup
import os.path
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import MultifieldParser, OrGroup

import requests



# Create your views here.

def index(request):
    return render(request, 'index.html', {'STATIC_URL':settings.STATIC_URL})

def libros(request):
    return render(request, 'libros.html', {'STATIC_URL':settings.STATIC_URL})



def populate_categorias():
    Categoria.objects.all().delete()
    categorias = ['Ciencias Políticas y sociales', 'Psicología y pedagogía', 'Autoayuda y espiritualidad',
                  'Historia', 'Ciencias', 'Medicina', 'Economía', 'Libros de texto y formación',
                  'Infantil', 'Literatura', 'Cómics', 'Cómics manga infantil y juvenil', 'Juvenil',
                  'Arte', 'Filología', 'Deportes y juegos', 'Cocina']
    for categoria in categorias:
        Categoria.objects.create(nombre=categoria)

def modelo_beautifulsoup(enlace):  # Imprime por consola los resultados de la primera página
    my_html_text = requests.get(enlace)
    soup = BeautifulSoup(my_html_text.text, "html.parser")
    libros = []

    # CATEGORIA
    categoria = ""
    ul = soup.find("ul", id="breadcrumb-flow")
    if ul is not None:
        li = ul.find_all("li")
        categoria = li[len(li) - 1].div.string
    print("Categoria: " + categoria + "\n")

    # LISTA DE LIBROS
    resultados_pagina = soup.find("div", class_="results-page")  # Buscando esto primero filtramos los libros de arriba
    libros_lista = resultados_pagina.find_all("div", class_="product")
    i = 0
    for x in libros_lista:
        i = i + 1
        print("*** Libro " + str(i) + " ***")

        # TITULO
        titulo = x.find("a", class_="title")
        if titulo is not None:
            titulo = titulo.string
        else:
            titulo = ""
        print("Titulo: " + titulo)

        # AUTOR
        div_author = x.find("div", class_="author")
        if div_author is not None:
            try:
                autor = div_author.a.string
            except:
                autor = div_author.div.string
        else:
            autor = ""
        print("Autor: " + autor)

        # BREVE DESCRIPCION
        breve_descripcion = x.find("div", class_="resumen")
        if breve_descripcion is not None:
            breve_descripcion = breve_descripcion.text
        else:
            breve_descripcion = ""
        print("Breve Descripcion: " + breve_descripcion)

        # FOTO PORTADA
        foto_portada = x.find("img", class_="v-lazy-image")
        if foto_portada is not None:
            foto_portada = foto_portada["data-src"]
        else:
            foto_portada = ""
        print("Foto Portada (enlace): " + foto_portada)

        # DETALLE ENLACE
        detalle_enlace = "https://www.casadellibro.com" + x.find("a", class_="title")['href']
        print("Detalle (enlace): " + detalle_enlace)

        # PUNTUACION MEDIA
        puntuacion_media = x.find("div", class_="rating")
        if puntuacion_media is not None:
            puntuacion_media = puntuacion_media.text.strip()
        else:
            puntuacion_media = ""
        print("Puntuacion media: " + puntuacion_media)
        print("----------------------------------------------")
        libro = [titulo, autor, breve_descripcion, foto_portada, categoria, detalle_enlace, puntuacion_media]
        libros.append(libro)

    return libros


def indexWhoosh(request):

    schema = Schema(idLibro=NUMERIC(stored=True), titulo=TEXT(stored=True), autor=TEXT(stored=True),
                    descripcion=TEXT(stored=True),
                    portada=TEXT(stored=True))

    if not os.path.exists("indiceWhoosh"):
        os.mkdir("indiceWhoosh")
    ix = create_in("indiceWhoosh", schema)
    writer = ix.writer()

    libros = Libro.objects.all()
    for libro in libros:
        writer.add_document(idLibro=libro.idLibro, titulo=libro.titulo, autor=libro.autor,
                            descripcion=libro.descripcion,
                            portada=libro.portada)
    writer.commit()

   # end_time = time.perf_counter()
   # end_cpu = time.process_time()

    # Time spent in total
    #print("Elapsed time: {0:.3f} (s)".format(end_time - start_time))
    # Time spent only CPU
    #print("CPU process time: {0:.3f} (s)".format(end_cpu - start_cpu))
    msg = '{} libros indexados'.format(len(libros))

    return render(request, 'whoosh.html', {'message': msg})

