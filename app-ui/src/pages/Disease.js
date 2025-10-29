import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import { getDisease } from '../api';
import DiseaseForm from './DiseaseForm';
import TopHeader from './Header';

const Disease = () => {
  let { diseaseId } = useParams();
  console.log("diseaseId =>", typeof diseaseId);
  const [disease, setDisease] = useState();

  useEffect(() => {
    const fetchData = async () => {
      const resp = await getDisease(diseaseId);
      setDisease(resp.data);
    }

    fetchData();
  }, [diseaseId]);

  console.log(disease);

  return (
    (disease?.id)
    ? <><TopHeader /><div className="App">
        <h2>Disease details</h2>
        <DiseaseForm key={`reporter-${disease.id}`} disease={disease} />
      </div></>
    : <div className='spinner'></div>
  )
};

export default Disease;