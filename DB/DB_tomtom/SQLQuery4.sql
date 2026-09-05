-- 1. „”Õ «·ÃœÊ· «·ﬁœÌ„ ⁄‘«‰ ‰‰Ÿ› «·œ‰Ì«
IF OBJECT_ID('dbo.Historical_Incidents_ADAS', 'U') IS NOT NULL 
  DROP TABLE dbo.Historical_Incidents_ADAS;
GO

-- 2. ≈‰‘«¡ «·ÃœÊ· «·ÃœÌœ »«·ÂÌﬂ· «·‘«„·
CREATE TABLE dbo.Historical_Incidents_ADAS (
    Incident_ID VARCHAR(50) PRIMARY KEY,
    Location_Name NVARCHAR(255),
    
    -- »Ì«‰«  «·Êﬁ 
    Incident_Date DATE,
    Incident_Time TIME,
    
    --  ›«’Ì· «·Õ«œÀ…
    Incident_Type NVARCHAR(100),
    Severity NVARCHAR(50),
    Cause NVARCHAR(255),
    Road_Delay_Minutes INT,
    
    -- Õ«·… «·”«∆ﬁ (ADAS)
    ADAS_Driver_Status NVARCHAR(100),
    
    -- «·»Ì∆… «·„ÕÌÿ… («·ÿﬁ” Êﬁ  «·Õ«œÀ…)
    Temperature_C FLOAT,
    Humidity_Pct INT,
    Wind_Speed_ms FLOAT,
    Weather_Condition NVARCHAR(100),
    
    -- «·»Ì∆… «·„ÕÌÿ… («·„—Ê— Êﬁ  «·Õ«œÀ…)
    CurrentSpeed INT,
    TrafficStatus NVARCHAR(50)
);
GO

-- ·· √ﬂœ ≈‰ «·ÃœÊ· « ⁄„· ’Õ
SELECT * FROM dbo.Historical_Incidents_ADAS;