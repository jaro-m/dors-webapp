import React from 'react';
import  { Navigate } from 'react-router-dom';
import TopHeader from './Header';


const Home = () => {
  if (!sessionStorage.getItem("access_token")) return <Navigate to='/login' />;

  return (
    <div>
      <TopHeader />;
      <h1>Now you are logged in</h1>
    </div>
  )
};

export default Home;
