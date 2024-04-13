-- Insert Members
INSERT INTO Members (FirstName, LastName, Email, DateOfBirth, Gender, FitnessGoal) VALUES
('John', 'Doe', 'johndoe@example.com', '1985-07-10', 'M', 'Increase Activity Level'),
('Jane', 'Smith', 'janesmith@example.com', '1992-11-30', 'F', 'Maintain Health'),
('Alice', 'Johnson', 'alicejohnson@example.com', '1988-05-16', 'F', 'Improve Fitness');

-- Insert Trainers
INSERT INTO Trainers (FirstName, LastName, Email, Specialization, AvailableTimes) VALUES
('Bob', 'Builder', 'bobbuilder@example.com', 'Strength Training', '{"Monday": ["08:00-12:00"], "Wednesday": ["14:00-18:00"]}'),
('Nancy', 'Rogers', 'nancyrogers@example.com', 'Yoga Instructor', '{"Tuesday": ["10:00-14:00"], "Thursday": ["16:00-20:00"]}');

-- Insert Admin Staff
INSERT INTO AdminStaff (FirstName, LastName, Email, Role) VALUES
('Bruce', 'Wayne', 'brucewayne@example.com', 'Manager'),
('Clark', 'Kent', 'clarkkent@example.com', 'Receptionist');

-- Insert Rooms
INSERT INTO Rooms (RoomName, Capacity) VALUES
('Aerobics Room', 20),
('Weight Room', 15);

-- Insert Equipment
INSERT INTO Equipment (EquipmentName, MaintenanceSchedule, RoomID) VALUES
('Treadmill', '2024-04-15', 2),
('Dumbbells', '2024-05-10', 2);

-- Insert Classes
INSERT INTO Classes (ClassName, RoomID, TrainerID, Schedule) VALUES
('Morning Yoga', 1, 2, '2024-06-01 08:00:00'),
('Weight Training', 2, 1, '2024-06-01 09:00:00');

-- Insert Personal Training Sessions
INSERT INTO PersonalTrainingSessions (MemberID, TrainerID, RoomID, ScheduledTime) VALUES
(1, 1, 2, '2024-06-03 10:00:00'),
(2, 2, 1, '2024-06-04 11:00:00');

-- Insert Member Classes (Many-to-Many Relationship)
INSERT INTO MemberClasses (MemberID, ClassID) VALUES
(1, 1),
(2, 2);

-- Insert Activity Logs
INSERT INTO ActivityLogs (MemberID, ActivityDate, ActivityType, Duration, CaloriesBurnt) VALUES
(1, '2024-06-02', 'Running', 30, 300),
(2, '2024-06-02', 'Cycling', 45, 450);

-- Insert Achievements
INSERT INTO Achievements (AchievementName, Description) VALUES
('Marathon Finisher', 'Completed a full marathon'),
('Yoga Master', 'Participated in 100 yoga sessions');

-- Insert Member Achievements
INSERT INTO MemberAchievements (MemberID, AchievementID, DateEarned) VALUES
(1, 1, '2024-06-01'),
(2, 2, '2024-06-01');

-- Insert Health Stats
INSERT INTO HealthStats (MemberID, RecordedDate, Weight, HeartRate, OtherMetrics) VALUES
(1, '2024-06-01', 85.0, 72, '{"blood_pressure": "120/80"}'),
(2, '2024-06-01', 65.0, 68, '{"blood_pressure": "110/70"}');
