from datetime import datetime
import sqlite3
import time

from bs4 import BeautifulSoup
import requests
import urllib
import os
import re


def modelo_beautifulsoup(enlace):  # Imprime por consola los resultados de la primera página
    my_html_text = requests.get(enlace)
    soup = BeautifulSoup(my_html_text.text, "html.parser")
    # CATEGORIA
    categoria = ""
    # subcategoria = ""
    ul = soup.find("ul", id="breadcrumb-flow")
    if ul is not None:
        li = ul.find_all("li")
        categoria = li[len(li) - 2].a.div.string
        # subcategoria = li[len(li) - 1].div.string
    print("Categoria: " + categoria)

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

        # DETALLES LIBRO ENLACE
        detalle_enlace = "https://www.casadellibro.com" + x.find('a', class_="title")['href']
        print("Detalle libro (enlace): " + detalle_enlace)

        # PUNTUACION MEDIA
        puntuacion_media = x.find("div", class_="rating")
        if puntuacion_media is not None:
            puntuacion_media = puntuacion_media.text.strip()
        else:
            puntuacion_media = ""
        print("Puntuacion media: " + puntuacion_media)
        print("----------------------------------------------")

if __name__ == "__main__":
    modelo_beautifulsoup("https://www.casadellibro.com/libros/ciencias-politicas-y-sociales/105000000")
