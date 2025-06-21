import { Link } from 'react-router-dom';
import React from 'react';
import './global.css';


const LandingPage: React.FC = () => {
  return (
    <div>
      <div className="top-left">
        <img src="/public/Image/phish-small.svg" alt="PhishScan Logo" className="logo" />
      </div>

      <div className="content">
        <h1>PhishScan</h1>
        <p>
          <span className="highlighted-ai">
          <span className="italic">Artificial Intelligence</span>
          <img src="src/assets/hilighter.svg" alt="underline" className="ai-underline" />          
          </span>{' '}
          Based solution for your long term digital security
        </p>

        <div className="button-group">
           <Link to="/execute" className="custom-button">Get Started</Link>
          <Link to="/info" className="custom-button2">Learn More</Link>
        </div>
      </div>

      <footer>© PhishScan2025</footer>
    </div>
  );
};

export default LandingPage;
