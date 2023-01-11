from django.db import models

# Create your models here.
class Pais(models.Model):
    name = models.TextField(verbose_name='Nombre en inglés')
    nombre = models.TextField(verbose_name='Nombre en español')
    iso3 = models.CharField(max_length=3, verbose_name='Abreviatura de 3 siglas')
    bandera = models.URLField(verbose_name='URL de su bandera')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )
        
class Posicion(models.Model):
    name = models.TextField(verbose_name='Posición (inglés)', unique=True)
    nombre = models.TextField(verbose_name='Posición (español)')
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )
        
class Conferencia(models.Model):
    name = models.TextField(verbose_name='Conference', unique=True)
    nombre = models.TextField(verbose_name='Conferencia', unique=True)
    img = models.URLField(verbose_name='URL imagen', null=True)
        
class Division(models.Model):
    name = models.TextField(verbose_name='Division', unique=True)
    nombre = models.TextField(verbose_name='División', unique=True)
    conferencia = models.ForeignKey(Conferencia, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )
        
class Equipo(models.Model):
    nombre = models.TextField(verbose_name='Nombre de la franquicia', unique=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    conferencia = models.ForeignKey(Conferencia, on_delete=models.SET_NULL, null=True)
    lugar = models.TextField(verbose_name='Localización')
    playoffs = models.PositiveSmallIntegerField(verbose_name='Participaciones en Playoffs', default=0)
    campeonatos = models.PositiveSmallIntegerField(verbose_name='Campeonatos NBA', default=0)
    titulos_conferencia = models.PositiveSmallIntegerField(verbose_name='Títulos de conferencia', default=0)
    titulos_division = models.PositiveSmallIntegerField(verbose_name='Títulos de división', default=0)
    escudo = models.URLField(verbose_name='URL de su escudo', null=True)
    estadio = models.TextField(verbose_name='Nombre de la cancha')
    url = models.URLField(verbose_name='URL en nba.com', null=True)
    #w-l
    wins = models.PositiveSmallIntegerField(verbose_name='Victorias esta temporada', default=0)
    loses = models.PositiveSmallIntegerField(verbose_name='Derrotas esta temporada', default=0)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )

class Jugador(models.Model):
    nombre = models.TextField(verbose_name='Nombre', unique=True)
    dorsal = models.PositiveSmallIntegerField(verbose_name='Dorsal', null=True)
    edad = models.PositiveSmallIntegerField(verbose_name='Edad', null=True)
    altura = models.CharField(max_length=30, verbose_name='Altura (m)', null=True)
    peso = models.TextField(verbose_name='Peso (kg)', null=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    exp = models.PositiveSmallIntegerField(verbose_name='Años como profesional', null=True)
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True)
    imagen = models.URLField(verbose_name='URL de su fotografía', null=True) 
    draft = models.TextField(verbose_name='Draft', null=True)
    posicion = models.ForeignKey(Posicion, on_delete=models.SET_NULL, null=True)
    #stats js da problemas
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        ordering = ('nombre', )
        
class SeasonLeaders(models.Model):
    category = models.TextField(verbose_name='Category')
    categoria = models.TextField(verbose_name='Categoría')
    lider = models.ForeignKey(Jugador, on_delete=models.SET_NULL, null=True)
    stat = models.FloatField()
