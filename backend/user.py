import bcrypt
from flask import current_app

class User:
    def __init__(self, username: str, password: str, db: object) -> None:
        self._username = username
        self._userID = None
        self._password = password
        self._isAuthenticated = False
        self.setUser(db)

    def setUser(self, db: object) -> None:
        # find the user
        query = "SELECT * FROM Users WHERE username = %s"
        user = db.executeQuery(query, [self._username], "one")

        # if the user exists, check if the username and password match
        if user:
            if self._username == user[1]:
                self._username = user[1]
                self._userID = user[0]

    def verifyPassword(self, passwordToCheck: str) -> bool:
        """
        Verfies if the password from the form matches what is in the
        database
        """
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
    def get(username: str, db: object):
        # find the user
        query = "SELECT * FROM Users WHERE username = %s"
        user = db.executeQuery(query, [username], "one")
        current_app.logger.info(user)
        if user:
            return User(user[1], user[2], db)
        else:
            return None

    @staticmethod
    def checkIfExists(username: str, db: object) -> bool:
        """
        Check if a user exists.
        """
        query = "SELECT * FROM Users WHERE username = %s"
        user = db.executeQuery(query, [username])
        # If user is found, return True, else False
        if user:
            return True
        else:
            return False

    @staticmethod
    def createUser(username: str, password: str, db: object) -> tuple:
        """
        This function takes in a username and password and database object.
        Then an attempt at creating a new user is completed.

        Parameters:
                username(str)
                password(str)
                db(object)

        Returns Tuples:
                (True, 0): Account creation is successful
                (False, 1): Username already exists
                (False, 2): Error occurred when connection to database
        """
        if not db:
            return (False, 2)
        if not User.checkIfExists(username, db):
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
            current_app.logger.info(type(hashed))
            params = [username, hashed]
            query = "INSERT INTO Users(username, password) VALUES(%s, %s);"
            db.executeQuery(query, params)
            return (True, 0)
        else:
            return (False, 1)


if __name__ == "__main__":
    query = "INSERT INTO Users(username, password) VALUES(%s, %s);"
    print(query.startswith("INSERT"))
