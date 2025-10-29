import { useEffect, useState } from 'react';
import { useParams, Navigate } from 'react-router-dom';

import { getDisease, getPatient, getReport } from '../api';
import EditReporter from './EditReporter';
import EditPatient from './EditPatient';
import EditDisease from './EditDisease';
import TopHeader from './Header';
import './EditReport.css';

const EditReport = () => {
  let { reportId } = useParams();
  const [report, setReport] = useState();
  const [patient, setPatient] = useState();
  const [disease, setDisease] = useState();

  useEffect(() => {
    const fetchReport = async () => {
      getReport(reportId).then(async (resp) => {
        if (resp?.error) {
          console.log(`Handle this error, message: ${resp.error?.message ? resp.error?.message : resp.error }`);
          if (resp.status === 401 || resp.status === 403) {
            Navigate("/");
          }
        } else if (resp?.status === 200) {
          setReport(resp.data);
          console.log({resp}, "Details updated successfully");

          const fetchPatient = async () => {
            const resp2 = await getPatient(report.patient_id);
            setPatient(resp2.data);
          }
          const fetchDisease = async () => {
            const resp3 = await getDisease(report.disease_id);
            setDisease(resp3.data);
          }

          fetchPatient();
          fetchDisease();
        }
      });
    }

    fetchReport();
  }, [reportId]);

  return (
    (report?.id !== undefined && patient?.id !== undefined && disease?.id !== undefined)
    ? <><TopHeader /><div className="App">
        <h2>Report details</h2>
        <div className='serv'>
          <ul>
            <li>
              <EditReporter key={`report-r-${report.id}`} reporter={report} />
            </li>
            <li>
              <EditPatient key={`patient-r-${report.id}`} patient={patient} />
            </li>
            <li>
              <EditDisease key={`disease-r-${report.id}`} disease={disease} />
            </li>
          </ul>
        </div>
      </div></>
    : <div className='spinner'></div>
  )

  // return (
  //   (report?.id && patient?.id && disease?.id)
  //   ? <><TopHeader /><div className="App">
  //       <h2>Report details</h2>
  //       <EditReportDetails key={`report-${report.id}`} report={report} />
  //     </div></>
  //   : <div className='spinner'></div>
  // )
};

export default EditReport;