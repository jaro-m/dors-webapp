import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { putReport, postPatient, postDisease } from '../api';
import './EditForm.css';

const EditReportDetails = ({report}) => {
  return (
    <Formik
      initialValues={report}
      validationSchema={Yup.object({
        first_name: Yup.string()
          .max(15, 'Must be 15 characters or less')
          .required('Required'),
        last_name: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        date_of_birth: Yup.string()
          .max(30, 'Must be 30 characters or less')
          .required('Required'),
        gender: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        medical_record_number: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        patient_address: Yup.string()
          .max(50, 'Must be 50 characters or less')
          .required('Required'),
        emergency_contact: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        // age: Yup.string()
        //   .max(20, 'Must be 20 characters or less')
        //   .required('Required'),
        // id: Yup.string()
        //   .max(20, 'Must be 20 characters or less')
        //   .required('Required'),
      })}
      onSubmit={(values, { setSubmitting }) => {
        putReport(values).then(async (data) => {
          if (data?.error) {
            console.log(
              `Handle this error, message: ${data.error?.message ? data.error?.message : data.error }`
            );
            alert(`ERROR: ${data.error?.message}`);
          } else if (data?.status === 200) {
            console.log("Details updated successfully");
            setSubmitting(false);
            alert("Details updated successfully");
          }
        })
      }}
    >
      <Form className='flex-container'>

        <div className='flex-row'>
          <label htmlFor="id">Id</label>
          <Field name="id" disabled={true} type="text" />
          <ErrorMessage name="id" />
        </div>

        <div className='flex-row'>
          <label htmlFor="first_name">First Name</label>
          <Field name="first_name" type="text" />
          <ErrorMessage name="first_name" />
        </div>

        <div className='flex-row'>
          <label htmlFor="last_name">Last Name</label>
          <Field name="last_name" type="text" />
          <ErrorMessage name="last_name" />
        </div>

        <div className='flex-row'>
          <label htmlFor="date_of_birth">Date of Birth</label>
          <Field name="date_of_birth" type="text" />
          <ErrorMessage name="date_of_birth" />
        </div>

        <div className='flex-row'>
          <label htmlFor="gender">Gender</label>
          <Field name="gender" type="text" />
          <ErrorMessage name="gender" />
        </div>

        <div className='flex-row'>
          <label htmlFor="patient_address">Patient Address</label>
          <Field name="patient_address" type="text" />
          <ErrorMessage name="patient_address" />
        </div>

        <div className='flex-row'>
          <label htmlFor="emergency_contact">Emergency Contact</label>
          <Field name="emergency_contact" type="text" />
          <ErrorMessage name="emergency_contact" />
        </div>

        <div className='flex-row'>
          <label htmlFor="age">Age</label>
          <Field name="age" disabled={true} type="text" />
          <ErrorMessage name="age" />
        </div>

        <div className='flex-row'>
          <button className='flex-row' type="submit">Submit</button>
        </div>
      </Form>
    </Formik>
  );
};

export default EditReportDetails;