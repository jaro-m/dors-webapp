import  { useState } from 'react';
import  { Navigate } from 'react-router-dom'
import './Login.css';

import axios from 'axios';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log({ formData }, "formData in the component");

    const requestBody = new FormData()

    try {
      for (const [key, value] of Object.entries(formData)) {
        requestBody.append(key, value);
      }

      const response = await axios.post('https://localhost:8000/token', requestBody);
      sessionStorage.setItem("access_token", response.data.access_token);

      setResponseMessage(`Success: ${response.data.access_token}`);
    } catch (error) {
      setResponseMessage(`Error: ${error.message}`);
    }
  };

  return sessionStorage.getItem("access_token")
    ? (<Navigate to='/' />)
    : (
      <div>
        <h1>Login to auhtorize the connections</h1>
        <div className='flex-container'>
          <form onSubmit={handleSubmit}>
            <label>
              <p className='flex-row'>username:</p>
              <input
                className='flex-item'
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </label>
            <label>
              <p className='flex-row'>password:</p>
              <input
                className='flex-item'
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </label>
            <div className='flex-row'>
              <button className='flex-button' type="submit">Submit</button>
            </div>
          </form>
          {responseMessage && <p>{responseMessage}</p>}
        </div>
      </div>
    );
};

export default Login;
