"""
Genera un fichero que es la nueva actividad que se quiere añadir, separando en segmentos
 y solo los no repetidos. Todavia no se unen al track original
"""
import gpxpy
import gpxpy.gpx
import sameTrack

track_original = 'Cerro_Batallones.gpx' # track grande al que queremos añadir
track_nuevo = 'MAL_fuente_teja.gpx' # nuevo track que queremos incluir en el grande, (solo los caminos no repetidos)


# Track original
with open(track_original, 'r') as gpx_file:
    gpxA = gpxpy.parse(gpx_file)

# Track con nueva ruta
with open(track_nuevo, 'r') as gpx_file:
    gpxB = gpxpy.parse(gpx_file)

# TODO de momento asumimos que los ficheros solo tienen 1 track y un solo segmento
segmentoA = gpxA.tracks[0].segments[0]
segmentoB = gpxB.tracks[0].segments[0]

# Iteramos cada punto del nuevo track `pointB`
# Por cada punto, recorremos todas las rutas del track original para ver si es un punto repetido
# Si esta repetido, lo marcamos con elevacion igual a -1
lenght_segmentoA = len(segmentoA.points)
for pointB in segmentoB.points:
    i = 0
    while(i < (lenght_segmentoA - 1)):
        if (sameTrack.sameTrack(segmentoA.points[i], segmentoA.points[i+1], pointB)):
            pointB.elevation = -1
            break
        i += 1

# Dividir el nuevo track en los segmentos no repetidos
# Recorre el nuevo track marcado con elevacion a -1 y 
# cuando encuentra un punto repetido añade el segmento
# TODO se podria unificar con el bucle anterior
lista_segmentos = [] # contendra las divisiones del nuevo track (solo las partes nuevas respecto al track original)
nuevo_segmento = gpxpy.gpx.GPXTrackSegment() # contiene la lista de puntos de cada segmento que se va conformando
for pointB in segmentoB.points:
    if pointB.elevation != -1:
        nuevo_segmento.points.append(pointB)
    elif nuevo_segmento: # si no esta vacio
        lista_segmentos.append(nuevo_segmento)
        nuevo_segmento = gpxpy.gpx.GPXTrackSegment()

# agregar el ultimo `nuevo_segmento` si no ha terminado en no repetidos
if nuevo_segmento: # si no esta vacio
    lista_segmentos.append(nuevo_segmento)

# Al track original `gpxA` añadimos los nuevos segmentos del Track nuevo `gpxB`
gpxA.tracks[0].segments.extend(lista_segmentos)

with open('nuevo.gpx', 'w') as f:
    f.write(gpxA.to_xml())


