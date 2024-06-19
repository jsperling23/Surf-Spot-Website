from haversine import haversine
from dbClass import Database


def haversineCalc(coord: tuple, db) -> dict:
    gal = []
    while len(gal) < 5:
        # query Buoys entity and find all the buoys that have coordinates
        # within 5% of given coordinates
        lowLat = coord[0] * 0.95
        upperLat = coord[0] * 1.05
        lowLong = coord[1] * 1.05
        upperLong = coord[1] * 0.95
        query = "SELECT * FROM Buoys WHERE (latitude BETWEEN %s AND %s) \
            AND (longitude BETWEEN %s AND %s) ORDER BY latitude DESC;"
        params = [lowLat, upperLat, lowLong, upperLong]
        data = db.executeQuery(query, params)

        # find shortest great arc length using haversine formula
        for value in data:
            dist = haversine(coord, (value[2], value[3]))
            gal.append((dist, value[1], value[4]))

        # sorts by the distance and convert to a dictionary
        # for purposes of serializing to JSON
        gal.sort()
        sortedDict = {}
        for value in gal:
            sortedDict[value[0]] = [value[1], value[2]]
    return sortedDict


if __name__ == "__main__":
    db = Database()
    coord = (37.7012073647, -122.5085449219)
    data = haversineCalc(coord, db)
    print(data)
