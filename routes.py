import csv
import requests
import time
import numpy

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

            # set time
            t = '01-01-1971 ' + trip['pickup_datetime'].split(' ')[1]
            dd = trip['pickup_datetime'].split(' ')[0] + 'T00:00:00Z'
            tt = time.strptime(t, "%m-%d-%Y %H:%M:%S")
            ttt = numpy.array([time.mktime(tt) + 1000000000], dtype = numpy.int64)
            properties = {
                "id": trip["id"],
                "vendor_id": int(trip["vendor_id"]),
                "pickup_date": dd,
                "pickup_time": trip['pickup_datetime'].split(' ')[1],
                "passenger_count": int(trip["passenger_count"]),
                "pickup_longitude": float(trip["pickup_longitude"]),
                "pickup_latitude": float(trip["pickup_latitude"]),
                "dropoff_longitude": float(trip["dropoff_longitude"]),
                "dropoff_latitude": float(trip["dropoff_latitude"])
            }
            # print(properties)
            # build list of ratios for timestamping
            norm = numpy.linalg.norm
            duration = res.json()['routes'][0]['duration']
            route = res.json()['routes'][0]['geometry']
            ways = numpy.array(res.json()['routes'][0]['geometry']['coordinates'])
            euclideans = numpy.zeros(len(ways))
            for i in range(len(ways) - 1):
                euclideans[i] = norm(ways[i] - ways[i+1])

            esum = euclideans.sum()
            if esum == 0:
                continue
            abs_ratios = euclideans / esum
            ratios = []

            def cum_r(base=0, i =0):
                if base == 0:
                    ratios.append(abs_ratios[i])
                elif len(ratios) == len(abs_ratios)-1:
                    ratios.append(0)
                    return
                else:
                    ratios.append(abs_ratios[i]+base)
                i += 1
                cum_r(ratios[-1], i)

            cum_r()
            ratios = numpy.array(ratios)
            durations = ((ratios * duration) + ttt).astype(numpy.int64)
            durations = ttt.tolist() + durations.tolist()[:-1]
            ways = ways.tolist()

            for i, w in enumerate(ways):
                w += [0, durations[i]]
            route['coordinates'] = ways
            route_geo = \
                f"""
                {{
                    "type": "Feature",
                    "geometry": {route},
                    "properties": {properties}
                }}
                    """


            route_geo = route_geo.replace("'",'"')
            route_geo = '       '+route_geo + ',\n'
            r.write(route_geo)
            print(count)
            count += 1
        return

router()
r.write(end)
r.close()


# Model format geojson""
# {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {
#         "vendor":  "A"
#       },
#       "geometry": {
#         "type": "LineString",
#         "coordinates": [
#           [-74.20986, 40.81773, 0, 1564184363],
#           [-74.20987, 40.81765, 0, 1564184396],
#           [-74.20998, 40.81746, 0, 1564184409]
#         ]
#       }
#     }
#   ]
# }