import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { postReporter } from '../api';
import './EditForm.css';

const ReporterForm = ({reporter}) => {
  return (
    <Formik
      initialValues={reporter}
      validationSchema={Yup.object({
        first_name: Yup.string()
          .max(15, 'Must be 15 characters or less')
          .required('Required'),
        last_name: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        job_title: Yup.string()
          .max(15, 'Must be 15 characters or less')
          .required('Required'),
        organization_name: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        organization_address: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        phone_number: Yup.string()
          .max(20, 'Validation needs some improvements')
          .required('Required'),
        email: Yup.string().email('Invalid email address').required('Required'),
      })}
      onSubmit={(values, { setSubmitting }) => {
        postReporter(values).then(async (data) => {
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
        <h3>Reporter details</h3>

        <div className='flex-row'>
          <label htmlFor="id">Id</label>
          <Field name="id" disabled={true} type="text" />
          <ErrorMessage name="firstName" />
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
          <label htmlFor="email">Email Address</label>
          <Field name="email" type="email" />
          <ErrorMessage name="email" />
        </div>

        <div className='flex-row'>
          <label htmlFor="job_title">Job Title</label>
          <Field name="job_title" type="text" />
          <ErrorMessage name="job_title" />
        </div>

        <div className='flex-row'>
          <label htmlFor="phone_number">Phone Number</label>
          <Field name="phone_number" type="text" />
          <ErrorMessage name="phone_number" />
        </div>

        <div className='flex-row'>
          <label htmlFor="organization_name">Organization Name</label>
          <Field name="organization_name" type="text" />
          <ErrorMessage name="organization_name" />
        </div>

        <div className='flex-row'>
          <label htmlFor="organization_address">Organization Address</label>
          <Field name="organization_address" type="text" />
          <ErrorMessage name="organization_address" />
        </div>

        <div className='flex-row'>
          <button className='flex-row' type="submit">Submit</button>
        </div>
      </Form>
    </Formik>
  );
};

export default ReporterForm;