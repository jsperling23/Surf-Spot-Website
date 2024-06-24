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
        self.initSpot(self._spotID)

    def initSpot(self, spotID: int) -> None:
        """
        Gets all the information for a surf spot, called upon object
        initialization.
        """
        query = "SELECT * FROM SurfSpots WHERE spotID = %s"
        params = [spotID]
        data = self._db.executeQuery(query, params, "one")
        self._userID = data[1]
        self._spotName = data[2]
        self._latitude = data[3]
        self._longitude = data[4]
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
            spot["buoy 2"] = data[6]
        return spot

    def updateSpot(self, name: str, latitude: float,
                   longitude: float, firstBuoyID: int = None,
                   secondBuoyID: int = None) -> bool:
        """
        Updates a surf spot in the database. Returns True if successful and
        False otherwise.
        """
        query = "UPDATE SurfSpots SET name = %s, latitude = %s,\
                longitude = %s, firstBuoyID = (SELECT buoyID \
                FROM Buoys WHERE buoyID = %s), secondBuoyID = \
                (SELECT buoyID FROM Buoys WHERE buoyID = %s)\
                WHERE spotID = %s"
        params = [name, latitude, longitude, firstBuoyID, secondBuoyID,
                  self._spotID]
        db = self._db
        result = db.executeQuery(query, params)
        print(result)
        if not result:
            return False
        return True

    def getIdeal(self) -> dict:
        pass

    def createIdeal(self, spotID: int, windDir: str, swellDir: str,
                    size: str, period: str, tideMax: float,
                    tideMin: float) -> bool:
        pass

    def updateIdeal(self, spotID: int, windDir: str, swellDir: str,
                    size: str, period: str, tideMax: float,
                    tideMin: float) -> bool:
        pass

    def deleteSpot(self) -> bool:
        pass

    def saveSession(self, windSpd: int, windDir: int, swellHgt: float,
                    swellPer: int, tide: float, swellActivity: str,
                    tideDir: str) -> bool:
        pass


def createSpot(userID: int, db: object, name: str, latitude: float,
               longitude: float, firstBuoyID: int = None,
               secondBuoyID: int = None) -> bool:
    """
    Creates a new surf spot and adds it to the database. Returns True if
    successful and False otherwise.
    """
    if firstBuoyID is None:
        query = "INSERT INTO SurfSpots (userID, name, latitude, longitude)\
                VALUES ((SELECT userID FROM Users WHERE userID = %s), %s,\
                %s, %s)"
        params = (userID, name, latitude, longitude)
    elif secondBuoyID is None:
        query = "INSERT INTO SurfSpots (userID, name, latitude, longitude,\
                firstBuoyID) VALUES ((SELECT userID FROM Users WHERE\
                userID = %s), %s, %s, %s, (SELECT buoyID FROM Buoys\
                WHERE buoyID = %s))"
        params = (userID, name, latitude, longitude, firstBuoyID)
    else:
        query = "INSERT INTO SurfSpots (userID, name, latitude, longitude,\
                firstBuoyID, secondBuoyID) VALUES ((SELECT userID FROM Users\
                WHERE userID = %s), %s, %s, %s, (SELECT buoyID FROM Buoys\
                WHERE buoyID = %s), (SELECT buoyID FROM Buoys\
                WHERE buoyID = %s))"
        params = (userID, name, latitude, longitude, firstBuoyID, secondBuoyID)

    response = db.executeQuery(query, params)
    if not response:
        return False

    return True


if __name__ == "__main__":
    db = Database()
    # d = createSpot(1, db, "billys", 420.32, 345.23)
    # e = createSpot(1, db, "Tommy's", 420.32, 345.23, 1)
    # f = createSpot(1, db, "Bommie's", 420.32, 345.23, 1, 2)
    spot = SurfSpot(10, db)
    print(spot.getSpot())
    spot.updateSpot("Slop Rock", 642.3, -23.2, 3, 6)
    print(spot.getSpot())

    SurfSpot(12, db)
    # SurfSpot(13, db)
