
CREATE DATABASE EgyptTrafficDB;
GO

USE EgyptTrafficDB;
GO


CREATE TABLE Locations (
    LocationID INT IDENTITY(1,1) PRIMARY KEY,
    LocationName VARCHAR(150) NOT NULL,    
    City VARCHAR(50) NOT NULL,              
    Latitude DECIMAL(9, 6) NOT NULL,
    Longitude DECIMAL(9, 6) NOT NULL,
    CreatedDate DATETIME DEFAULT GETDATE()
);
GO


CREATE TABLE Traffic_Logs (
    LogID BIGINT IDENTITY(1,1) PRIMARY KEY,
    LocationID INT FOREIGN KEY REFERENCES Locations(LocationID),
    CurrentSpeed INT NOT NULL,              
    NormalSpeed INT NOT NULL,              
    TrafficStatus VARCHAR(50),             
    RecordedAt DATETIME DEFAULT GETDATE()  
);
GO


CREATE INDEX IX_TrafficLogs_RecordedAt ON Traffic_Logs(RecordedAt);





CREATE TABLE WeatherData (
    Weather_ID INT IDENTITY(1,1) PRIMARY KEY,
    City_Name NVARCHAR(50) NOT NULL,
    Weather_DateHour DATETIME NOT NULL, 
    Temperature_C FLOAT,
    Humidity_Pct INT,
    Wind_Speed_ms FLOAT,
    Weather_Condition NVARCHAR(100),
    Record_Insertion_Time DATETIME DEFAULT GETDATE()            
);




SELECT * FROM Locations;
SELECT * FROM Traffic_Logs;
SELECT * FROM WeatherData;

