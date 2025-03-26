from flask import Flask, jsonify
from gtfs_tools import find_oilme_stops_and_routes
from gtfs_tools import get_schedule_for_route

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Tallinna bussid</h1><p>Vaata <a href='/api/oilme-routes'>Õilme liinide andmeid</a></p>"

@app.route("/api/oilme-routes")
def oilme_routes():
    result = find_oilme_stops_and_routes()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
