-- Members Table
CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    DateOfBirth DATE,
    Gender CHAR(1),
    FitnessGoal VARCHAR(255)
);

-- Trainers Table
CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    Specialization VARCHAR(100),
    AvailableTimes JSON  -- Storing availability as JSON for flexibility
);

-- Administrative Staff Table
CREATE TABLE AdminStaff (
    StaffID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(100) UNIQUE,
    Role VARCHAR(50)
);

-- Rooms Table
CREATE TABLE Rooms (
    RoomID SERIAL PRIMARY KEY,
    RoomName VARCHAR(50),
    Capacity INT
);

-- Equipment Table
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
    EquipmentName VARCHAR(50),
    MaintenanceSchedule DATE,
    RoomID INT REFERENCES Rooms(RoomID)
);

-- Classes Table
CREATE TABLE Classes (
    ClassID SERIAL PRIMARY KEY,
    ClassName VARCHAR(50),
    RoomID INT REFERENCES Rooms(RoomID),
    TrainerID INT REFERENCES Trainers(TrainerID),
    Schedule TIMESTAMP
);

-- Personal Training Sessions Table
CREATE TABLE PersonalTrainingSessions (
    SessionID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    TrainerID INT REFERENCES Trainers(TrainerID),
    RoomID INT REFERENCES Rooms(RoomID),
    ScheduledTime TIMESTAMP
);

-- Member Classes Many-to-Many Relationship Table
CREATE TABLE MemberClasses (
    MemberID INT REFERENCES Members(MemberID),
    ClassID INT REFERENCES Classes(ClassID),
    PRIMARY KEY (MemberID, ClassID)
);

-- Activity Logs Table
CREATE TABLE ActivityLogs (
    LogID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    ActivityDate DATE,
    ActivityType VARCHAR(100),
    Duration INT,  -- Duration in minutes
    CaloriesBurnt INT
);

-- Achievements Table
CREATE TABLE Achievements (
    AchievementID SERIAL PRIMARY KEY,
    AchievementName VARCHAR(100),
    Description TEXT
);

-- Member Achievements Many-to-Many Relationship Table
CREATE TABLE MemberAchievements (
    MemberID INT REFERENCES Members(MemberID),
    AchievementID INT REFERENCES Achievements(AchievementID),
    DateEarned DATE,
    PRIMARY KEY (MemberID, AchievementID)
);

-- Health Stats Table
CREATE TABLE HealthStats (
    StatID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    RecordedDate DATE,
    Weight DECIMAL(5, 2),
    HeartRate INT,
    OtherMetrics JSON  -- Flexible column for additional metrics
);
