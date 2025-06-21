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
        <div className="container">
          <h2>Start Scanning</h2>
          <p>Paste your suspicious link here...</p>
          <div className="input-wrapper">
          <input
            type="text"
            placeholder="https://example.com..."
            className="container input"
          />
          </div>
          <a href="unsafe.html" className="custom-button">
            Scan
          </a>
        </div>
      </div>
      <footer>© PhishScan2025</footer>
    </div>
  );
};

export default SafePage;
