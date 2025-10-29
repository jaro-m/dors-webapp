import DiseaseForm from './DiseaseForm';

const EditDisease = ({disease}) => {
  return <DiseaseForm key={`reporter-e-${disease.id}`} disease={disease} />;
};

export default EditDisease;