import csv
import requests

# reading data file
r = open('routes.geojson', 'a', encoding='utf8')
start = """\
{
    "type": "RouteCollection",
    "routes": [
"""
end = """    
    ]
}
"""
r.write(start)

def router():
        # returns a file object which is a buffered stream
    with open('./nyc-taxi-trip-duration/test.csv', 'r') as f:
        # DictReader returns a reader object, which is iterable by row. each row is mapped to dict.
        data = csv.DictReader(f)
        chunk = (next(data) for i in range(3))

        for trip in chunk:
            # print(trip)
            # parameter dictionary for http call
            p = {
                'service': 'route',
                'version': 'v1',
                'profile': 'driving',
                'coordinates': f'{trip["pickup_longitude"]},{trip["pickup_latitude"]};'
                               f'{trip["dropoff_longitude"]},{trip["dropoff_latitude"]}',
            }
            params = {
                'geometries': 'geojson',
                'generate_hints': 'false'
            }
            url = f'http://router.project-osrm.org/' \
                  f'{p["service"]}/{p["version"]}/{p["profile"]}/{p["coordinates"]}'
            try:
                res = requests.get(url, params) # response object
                res.raise_for_status() # raise http error method
            except requests.exceptions.HTTPError: # handle httperror class
                r.write(end)
                r.close()
                return

            route = res.json()['routes'][0]['geometry']
            route_geo = str({"geometry": route})
            route_geo = route_geo.replace("'",'"')
            route_geo = route_geo + ',\n'
            print(f'{route_geo}')
            r.write(route_geo)

r.write(end)
r.close()

