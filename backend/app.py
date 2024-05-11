# import libraries
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from flask_login import LoginManager, login_user, logout_user, login_required

# import backend functions
from buoyParser import parseBuoy
from haversineCalc import haversineCalc
from user import User

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secretKey")
CORS(app, supports_credentials=True)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    handle user login/authentication
    """
    return User.get(user_id)


@app.route("/login", methods=['POST'])
def login():
    """
    This function is used to authenicate a user and add then to a session.
    If the user or password is incorrect than a failure message is returned.
    """
    formData = request.json
    username = formData['username']
    password = formData['password']
    user = User.get(username)
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
    creation = User.createUser(username, password)
    if creation[0] is True:
        return jsonify({"result": "Account creation successful"}), 200
    elif creation[0] is False and creation[1] == 1:
        return jsonify({"result": "Username already exists"}), 409
    else:
        return jsonify({"result": "Internal service error"}), 500


@app.route("/auth", methods=["GET"])
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
    http://localhost:5000/request?stationID=<string>
    """

    # get buoy data
    param = request.args.get("stationID")
    data = parseBuoy(param)

    # return data to frontend
    return json.dumps(data)


@app.route("/findBuoys")
def findBuoys():
    """
    route to get the nearest buoys to a particular set of coordinates
    URL to use by frontend:
    http://127.0.0.1:5000/findBuoys?lat=<float>&long=<float>
    """
    lat = request.args.get('lat', type=float)
    long = request.args.get('long', type=float)
    coord = (lat, long)
    data = haversineCalc(coord)
    return json.dumps(data)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
