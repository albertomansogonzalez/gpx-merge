import gpxpy
import gpxpy.gpx

def sameTrack(A, B, P):
    # return si P pertenece al segmento entre A y B

    # Comprobacion por contencion en el bounding box, con un delta ampliado
    delta = 0.00005
    lat_min = min(A.latitude, B.latitude) - delta
    lat_max = max(A.latitude, B.latitude) + delta
    lon_min = min(A.longitude, B.longitude) - delta
    lon_max = max(A.longitude, B.longitude) + delta

    return (
        (lat_min <= P.latitude <= lat_max)
        and
        (lon_min <= P.longitude <= lon_max)
    )


    return (
        min(A.latitude, B.latitude) <= P.latitude <= max(A.latitude, B.latitude)
        and
        min(A.longitude, B.longitude) <= P.longitude <= max(A.longitude, B.longitude)
    )



if __name__ == "__main__":
    # Test basico para probar la funcion "sameTrack"
    
    A = gpxpy.gpx.GPXWaypoint(latitude=40.236533, longitude=-3.696033)
    B = gpxpy.gpx.GPXWaypoint(latitude=40.236821, longitude=-3.695477)
    P = gpxpy.gpx.GPXWaypoint(latitude=40.236716, longitude=-3.695691)
    if sameTrack(A,B,P):
        print("PASS")
    else:
        print("FAIL")

    if sameTrack(B,A,P):
        print("PASS")
    else:
        print("FAIL")

    if not sameTrack(A,P,B):
        print("PASS")
    else:
        print("FAIL")

    if not sameTrack(B,P,A):
        print("PASS")
    else:
        print("FAIL")

    A = gpxpy.gpx.GPXWaypoint(latitude=40.237374, longitude=-3.698487)
    P = gpxpy.gpx.GPXWaypoint(latitude=40.236396, longitude=-3.697800)
    B = gpxpy.gpx.GPXWaypoint(latitude=40.234688, longitude=-3.696572)

    if sameTrack(A,B,P):
        print("PASS")
    else:
        print("FAIL")

    if sameTrack(B,A,P):
        print("PASS")
    else:
        print("FAIL")
    
    if not sameTrack(A,P,B):
        print("PASS")
    else:
        print("FAIL")

    # Test case de puntos muy cercanos, pero fuera del bounding box
    A = gpxpy.gpx.GPXWaypoint(latitude=40.227530, longitude=-3.708670)
    B = gpxpy.gpx.GPXWaypoint(latitude=40.227590, longitude=-3.708616)
    P = gpxpy.gpx.GPXWaypoint(latitude=40.227584, longitude=-3.708599)
    if sameTrack(A,P,B):
        print("PASS")
    else:
        print("FAIL")

    A = gpxpy.gpx.GPXWaypoint(latitude=40.228522, longitude=-3.694337)
    B = gpxpy.gpx.GPXWaypoint(latitude=40.228776, longitude=-3.694579)
    P = gpxpy.gpx.GPXWaypoint(latitude=40.228803, longitude=-3.694259)
    if not sameTrack(A,P,B):
        print("PASS")
    else:
        print("FAIL")
    
    

