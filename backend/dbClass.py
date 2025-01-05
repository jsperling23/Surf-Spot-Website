import mysql.connector

from mysql.connector import errorcode

DEFAULT_CONN_POOL_SIZE = 3


class Database:
    def __init__(
                self, user: str, password: str, db_name: str, db_host: str,
                pool_size: int
                ):
        self._connected = False
        self._cnxpool = None
        self.__createPool(user, password, db_name, db_host, pool_size)

    def status(self):
        return self._connected and self._cnxpool is not None

    def __createPool(
                self, user: str, password: str, db_name: str, db_host: str,
                pool_size: int
    ) -> None:
        db_config = {
            "user": user,
            "password": password,
            "database": db_name,
            "host": db_host,
            "pool_reset_session": True
        }

        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="pool",
                pool_size=pool_size,
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

    def executeQuery(self, query: str, params: list, fetch: str = "all") -> \
            list:
        """
        Takes in a query and its parameters and returns the resulting list
        or an empty list if the query was unsuccessful. The fetch string is
        default to all but if you want to use the fetchone method, then
        set fetch to "one".
        """
        data = []
        cnx = None
        cursor = None
        try:
            # get connection and execute query
            cnx = self._cnxpool.get_connection()
            print("connection successful")
            cursor = cnx.cursor()
            print("Parameters:  ", params)
            cursor.execute(query, params)

            # what to do with query depending on questions
            if query.startswith(("INSERT", "UPDATE", "DELETE")):
                cnx.commit()
                data = ["success", cursor.lastrowid]
                print("Transaction committed")
            elif fetch == "all":
                data = cursor.fetchall()
            else:
                data = cursor.fetchone()

        # error handling
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        # close any connections
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

        return data


def factory(
    user: str,
    password: str,
    db_name: str,
    db_host: str,
    pool_size: int = DEFAULT_CONN_POOL_SIZE,
) -> Database | None:
    """
    Factory method for creating Database object
    """
    db = Database(user, password, db_name, db_host, pool_size)
    return db if db.status() else None
