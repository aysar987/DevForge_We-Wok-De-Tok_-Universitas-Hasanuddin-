import { Link } from 'react-router-dom';
import React from 'react';
import './global.css';

const SafePage: React.FC = () => {
  return (
    <div>
      <div className="top-left">
        <img
          src="/public/Image/phish-small.svg"
          alt="PhishScan Logo"
          className="logo"
        />
      </div>
      <div className="card-wrapper-center">
        <div className="gre-result-card safe">
          <h1>Result</h1>
          <h2>your link is proven</h2>
          <input type="text" value="https://abc.com..." disabled />

          <div className="gre-result-message">
            <p>
            <span className="highlight-gre">SAFE</span> - your link is proven unsafe by our system
            </p>
            <Link to="/info" className="learn-more blue">Learn More</Link>
            </div>
        </div>
      </div>
      <footer>© PhishScan2025</footer>
    </div>
  );
};

export default SafePage;
