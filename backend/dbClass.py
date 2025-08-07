import mysql.connector
from mysql.connector import errorcode

DEFAULT_CONN_POOL_SIZE = 3


class Database:
    def __init__(
                self, user: str, password: str, db_name: str, db_host: str,
                pool_size: int, logger: object, testing: bool = False
                ):
        self._connected = False
        self._cnxpool = None
        self.logger = logger
        self.testing = testing
        self.__createPool(user, password, db_name, db_host, pool_size)

    def status(self) -> bool:
        """
        Returns true if db is usable and false otherwise
        """
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
            self.logger.info("pool successfully created")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.logger.warning("Something is wrong with your \
                                    user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.logger.warning("Database does not exist")
            else:
                self.logger.warning(err)

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
            self.logger.info("connection successful")
            cursor = cnx.cursor()
            self.logger.info("Parameters:  %s", params)
            cursor.execute(query, params)

            # what to do with query depending on questions
            if query.startswith(("INSERT", "UPDATE", "DELETE")) and\
                    not self.testing:
                cnx.commit()
                data = ["success", cursor.lastrowid]
                self.logger.info("Transaction committed")
            elif fetch == "all":
                data = cursor.fetchall()
            else:
                data = cursor.fetchone()

        # error handling
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.logger.warning("Something is wrong with your user name or\
                                    password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.logger.warning("Database does not exist")
            else:
                self.logger.warning(err)

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
    logger: object,
    testing: bool = False,
    pool_size: int = DEFAULT_CONN_POOL_SIZE
) -> Database | None:
    """
    Factory method for creating Database object
    """
    if testing:
        db = Database(user, password, db_name, db_host,
                      pool_size, logger, testing)
    else:
        db = Database(user, password, db_name,
                      db_host, pool_size, logger)
    return db if db.status() else None
