USE EgyptTrafficDB;
GO

CREATE TABLE Historical_Incidents_ADAS (
    Incident_ID VARCHAR(50) PRIMARY KEY,
    Location_Name NVARCHAR(255),
    Incident_Date DATE,
    Incident_Time TIME,
    Incident_Type NVARCHAR(100),
    Severity NVARCHAR(50),
    Cause NVARCHAR(100),
    ADAS_Driver_Status NVARCHAR(100),
    Road_Delay_Minutes INT
);


select * from Historical_Incidents_ADAS