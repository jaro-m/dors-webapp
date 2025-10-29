import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import { getReporter } from '../api';
import ReporterForm from './ReporterForm';
import TopHeader from './Header';

const Reporter = () => {
  let { reporterId } = useParams();
  const [reporter, setReporter] = useState();

  useEffect(() => {
    const fetchData = async () => {
      const resp = await getReporter(reporterId);
      setReporter(resp.data);
    }

    fetchData();
  }, [reporterId]);

  console.log(reporter);

  return (
    (reporter?.id)
    ? <><TopHeader /><div className="App">
        <h2>Reporter details</h2>
        <ReporterForm key={`reporter-${reporter.id}`} reporter={reporter} />
      </div></>
    : <div className='spinner'></div>
  )
};

export default Reporter;