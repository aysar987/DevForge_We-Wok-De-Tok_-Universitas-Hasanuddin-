<<<<<<< HEAD
import React from 'react';
import './Landing-Page.css';
=======
import { Link } from 'react-router-dom';
import React from 'react';
import './global.css';

>>>>>>> 679a7443d32afd7e5126dbe721e69c96eb5c46eb

const LandingPage: React.FC = () => {
  return (
    <div>
      <div className="top-left">
        <img src="/public/Image/phish-small.svg" alt="PhishScan Logo" className="logo" />
      </div>

      <div className="content">
        <h1>PhishScan</h1>
        <p>
<<<<<<< HEAD
          <span className="italic">Artificial Intelligence</span>{' '}
=======
          <span className="highlighted-ai">
          <span className="italic">Artificial Intelligence</span>
          <img src="src/assets/hilighter.svg" alt="underline" className="ai-underline" />          
          </span>{' '}
>>>>>>> 679a7443d32afd7e5126dbe721e69c96eb5c46eb
          Based solution for your long term digital security
        </p>

        <div className="button-group">
<<<<<<< HEAD
          <a href="/scanner.html" className="btn btn-blue">Get Started</a>
          <a href="/infopage.html" className="btn btn-outline">Learn More</a>
        </div>
      </div>

      <footer>© 2025 Your Website. All rights reserved.</footer>
=======
           <Link to="/execute" className="custom-button">Get Started</Link>
          <Link to="/info" className="custom-button2">Learn More</Link>
        </div>
      </div>

      <footer>© PhishScan2025</footer>
>>>>>>> 679a7443d32afd7e5126dbe721e69c96eb5c46eb
    </div>
  );
};

export default LandingPage;
