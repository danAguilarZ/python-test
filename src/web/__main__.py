from flask import Flask, jsonify, request, render_template
from web import args
import sqlite3
from web import config
import requests
from math import ceil


def get_total_users(database: str, table: str) -> int:
    connection = sqlite3.connect(database, uri=True)
    cursor = connection.cursor()

    total_users = cursor.execute("SELECT COUNT() FROM %s" % table).fetchone()[0]

    connection.close()

    return int(total_users)


def create_app(database_configuration: dict, flask_configuration: dict = None) -> Flask:
    application = Flask(__name__)
    application.config["DEBUG"] = True if not flask_configuration else flask_configuration.get("debug_mode", True)

    total = get_total_users(database_configuration["database"], database_configuration["table"])

    @application.errorhandler(404)
    def not_found():
        return "<html><head></head><body><h1>Page Not Found: 404</h1></body></html>"

    @application.errorhandler(Exception)
    def internal_server_error():
        return "<html><head></head><body><h1>Oops! Internal Server Error, we are working for you</h1></body></html>"

    @application.route("/profiles", methods=["GET"])
    def get_profiles():
        arguments = []
        query = "SELECT * FROM %s" % database_configuration["table"]
        size = args.size
        if "username" in request.args:
            query += " WHERE username=?"
            arguments.append(request.args["username"])
        if "size" in request.args:
            size = int(request.args["size"])
        if "order_by" in request.args:
            query += " ORDER BY %s ASC" % request.args["order_by"]
        if "page" in request.args:
            query += " LIMIT %s, %s" % ((int(request.args["page"]) - 1) * size, size)
        else:
            query += " LIMIT %s" % size

        connection = sqlite3.connect(database_configuration["database"], uri=True)
        cursor = connection.cursor()

        try:
            profiles = cursor.execute(query, tuple(arguments))
        except sqlite3.OperationalError as e:
            print(e)
            return jsonify([])

        result = []

        for profile in profiles.fetchall():
            result.append({
                "id": profile[0],
                "username": profile[1],
                "type": profile[2],
                "avatar": profile[3],
                "page": profile[4]
            })

        cursor.close()
        connection.close()

        return jsonify(result)

    @application.route("/", methods=["GET", "POST"])
    def index():
        multimap = request.args if request.method == "GET" else request.form
        request_params = multimap.to_dict(flat=True)
        order_by = None

        request_profiles = {
            "page": int(request_params.get("page", 1)),
            "size": int(request_params.get("size", args.size))
        }
        if request_profiles["size"] < 0:
            request_profiles["size"] = int(args.size)
        if "previous" in request_params:
            request_profiles["page"] = request_profiles["page"] - 1
        if "next" in request_params:
            request_profiles["page"] = request_profiles["page"] + 1
        if "order_by" in request_params:
            request_profiles["order_by"] = request_params["order_by"]
            order_by = request_params["order_by"]

        number_pages = ceil(total / int(request_profiles["size"]))

        response = requests.get(
            "http://127.0.0.1:{0}/profiles".format(args.port),
            params=request_profiles
        )

        return render_template(
            "index.html", users=response.json(),
            size=request_profiles["size"],
            page=request_profiles["page"],
            number_pages=number_pages,
            port=args.port,
            order_by=order_by
        )

    return application


if __name__ == '__main__':
    app = create_app(config.get("sqlite"), config.get("flask", None))

    app.run(port=args.port, debug=False)
