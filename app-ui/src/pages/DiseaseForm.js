// import { useState } from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { postDisease } from '../api';
import './EditForm.css';

const DiseaseForm = ({disease}) => {
  // const [writable, setWritable] = useState(false);

  return (
    <Formik
      initialValues={{...disease, switch: true }}
      validationSchema={Yup.object({
        // id: Yup.string()
        //   .max(15, 'Must be 15 characters or less')
        //   .required('Required'),
        category: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        date_detected: Yup.string()
          .max(30, 'Must be 30 characters or less')
          .required('Required'),
        symptoms: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        severity_level: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        lab_results: Yup.string()
          .max(50, 'Must be 50 characters or less')
          .required('Required'),
        treatment_status: Yup.string()
          .max(20, 'Must be 20 characters or less')
          .required('Required'),
        // created_by: Yup.string()
        //   .max(20, 'Must be 20 characters or less')
        //   .required('Required'),
        // updated_by: Yup.string()
        //   .max(20, 'Must be 20 characters or less')
        //   .required('Required'),
        // date_created: Yup.string()
        //   .max(30, 'Must be 30 characters or less')
        //   .required('Required'),
        // date_updated: Yup.string()
        //   .max(30, 'Must be 30 characters or less')
        //   .required('Required'),
      })}
      onSubmit={(values, { setSubmitting }) => {
        postDisease(values).then(async (data) => {
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
        <p>Disease</p>

        {/* <div className='flex-row'>
          <label htmlFor='switch'>Read/Write</label>
          <Field name="switch" type="radio" onClick={() => setWritable(!writable)}/>
        </div> */}

        <div className='flex-row'>
          <label htmlFor="id">Id</label>
          <Field name="id" disabled={true} type="text" />
          <ErrorMessage name="id" />
        </div>

        <div className='flex-row'>
          <label htmlFor="category">Category</label>
          <Field name="category" type="text" />
          <ErrorMessage name="category" />
        </div>

        <div className='flex-row'>
          <label htmlFor="date_detected">Date Detected</label>
          <Field name="date_detected" type="text" />
          <ErrorMessage name="date_detected" />
        </div>

        <div className='flex-row'>
          <label htmlFor="symptoms">Symptoms</label>
          <Field name="symptoms" type="text" />
          <ErrorMessage name="symptoms" />
        </div>

        <div className='flex-row'>
          <label htmlFor="severity_level">Severity Level</label>
          <Field name="severity_level" type="text" />
          <ErrorMessage name="severity_level" />
        </div>

        <div className='flex-row'>
          <label htmlFor="lab_results">Lab Results</label>
          <Field name="lab_results" type="text" />
          <ErrorMessage name="lab_results" />
        </div>

        <div className='flex-row'>
          <label htmlFor="treatment_status">Treatment Status</label>
          <Field name="treatment_status" type="text" />
          <ErrorMessage name="treatment_status" />
        </div>

        <div className='flex-row'>
          <label htmlFor="created_by">Created By</label>
          <Field name="created_by" disabled={true} type="text" />
          <ErrorMessage name="created_by" />
        </div>

        <div className='flex-row'>
          <label htmlFor="updated_by">Updated By</label>
          <Field name="updated_by" disabled={true} type="text" />
          <ErrorMessage name="updated_by" />
        </div>

        <div className='flex-row'>
          <label htmlFor="date_created">Date Created</label>
          <Field name="date_created" disabled={true} type="text" />
          <ErrorMessage name="date_created" />
        </div>

        <div className='flex-row'>
          <label htmlFor="date_updated">Date Updated</label>
          <Field name="date_updated" disabled={true} type="text" />
          <ErrorMessage name="date_updated" />
        </div>

        <div className='flex-row'>
          <button className='flex-row' type="submit">Submit</button>
        </div>
      </Form>
    </Formik>
  );
};

export default DiseaseForm;