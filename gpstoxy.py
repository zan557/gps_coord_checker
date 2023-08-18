
from geographiclib.geodesic import Geodesic
from typing import List
from flask import Flask,request,jsonify,render_template

app = Flask(__name__,template_folder="templates")

geod = Geodesic.WGS84  # define the WGS84 ellipsoid

mem_store = []

def is_valid_latitude(latitude: float) -> bool:
    return -90.0 <= latitude <= 90.0

def is_valid_longitude(longitude: float) -> bool:
    return -180.0 <= longitude <= 180.0

def distance_between_coords(coordA: List[float], coordB: List[float]) -> float:
    if len(coordA) != 2 or len(coordB) != 2:
        raise ValueError("Coordinates must have exactly two values (latitude and longitude)")

    latitude_A, longitude_A = coordA
    latitude_B, longitude_B = coordB

    if not (is_valid_latitude(latitude_A) and is_valid_longitude(longitude_A)):
        raise ValueError("Invalid latitude or longitude in coordA")

    if not (is_valid_latitude(latitude_B) and is_valid_longitude(longitude_B)):
        raise ValueError("Invalid latitude or longitude in coordB")

    rslt=geod.Inverse(latitude_A,longitude_A,latitude_B,longitude_B)
    distance= rslt["s12"]
    mem_store.append({"coordA":coordA,"coordB":coordB,"distance":distance})
    return rslt

legend={"lat1": "latitude of point 1","lon1":"longitude of point 1","lat2":"latitude of point 2","lon2":"longitude of point 2","a12":"spherical arc length from the first point to the second in degrees","s12":"the distance from the first point to the second in meters","azi1":"azimuth at the first point in degrees","azi2":"azimuth at the second point in degrees"}

@app.route('/distance', methods=['POST'])
def calc_dist():
    try:
        data = request.get_json()
        coordA = data['coordA']
        coordB = data['coordB']
        rslt = distance_between_coords(coordA, coordB)
        return jsonify({'distance': rslt})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route("/viewer")
def display_map():
    return jsonify(mem_store)

@app.route("/coords", methods=["POST"])
def store_coord():
    return 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
