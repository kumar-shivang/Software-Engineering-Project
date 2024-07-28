from flask import Flask, jsonify

from api import init_api

from database import init_db
from database.generate_data import generate_all


app = Flask(__name__)
init_api(app)

init_db()

generate_all()


@app.route("/get_all_routes")
def get_all_routes():
    # return in json format
    url_map = app.url_map
    return jsonify({rule.endpoint: rule.rule for rule in url_map.iter_rules()})


if __name__ == "__main__":
    app.run(debug=True)
