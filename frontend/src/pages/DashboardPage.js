import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Map from '../components/Map';

const DashboardPage = () => {
  const [students, setStudents] = useState([]);
  const [geofences, setGeofences] = useState([]);

  useEffect(() => {
    const fetchStudents = async () => {
      const res = await axios.get('/students/');
      setStudents(res.data);
    };
    const fetchGeofences = async () => {
      const res = await axios.get('/geofences/');
      setGeofences(res.data);
    };
    fetchStudents();
    fetchGeofences();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <Map students={students} geofences={geofences} />
    </div>
  );
};

export default DashboardPage;
