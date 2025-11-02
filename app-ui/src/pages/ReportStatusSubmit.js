import { Formik, Field, Form } from 'formik';
import * as Yup from 'yup';
import { putReport } from '../api';
import './EditForm.css';

const ReportStatusSubmit = ({report}) => {
  console.log({ report }, "report prop" );
  return (
    <Formik
      initialValues={report}
      validationSchema={Yup.object({
        status: Yup.string()
          .required()
          .oneOf(["Draft", "Submitted", "Under Review", "Approved"])
          .label("Change status"),
      })}
      onSubmit={(values, { setSubmitting }) => {
        console.log("submitting the report");
        putReport(values).then(async (data) => {
          if (data?.error) {
            console.log(`Handle this error, message: ${data.error?.message ? data.error?.message : data.error }`);
            alert(`ERROR: ${data.error?.message}`);
          } else if (data?.status === 200) {
            console.log("Details updated successfully");
            setSubmitting(false);
            alert("Details updated successfully");
          }
        })
      }}
    >
      <Form className='flex-container-login'>
        <h4>Report Status</h4>

        <Field name="status" as="select" className="flex-row select-button">
          <option value="Draft">Draft</option>
          <option value="Submitted">Submitted</option>
          <option value="Under Review">Under Review</option>
          <option value="Approved">Approved</option>
        </Field>

        <div className='flex-row'>
          <button className='flex-row' type="submit">Submit Report Status</button>
        </div>
      </Form>
    </Formik>
  );
};

export default ReportStatusSubmit;