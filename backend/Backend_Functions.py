from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import json
import main
from datetime import datetime
app = Flask(__name__)
CORS(app)


@app.route('/register_member', methods=['POST'])
def register_member():
    data = request.get_json()
    try:
        first_name = data.get('firstName', '')
        last_name = data.get('lastName', '')
        email = data.get('email', '')
        date_of_birth = data.get('dateOfBirth', '')
        gender = data.get('gender', '').capitalize()
        fitness_goal = data.get('fitnessGoal', '')


        if date_of_birth:
            try:

                datetime.strptime(date_of_birth, '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Invalid date format, should be YYYY-MM-DD'}), 400
        else:
            return jsonify({'error': 'Date of birth is required'}), 400

        main.register_member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=date_of_birth,
            gender=gender,
            fitness_goal=fitness_goal
        )
        return jsonify({'message': 'Member registered successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


def display_member_dashboard(member_id):
    conn = main.connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                # Dictionary to hold all data
                dashboard_data = {
                    'exercise_routines': [],
                    'achievements': [],
                    'health_statistics': []
                }

                # Fetch exercise routines
                cursor.execute("""
                    SELECT ActivityDate, ActivityType, Duration, CaloriesBurnt FROM ActivityLogs WHERE MemberID = %s;
                """, (member_id,))
                activities = cursor.fetchall()
                for activity in activities:
                    date, activity_type, duration, calories_burnt = activity
                    dashboard_data['exercise_routines'].append({
                        'Date': date.strftime("%Y-%m-%d"),  # Format date as string
                        'Type': activity_type,
                        'Duration (min)': duration,
                        'Calories Burnt': calories_burnt
                    })

                # Fetch achievements
                cursor.execute("""
                    SELECT AchievementName, DateEarned FROM Achievements
                    JOIN MemberAchievements ON Achievements.AchievementID = MemberAchievements.AchievementID
                    WHERE MemberAchievements.MemberID = %s;
                """, (member_id,))
                achievements = cursor.fetchall()
                for achievement in achievements:
                    name, date_earned = achievement
                    dashboard_data['achievements'].append({
                        'Achievement Name': name,
                        'Date Earned': date_earned.strftime("%Y-%m-%d")
                    })

                # Fetch health statistics
                cursor.execute("""
                    SELECT RecordedDate, Weight, HeartRate, OtherMetrics FROM HealthStats WHERE MemberID = %s;
                """, (member_id,))
                health_stats = cursor.fetchall()
                for stat in health_stats:
                    date, weight, heart_rate, other_metrics = stat
                    dashboard_data['health_statistics'].append({
                        'Recorded Date': date.strftime("%Y-%m-%d"),
                        'Weight (kg)': weight,
                        'Heart Rate': heart_rate,
                        'Other Metrics': other_metrics
                    })

                return jsonify(dashboard_data), 200
        except psycopg2.Error as e:
            return jsonify({'error': str(e)}), 400
        finally:
            conn.close()
    return jsonify({'error': 'Database connection failed'}), 500

@app.route('/update_member_profile', methods=['POST'])
def update_member_profile():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Check if all necessary data is provided
    required_fields = ['memberId', 'firstName', 'lastName', 'email', 'fitnessGoal']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required parameters'}), 400

    member_id = data['memberId']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    fitness_goal = data['fitnessGoal']

    try:
        conn = main.connect_db()  # Ensure you have a function to connect to the database
        if conn is not None:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Members
                    SET FirstName = %s, LastName = %s, Email = %s, FitnessGoal = %s
                    WHERE MemberID = %s;
                """, (first_name, last_name, email, fitness_goal, member_id))
                conn.commit()
                return jsonify({'message': 'Profile updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to connect to the database'}), 500
    except psycopg2.Error as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/member_dashboard/<int:member_id>', methods=['GET'])
def get_member_dashboard(member_id):
    return display_member_dashboard(member_id)


@app.route('/book_personal_training', methods=['POST'])
def book_personal_training():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['memberId', 'trainerId', 'roomId', 'scheduledTime']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required parameters'}), 400

    member_id = data['memberId']
    trainer_id = data['trainerId']
    room_id = data['roomId']
    scheduled_time = data['scheduledTime']  # This should ideally be just the time 'HH:MM'

    try:

        time_only = scheduled_time.split('T')[1] if 'T' in scheduled_time else scheduled_time

        # Combine with a fixed or calculated date
        date_for_scheduling = '2024-04-17'
        full_timestamp = f'{date_for_scheduling}T{time_only}'
        scheduled_datetime = datetime.strptime(full_timestamp, '%Y-%m-%dT%H:%M')

        if not main.check_trainer_availability(trainer_id, scheduled_datetime.strftime('%A'), time_only):
            return jsonify({'message': 'Trainer is not available at this time'}), 400

        main.book_personal_training_session(
            member_id=member_id,
            trainer_id=trainer_id,
            room_id=room_id,
            scheduled_time=scheduled_datetime.strftime('%Y-%m-%d %H:%M')  # Format to match database expectations
        )
        return jsonify({'message': 'Training session booked successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/register_class', methods=['POST'])
def register_class():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Extracting member_id and class_id from the data
    member_id = data.get('memberId')
    class_id = data.get('classId')

    # Check if both IDs are provided
    if not member_id or not class_id:
        return jsonify({'error': 'Missing member ID or class ID'}), 400

    try:
        conn = main.connect_db()
        if conn is not None:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO MemberClasses (MemberID, ClassID)
                    VALUES (%s, %s);
                """, (member_id, class_id))
                conn.commit()
                return jsonify({'message': 'Registered for class successfully'}), 200
        else:
            return jsonify({'error': 'Failed to connect to the database'}), 500
    except psycopg2.Error as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/update_trainer_availability', methods=['POST'])
def update_trainer_availability():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Validate required fields
    required_fields = ['trainerId', 'availableTimes']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required parameters'}), 400

    trainer_id = data['trainerId']
    available_times = data['availableTimes']

    # Validate the datetime format or other conditions as needed
    try:
        conn = main.connect_db()
        if conn is not None:
            with conn.cursor() as cursor:
                available_times_json = json.dumps(available_times)
                cursor.execute("""
                    UPDATE Trainers
                    SET AvailableTimes = %s
                    WHERE TrainerID = %s;
                """, (available_times_json, trainer_id))
                conn.commit()  # Commit the transaction
                return jsonify({'message': 'Trainer availability updated successfully'}), 200
        else:
            return jsonify({'error': 'Failed to connect to the database'}), 500
    except psycopg2.Error as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/view_member_by_name', methods=['GET'])
def view_member_by_name():
    search_name = request.args.get('search_name')
    if not search_name:
        return jsonify({'error': 'No search name provided'}), 400

    conn = main.connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT MemberID, FirstName, LastName, Email, DateOfBirth, Gender, FitnessGoal FROM Members
                    WHERE FirstName ILIKE %s OR LastName ILIKE %s;
                """, ('%' + search_name + '%', '%' + search_name + '%'))
                members = cursor.fetchall()
                member_list = [{
                    'MemberID': member[0],
                    'FirstName': member[1],
                    'LastName': member[2],
                    'Email': member[3],
                    'DateOfBirth': member[4].strftime("%Y-%m-%d") if member[4] else "N/A",
                    'Gender': member[5],
                    'FitnessGoal': member[6]
                } for member in members]
                return jsonify(member_list), 200
        except psycopg2.Error as e:
            return jsonify({'error': f"Database error: {str(e)}"}), 500
        finally:
            if conn:
                conn.close()
    else:
        return jsonify({'error': 'Database connection failed'}), 500

@app.route('/update_room_booking', methods=['POST'])
def update_room_booking():
    data = request.get_json()
    if not data or 'roomId' not in data or 'newCapacity' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400

    room_id = data['roomId']
    new_capacity = data['newCapacity']

    conn = main.connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Rooms
                    SET Capacity = %s
                    WHERE RoomID = %s;
                """, (new_capacity, room_id))
                conn.commit()
                return jsonify({'message': 'Room capacity updated successfully'}), 200
        except psycopg2.Error as e:
            return jsonify({'error': f'Failed to update room capacity: {str(e)}'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500

@app.route('/update_equipment_maintenance', methods=['POST'])
def update_equipment_maintenance():
    data = request.get_json()
    if not data or 'equipmentId' not in data or 'newMaintenanceDate' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400

    equipment_id = data['equipmentId']
    new_maintenance_date = data['newMaintenanceDate']

    conn = main.connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Equipment
                    SET MaintenanceSchedule = %s
                    WHERE EquipmentID = %s;
                """, (new_maintenance_date, equipment_id))
                conn.commit()
                return jsonify({'message': 'Equipment maintenance schedule updated successfully'}), 200
        except psycopg2.Error as e:
            return jsonify({'error': f'Failed to update equipment maintenance: {str(e)}'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500


@app.route('/update_class_schedule', methods=['POST'])
def update_class_schedule():
    data = request.get_json()
    if not data or 'classId' not in data or 'newSchedule' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400

    class_id = data['classId']
    new_schedule = data['newSchedule']

    conn = main.connect_db()
    if conn is not None:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE Classes
                    SET Schedule = %s
                    WHERE ClassID = %s;
                """, (new_schedule, class_id))
                conn.commit()
                return jsonify({'message': 'Class schedule updated successfully'}), 200
        except psycopg2.Error as e:
            return jsonify({'error': f'Failed to update class schedule: {str(e)}'}), 500
        finally:
            conn.close()
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500


def log_payment(member_id, amount):
    print(f"Logged payment for Member ID {member_id}: ${amount} has been successfully recorded.")

@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.get_json()
    if not data or 'memberId' not in data or 'amountDue' not in data:
        return jsonify({'error': 'Missing required payment details'}), 400

    member_id = data['memberId']
    amount_due = data['amountDue']

    # Simulate payment processing
    try:
        if not member_id or not amount_due:
            return jsonify({'error': 'Invalid payment details provided'}), 400


        log_payment(member_id, amount_due)
        return jsonify({'message': f'Payment processed for Member ID {member_id}: ${amount_due} has been successfully charged.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
