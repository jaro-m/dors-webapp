import PatientForm from './PatientForm';

const EditPatient = ({patient}) => {
  return <PatientForm key={`patient-e-${patient.id}`} patient={patient} />;
};

export default EditPatient;