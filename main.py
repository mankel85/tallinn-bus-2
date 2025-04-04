from flask import Flask, jsonify, render_template, request
from gtfs_tools import find_oilme_stops_and_routes, get_schedule_for_route

app = Flask(__name__, template_folder="templates", static_folder="static")
@app.before_request
def before_any():
    print("Request received:", request.path)

@app.route("/")
def home():
    data = find_oilme_stops_and_routes()
    return render_template("index.html", routes=data["routes_with_oilme"])

@app.route("/api/schedule/<route>")
def schedule(route):
    return jsonify(get_schedule_for_route(route))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
