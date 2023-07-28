# gps_coord_checker
Containerized web server that returns XY distance between two coords

This app uses Flask as the server and geographiclibs to perform the necessary calculations.

## Usage
Run the container, the server listens on port 8080 and expects a JSON message as specified in req.json.
Post the json message to /distance to receive a Geodesic dictionary containing the results of the computation.
