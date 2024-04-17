--Get buoys between a specific latitude and longitude range
SELECT * FROM Buoys
WHERE 
    (latitude BETWEEN :lower AND :upper)
    AND
    (longitude BETWEEN :lower AND :upper)
ORDER BY latitude DESC;