import json
import requests


def parseBuoy(stationID) -> dict:
    """
    This function opens a file containing raw buoy data and returns a
    dict containing various parameters and their respective numbers.

    buoyData: .txt file containing the raw buoy data
    """

    # open the file, split lines, and define variables
    data = buoyRequest(stationID)
    content = data[0].splitlines()
    dataDict = {'WDIR': None, 'WSPD': None, 'WVHT': None, 'DPD': None,
                'MWD': None, 'WTMP': None}
    firstRow = content[0].split()

    # iterate through the first row and map the buoy parameters to their
    # most recent readings
    for i in range(len(firstRow)):
        if firstRow[i] in dataDict:
            dataDict[firstRow[i]] = content[2].split()[i]

    return json.dumps(dataDict)


def buoyRequest(stationID) -> (tuple):
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
