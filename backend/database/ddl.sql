DROP TABLE IF EXISTS Buoys, Users, SurfSpots, IdealConditions;

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
    userID int NULL,
    firstBuoyID int NULL,
    secondBuoyID int NULL,
    PRIMARY KEY (spotID),
    FOREIGN KEY (firstBuoyID) REFERENCES Buoys(buoyID) ON DELETE SET NULL,
    FOREIGN KEY (secondBuoyID) REFERENCES Buoys(buoyID) ON DELETE SET NULL,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE SET NULL
);

CREATE TABLE IdealConditions(
    conditionID int AUTO_INCREMENT NOT NULL UNIQUE,
    spotID INT NOT NULL,
    windUpper int NOT NULL,
    windLower int NOT NULL,
    windDirectionUpper int NOT NULL,
    windDirectionLower int NOT NULL,
    swellHeightUpper float(4, 2) NOT NULL,
    swellHeightLower float(4, 2) NOT NULL,
    swellPeriodUpper int NOT NULL,
    swellPeriodLower int NOT NULL,
    tideUpper float(3, 1) NOT NULL,
    tideLower float(3, 1) NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (spotID) REFERENCES SurfSpots ON DELETE CASCADE
);

CREATE TABLE SavedSessions(
    sessionID int AUTO_INCREMENT NOT NULL UNIQUE,
    spotID INT NOT NULL,
    windSpeed int NOT NULL,
    windDirection int NOT NULL,
    swellHeight float(4, 2) NOT NULL,
    swellPeriod int NOT NULL,
    tide float(3, 1) NOT NULL,
    swellActivity VARCHAR(15)
    tideDirection VARCHAR(15)
    description VARCHAR(255),
    FOREIGN KEY (spotID) REFERENCES SurfSpots ON DELETE CASCADE
);
