import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import { getPatient } from '../api';
import PatientForm from './PatientForm';
import TopHeader from './Header';

const Patient = () => {
  let { patientId } = useParams();
  const [patient, setPatient] = useState();

  useEffect(() => {
    const fetchData = async () => {
      const resp = await getPatient(patientId);
      setPatient(resp.data);
    }

    fetchData();
  }, [patientId]);

  console.log(patient);

  return (
    (patient?.id)
    ? <><TopHeader /><div className="App">
        <h2>Patient details</h2>
        <PatientForm key={`patient-${patient.id}`} patient={patient} />
      </div></>
    : <div className='spinner'></div>
  )
};

export default Patient;