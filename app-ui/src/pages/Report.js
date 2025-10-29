import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import { getReport } from '../api';
import ReportDetails from './ReportDetails';
import TopHeader from './Header';

const Report = () => {
  let { reportId } = useParams();
  const [report, setReport] = useState({});
  const headers = [
    "ID",
    "Status",
    "Reporter",
    "Date Created",
    "Created By",
    "Date Updated",
    "Updated By",
    "Patient",
    "Disease",
  ]

  useEffect(() => {
    const fetchData = async () => {
      const resp = await getReport(reportId);
      setReport(resp.data);
    }
    try {
      fetchData();
    } catch(err) {
      alert(`ERRER: ${err}`);
      console.log(`Report page error: ${err}`);
    }
  }, [reportId]);

  console.log(report);

  return (
    <><TopHeader />
    <div className="App">
      <h1>Report</h1>
      <table key={`report ${report.date_created}`}>
        <thead>
          <tr>
            {headers.map((header) => (<th>{header}</th>))}
          </tr>
        </thead>
        <ReportDetails key={report.id} report={report} />
      </table>
    </div></>
  );
};

export default Report;