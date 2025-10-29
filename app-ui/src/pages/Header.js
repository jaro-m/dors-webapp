import  { Link, Navigate } from 'react-router-dom'
import './Header.css';

const TopHeader = () => {
  if (!sessionStorage.getItem("access_token")) return <Navigate to='/login' />;

  return (
    <div className='header-container'>
      <nav>
        <Link className="link" to="/reports">Reports</Link>
        <Link className="link" to="/about">About</Link>
        <Link className="link" to="/logout">Logout</Link>
      </nav>
    </div>
  );
};

export default TopHeader;
