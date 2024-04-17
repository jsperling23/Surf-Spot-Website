DROP TABLE IF EXISTS Buoys, Users, SurfSpots;

CREATE TABLE Buoys(
    buoyID int AUTO_INCREMENT NOT NULL UNIQUE,
    stationID VARCHAR(10) NOT NULL UNIQUE,
    latitude DECIMAL(10,3) NOT NULL,
    longitude DECIMAL(10,3) NOT NULL,
    description VARCHAR(255),
    PRIMARY KEY (buoyID)
);

CREATE INDEX lat_long ON Buoys(latitude, longitude);

CREATE TABLE Users(
    userID int AUTO_INCREMENT NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (userID)
);

CREATE TABLE SurfSpots(
    spotID int AUTO_INCREMENT NOT NULL UNIQUE,
    firstBuoyID int NULL,
    secondBuoyID int NULL,
    PRIMARY KEY (spotID),
    FOREIGN KEY (firstBuoyID) REFERENCES Buoys(buoyID) ON DELETE SET NULL,
    FOREIGN KEY (secondBuoyID) REFERENCES Buoys(buoyID) ON DELETE SET NULL
);