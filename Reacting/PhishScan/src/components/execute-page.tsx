import React from 'react';
import './global.css';

const PhishScanPage: React.FC = () => {
  return (
    <div>
      <div className="top-left">
        <img
          src="img/Logo_PhishScan.png"
          alt="PhishScan Logo"
          className="logo"
        />
      </div>

      <div className="card-wrapper-center">
        <div className="container">
          <h2>Start Scanning</h2>
          <p>Paste your suspicious link here</p>
          <input
            type="text"
            placeholder="https://xxx.com..."
            disabled
          />
          <a href="unsafe.html" className="scan-btn">
            Scan
          </a>
        </div>
      </div>
    </div>
  );
};

export default PhishScanPage;
