import  { Navigate } from 'react-router-dom'

const Logout = () => {
  if (sessionStorage.getItem("access_token")) {
    sessionStorage.removeItem("access_token");
  }

  return <Navigate to='/' />
};

export default Logout;
