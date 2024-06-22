class SurfSpot:
    def __init__(self, spotID: int):
        self._spotID = spotID
        self._spotName = None
        self._buoy1 = None
        self._buoy2 = None

    def getSpot(self, spotID: int, db: object) -> None:
        """
        Gets all the information for a surf spot
        """
        query = "SELECT * FROM SurfSpots WHERE spotID = %s"
        params = [spotID]
        data = db.executeQuery(query, params)
        self._spotName = data[1]
        if len(data) == 4:
            self._buoy1 = data[2]
            self._buoy2 = data[3]
        elif len(data) == 3:
            self._buoy1 = data[2]
        return


def createSpot(userID: int, db: object,  firstBuoyID: int = None,
               secondBuoyID: int = None) -> bool:
    """
    Creates a new surf spot and adds it to the database. Returns True if
    successful and False otherwise.
    """
    if firstBuoyID is None:
        query = "INSERT INTO SurfSpots (userID) VALUES (%s)"
        params = (userID)
    elif secondBuoyID is None:
        query = "INSERT INTO SurfSpots (userID, firstBuoyID) VALUES (\
                %s, %s)"
        params = (userID, firstBuoyID)
    else:
        query = "INSERT INTO SurfSpots (userID, firstBuoyID, \
                    secondBuoyID) VALUES (%s, %s, %s)"
        params = (userID, secondBuoyID)

    response = db.executeQuery(query, params)
    if not response:
        return False

    return True
