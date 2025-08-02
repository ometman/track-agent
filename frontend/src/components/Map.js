import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const Map = ({ students, geofences }) => {
  return (
    <MapContainer center={[51.505, -0.09]} zoom={13} style={{ height: '100vh', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {students.map(student => (
        <Marker key={student.id} position={[student.latitude, student.longitude]}>
          <Popup>
            {student.name}
          </Popup>
        </Marker>
      ))}
      {geofences.map(geofence => (
        <Circle
          key={geofence.id}
          center={[geofence.latitude, geofence.longitude]}
          radius={geofence.radius}
        />
      ))}
    </MapContainer>
  );
};

export default Map;
