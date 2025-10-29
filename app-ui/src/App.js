import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import EditReport from './pages/EditReport';
import NotFound from './pages/NotFound';
import Login from './pages/Login';
import Logout from './pages/Logout';
import Disease from './pages/Disease';
import Patient from './pages/Patient';
import Report from './pages/Report';
import Reporter from './pages/Reporter';
// import Reporter2 from './pages/Reporter2';
import Reports from './pages/Reports';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/login" element={<Login />} />
      <Route path="/logout" element={<Logout />} />
      <Route path="/disease/:diseaseId" element={<Disease />} />
      <Route path="/patient/:patientId" element={<Patient />} />
      <Route path="/reporter/:reporterId" element={<Reporter />} />
      <Route path="/reports" element={<Reports />} />
      <Route path="/report/:reportId" element={<EditReport />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default App;
