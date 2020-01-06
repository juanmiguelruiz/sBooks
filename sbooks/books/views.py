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
    return render(request, 'index.html', {'STATIC_URL': settings.STATIC_URL})

def libros(request):
    return render(request, 'libros.html', {'STATIC_URL': settings.STATIC_URL})

def libro(request):
    return render(request, 'libro.html', {'STATIC_URL': settings.STATIC_URL})

def top(request):
    return render(request, 'top.html', {'STATIC_URL': settings.STATIC_URL})

def parati(request):
    return render(request, 'parati.html', {'STATIC_URL': settings.STATIC_URL})

def similares(request):
    return render(request, 'similares.html', {'STATIC_URL': settings.STATIC_URL})


# -----CARGAR DB-----
def populate_libros(request):
    # cargamos primero las categorias
    populate_categorias()

    Libro.objects.all().delete()
    lista_libros = []
    # Enlaces a los libros de todas las categorias
    lista_enlaces_categorias = \
        ["https://www.casadellibro.com/libros/ciencias-politicas-y-sociales/105000000",
         "https://www.casadellibro.com/libros/psicologia-y-pedagogia/130000000",
         "https://www.casadellibro.com/libros/autoayuda-y-espiritualidad/102000000",
         "https://www.casadellibro.com/libros/historia/115000000",
         "https://www.casadellibro.com/libros/ciencias/103000000",
         "https://www.casadellibro.com/libros/medicina/123000000",
         "https://www.casadellibro.com/libros/economia/110000000",
         "https://www.casadellibro.com/libros/libros-de-texto-y-formacion/132000000",
         "https://www.casadellibro.com/libros/literatura/121000000",
         "https://www.casadellibro.com/libros/literatura/narrativa-en-bolsillo/121005000",
         "https://www.casadellibro.com/libros/literatura/en-otros-idiomas/121003000",
         "https://www.casadellibro.com/libros/infantil/infantil-0-a-2-anos/117001000",
         "https://www.casadellibro.com/libros/infantil/infantil-3-a-5-anos/117005000",
         "https://www.casadellibro.com/libros/infantil/infantil-6-a-8-anos/117002000",
         "https://www.casadellibro.com/libros/infantil/infantil-9-a-12-anos/117003000",
         "https://www.casadellibro.com/libros/comics/411000000",
         "https://www.casadellibro.com/libros/comics/manga/411006000",
         "https://www.casadellibro.com/libros/comics-manga-infantil-y-juvenil/412000000",
         "https://www.casadellibro.com/libros/comics-manga-infantil-y-juvenil/manga-juvenil/412004000",
         "https://www.casadellibro.com/libros/juvenil/117001014",
         "https://www.casadellibro.com/libros/arte/101000000",
         "https://www.casadellibro.com/libros/filologia/112000000",
         "https://www.casadellibro.com/libros/deportes-y-juegos/108000000",
         "https://www.casadellibro.com/libros/cocina/106000000"]

    for enlace in lista_enlaces_categorias:
        print("************* Añadiendo libros del enlace: " + enlace + " ****************")
        libros_scraping = scraping_beautifulsoup(enlace)
        i = 0
        for libro in libros_scraping:
            print("----- Añadiendo libro: " + str(i) + " --------")
            print(libro[4])
            lista_libros.append(Libro(titulo=libro[0], autor=libro[1], descripcion=libro[2], portada=libro[3],
                                      categoria=Categoria.objects.get(nombre=libro[4]), detalle_enlace=libro[5],
                                      puntuacion_media=libro[6]))
            i = i + 1
    Libro.objects.bulk_create(lista_libros)
    print("*********************************************************")
    print("Libros añadidos: " + str(Libro.objects.count()))
    print("---------------------------------------------------------")

    return render(request, 'index.html', {'STATIC_URL': settings.STATIC_URL})


def populate_categorias():
    Categoria.objects.all().delete()
    categorias = ['Ciencias Políticas y Sociales', 'Psicología y Pedagogía', 'Autoayuda y Espiritualidad',
                  'Historia', 'Ciencias', 'Medicina', 'Economía', 'Libros de Texto y Formación',
                  'Infantil', 'Literatura', 'Cómics', 'Cómics manga infantil y juvenil', 'Juvenil',
                  'Arte', 'Filología', 'Deportes y juegos', 'Cocina']
    i = 0
    for categoria in categorias:
        print("Añadiendo categoria: " + categoria)
        Categoria.objects.create(nombre=categoria)
        i = i + 1
    print("Se han añadido " + str(Categoria.objects.count()) + " categorías")


def scraping_beautifulsoup(enlace):  # Imprime por consola los resultados de la primera página
    my_html_text = requests.get(enlace)
    soup = BeautifulSoup(my_html_text.text, "html.parser")
    libros = []

    # CATEGORIA
    categoria = ""
    ul = soup.find("ul", id="breadcrumb-flow")
    if ul is not None:
        li = ul.find_all("li")
        categoria = li[2].div.string
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
    schema = Schema(idLibro=NUMERIC(stored=True), titulo=KEYWORD(stored=True), autor=KEYWORD(stored=True),
                    descripcion=TEXT(stored=True), portada=TEXT(stored=True),categoria=TEXT(stored=True),
                    detalle_enlace=TEXT(stored=True), puntuacion_media=TEXT(stored=True),puntuaciones=TEXT(stored=True))

    if not os.path.exists("indiceWhoosh"):
        os.mkdir("indiceWhoosh")
    ix = create_in("indiceWhoosh", schema)
    writer = ix.writer()

    libros = Libro.objects.all()
    for libro in libros:
        writer.add_document(idLibro=libro.idLibro, titulo=libro.titulo, autor=libro.autor,
                            descripcion=str(libro.descripcion),portada=str(libro.portada),categoria= str(libro.categoria),
                            detalle_enlace=str(libro.detalle_enlace), puntuacion_media=libro.puntuacion_media,
                            puntuaciones=str(libro.puntuaciones))

    writer.commit()
    msg = '{} libros indexados'.format(len(libros))


    return render(request, 'message.html', {'message': msg})


# Search-whoosh products by query
def searchWhoosh(request):
    ix = open_dir("indiceWhoosh")
    qp = MultifieldParser(['titulo', 'name', 'category', 'price'], schema=ix.schema, group=OrGroup)

    q = qp.parse(request.GET.get('query'))

    with ix.searcher() as searcher:
        # Gets the top X results for the query where X=query_limit
        results = searcher.search(q, limit=int(request.GET.get('query_limit')))
        print("{} products".format(len(results)))
        results_json = []
        for r in results:
            # product = r['brand']+" - "+r['name']+" - "+r['category']+" - "+str(r['price'])+"€"
            product = [r['sku'], r['image'], r['brand'], r['name'], r['category'], r['price']]
            results_json.append(product)
        print('--------------END SEARCH--------------')
    print(results_json)
    mimetype = 'application/json'
    return HttpResponse(json.dumps(results_json), mimetype)


