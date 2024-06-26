from haversine import haversine
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os


def haversineCalc(coord: tuple) -> dict:
    load_dotenv()
    dbUser = os.getenv("dbUser")
    dbPassword = os.getenv("dbPassword")
    dbName = os.getenv("dbName")
    dbHost = os.getenv("dbHost")
    try:
        # connect to database
        cnx = mysql.connector.connect(user=dbUser,
                                      password=dbPassword,
                                      host=dbHost,
                                      database=dbName)
        # print("mysql Connection Successful")
        cursor = cnx.cursor()
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
            cursor.execute(query, (lowLat, upperLat, lowLong, upperLong))
            data = cursor.fetchall()

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

    # error handling
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    # close connections
    finally:
        cursor.close()
        cnx.close()

    return False


if __name__ == "__main__":
    coord = (37.7012073647, -122.5085449219)
    data = haversineCalc(coord)
    print(data)
