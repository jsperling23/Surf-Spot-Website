from haversine import haversine
from dbClass import Database


def normalizeCoord(lat: float, long: float) -> float:
    """
    If the coordinate is out of range, normalize it within
    the correct range
    """
    if not -90 <= lat <= 90:
        lat = ((lat + 90) % 180) - 90
    if not -180 <= long <= 180:
        long = ((long + 180) % 360) - 180

    return lat, long


def haversineCalc(coord: tuple, db: object) -> dict:
    """
    This function takes in a coordinate and a database object and
    finds the great arc length between the closest buoys and returns them
    in a dictionary.
    """
    gal = []
    count = 0
    lowLat = coord[0] * 0.95
    upperLat = coord[0] * 1.05
    lowLong = coord[1] * 1.05
    upperLong = coord[1] * 0.95

    while len(gal) < 5 and count < 10:
        # query Buoys entity and find all the buoys that have coordinates
        # within 5% of given coordinates
        count += 1
        lowLat *= 0.90
        upperLat *= 1.1
        lowLong *= 1.1
        upperLong *= 0.90

        lowLat, lowLong = normalizeCoord(lowLat, lowLong)
        upperLat, upperLong = normalizeCoord(upperLat, upperLong)

        query = "SELECT * FROM Buoys WHERE (latitude BETWEEN %s AND %s) \
            AND (longitude BETWEEN %s AND %s) ORDER BY latitude DESC;"
        params = [lowLat, upperLat, lowLong, upperLong]
        data = db.executeQuery(query, params)

        # find shortest great arc length using haversine formula
        for value in data:
            dist = haversine(coord, (value[2], value[3]))
            gal.append((dist, value[1], value[4], value[2], value[3]))

        # sorts by the distance and convert to a dictionary
        # for purposes of serializing to JSON
        gal.sort()
        sortedDict = {}
        for value in gal:
            sortedDict[value[0]] = [value[1], value[2], value[3], value[4]]
            if len(sortedDict) >= 20:
                break
    print(sortedDict)
    return sortedDict


if __name__ == "__main__":
    db = Database()
    coord = (34.113315, -121.124997)
    data = haversineCalc(coord, db)
    print(data)
