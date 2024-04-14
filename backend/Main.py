import psycopg2
import json
from datetime import datetime
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from flask import jsonify


def connect_db():
    # Connecting to the datebase
    try:
        conn = psycopg2.connect(
            dbname='FinalProject',
            user='postgres',
            password='dollar25A',
            host='localhost'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


def register_member(first_name, last_name, email, date_of_birth, gender, fitness_goal):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Members (FirstName, LastName, Email, DateOfBirth, Gender, FitnessGoal)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """, (first_name, last_name, email, date_of_birth, gender, fitness_goal))
                print("Member registered successfully.")
        except psycopg2.Error as e:
            print(f"Failed to register member: {e}")
        finally:
            conn.close()


def update_member_profile(member_id, first_name, last_name, email, fitness_goal):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Members
                    SET FirstName = %s, LastName = %s, Email = %s, FitnessGoal = %s
                    WHERE MemberID = %s;
                    """, (first_name, last_name, email, fitness_goal, member_id))
                print("Member profile updated successfully.")
        except psycopg2.Error as e:
            print(f"Failed to update member profile: {e}")
        finally:
            conn.close()


def display_member_dashboard(member_id):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                # Fetch exercise routines
                cursor.execute("""
                    SELECT ActivityDate, ActivityType, Duration, CaloriesBurnt FROM ActivityLogs WHERE MemberID = %s;
                    """, (member_id,))
                activities = cursor.fetchall()
                print(f"Exercise Routines for Member ID {member_id}:")
                print(f"{'Date':<12} {'Type':<20} {'Duration (min)':<15} {'Calories Burnt':<15}")
                for activity in activities:
                    date, activity_type, duration, calories_burnt = activity
                    print(f"{date:%Y-%m-%d:<12} {activity_type:<20} {duration:<15} {calories_burnt:<15}")

                # Fetch achievements
                cursor.execute("""
                    SELECT Achievements.AchievementName, MemberAchievements.DateEarned
                    FROM Achievements
                    JOIN MemberAchievements ON Achievements.AchievementID = MemberAchievements.AchievementID
                    WHERE MemberAchievements.MemberID = %s;
                    """, (member_id,))
                achievements = cursor.fetchall()
                print("\nAchievements:")
                print(f"{'Achievement Name':<30} {'Date Earned':<15}")
                for achievement in achievements:
                    name, date_earned = achievement
                    print(f"{name:<30} {date_earned:%Y-%m-%d:<15}")

                # Fetch health statistics
                cursor.execute("""
                    SELECT RecordedDate, Weight, HeartRate, OtherMetrics FROM HealthStats WHERE MemberID = %s;
                    """, (member_id,))
                health_stats = cursor.fetchall()
                print("\nHealth Statistics:")
                print(f"{'Recorded Date':<15} {'Weight (kg)':<12} {'Heart Rate':<12} {'Other Metrics':<20}")
                for stat in health_stats:
                    date, weight, heart_rate, other_metrics = stat
                    other_metrics_display = ', '.join(
                        [f"{key}: {value}" for key, value in other_metrics.items()]) if other_metrics else ''
                    print(f"{date:%Y-%m-%d:<15} {weight:<12.2f} {heart_rate:<12} {other_metrics_display:<20}")

        except psycopg2.Error as e:
            print(f"Failed to retrieve dashboard data: {e}")
        finally:
            conn.close()


def book_personal_training_session(member_id, trainer_id, room_id, scheduled_time):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO PersonalTrainingSessions (MemberID, TrainerID, RoomID, ScheduledTime)
                    VALUES (%s, %s, %s, %s);
                    """, (member_id, trainer_id, room_id, scheduled_time))
                print("Personal training session booked successfully.")
        except psycopg2.Error as e:
            print(f"Failed to book training session: {e}")
        finally:
            conn.close()


def register_for_class(member_id, class_id):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO MemberClasses (MemberID, ClassID)
                    VALUES (%s, %s);
                    """, (member_id, class_id))
                print("Registered for class successfully.")
        except psycopg2.Error as e:
            print(f"Failed to register for class: {e}")
        finally:
            conn.close()


def update_trainer_availability(trainer_id, available_times_json):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Trainers
                    SET AvailableTimes = %s
                    WHERE TrainerID = %s;
                    """, (available_times_json, trainer_id))
                print("Trainer availability updated successfully.")
        except psycopg2.Error as e:
            print(f"Failed to update trainer availability: {e}")
        finally:
            conn.close()


def view_member_profile_by_name(search_name):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                # Using = for exact matching
                cursor.execute("""
                    SELECT MemberID, FirstName, LastName, Email FROM Members 
                    WHERE FirstName = %s OR LastName = %s;
                    """, (search_name, search_name))
                members = cursor.fetchall()
                for member in members:
                    print(member)
        except psycopg2.Error as e:
            print(f"Error retrieving member profiles: {e}")
        finally:
            conn.close()
    else:
        print("Failed to connect to the database.")


def check_trainer_availability(trainer_id, requested_day, requested_time):
    conn = connect_db()
    if conn is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT AvailableTimes FROM Trainers WHERE TrainerID = %s;", (trainer_id,))
            result = cursor.fetchone()
            if not result:
                return jsonify({'error': 'No availability data found for the trainer'}), 404

            available_times = result[0]  # This should be a JSON or dictionary
            if requested_day not in available_times:
                return jsonify({'available': False, 'message': f'Trainer {trainer_id} does not work on {requested_day}.'}), 200

            for interval in available_times[requested_day]:
                start_time, end_time = interval.split('-')
                requested_dt = datetime.strptime(requested_time, "%H:%M")
                start_dt = datetime.strptime(start_time, "%H:%M")
                end_dt = datetime.strptime(end_time, "%H:%M")

                if start_dt <= requested_dt < end_dt:
                    return jsonify({'available': True, 'message': f'Trainer {trainer_id} is available from {start_time} to {end_time} on {requested_day}.'}), 200

            return jsonify({'available': False, 'message': f'Trainer {trainer_id} is not available at {requested_time} on {requested_day}.'}), 200

    except psycopg2.Error as e:
        return jsonify({'error': f'Error checking trainer availability: {str(e)}'}), 400
    finally:
        conn.close()

def process_payment(member_id, amount_due):
    # This function would interface with a payment processing service in a real application
    print(f"Processed payment for Member ID {member_id}: ${amount_due} has been successfully charged.")


def update_room_booking(room_id, new_capacity):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Rooms
                    SET Capacity = %s
                    WHERE RoomID = %s;
                    """, (new_capacity, room_id))
                print("Room capacity updated successfully.")
        except psycopg2.Error as e:
            print(f"Failed to update room capacity: {e}")
        finally:
            conn.close()


def update_equipment_maintenance(equipment_id, new_maintenance_date):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Equipment
                    SET MaintenanceSchedule = %s
                    WHERE EquipmentID = %s;
                    """, (new_maintenance_date, equipment_id))
                print("Equipment maintenance schedule updated successfully.")
        except psycopg2.Error as e:
            print(f"Failed to update equipment maintenance: {e}")
        finally:
            conn.close()


def update_class_schedule(class_id, new_schedule):
    conn = connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Classes
                    SET Schedule = %s
                    WHERE ClassID = %s;
                    """, (new_schedule, class_id))
                print("Class schedule updated successfully.")
        except psycopg2.Error as e:
            print(f"Failed to update class schedule: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    # Test connection to the database
    if connect_db() is not None:
        print("Connection to the database was successful.")

    # Test user registration
    register_member(
        first_name="Emily",
        last_name="Johnson",
        email="emily.johnson@example.com",
        date_of_birth="1992-03-15",
        gender="F",
        fitness_goal="Improve Fitness"
    )

    # Test updating member profile
    update_member_profile(
        member_id=1,  # 1 MUST BE a valid MemberID
        first_name="Emily",
        last_name="Johnson",
        email="emilyj@example.com",  # Simulating an email change
        fitness_goal="Maintain Health"
    )

    # # Test booking a personal training session
    book_personal_training_session(
        member_id=1,
        trainer_id=1,  # 1 is a valid TrainerID
        room_id=1,  # 1 is a valid RoomID
        scheduled_time="2024-06-15 10:00:00"
    )

    # # Test registering for a class
    register_for_class(
        member_id=2,
        class_id=1  # Assuming 1 is a valid ClassID
    )

    # # Test updating trainer availability
    update_trainer_availability(
        trainer_id=1,
        available_times_json='{"Tuesday": ["08:00-12:00"], "Wednesday": ["14:00-18:00"]}'
    )

    # # Test administrative function: update room booking
    update_room_booking(
        room_id=1,
        new_capacity=25  # Updating room capacity
    )

    # # Test updating equipment maintenance schedule
    update_equipment_maintenance(
        equipment_id=1,  # Assuming 1 is a valid EquipmentID
        new_maintenance_date="2024-12-01"
    )

    # # Test updating a class schedule
    update_class_schedule(
        class_id=1,  # Assuming 1 is a valid ClassID
        new_schedule="2024-06-20 08:00:00"
    )

    # # Display the member dashboard (assuming MemberID 1 has data)
    display_member_dashboard(
        member_id=1
    )

    trainer_id = 1
    requested_day = 'Tuesday'  # Specify the day of the week
    requested_time = '08:00'  # Specify the exact time to check for availability
    check_trainer_availability(trainer_id, requested_day, requested_time)
    # Test viewing member profiles by name
    search_name = "Emily"  # Example name
    print("\nTesting View Member Profile by Name:")
    view_member_profile_by_name(search_name)

    # Test mock billing and payment processing
    member_id = 1  # Example member ID
    amount_due = 100.00  # Example amount
    print("\nTesting Billing and Payment Processing:")
    process_payment(member_id, amount_due)