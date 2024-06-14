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

