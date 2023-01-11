![Portada](https://i.imgur.com/zWxVLlF.png)
## Objetivos de la aplicación
La aplicación está destinada a los amantes de la NBA, ofreciendo datos de los equipos y jugadores de la liga, así cómo informa del estado de la clasificación de cada conferencia. Además, incorpora un buscador que ofrece la posibilidad de realizar búsquedas a gran velocidad para encontrar a tus equipos/jugadores favoritos de forma sencilla.

La aplicación ha sido confeccionada con las herramientas aprendidas durante la asignatura, haciendo uso del Web Scraping para la carga de datos extraídos de dos webs diferentes, de Django para la confección del proyecto y Whoosh para las búsquedas.

## Descripción de las partes del proyecto y el uso de las herramientas
Este proyecto puede dividirse en 4 partes o módulos principales:
1.	La página en sí misma.
2.	El módulo de equipos.
3.	El módulo de jugadores.
4.	El módulo de “administración”.

### La página
Como base para el resto de los módulos de la aplicación, se ha desarrollado una página web simple. Esta página no tiene habilitada la posibilidad de iniciar sesión y registrarse ya que su utilidad es puramente informativa y, de esta manera, cualquier usuario puede acceder a la información sin necesidad de crearse una cuenta.

Por otra parte, para el estilo se le ha dado un diseño sencillo mediante CSS, y se han recogido todas las opciones disponibles para el usuario en una barra de navegación superior.

Para el desarrollo de la página, se ha utilizado Django 3.2.16 y Bootstrap.

### Equipos
Este módulo se nutre para su composición de 2 páginas web diferentes: de NBA.com (la página oficial de la liga) y de Hispanos NBA (la cual contiene información detallada, en español, de los 30 equipos que componen la liga). 

Cada equipo contiene información sobre su nombre, escudo, ciudad, estadio, división y conferencias a las que pertenece, títulos de división, títulos de conferencia, participaciones en playoffs, campeonatos de la NBA y récord de victorias-derrotas que tiene en la temporada actual.

Mediante el uso de BeautifulSoup 4, se ha realizado el Scraping en ambas webs, extrayendo de la página oficial el nombre, escudo y récord de victorias-derrotas y el resto de la información procedente de Hispanos NBA.

Una vez almacenados los equipos, se ha hecho uso de la herramienta Whoosh para permitir la búsqueda de los mismos por el usuario. Dicha búsqueda puede realizarse tanto por nombre como por división y conferencia.

Los equipos son mostrados en la ventana de Inicio, clasificados por conferencia y división: 

![Captura 1](https://i.imgur.com/uCryryS.png)
 
Como se aprecia en la imagen, desde esta vista podemos acceder a cada uno de los equipos individualmente para visualizar su información:

![Captura 2](https://i.imgur.com/7k2bbH0.png)
 
De igual forma, si accedemos en “Clasificación”, podremos ver el estado actual de la clasificación de cada conferencia en temporada regular.

### Jugadores
Este módulo contiene la información de los jugadores de la liga. Dicha información se extrae únicamente de NBA.com.

De cada jugador se registra: su nombre, dorsal, edad, altura(m), peso(kg), nacionalidad, años de experiencia en la liga, equipo al que pertenece, año y ronda en la que fue drafteado, posición en la pista y una imagen oficial.

Desde la vista de equipo, tenemos acceso a la plantilla completa de cada equipo, con enlaces individuales para poder ver la información de cada jugador:

![Captura 3](https://i.imgur.com/M336OBT.png)
 
De igual forma, desde la vista de “Líderes estadísticos”, podemos observar qué jugadores están en este momento liderando las principales estadísticas de la NBA:
 
![Captura 4](https://i.imgur.com/mlOLEpU.png)

Al igual que con los equipos, se ha usado Beautifulsoup 4, para obtener la información de la web, y Whoosh para indexar la información. 

Para los jugadores también se puede utilizar el buscador que aparece en la barra de navegación. Esta búsqueda puede realizarse tanto por nombre como por equipo, país y posición.

### Administración
En la barra de navegación encontramos el desplegable “Base de Datos”, el cual ofrece 2 opciones diferentes al usuario: poblar la base de datos (actualizando la información) e indexar los resultados.

## Manual de uso
En la ventana de comandos y con permisos de administrador, ejecutar el comando pip install -r requirements.txt para instalar las librerías, y python manage.py runserver para ejecutar la aplicación. Tras esto, al acceder a http://127.0.0.1:8000/ nos encontraremos en el menú de inicio.

Adicionalmente tendremos las siguientes acciones disponibles:
* Clasificación: se podrá ver la tabla clasificatoria de ambas conferencias. 
* Líderes estadísticos: se podrá ver el top5 jugadores en 6 estadísticas principales. 
* Base de datos: se podrá poblar la base de datos o indexar los registros de jugadores y equipos.
* Buscar: se podrá buscar jugadores y/o equipos. Ejemplos de búsqueda: “oeste”, “España”, “alero”, “Celtics”, “Oklahoma”, “central”.
