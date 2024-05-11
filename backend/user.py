import mysql.connector
from mysql.connector import errorcode
import bcrypt
from dotenv import load_dotenv
import os


class User:
    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._userID = None
        self._password = password
        self._isAuthenticated = False
        self.setUser()

    def setUser(self) -> None:
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
            print("mysql Connection Successful")
            cursor = cnx.cursor()

            # find the user
            query = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(query, [self._username])
            user = cursor.fetchone()

            # if the user exists, check if the username and password match
            if user:
                if self._username == user[1]:
                    self._username = user[1]
                    self._userID = user[0]

        # error handling
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        # close connection and return
        cursor.close()
        cnx.close()
        return

    def verifyPassword(self, passwordToCheck):
        check = bcrypt.checkpw(passwordToCheck.encode('utf-8'),
                               self._password.encode('utf-8'))
        if check:
            self._isAuthenticated = True
        return check

    def getPrimaryKey(self) -> str:
        return self._userID

    # flask-login methods
    def is_authenticated(self) -> str:
        return self._isAuthenticated

    def is_active(self) -> str:
        return True

    def is_anonymous(self) -> str:
        return False

    def get_id(self) -> str:
        return self._username

    @staticmethod
    def get(username: str):
        load_dotenv()
        dbUser = os.getenv("dbUser")
        dbPassword = os.getenv("dbPassword")
        dbName = os.getenv("dbName")
        dbHost = os.getenv("dbHost")
        # check if in database
        try:
            # connect to database
            cnx = mysql.connector.connect(user=dbUser,
                                          password=dbPassword,
                                          host=dbHost,
                                          database=dbName)
            print("mysql Connection Successful")
            cursor = cnx.cursor()

            # find the user
            query = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(query, [username])
            user = cursor.fetchone()
            if user:
                return User(user[1], user[2])
        # error handling
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        # close connection and return
        cursor.close()
        cnx.close()
        return None

    @staticmethod
    def checkIfExists(username: str) -> bool:
        try:
            load_dotenv()
            dbUser = os.getenv("dbUser")
            dbPassword = os.getenv("dbPassword")
            dbName = os.getenv("dbName")
            dbHost = os.getenv("dbHost")
            # connect to database
            cnx = mysql.connector.connect(user=dbUser,
                                          password=dbPassword,
                                          host=dbHost,
                                          database=dbName)
            print("mysql Connection Successful")
            cursor = cnx.cursor()
            query = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(query, [username])
            user = cursor.fetchone()
            cursor.close()
            cnx.close()

            # If user is found, return True, else False
            return user is not None

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return None

    @staticmethod
    def createUser(username: str, password: str) -> tuple:
        """
        This function takes in a username and password. It uses a try/except
        block to connect to the database and assuming the connection is
        successful, then an attempt at creating a new user is completed.

        Parameters:
                username(str)
                password(str)

        Returns Tuples:
                (True, 0): Account creation is successful
                (False, 1): Username already exists
                (False, 2): Error occurred when connection to database
        """
        try:
            load_dotenv()
            dbUser = os.getenv("dbUser")
            dbPassword = os.getenv("dbPassword")
            dbName = os.getenv("dbName")
            dbHost = os.getenv("dbHost")
            # connect to database
            cnx = mysql.connector.connect(user=dbUser,
                                          password=dbPassword,
                                          host=dbHost,
                                          database=dbName)
            print("mysql Connection Successful")
            if not User.checkIfExists(username):
                cursor = cnx.cursor()
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
                query = "INSERT INTO Users(username, password) VALUES(%s, %s)"
                cursor.execute(query, [username, hashed])

                # close connection and return if account creation successful
                cnx.commit()
                cursor.close()
                cnx.close()
                return (True, 0)
            else:
                return (False, 1)

        # error handling
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            return (False, 2)


if __name__ == "__main__":
    user = User.get("test")
    print(user.verifyPassword(), user.is_authenticated())
