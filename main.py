"""
Genera un fichero formado por el track original mas todos los tracks que haya en un directorio. 
Unicamente añade las partes nuevas. 
"""
import os 
import sys
import glob 
import gpxpy
from gpx_folder_merger import gpxMerger  

data_dir = 'RUTAS BICI MADRID'
track_original =os.path.join(data_dir,'ACEPTO_EL_DESAFIO_Cerro_de_los_Batallones_2024.gpx')
pattern = 'Martín_de+Frutos*.gpx'
gpx_files = glob.glob(os.path.join(data_dir,pattern))
merged_gpx_name = os.path.join(data_dir,'Merged_track.gpx') 

# Track original
try:
    with open(track_original, 'r') as gpx_file:
        gpxA = gpxpy.parse(gpx_file)
except:
    print("Error abriendo el fichero {}".format(track_original))
    sys.exit(1)

for i, gpxFile in enumerate(gpx_files): 
    
    # Cargamos nueva ruta de acuerdo con el patrón
    try:
        # Track con nueva ruta
        with open(gpxFile, 'r') as gpx_file:
            print('Cargando la ruta : {}/{}'.format(i,len(gpx_files)))
            gpxB = gpxpy.parse(gpxFile)
    except:
        print("Error abriendo el fichero {}".format(gpxFile)) 
        sys.exit(2)
        
    # Unimos dicha ruta al gpx A 
    gpxMerger(gpxA, gpxB)

# Finalmente, escribimos el gpx final 
with open(merged_gpx_name, 'w') as f:
    f.write(gpxA.to_xml())
