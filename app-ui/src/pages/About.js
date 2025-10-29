import TopHeader from './Header';
import './About.css';

const About = () => {
  return (
    <><TopHeader />
    <h1>About Page</h1>
    <div className='flex-container'>
      <p>This app allows to create reports about diseases.</p>
      <p>You can click on some links (blue text)</p>
    </div>
    </>
  )
};

export default About;
