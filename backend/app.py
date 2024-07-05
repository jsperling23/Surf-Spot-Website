# import libraries
import os
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required

# import backend functions
from buoyParser import parseBuoy
from haversineCalc import haversineCalc
from user import User
from dbClass import Database
from surfSpot import SurfSpot  # , createSpot

# setup flask server and login
app = Flask(__name__)
app.secret_key = os.getenv("secretKey")
login_manager = LoginManager()
login_manager.init_app(app)

# connect to database
db = Database()
if not db.status():
    print("database connection failed")


# Authenication and User routes
@login_manager.user_loader
def load_user(user_id):
    """
    handle user login/authentication
    """
    return User.get(user_id, db)


@app.route("/login", methods=['POST'])
def login():
    """
    This function is used to authenicate a user and add then to a session.
    If the user or password is incorrect than a failure message is returned.
    """
    formData = request.json
    username = formData['username']
    password = formData['password']
    user = User.get(username, db)
    if user:
        user.verifyPassword(password)
        if user.is_authenticated():
            login_user(user)
            print("User Login Successful!")
            return jsonify({"result": "Login Successful"}), 200
    return jsonify({"result": "Login Failed"}), 401


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
    username = formData['username']
    password = formData['password']
    print("username: ", username, "password: ", password)
    creation = User.createUser(username, password, db)
    if creation[0] is True:
        return jsonify({"result": "Account creation successful"}), 200
    elif creation[0] is False and creation[1] == 1:
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
    print("User logged out successfully")
    return jsonify({"result": "Logout Successful"}), 200


@app.get("/request")
def buoyRequest():
    """
    route for getting buoy data for the station ID passed in the get request.
    To use this route the following request URL should be utilized:
    /request?stationID=<string>
    """

    # get buoy data
    param = request.args.get("stationID")
    data = parseBuoy(param)
    print(data)
    # return data to frontend
    return jsonify(data)


# Buoy data and surf spot routes
@app.route("/findBuoys")
def findBuoys():
    """
    route to get the nearest buoys to a particular set of coordinates
    URL to use by frontend:
    /findBuoys?lat=<float>&long=<float>
    """
    lat = request.args.get('lat', type=float)
    long = request.args.get('long', type=float)
    coord = (lat, long)
    data = haversineCalc(coord, db)
    return jsonify(data)


@app.route("/surfSpot", methods=["GET", "POST"])
def spotRoute():
    """
    Route for getting a surf spot and creating a new surf spot.
    GET: Returns a JSON object of a surf spot or an empty object
    if it doesn't exist. /surfSpot?spotID=<int>
    POST: Takes in form data from the request and returns 201
    if successful or a 409 error otherwise.
    """
    if request.method == "GET":
        spotID = request.args.get('spotID', type=int)
        spot = SurfSpot(spotID, db)
        data = {}
        if spot.isValid:
            data = spot.getSpot()
            if data["buoy1"]:
                data["buoy1"] = parseBuoy(data["buoy1"])
            if data["buoy2"]:
                data["buoy2"] = parseBuoy(data["buoy2"])
        return jsonify(data)

    if request.method == "POST":
        formData = request.json
        spotID = formData["spotID"]
        name = formData["name"]
        latitude = formData["latitude"]
        longitude = formData["longitude"]
        firstBuoyID = formData["firstBuoyID"]
        secondBuoyID = formData["secondBuoyID"]
        spot = SurfSpot(spotID, db)
        if spot.isValid:
            result = spot.updateSpot(name, latitude, longitude,
                                     firstBuoyID, secondBuoyID)
            if result:
                return jsonify({"result": "Spot Updated"}), 201
            return jsonify({"result": "Error occurred"}), 409
        return jsonify({"result": "Spot doesn't exist"}), 409


if __name__ == "__main__":
    app.run(port=5000, debug=True)
