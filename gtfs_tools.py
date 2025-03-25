import tempfile
import requests
import zipfile
import io
import csv

def find_oilme_stops_and_routes():
    zip_url = 'https://transport.tallinn.ee/data/gtfs.zip'
    response = requests.get(zip_url)
    zip_path = tempfile.mktemp()
    with open(zip_path, 'wb') as f:
        f.write(response.content)

    oilme_stop_ids = []
    stops_data = {}
    routes_data = {}
    trip_data = {}
    routes_with_oilme = set()

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open('stops.txt') as stops_file:
            stops_text = io.TextIOWrapper(stops_file, encoding='utf-8-sig')
            reader = csv.DictReader(stops_text)
            for row in reader:
                stops_data[row['stop_id']] = row
                if 'Õilme' in row['stop_name']:
                    oilme_stop_ids.append(row['stop_id'])

        with zip_ref.open('routes.txt') as routes_file:
            routes_text = io.TextIOWrapper(routes_file, encoding='utf-8-sig')
            reader = csv.DictReader(routes_text)
            for row in reader:
                routes_data[row['route_id']] = row

        with zip_ref.open('trips.txt') as trips_file:
            trips_text = io.TextIOWrapper(trips_file, encoding='utf-8-sig')
            reader = csv.DictReader(trips_text)
            for row in reader:
                trip_data[row['trip_id']] = row

        if oilme_stop_ids:
            with zip_ref.open('stop_times.txt') as stop_times_file:
                stop_times_text = io.TextIOWrapper(stop_times_file, encoding='utf-8-sig')
                reader = csv.DictReader(stop_times_text)
                for row in reader:
                    if row['stop_id'] in oilme_stop_ids:
                        trip_id = row['trip_id']
                        if trip_id in trip_data:
                            route_id = trip_data[trip_id]['route_id']
                            if route_id in routes_data:
                                route_short_name = routes_data[route_id]['route_short_name']
                                routes_with_oilme.add(route_short_name)

    return {
        "oilme_stop_ids": oilme_stop_ids,
        "routes_with_oilme": sorted(list(routes_with_oilme))
    }
