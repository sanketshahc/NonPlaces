import csv
import requests

# opening geojson file for writing
r = open('routes.geojson', 'a', encoding='utf8')
start = """\
{
    "type": "FeatureCollection",
    "features": [
"""
end = """    
    ]
}
"""
r.write(start)

def router():
        # opening data file...returns a file object which is a buffered stream
    with open('dataset/taxi_data.csv', 'r') as f:
        # DictReader returns a reader object, which is iterable by row. each row is mapped to dict.
        data = csv.DictReader(f)
        # chunk = (next(data) for i in range(3)) # chunk for testing

        count = 1
        for trip in data:
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
            # res = requests.get(url, params)  # response object
            try:
                res = requests.get(url, params) # response object
                res.raise_for_status() # raise http error method
            except requests.exceptions.HTTPError: # handle httperror class
                print("HTTPError!")
                r.write(end)
                r.close()
                return

            route = res.json()['routes'][0]['geometry']
            route_geo = str({"geometry": route})
            route_geo = route_geo.replace("'",'"')
            route_geo = '       '+route_geo + ',\n'
            # print(f'{route_geo}')
            r.write(route_geo)
            print(count)
            count += 1
        return


router()
r.write(end)
r.close()

