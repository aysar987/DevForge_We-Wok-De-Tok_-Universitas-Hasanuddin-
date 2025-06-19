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
          <a href="/src/components/execute-page.tsx" className="custom-button">Get Started</a>
          <a href="/src/components/Info-page.tsx" className="custom-button2">Learn More</a>
        </div>
      </div>

      <footer>© PhishScan2025</footer>
    </div>
  );
};

export default LandingPage;
