# import libraries
import datetime
import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_login import LoginManager, login_required, login_user, logout_user

from appConfig import AppConfig

# import backend functions
from buoyParser import allBuoys, parseBuoy
from db import DatabaseHandler, factory
from haversineCalc import haversineCalc
from surfSpot import SurfSpot, createSpot, deleteSession, getAllSessions, getAllSpots
from user import User

load_dotenv()

config = AppConfig(
    **{
        "db_user": os.getenv("DB_USER"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_name": os.getenv("DB_NAME"),
        "db_host": os.getenv("DB_HOST"),
        "secret_key": os.getenv("SECRET_KEY"),
    }
)
db: DatabaseHandler | None = factory(
    user=config.db_user,
    password=config.db_password,
    db_name=config.db_name,
    db_host=config.db_host,
)
if not db:
    raise Exception("Could not connect to db")

app = Flask(__name__)
app.secret_key = os.getenv("secretKey")
login_manager = LoginManager()
login_manager.init_app(app)
app.logger.setLevel(logging.INFO)


# Authenication and User routes
@login_manager.user_loader
def load_user(user_id):
    """
    handle user login/authentication
    """
    return User.get(user_id, db)


@app.get("/health")
def health():
    return jsonify({"status": "Active", "serverTs": datetime.datetime.now()}), 200


@app.route("/login", methods=["POST"])
def login():
    """
    This function is used to authenticate a user and add then to a session.
    If the user or password is incorrect than a failure message is returned.
    """
    formData = request.json
    if not formData:
        return jsonify({"result": "Bad request. No data passed to form!"}), 400
    username = formData["username"]
    password = formData["password"]
    user = User.get(username, db)
    if not user:
        return jsonify({"result": "Login Failed"}), 401

    user.verifyPassword(password)
    if not user.is_authenticated():
        return jsonify({"result": "Login Failed"}), 401

    login_user(user)
    app.logger.info("User Login Successful!")
    return jsonify({"result": "Login Successful", "userID": user._userID}), 200


@app.route("/createUser", methods=["POST"])
def createUser():
    """
    Route used to create a user. POST method that takes in a username
    and password from frontend form. If the username already exists it
    returns a 409 conflict reponse since the username already exists.
    Otherwise, it will return 200 if successful or 500 if there is some
    internal error such as a bad database connection.
    """
    formData = request.json
    if not formData:
        return jsonify({"result": "Bad request"}), 400
    username = formData["username"]
    password = formData["password"]

    # NEVER LOG PASSWORDS EVER -- this is a large security risk -> If logs are compromised, then credentials are compromised.
    # app.logger.info("username: ", username, "password: ", password)
    app.logger.info(f"{username = }")
    creation = User.createUser(username, password, db)
    if creation[0] == True:
        return jsonify({"result": "Account creation successful"}), 200
    elif creation[0] == False and creation[1] == 1:
        return jsonify({"result": "Username already exists"}), 409
    else:
        return jsonify({"result": "Internal service error"}), 500


@app.route("/auth", methods=["GET", "OPTIONS"])
@login_required
def auth():
    """
    Used by the frontend to quickly verify if the user is logged in when
    navigating between pages. It will either return an error if the user
    is not logged in or it simply returns an empty string if the
    user is logged in
    """
    return ""


@app.route("/logout")
@login_required
def logout():
    """
    Function used to logout a user from a Flask-Login session
    """
    logout_user()
    app.logger.info("User logged out successfully")
    return jsonify({"result": "Logout Successful"}), 200


@app.get("/request")
def buoyRequest():
    """
    route for getting buoy data for the station ID passed in the get request.
    To use this route the following request URL should be utilized:
    /request?stationID=<string>
    """

    # get all buoys
    # TODO: This is going to be a lot of data if there
    # are many stations... consider pagination if all buoys are
    # requested
    if request.args.get("stationID") == "all":
        data = allBuoys(db)
        if data:
            return jsonify(data), 200
        return jsonify({"result": "Error occurred"}), 409

    # get a single buoys data
    else:
        param = request.args.get("stationID")
        data = parseBuoy(param)
        app.logger.info(data)
        return jsonify(data)


# Buoy data and surf spot routes
@app.route("/findBuoys")
def findBuoys():
    """
    route to get the nearest buoys to a particular set of coordinates
    URL to use by frontend:
    /findBuoys?lat=<float>&long=<float>
    """
    lat = request.args.get("lat", type=float)
    long = request.args.get("long", type=float)
    coord = (lat, long)
    data = haversineCalc(coord, db)
    return jsonify(data)


@app.route("/surfSpot", methods=["GET", "PUT", "POST", "DELETE"])
@login_required
def spotRoute():
    """
    Route for getting a surf spot and creating a new surf spot.
    GET: Returns a JSON object of a surf spot or an empty object
    if it doesn't exist. /surfSpot?spotID=<int>
    POST: Takes in form data from the request and returns 201
    if successful or a 409 error otherwise.
    PUT: Edits both the ideal conditions and spot data. Avoids
    multiple requests to the backend this way.
    """
    if request.method == "GET":
        userID = request.args.get("userID", type=int)
        data = getAllSpots(userID, db)
        return jsonify(data)

    if request.method == "PUT":
        formData = request.json
        if not formData:
            return jsonify({"result": "Bad request"}), 400

        spotID = formData["spotID"]
        name = formData["name"]
        latitude = formData["latitude"]
        longitude = formData["longitude"]
        firstStation = formData["firstStation"]
        secondStation = formData["secondStation"]

        windDir = formData["windDir"]
        swellDir = formData["swellDir"]
        size = formData["size"]
        period = formData["period"]
        tideMax = formData["tideMax"]
        tideMin = formData["tideMin"]
        spot = SurfSpot(spotID, db)
        if spot.isValid:
            result1 = spot.updateSpot(
                name, latitude, longitude, firstStation, secondStation
            )
            result2 = spot.updateIdeal(
                windDir, swellDir, size, period, tideMax, tideMin
            )
            if result1 and result2:
                return jsonify({"result": "Spot Updated"}), 201
            elif not result1 and result2 == True:
                return (
                    jsonify(
                        {
                            "result": "Error occurred during\
                                spot update"
                        }
                    ),
                    409,
                )
            elif not result2 and result1 == True:
                return (
                    jsonify(
                        {
                            "result": "Error occurred during\
                                ideal update"
                        }
                    ),
                    409,
                )
        return jsonify({"result": "Error occurred"}), 409

    if request.method == "DELETE":
        spotID = request.args.get("spotID", type=int)
        spot = SurfSpot(spotID, db)
        if not spotID:
            return jsonify({"result": "Bad request"}), 400
        if spot.isValid:
            result = spot.deleteSpot()
            if result:
                return jsonify({"result": "Spot Deleted"}), 201
        return jsonify({"result": "Error occurred"}), 409

    if request.method == "POST":
        formData = request.json
        if not formData:
            return jsonify({"result": "Bad request"}), 400
        userID = formData["userID"]
        name = formData["name"]
        latitude = formData["latitude"]
        longitude = formData["longitude"]
        firstBuoyID = formData["firstBuoyID"]
        secondBuoyID = formData["secondBuoyID"]
        result = createSpot(
            userID, db, name, latitude, longitude, firstBuoyID, secondBuoyID
        )
        if result:
            return jsonify({"result": "Spot Created", "spotID": result[1]}), 201
        return jsonify({"result": "Error occurred"}), 409


@app.route("/ideal", methods=["GET", "POST", "PUT"])
@login_required
def ideal():
    """
    Route that can be used to read, create, or update the ideal
    conditions for a surf spot. Returns 201 if successful and 401
    otherwise.
    """
    if request.method == "GET":
        spotID = request.args.get("spotID")
        if not spotID:
            return jsonify({"result": "Bad request"}), 400

        spot = SurfSpot(spotID, db)
        data = {}
        if spot.isValid:
            data = spot.getIdeal()
        return jsonify(data)

    if request.method == "POST":
        formData = request.json
        if not formData:
            return jsonify({"result": "Bad request"}), 400
        spotID = formData["spotID"]
        spot = SurfSpot(spotID, db)
        windDir = formData["windDir"]
        swellDir = formData["swellDir"]
        size = formData["size"]
        period = formData["period"]
        tideMax = formData["tideMax"]
        tideMin = formData["tideMin"]
        result = spot.createIdeal(windDir, swellDir, size, period, tideMax, tideMin)
        if result:
            return jsonify({"result": "Ideal Created"}), 201
        return jsonify({"result": "Error occurred"}), 409

    if request.method == "PUT":
        formData = request.json
        if not formData:
            return jsonify({"result": "Bad request"}), 400
        spotID = formData["spotID"]
        spot = SurfSpot(spotID, db)
        windDir = formData["windDir"]
        swellDir = formData["swellDir"]
        size = formData["size"]
        period = formData["period"]
        tideMax = formData["tideMax"]
        tideMin = formData["tideMin"]
        result = spot.updateIdeal(windDir, swellDir, size, period, tideMax, tideMin)
        if result:
            return jsonify({"result": "Ideal updated"}), 201
        return jsonify({"result": "Error occurred"}), 409


@app.route("/Sessions", methods=["GET", "POST", "DELETE", "PUT"])
@login_required
def savedSessions():
    """
    Route to save a surf session or get previously saved
    surf sessions. POST returns a 201 if successful and a 409
    error code otherwise
    """
    if request.method == "GET":
        userID = request.args.get("userID", type=int)
        if not userID:
            return jsonify({"result": "Bad request"}), 400

        data = getAllSessions(userID, db)
        if not data:
            data = []

        return jsonify(data)

    if request.method == "POST":
        formData = request.json
        if not formData:
            return jsonify({"result": "Bad request"}), 400
        spotID = formData["spotID"]
        spot = SurfSpot(spotID, db)
        date = formData["date"]
        windSpd = formData["windSpd"]
        windDir = formData["windDir"]
        swellHgt = formData["swellHgt"]
        swellPer = formData["swellPer"]
        swellDir = formData["swellDir"]
        tide = formData["tide"]
        swellAct = formData["swellAct"]
        tideDir = formData["tideDir"]
        description = formData["description"]
        result = spot.saveSession(
            date,
            windSpd,
            windDir,
            swellHgt,
            swellPer,
            swellDir,
            tide,
            swellAct,
            tideDir,
            description,
        )
        if not result:
            return jsonify({"result": "Error occurred"}), 409
        return jsonify({"result": "Session saved"}), 201

    if request.method == "PUT":
        formData = request.json
        if not formData:
            return jsonify({"result": "Bad request"}), 400

        spotID = formData["spotID"]
        spot = SurfSpot(spotID, db)
        sessionID = formData["sessionID"]
        date = formData["date"]
        windSpd = formData["windSpd"]
        windDir = formData["windDir"]
        swellHgt = formData["swellHgt"]
        swellPer = formData["swellPer"]
        swellDir = formData["swellDir"]
        tide = formData["tide"]
        swellAct = formData["swellAct"]
        tideDir = formData["tideDir"]
        description = formData["description"]
        result = spot.editSession(
            date,
            windSpd,
            windDir,
            swellHgt,
            swellPer,
            swellDir,
            tide,
            swellAct,
            tideDir,
            description,
            sessionID,
        )
        if result:
            return jsonify({"result": "Session Edited Successfully"}), 201
        return jsonify({"result": "Error occurred"}), 409

    if request.method == "DELETE":
        sessionID = request.args.get("sessionID", type=int)
        if not sessionID:
            return jsonify({"result": "Bad request"}), 400

        result = deleteSession(sessionID, db)
        if not result:
            return jsonify({"result": "Error occurred"}), 409

        return jsonify({"result": "Session Deleted"}), 201


if __name__ == "__main__":
    app.run(port=5000, debug=True)
