import React from 'react';
import './Landing-Page.css';

const LandingPage: React.FC = () => {
  return (
    <div>
      <div className="top-left">
        <img src="/public/Image/phish-small.svg" alt="PhishScan Logo" className="logo" />
      </div>

      <div className="content">
        <h1>PhishScan</h1>
        <p>
          <span className="italic">Artificial Intelligence</span>{' '}
          Based solution for your long term digital security
        </p>

        <div className="button-group">
          <a href="/scanner.html" className="btn btn-blue">Get Started</a>
          <a href="/infopage.html" className="btn btn-outline">Learn More</a>
        </div>
      </div>

      <footer>© 2025 Your Website. All rights reserved.</footer>
    </div>
  );
};

export default LandingPage;
