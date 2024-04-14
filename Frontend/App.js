import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

function Home() {
  return (
    <div className="container mt-3">
      <h1>Welcome to Gym Membership Management</h1>
      <div className="btn-group">
        <Link to="/member" className="btn btn-primary">Member</Link>
        <Link to="/trainer" className="btn btn-secondary">Trainer</Link>
        <Link to="/admin" className="btn btn-success">Admin</Link>
      </div>
    </div>
  );
}

function MemberPage() {
  return (
    <div className="container">
      <h2>Member Functions</h2>
      <Link to="/register-member" className="btn btn-primary">Register Member</Link>
      <Link to="/member-dashboard" className="btn btn-secondary">View Dashboard</Link>
      <Link to="/book-training" className="btn btn-info">Book Training</Link>
      <Link to="/register-class" className="btn btn-info">Register for Class</Link>
      <Link to="/update-member-profile" className="btn btn-warning">Update Profile</Link>

    </div>
  );
}

function TrainerPage() {
    return (
        <div className="container">
            <h2>Trainer Functions</h2>
            <div className="list-group">
                <Link to="/set-trainer-availability" className="list-group-item list-group-item-action">
                    Set Availability
                </Link>
                <Link to="/view-member-profiles" className="list-group-item list-group-item-action">
                    View Member Profiles
                </Link>
            </div>
        </div>
    );
}

function AdminPage() {
  return (
    <div className="container">
      <h2>Admin Functions</h2>
      <Link to="/manage-rooms" className="btn btn-primary">Manage Rooms</Link>
      <Link to="/update-equipment-maintenance" className="btn btn-secondary">Manage Equipment</Link>
      <Link to="/update-class-schedule" className="btn btn-info">Update Class Schedule</Link>
      <Link to="/process-payments" className="btn btn-danger">Process Payments</Link>
    </div>
  );
}

function RegisterMember() {
  const [memberData, setMemberData] = useState({
    firstName: '', lastName: '', email: '', dateOfBirth: '', gender: '', fitnessGoal: ''
  });
  const [message, setMessage] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setMemberData({ ...memberData, [name]: value });
  };

  const registerMember = () => {
    axios.post('http://127.0.0.1:5000/register_member', memberData)
      .then(response => setMessage(response.data.message))
      .catch(error => setMessage(error.response.data.error));
  };

  return (
    <div className="container">
      <h2>Register Member</h2>
      <form>
        {Object.entries(memberData).map(([key, value]) => (
          <div className="form-group" key={key}>
            <label>{key.charAt(0).toUpperCase() + key.slice(1)}</label>
            <input
              type={key === 'dateOfBirth' ? 'date' : 'text'}
              className="form-control"
              name={key}
              value={value}
              onChange={handleInputChange}
            />
          </div>
        ))}
        <button type="button" className="btn btn-primary" onClick={registerMember}>Register</button>
      </form>
      {message && <div className="alert alert-info">{message}</div>}
    </div>
  );
}
function MemberDashboard() {
  const [memberId, setMemberId] = useState(''); // To store the member ID input by the user
  const [dashboardData, setDashboardData] = useState(''); // To store the dashboard data or error message
  const [loading, setLoading] = useState(false); // To indicate loading state

  const fetchMemberDashboard = () => {
    if (!memberId) {
      setDashboardData("Please enter a valid Member ID.");
      return;
    }
    setLoading(true); // Start loading
    axios.get(`http://127.0.0.1:5000/member_dashboard/${memberId}`)
      .then(response => {
        const data = response.data;
        // Formatting JSON data for display using JSON.stringify
        setDashboardData(JSON.stringify(data, null, 2));
        setLoading(false); // End loading
      })
      .catch(error => {
        // Handling errors and showing appropriate message
        const errorMessage = error.response ? error.response.data.error : 'Server down';
        setDashboardData(`Error: ${errorMessage}`);
        setLoading(false); // End loading
      });
  };

  return (
    <div className="container">
      <h2>Member Dashboard</h2>
      <div className="form-group">
        <label htmlFor="memberId">Enter Member ID:</label>
        <input
          type="text"
          className="form-control"
          id="memberId"
          value={memberId}
          onChange={(e) => setMemberId(e.target.value)}
          placeholder="Member ID"
        />
      </div>
      <button className="btn btn-primary" onClick={fetchMemberDashboard} disabled={loading}>
        {loading ? 'Loading...' : 'Fetch Dashboard'}
      </button>
      {dashboardData && (
        <div className="mt-3">
          <h4>Dashboard Data:</h4>
          <pre>{dashboardData}</pre>
        </div>
      )}
    </div>
  );
}
function BookTraining() {
  const [trainingSession, setTrainingSession] = useState({
    memberId: '',
    trainerId: '',
    roomId: '',
    scheduledTime: ''
  });
  const [message, setMessage] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setTrainingSession({ ...trainingSession, [name]: value });
  };

  const bookTraining = () => {
    if (!trainingSession.memberId || !trainingSession.trainerId || !trainingSession.roomId || !trainingSession.scheduledTime) {
      setMessage('All fields are required');
      return;
    }

    axios.post('http://127.0.0.1:5000/book_personal_training', trainingSession)
      .then(response => {
        setMessage(`Success: ${response.data.message}`);
      })
      .catch(error => {
        setMessage(`Error: ${error.response ? error.response.data.error : 'Server down'}`);
      });
  };

  return (
    <div className="container">
      <h2>Book Training Session</h2>
      <form>
        <div className="form-group">
          <label>Member ID</label>
          <input type="text" className="form-control" name="memberId" value={trainingSession.memberId} onChange={handleInputChange} />
        </div>
        <div className="form-group">
          <label>Trainer ID</label>
          <input type="text" className="form-control" name="trainerId" value={trainingSession.trainerId} onChange={handleInputChange} />
        </div>
        <div className="form-group">
          <label>Room ID</label>
          <input type="text" className="form-control" name="roomId" value={trainingSession.roomId} onChange={handleInputChange} />
        </div>
        <div className="form-group">
          <label>Scheduled Time</label>
          <input type="datetime-local" className="form-control" name="scheduledTime" value={trainingSession.scheduledTime} onChange={handleInputChange} />
        </div>
        <button type="button" className="btn btn-primary" onClick={bookTraining}>Book Session</button>
      </form>
      {message && <div className="alert alert-info">{message}</div>}
    </div>
  );
}
function RegisterClass() {
  const [classRegistration, setClassRegistration] = useState({
    memberId: '',
    classId: ''
  });
  const [message, setMessage] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setClassRegistration({ ...classRegistration, [name]: value });
  };

  const registerClass = () => {
    axios.post('http://127.0.0.1:5000/register_class', classRegistration)
      .then(response => setMessage(`Success: ${response.data.message}`))
      .catch(error => setMessage(`Error: ${error.response ? error.response.data.error : 'Server down'}`));
  };

  return (
    <div className="container">
      <h2>Register for Class</h2>
      <form>
        <div className="form-group">
          <label>Member ID</label>
          <input
            type="text"
            className="form-control"
            name="memberId"
            value={classRegistration.memberId}
            onChange={handleInputChange}
            placeholder="Enter your Member ID"
          />
        </div>
        <div className="form-group">
          <label>Class ID</label>
          <input
            type="text"
            className="form-control"
            name="classId"
            value={classRegistration.classId}
            onChange={handleInputChange}
            placeholder="Enter the Class ID"
          />
        </div>
        <button type="button" className="btn btn-primary" onClick={registerClass}>Register</button>
      </form>
      {message && <div className="alert alert-info">{message}</div>}
    </div>
  );
}
function UpdateMemberProfile() {
    const [memberProfile, setMemberProfile] = useState({
        memberId: '',
        firstName: '',
        lastName: '',
        email: '',
        fitnessGoal: ''
    });
    const [message, setMessage] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setMemberProfile({ ...memberProfile, [name]: value });
    };

    const updateProfile = () => {
        axios.post('http://127.0.0.1:5000/update_member_profile', memberProfile)
            .then(response => setMessage(`Success: ${response.data.message}`))
            .catch(error => setMessage(`Error: ${error.response ? error.response.data.error : 'Server down'}`));
    };

    return (
        <div className="container">
            <h2>Update Member Profile</h2>
            <form>
                <div className="form-group">
                    <label>Member ID</label>
                    <input
                        type="text"
                        className="form-control"
                        name="memberId"
                        value={memberProfile.memberId}
                        onChange={handleInputChange}
                        placeholder="Member ID"
                    />
                </div>
                <div className="form-group">
                    <label>First Name</label>
                    <input
                        type="text"
                        className="form-control"
                        name="firstName"
                        value={memberProfile.firstName}
                        onChange={handleInputChange}
                        placeholder="First Name"
                    />
                </div>
                <div className="form-group">
                    <label>Last Name</label>
                    <input
                        type="text"
                        className="form-control"
                        name="lastName"
                        value={memberProfile.lastName}
                        onChange={handleInputChange}
                        placeholder="Last Name"
                    />
                </div>
                <div className="form-group">
                    <label>Email</label>
                    <input
                        type="email"
                        className="form-control"
                        name="email"
                        value={memberProfile.email}
                        onChange={handleInputChange}
                        placeholder="Email"
                    />
                </div>
                <div className="form-group">
                    <label>Fitness Goal</label>
                    <input
                        type="text"
                        className="form-control"
                        name="fitnessGoal"
                        value={memberProfile.fitnessGoal}
                        onChange={handleInputChange}
                        placeholder="Fitness Goal"
                    />
                </div>
                <button type="button" className="btn btn-primary" onClick={updateProfile}>Update Profile</button>
            </form>
            {message && <div className="alert alert-info">{message}</div>}
        </div>
    );
}

function SetTrainerAvailability() {
    const [availabilityData, setAvailabilityData] = useState({
        trainerId: '',
        startDate: '',
        endDate: ''
    });
    const [message, setMessage] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setAvailabilityData(prev => ({ ...prev, [name]: value }));
    };

    const updateAvailability = () => {
        const formattedData = {
            trainerId: availabilityData.trainerId,
            availableTimes: {
                startDate: availabilityData.startDate,
                endDate: availabilityData.endDate
            }
        };
        axios.post('http://127.0.0.1:5000/update_trainer_availability', formattedData)
            .then(response => setMessage('Availability updated successfully'))
            .catch(error => setMessage(`Error updating availability: ${error.response ? error.response.data.error : 'Server down'}`));
    };

    return (
        <div className="container">
            <h2>Set Your Availability</h2>
            <div className="form-group">
                <label>Trainer ID</label>
                <input
                    type="text"
                    className="form-control"
                    name="trainerId"
                    value={availabilityData.trainerId}
                    onChange={handleInputChange}
                    placeholder="Trainer ID"
                />
            </div>
            <div className="form-group">
                <label>Start Date and Time</label>
                <input
                    type="datetime-local"
                    className="form-control"
                    name="startDate"
                    value={availabilityData.startDate}
                    onChange={handleInputChange}
                />
            </div>
            <div className="form-group">
                <label>End Date and Time</label>
                <input
                    type="datetime-local"
                    className="form-control"
                    name="endDate"
                    value={availabilityData.endDate}
                    onChange={handleInputChange}
                />
            </div>
            <button className="btn btn-primary" onClick={updateAvailability}>Update Availability</button>
            {message && <div className="alert alert-success">{message}</div>}
        </div>
    );
}

function ViewMemberProfiles() {
    const [searchName, setSearchName] = useState('');
    const [profiles, setProfiles] = useState([]);
    const [message, setMessage] = useState('');

    const searchProfiles = () => {
        if (!searchName.trim()) {
            setMessage("Please enter a name to search.");
            return;
        }
        axios.get(`http://127.0.0.1:5000/view_member_by_name?search_name=${searchName}`)
            .then(response => {
                setProfiles(response.data);
                if (response.data.length === 0) {
                    setMessage("No profiles found.");
                } else {
                    setMessage('');
                }
            })
            .catch(error => {
                const errorMessage = error.response ? error.response.data.error : 'Server down';
                setMessage(`Error fetching profiles: ${errorMessage}`);
            });
    };

    return (
        <div className="container">
            <h2>View Member Profiles</h2>
            <input
                type="text"
                className="form-control"
                value={searchName}
                onChange={(e) => setSearchName(e.target.value)}
                placeholder="Enter Member Name"
            />
            <button className="btn btn-primary mt-2" onClick={searchProfiles}>Search</button>
            {profiles.length > 0 && (
                <div className="mt-3">
                    {profiles.map((profile, index) => (
                        <div key={index} className="card mt-2">
                            <div className="card-body">
                                <h5 className="card-title">{profile.FirstName} {profile.LastName}</h5>
                                <p className="card-text">Email: {profile.Email}</p>
                                <p className="card-text">Date of Birth: {profile.DateOfBirth}</p>
                                <p className="card-text">Gender: {profile.Gender}</p>
                                <p className="card-text">Fitness Goal: {profile.FitnessGoal}</p>
                            </div>
                        </div>
                    ))}
                </div>
            )}
            {message && <div className="alert alert-info mt-2">{message}</div>}
        </div>
    );
}
function ProcessPayment() {
    const [paymentData, setPaymentData] = useState({
        memberId: '',
        amountDue: ''
    });
    const [message, setMessage] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setPaymentData({ ...paymentData, [name]: value });
    };

    const processPayment = () => {
        axios.post('http://127.0.0.1:5000/process_payment', paymentData)
            .then(response => setMessage(`Success: Payment processed for Member ID ${paymentData.memberId}: $${paymentData.amountDue} has been successfully charged.`))
            .catch(error => setMessage(`Error: ${error.response ? error.response.data.error : 'Server down'}`));
    };

    return (
        <div className="container">
            <h2>Process Payment</h2>
            <form>
                <div className="form-group">
                    <label>Member ID</label>
                    <input
                        type="text"
                        className="form-control"
                        name="memberId"
                        value={paymentData.memberId}
                        onChange={handleInputChange}
                        placeholder="Enter Member ID"
                    />
                </div>
                <div className="form-group">
                    <label>Amount Due ($)</label>
                    <input
                        type="number"
                        className="form-control"
                        name="amountDue"
                        value={paymentData.amountDue}
                        onChange={handleInputChange}
                        placeholder="Enter Amount"
                    />
                </div>
                <button type="button" className="btn btn-primary" onClick={processPayment}>Process Payment</button>
            </form>
            {message && <div className="alert alert-info">{message}</div>}
        </div>
    );
}
function UpdateEquipmentMaintenance() {
    const [maintenanceData, setMaintenanceData] = useState({
        equipmentId: '',
        newMaintenanceDate: ''
    });
    const [message, setMessage] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setMaintenanceData({ ...maintenanceData, [name]: value });
    };

    const updateMaintenance = () => {
        axios.post('http://127.0.0.1:5000/update_equipment_maintenance', maintenanceData)
            .then(response => setMessage(`Success: Maintenance schedule updated successfully for Equipment ID ${maintenanceData.equipmentId}.`))
            .catch(error => setMessage(`Error: ${error.response ? error.response.data.error : 'Server down'}`));
    };

    return (
        <div className="container">
            <h2>Update Equipment Maintenance</h2>
            <form>
                <div className="form-group">
                    <label>Equipment ID</label>
                    <input
                        type="text"
                        className="form-control"
                        name="equipmentId"
                        value={maintenanceData.equipmentId}
                        onChange={handleInputChange}
                        placeholder="Enter Equipment ID"
                    />
                </div>
                <div className="form-group">
                    <label>New Maintenance Date</label>
                    <input
                        type="date"
                        className="form-control"
                        name="newMaintenanceDate"
                        value={maintenanceData.newMaintenanceDate}
                        onChange={handleInputChange}
                    />
                </div>
                <button type="button" className="btn btn-primary" onClick={updateMaintenance}>Update Maintenance</button>
            </form>
            {message && <div className="alert alert-info">{message}</div>}
        </div>
    );
}
function UpdateClassSchedule() {
    const [classSchedule, setClassSchedule] = useState({
        classId: '',
        newSchedule: ''
    });
    const [message, setMessage] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setClassSchedule({ ...classSchedule, [name]: value });
    };

    const updateSchedule = () => {
        axios.post('http://127.0.0.1:5000/update_class_schedule', classSchedule)
            .then(response => setMessage(`Success: Class schedule updated successfully for Class ID ${classSchedule.classId}.`))
            .catch(error => setMessage(`Error: ${error.response ? error.response.data.error : 'Server down'}`));
    };

    return (
        <div className="container">
            <h2>Update Class Schedule</h2>
            <form>
                <div className="form-group">
                    <label>Class ID</label>
                    <input
                        type="text"
                        className="form-control"
                        name="classId"
                        value={classSchedule.classId}
                        onChange={handleInputChange}
                        placeholder="Enter Class ID"
                    />
                </div>
                <div className="form-group">
                    <label>New Schedule</label>
                    <input
                        type="datetime-local"
                        className="form-control"
                        name="newSchedule"
                        value={classSchedule.newSchedule}
                        onChange={handleInputChange}
                    />
                </div>
                <button type="button" className="btn btn-primary" onClick={updateSchedule}>Update Schedule</button>
            </form>
            {message && <div className="alert alert-info">{message}</div>}
        </div>
    );
}
function ManageRooms() {
    const [roomData, setRoomData] = useState({
        roomId: '',
        newCapacity: ''
    });
    const [message, setMessage] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setRoomData({ ...roomData, [name]: value });
    };

    const updateRoomCapacity = () => {
        axios.post('http://127.0.0.1:5000/update_room_booking', roomData)
            .then(response => setMessage(`Success: Room capacity updated successfully for Room ID ${roomData.roomId}.`))
            .catch(error => setMessage(`Error: ${error.response ? error.response.data.error : 'Server down'}`));
    };

    return (
        <div className="container">
            <h2>Manage Room Capacity</h2>
            <form>
                <div className="form-group">
                    <label>Room ID</label>
                    <input
                        type="text"
                        className="form-control"
                        name="roomId"
                        value={roomData.roomId}
                        onChange={handleInputChange}
                        placeholder="Enter Room ID"
                    />
                </div>
                <div className="form-group">
                    <label>New Capacity</label>
                    <input
                        type="number"
                        className="form-control"
                        name="newCapacity"
                        value={roomData.newCapacity}
                        onChange={handleInputChange}
                        placeholder="Enter New Capacity"
                    />
                </div>
                <button type="button" className="btn btn-primary" onClick={updateRoomCapacity}>Update Capacity</button>
            </form>
            {message && <div className="alert alert-info">{message}</div>}
        </div>
    );
}
function App() {
  return (
    <Router>
      <div>
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <Link className="navbar-brand" to="/">Home</Link>
        </nav>
        <Switch>
          <Route path="/member" component={MemberPage} />
          <Route path="/trainer" component={TrainerPage} />
          <Route path="/admin" component={AdminPage} />
          <Route path="/register-member" component={RegisterMember} />
          <Route path="/member-dashboard" component={MemberDashboard} />
          <Route path="/book-training" component={BookTraining} />
          <Route path="/register-class" component={RegisterClass} />
          <Route path="/update-member-profile" component={UpdateMemberProfile} />
          <Route path="/set-trainer-availability" component={SetTrainerAvailability} />
          <Route path="/view-member-profiles" component={ViewMemberProfiles} />
          <Route path="/process-payments" component={ProcessPayment} />
          <Route path="/update-equipment-maintenance" component={UpdateEquipmentMaintenance} />
          <Route path="/update-class-schedule" component={UpdateClassSchedule} />
          <Route path="/manage-rooms" component={ManageRooms} />
          <Route path="/" exact component={Home} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
