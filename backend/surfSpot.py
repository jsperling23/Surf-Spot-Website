from dbClass import Database


class SurfSpot:
    def __init__(self, spotID: int, db: object):
        self._spotID = spotID
        self._userID = None
        self._spotName = None
        self._longitude = None
        self._latitude = None
        self._buoy1 = None
        self._buoy2 = None
        self._db = db
        self.isValid = False
        self.initSpot(self._spotID)

    def initSpot(self, spotID: int) -> None:
        """
        Gets all the information for a surf spot, called upon object
        initialization.
        """
        query = "SELECT * FROM SurfSpots WHERE spotID = %s"
        params = [spotID]
        data = self._db.executeQuery(query, params, "one")
        if data:
            self._userID = data[1]
            self._spotName = data[2]
            self._latitude = data[3]
            self._longitude = data[4]
            self.isValid = True
            if len(data) == 7:
                self._buoy1 = data[5]
                self._buoy2 = data[6]
            elif len(data) == 6:
                self._buoy1 = data[4]
        return

    def getSpot(self) -> dict:
        """
        Returns a dictionary containing all the information about
        a surf spot. It will return an empty dictionary if something
        goes wrong,
        """
        if self._buoy2 is not None:
            query = "SELECT SurfSpots.spotID, SurfSpots.userID,\
                    SurfSpots.name, SurfSpots.latitude, SurfSpots.longitude,\
                    buoy1.stationID AS buoy1, buoy2.stationID AS buoy2 FROM\
                    SurfSpots INNER JOIN Buoys AS buoy1 ON\
                    SurfSpots.firstBuoyID = buoy1.buoyID INNER JOIN Buoys AS\
                    buoy2 ON SurfSpots.secondBuoyID = buoy2.buoyID WHERE\
                    SurfSpots.spotID = %s"
        elif self._buoy1 is not None:
            query = "SELECT SurfSpots.spotID, SurfSpots.userID,\
                    SurfSpots.name, SurfSpots.latitude, SurfSpots.longitude,\
                    buoy1.stationID AS buoy1, SurfSpots.secondBuoyID FROM\
                    SurfSpots INNER JOIN Buoys AS buoy1 ON\
                    SurfSpots.firstBuoyID = buoy1.buoyID WHERE\
                    SurfSpots.spotID = %s"
        else:
            query = "SELECT * FROM SurfSpots WHERE spotID = %s"
        params = [self._spotID]
        spot = {}
        db = self._db
        data = db.executeQuery(query, params, "one")
        if data:
            spot["spotID"] = data[0]
            spot["userID"] = data[1]
            spot["name"] = data[2]
            spot["latitude"] = data[3]
            spot["longitude"] = data[4]
            spot["buoy1"] = data[5]
            spot["buoy2"] = data[6]
        return spot

    def updateSpot(self, name: str, latitude: float,
                   longitude: float, firstStation: str = None,
                   secondStation: str = None) -> bool:
        """
        Updates a surf spot in the database. Returns True if successful and
        False otherwise.
        """
        query = "UPDATE SurfSpots SET name = %s, latitude = %s,\
                longitude = %s, firstBuoyID = (SELECT buoyID \
                FROM Buoys WHERE stationID = %s), secondBuoyID = \
                (SELECT buoyID FROM Buoys WHERE stationID = %s)\
                WHERE spotID = %s"
        params = [name, latitude, longitude, firstStation, secondStation,
                  self._spotID]
        db = self._db
        result = db.executeQuery(query, params)

        if not result:
            return False
        return True

    def getIdeal(self) -> dict:
        """
        Gets the ideal conditions and returns them in a dictionary. If any
        issues pop up an empty dictionary is returned.
        """
        query = "SELECT * FROM IdealConditions WHERE spotID = %s"
        params = [self._spotID]
        db = self._db
        data = db.executeQuery(query, params, "one")
        ideal = {}
        if data:
            ideal["conditionID"] = data[0]
            ideal["spotID"] = data[1]
            ideal["windDir"] = data[2]
            ideal["swellDir"] = data[3]
            ideal["waveSize"] = data[4]
            ideal["period"] = data[5]
            ideal["tideMax"] = data[6]
            ideal["tideMin"] = data[7]
        return ideal

    def createIdeal(self, windDir: str, swellDir: str,
                    size: str, period: str, tideMax: float,
                    tideMin: float) -> bool:
        """
        Creates an entry in the IdealConditions table for a spots
        ideal conditions. Only one entry allowed per spot. This
        function returns True if successful and False otherwise.
        """
        query = "INSERT INTO IdealConditions (spotID, windDirection,\
                swellDirection, waveSize, swellPeriod, tideUpper, tideLower)\
                VALUES ((SELECT spotID FROM SurfSpots WHERE\
                spotID = %s), %s, %s, %s, %s, %s, %s)"
        params = [self._spotID, windDir, swellDir, size, period, tideMax,
                  tideMin]
        db = self._db
        result = db.executeQuery(query, params)

        if not result:
            return False
        return True

    def updateIdeal(self, windDir: str, swellDir: str,
                    size: str, period: str, tideMax: float,
                    tideMin: float) -> bool:
        """
        Updates the ideal conditions for a specific surf spot. Returns
        True if successful and False otherwise.
        """
        query = "UPDATE IdealConditions SET windDirection = %s,\
                swellDirection = %s, waveSize = %s, swellPeriod = %s,\
                tideUpper = %s, tideLower = %s WHERE spotID = %s"
        params = [windDir, swellDir, size, period, tideMax, tideMin,
                  self._spotID]
        db = self._db
        result = db.executeQuery(query, params)

        if not result:
            return False
        return True

    def deleteSpot(self) -> bool:
        """
        Deletes a spot from the SurfSpots table
        """
        query = "DELETE FROM SurfSpots WHERE spotID = %s"
        params = [self._spotID]
        db = self._db
        result = db.executeQuery(query, params)

        if not result:
            return False
        return True

    def saveSession(self, date: str, windSpd: int, windDir: int,
                    swellHgt: float, swellPer: int, swellDir: int, tide: float,
                    swellAct: str, tideDir: str, description: str) -> bool:
        """
        Saves a session to the SavedSessions Table
        """
        query = "INSERT INTO SavedSessions (spotID, userID, date, windSpeed,\
                windDirection, swellHeight, swellPeriod, swellDirection, tide,\
                swellActivity, tideDirection, description) VALUES ((SELECT\
                spotID FROM SurfSpots WHERE spotID = %s), (SELECT userID FROM\
                Users WHERE userID = %s),%s, %s, %s, %s, %s, %s, %s, %s, %s,\
                %s)"
        params = [self._spotID, self._userID, date, windSpd, windDir, swellHgt,
                  swellPer, swellDir, tide, swellAct, tideDir, description]
        db = self._db
        result = db.executeQuery(query, params)
        if not result:
            return False
        return True

    def editSession(self, date: str, windSpd: int, windDir: int,
                    swellHgt: float, swellPer: int, swellDir: int, tide: float,
                    swellAct: str, tideDir: str, description: str,
                    sessionID: int) -> bool:
        """
        Edits a session in the SavedSessions Table
        """
        query = "UPDATE SavedSessions SET date = %s, windSpeed = %s,\
                windDirection = %s, swellHeight = %s, swellPeriod = %s,\
                swellDirection = %s, tide = %s, swellActivity = %s,\
                tideDirection = %s, description = %s WHERE sessionID = %s"
        params = [date, windSpd, windDir, swellHgt,
                  swellPer, swellDir, tide, swellAct, tideDir, description,
                  sessionID]
        db = self._db
        result = db.executeQuery(query, params)
        if not result:
            return False
        return True

    def getSessions(self) -> dict:
        """
        Returns all sessions in a dictionary where the key is the date and
        the value is a dictionary containing the session information. If
        there are no sessions or something goes wrong, an empty dictionary
        is returned.
        """
        sessions = {}
        query = "SELECT * FROM SavedSessions WHERE SpotID = %s"
        params = [self._spotID]
        db = self._db
        data = db.executeQuery(query, params)

        for sesh in data:
            sessions[sesh[0]] = {
                "SessionID": sesh[0],
                "spotID": sesh[1],
                "date": sesh[2],
                "windSpd": sesh[3],
                "windDir": sesh[4],
                "swellHgt": sesh[5],
                "period": sesh[6],
                "swellDir": sesh[7],
                "tide": sesh[8],
                "swellActivity": sesh[9],
                "description": sesh[10]
            }

        return sessions


def deleteSession(sessionID: int, db: object) -> bool:
    """
    Deletes a session from the session table. Returns True if
    successful and False otherwise.
    """
    query = "DELETE FROM SavedSessions WHERE SessionID = %s"
    params = [sessionID]
    result = db.executeQuery(query, params)

    if not result:
        return False
    return True


def createSpot(userID: int, db: object, name: str, latitude: float,
               longitude: float, firstStationID: str = None,
               secondStationID: str = None) -> bool:
    """
    Creates a new surf spot and adds it to the database. Returns True if
    successful and False otherwise.
    """
    if firstStationID is None:
        query = "INSERT INTO SurfSpots (userID, name, latitude, longitude)\
                VALUES ((SELECT userID FROM Users WHERE userID = %s), %s,\
                %s, %s)"
        params = (userID, name, latitude, longitude)
    elif secondStationID is None:
        query = "INSERT INTO SurfSpots (userID, name, latitude, longitude,\
                firstBuoyID) VALUES ((SELECT userID FROM Users WHERE\
                userID = %s), %s, %s, %s, (SELECT buoyID FROM Buoys\
                WHERE stationID = %s))"
        params = (userID, name, latitude, longitude, firstStationID)
    else:
        query = "INSERT INTO SurfSpots (userID, name, latitude, longitude,\
                firstBuoyID, secondBuoyID) VALUES ((SELECT userID FROM Users\
                WHERE userID = %s), %s, %s, %s, (SELECT buoyID FROM Buoys\
                WHERE stationID = %s), (SELECT buoyID FROM Buoys\
                WHERE stationID = %s))"
        params = (userID, name, latitude, longitude, firstStationID,
                  secondStationID)

    response = db.executeQuery(query, params)
    if not response:
        return False

    return True, response[1]


def getAllSpots(userID: int, db: object) -> dict:
    query = "SELECT spotID FROM SurfSpots WHERE userID = %s"
    data = db.executeQuery(query, [userID])
    spots = {}
    if data:
        for spot in data:
            current = SurfSpot(spot[0], db)
            print(current)
            spots[spot[0]] = current.getSpot()
            spots[spot[0]]["ideal"] = current.getIdeal()
    return spots


def getAllSessions(userID: int, db: object) -> dict:
    query = "SELECT SavedSessions.sessionID, SavedSessions.date,\
            SavedSessions.windSpeed, SavedSessions.windDirection,\
            SavedSessions.swellHeight, SavedSessions.swellPeriod,\
            SavedSessions.swellDirection, SavedSessions.tide,\
            SavedSessions.swellActivity, SavedSessions.tideDirection,\
            SavedSessions.description, SurfSpots.name, SurfSpots.spotID FROM\
            SavedSessions INNER JOIN SurfSpots ON SavedSessions.spotID =\
            SurfSpots.spotID WHERE SavedSessions.userID = %s"
    data = db.executeQuery(query, [userID])
    sessions = {}
    if data:
        for sesh in data:
            sessions[sesh[0]] = {
                "date": sesh[1],
                "windSpeed": sesh[2],
                "windDirection": sesh[3],
                "swellHeight": sesh[4],
                "swellPeriod": sesh[5],
                "swellDirection": sesh[6],
                "tide": sesh[7],
                "swellActivity": sesh[8],
                "tideDirecton": sesh[9],
                "description": sesh[10],
                "name": sesh[11],
                "sessionID": sesh[0],
                "spotID": sesh[12]
            }
    return sessions


if __name__ == "__main__":
    db = Database()
    # getAllSessions(1, db)
    # d = createSpot(1, db, "billys", 420.32, 345.23)
    # print(d)
    # e = createSpot(1, db, "Tommy's", 420.32, 345.23, 1)
    # f = createSpot(1, db, "Bommie's", 420.32, 345.23, 1, 2)
    # print(getAllSpots(1, db))
    # spot = SurfSpot(1, db)
    # print(spot.deleteSpot())
    print(deleteSession(1, db))
    # spot.createIdeal("NW", "W", "Overhead", "Long", 3.00, -1.00)
    # spot.saveSession("2024-06-28", 15, 270, 6.5, 16, 270,
    # 3.9, "increasing", "slack", "Holy hell it was macking")

    # print(spot.deleteSpot())
    # spot.updateIdeal("NE", "WNW", "Triple Overhead", "Medium", 5.3, -0.6)

    # SurfSpot(12, db)
    # SurfSpot(13, db)
