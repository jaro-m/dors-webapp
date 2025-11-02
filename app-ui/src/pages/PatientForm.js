import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { postPatient } from '../api';
import './EditForm.css';

const PatientForm = ({patient}) => {
  return (
    <Formik
      initialValues={patient}
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
          .required()
          .oneOf(["Female", "Male", "Other"])
          .label("Select Gender"),
        medical_record_number: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        patient_address: Yup.string()
          .max(50, 'Must be 50 characters or less')
          .required('Required'),
        emergency_contact: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
      })}
      onSubmit={(values, { setSubmitting }) => {
        postPatient(values).then(async (data) => {
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
      <Form className='flex-container'>
        <h3>Patient details</h3>

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

        <label className="formfield-label" htmlFor="gender">Gender</label>
         <Field name="gender" as="select" className="flex-row select-button">
          <option value="Female">Female</option>
          <option value="Male">Male</option>
          <option value="Other">Other</option>
        </Field>

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

export default PatientForm;