from django.db import models

# Create your models here.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Libro(models.Model):
    idLibro = models.AutoField(primary_key=True)
    titulo = models.CharField(verbose_name="Titulo", max_length=50)
    autor = models.CharField(verbose_name='Autor', max_length=50)
    descripcion = models.TextField(verbose_name="Descripcion")
    portada = models.TextField(verbose_name="Portada")
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    detalle_enlace = models.TextField(verbose_name='Detalle (enlace)')
    puntuacion_media = models.IntegerField(verbose_name='Puntuación media', null=True)
    puntuaciones = models.ManyToManyField(User, through='Puntuacion')

    def __str__(self):
        return self.titulo


class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)

    CATEGORIAS = (('CIENCIAS POLÍTICAS Y SOCIALES', 'CIENCIAS POLÍTICAS Y SOCIALES'),
                  ('PSICOLOGÍA Y PEDAGOGÍA', 'PSICOLOGÍA Y PEDAGOGÍA'),
                  ('AUTOAYUDA Y ESPIRITUALIDAD', 'AUTOAYUDA Y ESPIRITUALIDAD'),
                  ('HISTORIA', 'HISTORIA'), ('CIENCIAS', 'CIENCIAS'),
                  ('MEDICINA', 'MEDICINA'), ('ECONOMÍA', 'ECONOMÍA'),
                  ('LIBROS DE TEXTO Y FORMACIÓN', 'LIBROS DE TEXTO Y FORMACIÓN'),
                  ('INFANTIL', 'INFANTIL'),
                  ('LITERATURA', 'LITERATURA'),
                  ('CÓMICS', 'CÓMICS'), ('CÓMICS MANGA INFANTIL Y JUVENIL', 'CÓMICS MANGA INFANTIL Y JUVENIL'),
                  ('JUVENIL', 'JUVENIL'),
                  ('ARTE', 'ARTE'), ('FILOLOGÍA', 'FILOLOGÍA'), ('DEPORTES Y JUEGOS', 'DEPORTES Y JUEGOS'),
                  ('COCINA', 'COCINA'))
    nombre = models.TextField(verbose_name='Categoria', choices=CATEGORIAS)

    def __str__(self):
        return self.nombre


class Puntuacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(verbose_name='Puntuación', validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return "Usuario: " + str(self.usuario) + " al Libro: " + str(self.libro)
    class Meta:
        ordering = ('usuario', )
