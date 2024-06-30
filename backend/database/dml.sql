--Get buoys between a specific latitude and longitude range
SELECT * FROM Buoys
WHERE 
    (latitude BETWEEN :lower AND :upper)
    AND
    (longitude BETWEEN :lower AND :upper)
ORDER BY latitude DESC;

--Create a new surf spot no buoys
INSERT INTO SurfSpots (userID) VALUES (:userID)

--Create a new surf spot one buoys
INSERT INTO SurfSpots (userID, firstBuoyID) VALUES (:userID, :firstBuoyID)

--Create a new surf spot two buoys
INSERT INTO SurfSpots (userID, firstBuoyID, secondBuoyID) VALUES (:userID, :firstBuoyID, :secondBuoyID)

--Get surf spot and station ID info

SELECT SurfSpots.spotID, SurfSpots.userID, SurfSpots.name, SurfSpots.latitude, SurfSpots.longitude, buoy1.stationID AS buoy1, buoy2.stationID AS buoy2 FROM SurfSpotsINNER JOIN Buoys AS buoy1 ON SurfSpots.firstBuoyID = buoy1.buoyIDINNER JOIN Buoys AS buoy2 ON SurfSpots.secondBuoyID = buoy2.buoyID WHERE SurfSpots.spotID = %s