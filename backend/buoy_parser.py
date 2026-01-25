import requests
from db_class import Database


def all_buoys(db: object) -> dict:
    """
    This function takes in a database object and returns all buoys
    in the database in a dictionary.
    """
    buoys = {}
    query = "SELECT * FROM Buoys"
    data = db.execute_query(query, [])
    if data:
        for buoy in data:
            buoys[buoy[0]] = {
                                "buoyID": buoy[0],
                                "stationID": buoy[1],
                                "latitude": buoy[2],
                                "longitude": buoy[3],
                                "description": buoy[4]
                }
    return buoys


def parseBuoy(stationID) -> dict | None:
    """
    This function opens a file containing raw buoy data and returns a
    dict containing various parameters and their respective numbers.

    buoyData: .txt file containing the raw buoy data
    """

    # open the file, split lines, and define variables
    data = buoy_request(stationID)
    dataDict = None
    if data[0]:
        content = data[0].splitlines()
        dataDict = {'WDIR': None, 'WSPD': None, 'WVHT': None, 'DPD': None,
                    'MWD': None, 'WTMP': None}
        firstRow = content[0].split()

        # iterate through the first row and map the buoy parameters to their
        # most recent readings
        for i in range(len(firstRow)):
            if firstRow[i] in dataDict:
                dataDict[firstRow[i]] = content[2].split()[i]

    return dataDict


def buoy_request(stationID) -> (tuple):
    """
    Function used to request the URL of the buoy and returns a
    tuple containing the request reponse and the status code.
    stationId: Int of the station requested.
    """

    # request the station
    url = f'https://www.ndbc.noaa.gov/data/realtime2/{stationID}.txt'
    response = requests.get(url)

    # check response and return text file or error depending on if it worked
    if response.status_code == 200:
        return (response.text, response.status_code)
    else:
        return (None, response.status_code)

