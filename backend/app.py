#import libraries
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from flask_login import LoginManager, login_user, logout_user, login_required

#import backend functions
from buoyParser import parseBuoy
from haversineCalc import haversineCalc
from user import User

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secretKey")
CORS(app, supports_credentials=True)
login_manager = LoginManager()
login_manager.init_app(app)

#handle user login/authentication
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/login", methods=['POST'])
def login():
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
    formData = request.json
    username = formData['username']
    password = formData['password']
    print("username: ", username, "password: ", password)
    User.createUser(username, password)
    return ""

    
@app.route("/auth", methods=["GET"])
@login_required
def auth():
    return ""

@app.route("/logout")
@login_required
def logout():
    logout_user()
    print("User logged out successfully")
    return jsonify({"result": "Logout Successful"}), 200

#route for getting buoy data for the station ID passed in the get request
@app.get("/request")
def buoyRequest():
    #get buoy data
    param = request.args.get("stationID")
    data = parseBuoy(param)

    #return data to frontend
    return json.dumps(data)

#route to get the nearest buoys to a particular set of coordinates
#URL to use by frontend: http://127.0.0.1:5000/findBuoys?lat=<float>&long=<float>
@app.route("/findBuoys")
def findBuoys():
    lat = request.args.get('lat', type=float)
    long = request.args.get('long', type=float)
    coord = (lat, long)
    data = haversineCalc(coord)
    return json.dumps(data)

if __name__ == "__main__":
    app.run(port = 5000, debug = True)
