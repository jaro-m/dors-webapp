import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import { getDisease, getPatient, getReport, getReporter } from '../api';
import EditReporter from './EditReporter';
import EditPatient from './EditPatient';
import EditDisease from './EditDisease';
import ReportStatusSubmit from './ReportStatusSubmit';
import TopHeader from './Header';
import Home from './Home';
import Spinner from './Spinner';
import './EditReport.css';

const EditReport = () => {
  let { reportId } = useParams();
  const [report, setReport] = useState();
  const [reporter, setReporter] = useState();
  const [patient, setPatient] = useState();
  const [disease, setDisease] = useState();
  const [toLogin, setToLogin] = useState(false);

  useEffect(() => {
    const fetchReport = async () => {
      getReport(reportId).then(async (resp) => {
        if (resp?.error) {
          console.log(`Handle this error: ${resp.error?.message ? resp.error?.message : resp.error }`);
          if (resp.error === "not authorized") {
            sessionStorage.removeItem("access-token");
            setToLogin(true);
          }
        } else if (resp?.data && resp.status === 200) {
          setReport(resp.data);
          console.log({resp}, "Details updated successfully");

          const fetchReporter = async () => {
            const resp1 = await getReporter(resp.data.reporter_id);
            setReporter(resp1.data);
          }
          const fetchPatient = async () => {
            const resp2 = await getPatient(resp.data.patient_id);
            setPatient(resp2.data);
          }
          const fetchDisease = async () => {
            const resp3 = await getDisease(resp.data.disease_id);
            setDisease(resp3.data);
          }

          fetchReporter();
          fetchPatient();
          fetchDisease();
        }
      });
    }

    fetchReport();
  }, [reportId]);

  return (
    (toLogin) ? <Home /> :
      (report?.id !== undefined && reporter?.id !== undefined && patient?.id !== undefined && disease?.id !== undefined)
      ? <><TopHeader /><div className="App">
          <h2>Report details</h2>
          <div className='serv'>
            <ul>
              <li>
                <EditReporter key={`report-r-${report.id}`} reporter={reporter} />
              </li>
              <li>
                <EditPatient key={`patient-r-${report.id}`} patient={patient} />
              </li>
              <li>
                <EditDisease key={`disease-r-${report.id}`} disease={disease} />
              </li>
            </ul>
          </div>
          <hr />
          <ReportStatusSubmit key={`report-status-${report.id}`} report={report} />
        </div></>
      : <Spinner />
  )
};

export default EditReport;