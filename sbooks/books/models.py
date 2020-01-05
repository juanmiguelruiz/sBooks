from django.db import models

# Create your models here.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nick = models.CharField(verbose_name="Nick", max_length=10, unique="True")
    nombre = models.CharField(verbose_name="Nombre", max_length=50)
    apellidos = models.CharField(verbose_name="Apellidos", max_length=50)
    pais = models.CharField(verbose_name="País", max_length=50)
    ciudad = models.CharField(verbose_name="Ciudad", max_length=50)

    def __str__(self):
        return self.apellidos, self.nombre


class Libro(models.Model):
    idLibro = models.AutoField(primary_key=True)
    titulo = models.CharField(verbose_name="Titulo", max_length=50)
    autor = models.CharField(verbose_name='Autor', max_length=50)
    descripcion = models.TextField(verbose_name="Descripcion")
    portada = models.TextField(verbose_name="Portada")
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    detalle_enlace = models.TextField(verbose_name='Detalle (enlace)')
    puntuacion_media = models.TextField(verbose_name='Puntuación media')
    puntuaciones = models.ManyToManyField(Usuario, through='Puntuacion')

    def __str__(self):
        return self.titulo


class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)

    CATEGORIAS = (('Ciencias Políticas y sociales', 'Ciencias Políticas y sociales'),
                  ('Psicología y pedagogía', 'Psicología y pedagogía'),
                  ('Autoayuda y espiritualidad', 'Autoayuda y espiritualidad'),
                  ('Historia', 'Historia'), ('Ciencias', 'Ciencias'),
                  ('Medicina', 'Medicina'), ('Economía', 'Economía'),
                  ('Libros de texto y formación', 'Libros de texto y formación'),
                  ('Infantil', 'Infantil'),
                  ('Literatura', 'Literatura'),
                  ('Cómics', 'Cómics'), ('Cómics manga infantil y juvenil', 'Cómics manga infantil y juvenil'),
                  ('Juvenil', 'Juvenil'),
                  ('Arte', 'Arte'), ('Filología', 'Filología'), ('Deportes y juegos', 'Deportes y juegos'),
                  ('Cocina', 'Cocina'))
    nombre = models.TextField(verbose_name='Categoria', choices=CATEGORIAS)

    def __str__(self):
        return self.nombre


class Puntuacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(verbose_name='Puntuación', validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.puntuacion
