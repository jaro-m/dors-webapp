import { useEffect, useState } from 'react';
import  { Navigate } from 'react-router-dom';
import "./Reports.css";

import { getRecent, getReports } from '../api';
import ReportDetails from './ReportDetails';
import RecentReport from './RecentReport';
import TopHeader from './Header';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [recent, setRecent] = useState({});
  const headers = [
    "ID", "Status", "Reporter", "Date Created", "Created By",
    "Date Updated", "Updated By", "Patient", "Disease",
  ]

  useEffect(() => {
    const fetchData = async () => {
      const resp = await getReports();
      if (resp?.error) return <Navigate to='/login' />;
      setReports(resp.data);
    }

    fetchData();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      const resp = await getRecent();
      setRecent(resp.data);
    }

    fetchData();
  }, []);

  console.log(reports);

  return (
    <><TopHeader />
    <div className="App">
      <h1>Reports</h1>
      <table key={"report list"}>
        <thead>
          <tr>
            {headers.map((header) => (<th>{header}</th>))}
          </tr>
        </thead>
        {reports.map((report) => (
          <ReportDetails key={report.id} report={report} />
        ))}
      </table>
      {Boolean(recent?.id)
      ? <><h2>Recent Submission</h2><table key={"recent report list"}>
            <thead>
              <tr>
                {headers.map((header) => (<th>{header}</th>))}
              </tr>
            </thead>
            <RecentReport key={recent.id} report={recent} />
          </table></>
      : null}
    </div></>
    );
};

export default Reports;