"""
Genera un fichero formado por el track original mas el nuevo track
separado en segmentos y solo los puntos no repetidos.
"""
import gpxpy
import gpxpy.gpx
import sameTrack

track_original = 'nuevo.gpx' # track grande al que queremos añadir
track_nuevo = 'Bosque_Warner.gpx' # nuevo track que queremos incluir en el grande, (solo los caminos no repetidos)


# Track original
with open(track_original, 'r') as gpx_file:
    gpxA = gpxpy.parse(gpx_file)

# Track con nueva ruta
with open(track_nuevo, 'r') as gpx_file:
    gpxB = gpxpy.parse(gpx_file)

# TODO de momento asumimos que el fichero nuevo solo tienen 1 track y un solo segmento
segmentoB = gpxB.tracks[0].segments[0]

# Iteramos cada punto del nuevo track `pointB`
# Por cada punto, recorremos todas las rutas del track original para ver si es un punto repetido
# Si esta repetido, lo marcamos con elevacion igual a -1
i = 0 # indice para recorrer los puntos del track original
i_segmento = 0 # indice para recorrer todos los segmentos
n_segmentos = len(gpxA.tracks[0].segments) # numero de segmentos que hay en el track original

for pointB in segmentoB.points:
    flag_pto_encontrado = False # flag utilizada para parar de recorrer los segmentos cuando ya se ha encontrado el punto
    inicio_indice = i - 3 # indice en el que se encontro la ultima colision con el track original, retrocedemos el indice buscador por si acaso
    if (inicio_indice < 0): inicio_indice = 0
    i = inicio_indice

    inicio_i_segmento = i_segmento # continuamos buscando por el segmento porque el que estabamos
    while True: # bucle para iterar sobre todos los segmentos

        segmentoA = gpxA.tracks[0].segments[i_segmento]
        lenght_segmentoA = len(segmentoA.points) - 1

        # Se hace un bucle para buscar un punto coincidente en todo el track original
        # iteramos desde la posicion `indice_inicio` hasta el final del camino + desde el principio hasta otra vez el inicio
        # (como un recorrido en aritmetica modular)
        while True: # bucle para iterar los puntos de cada segmento
            i_prev = i # variable para ver si hemos vuelto al inicio del indice

            # calculamos una aproximacion de la distancia, para skipear punto de manera proporcional
            distancia_latitude = abs(segmentoA.points[i].latitude - pointB.latitude)
            distancia_longitude = abs(segmentoA.points[i].longitude - pointB.longitude)
            if (distancia_latitude > 0.002) or (distancia_longitude > 0.002): # si el punto esta muy lejano (200m aprox), podemos skipear algunos puntos
                i += int((distancia_latitude + distancia_latitude) * 1000) # se saltan puntos en proporcion a la distancia con un factor
            else: # el punto si esta cerca
                # calcula si el punto pertenece al segmento
                if (sameTrack.sameTrack(segmentoA.points[i], segmentoA.points[i+1], pointB)):
                    pointB.elevation = -1
                    flag_pto_encontrado = True
                    break
            # avanzamos al siguiente punto
            i += 1
            if i >= (lenght_segmentoA - 1): i = 0 # para el desbordamiento del indice

            # comprobacion en aritmetica modular, si ya hemos vuelto al inicio del indice
            if (i_prev < i): # sin envolvimiento
                if (i_prev < inicio_indice <= i):
                    break
            else: #con envolvimiento
                if (inicio_indice >= i_prev or inicio_indice <= i):
                    break
        # si ya se ha encontrado el punto en algun segmento, seguimos con el siguiente punto
        if flag_pto_encontrado:
            break
        i_segmento = (i_segmento + 1) % n_segmentos # recorrer segmentos con aritmetica modular
        i = 0 # resetamos el indice de recorrer los puntos de cada segmento
        if i_segmento == inicio_i_segmento: # si ya hemos buscado en todos los segmentos
            break


# Dividir el nuevo track en los segmentos no repetidos
# Recorre el nuevo track marcado con elevacion a -1 y 
# cuando encuentra un punto repetido añade el segmento
# TODO se podria unificar con el bucle anterior
lista_segmentos = [] # contendra las divisiones del nuevo track (solo las partes nuevas respecto al track original)
nuevo_segmento = gpxpy.gpx.GPXTrackSegment() # contiene la lista de puntos de cada segmento que se va conformando
for pointB in segmentoB.points:
    if pointB.elevation != -1:
        nuevo_segmento.points.append(pointB)
    elif nuevo_segmento.get_points_no() > 0: # si no esta vacio
        lista_segmentos.append(nuevo_segmento)
        nuevo_segmento = gpxpy.gpx.GPXTrackSegment()

# agregar el ultimo `nuevo_segmento` si no ha terminado en no repetidos
if nuevo_segmento.get_points_no() > 0: # si no esta vacio
    lista_segmentos.append(nuevo_segmento)

# Al track original `gpxA` añadimos los nuevos segmentos del Track nuevo `gpxB`
gpxA.tracks[0].segments.extend(lista_segmentos)

with open('nuevo.gpx', 'w') as f:
    f.write(gpxA.to_xml())


