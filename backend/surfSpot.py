import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv


class SurfSpot:
    def __init__(self, spotID: int):
        self._spotID = spotID

    @staticmethod
    def createSpot(userID: int, firstBuoyID: int = None, secondBuoyID: int
                   = None) -> bool:
        """
        Creates a new surf spot and adds it to the database. Returns True if
        successful and False otherwise.
        """
        result = None
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

            cursor.execute(query, params)
            result = True

        # error handling
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            result = False

        # close connections
        finally:
            cursor.close()
            cnx.close()
        return result
