"""
Genera un fichero que es la nueva actividad que se quiere añadir, en la que estan marcados los puntos
considerador repetidos con una elevacion de -1. Todavia no se unen al track original
"""
import gpxpy
import sameTrack

track_original = 'MAL_fuente_teja.gpx' # track grande al que queremos añadir
track_nuevo = 'Cerro_Batallones.gpx' # nuevo track que queremos incluir en el grande, (solo los caminos no repetidos)


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
for pointB in segmentoB.points:
    for i in range(len(segmentoA.points) - 1):
        if (sameTrack.sameTrack(segmentoA.points[i], segmentoA.points[i+1], pointB)):
            pointB.elevation = -1
            break
    
with open('nuevo.gpx', 'w') as f:
    f.write(gpxB.to_xml())


