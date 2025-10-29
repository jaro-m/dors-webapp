const ReportDetails = ({report}) => {
  return (
    <tbody>
      <tr key={report.date_created}>
          <td>{report.id}</td>
          {(report.status !== "Draft") ? <td>{report.status}</td> :
          <td><a href={`/report/${report.id}`}>{report.status}</a></td>}
          <td><a href={`/reporter/${report.reporter_id}`}>{report.reporter?.first_name} {report.reporter?.last_name}</a></td>
          <td>{report.date_created}</td>
          <td>{report.created_by}</td>
          <td>{report.date_updated}</td>
          <td>{report.updated_by}</td>
          <td><a href={`/patient/${report.patient_id}`}>{report.patient?.first_name} {report.reporter?.last_name}</a></td>
          <td><a href={`/disease/${report.disease_id}`}>{report.disease?.name}</a></td>
      </tr>
    </tbody>
  )
};

export default ReportDetails;
