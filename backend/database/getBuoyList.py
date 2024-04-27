# This script will scrape the NOAA website and fill the database table
# Buoys with buoy metadata

import requests
import json
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os


def getBuoyList() -> dict:
    """
    This function scrapes the station ID, coordinates, and station label
    from the NOAA website and returns a dictionary containing the coordinates
    as a key and a tuple of the station ID/label.
    """
    URL = "https://www.ndbc.noaa.gov/widgets/"
    request = requests.get(URL)
    soup = BeautifulSoup(request.text, 'html.parser')
    stations = soup.find('select', id='stationid').find_all('option')
    scrapeData = {}

    # split and clean the data
    for i in range(1, len(stations)):
        station = stations[i].text
        data = station.split('|')
        stationID = (data[0]).strip()
        label = (data[2]).strip()
        location = data[1].split(',')
        coordinates = (float(location[0]), float(location[1]))
        scrapeData[str(coordinates)] = (stationID, label)

    sortedData = dict(sorted(scrapeData.items()))
    return sortedData


def openBuoyList() -> dict:
    with open("buoyList", "r") as file:
        data = json.load(file)
    new = {}
    for key, value in data.items():
        convert = key.split(',')
        lat = float(convert[0].replace('(', ''))
        long = float(convert[1].replace(')', ''))
        new[(lat, long)] = value
    return new


if __name__ == "__main__":

    # connect to mysql
    try:
        load_dotenv()
        dbUser = os.getenv("dbUser")
        dbPassword = os.getenv("dbPassword")
        dbName = os.getenv("dbName")
        dbHost = os.getenv("dbHost")
        cnx = mysql.connector.connect(user=dbUser,
                                      password=dbPassword,
                                      host=dbHost,
                                      database=dbName)
        print("mysql Connection Successful")
        cursor = cnx.cursor()
        result = getBuoyList()

        # insert buoys
        for line, value in result.items():
            coord = line.split(',')
            lat = float(coord[0].replace('(', ''))
            long = float(coord[1].replace(')', ''))
            query = "INSERT INTO Buoys (stationID, latitude,\
            longitude, description) VALUES (%s, %s, %s, %s)"
            params = (value[0], lat, long, value[1])
            cursor.execute(query, params)

    # error handling
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    # close connections
    else:
        cnx.commit()
        cursor.close()
        cnx.close()
