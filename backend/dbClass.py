import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv


class Database:
    def __init__(self):
        self._connected = False
        self._cnxpool = None
        self.createPool()

    def status(self):
        return self._connected

    def createPool(self) -> None:
        load_dotenv()
        dbUser = os.getenv("dbUser")
        dbPassword = os.getenv("dbPassword")
        dbName = os.getenv("dbName")
        dbHost = os.getenv("dbHost")

        db_config = {
            "user": dbUser,
            "password": dbPassword,
            "database": dbName,
            "host": dbHost
        }

        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="pool",
                pool_size=2,
                **db_config
                )
            self._connected = True
            self._cnxpool = cnxpool
            print("pool successfully created")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def executeQuery(self, query: str, params: list) -> list:
        """
        Takes in a query and its parameters and returns the resulting list
        or an empty list if the query was unsuccessful
        """
        data = []
        try:
            # get connection and execute query
            cnx = self._cnxpool.get_connection()
            print("connection successful")
            cursor = cnx.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall()
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

        return data
