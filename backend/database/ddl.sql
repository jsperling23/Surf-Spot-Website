SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS Buoys, Users, SurfSpots, IdealConditions, SavedSessions;

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
    userID int NOT NULL,
    name VARCHAR(50) NOT NULL,
    latitude DECIMAL(10,3) NOT NULL,
    longitude DECIMAL(10,3) NOT NULL,
    firstBuoyID int NULL,
    secondBuoyID int NULL,
    PRIMARY KEY (spotID),
    FOREIGN KEY (firstBuoyID) REFERENCES Buoys(buoyID) ON DELETE SET NULL,
    FOREIGN KEY (secondBuoyID) REFERENCES Buoys(buoyID) ON DELETE SET NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE IdealConditions(
    conditionID int AUTO_INCREMENT NOT NULL UNIQUE,
    spotID INT NOT NULL,
    windDirection VARCHAR(10) NOT NULL,
    swellDirection VARCHAR(10) NOT NULL,
    waveSize VARCHAR(30) NOT NULL,
    swellPeriod VARCHAR(10) NOT NULL,
    tideUpper DECIMAL(3, 1) NOT NULL,
    tideLower DECIMAL(3, 1) NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (spotID) REFERENCES SurfSpots(spotID) ON DELETE CASCADE
);

CREATE TABLE SavedSessions(
    sessionID INT AUTO_INCREMENT NOT NULL UNIQUE,
    spotID INT NOT NULL,
    windSpeed INT NOT NULL,
    windDirection INT NOT NULL,
    swellHeight DECIMAL(4, 2) NOT NULL,
    swellPeriod INT NOT NULL,
    swellDirection INT NOT NULL,
    tide DECIMAL(3, 1) NOT NULL,
    swellActivity VARCHAR(15),
    tideDirection VARCHAR(15),
    description VARCHAR(255),
    FOREIGN KEY (spotID) REFERENCES SurfSpots(spotID) ON DELETE CASCADE
);
