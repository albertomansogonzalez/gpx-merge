import gpxpy
import gpxpy.gpx

def sameTrack(A, B, P):
    # return si P pertenece al segmento entre A y B

    # Comprobacion por contencion en el bounding box
    # TODO no funciona bien del todo esta aproximacion
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

