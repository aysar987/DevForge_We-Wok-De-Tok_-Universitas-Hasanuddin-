import { Link } from 'react-router-dom';
import React from 'react';
import './global.css';

const PhishScanInfo: React.FC = () => {

  const scrollLeft = () => {
    const slider = document.getElementById('cardSlider');
    if (slider) {
      slider.scrollBy({ left: -300, behavior: 'smooth' });
    }
  };

  const scrollRight = () => {
    const slider = document.getElementById('cardSlider');
    if (slider) {
      slider.scrollBy({ left: 300, behavior: 'smooth' });
    }
  };

  return (
    <div>
      <div className="top-left">
        <img src="/public/Image/phish-small.svg" alt="PhishScan Logo" className="logo" />
      </div>

      <section id="Learn-More">
        <h1>ABOUT PHISHING LINKS</h1>
        <p>
          <span className="italic">Phishing Links</span> - a phishing method using malicious URLs designed to trick
          you into revealing sensitive information or downloading malware.
        </p>

        <div className="slide-header">
          <h2>TIPS TO STAY SAFE</h2>
          <div className="slide-buttons">
            <button className="scroll-btn left" onClick={scrollLeft}>←</button>
            <button className="scroll-btn rights" onClick={scrollRight}>→</button>
          </div>
        </div>

        <div className="card-slider" id="cardSlider">
          <div className="card">
            <h3>Suspicious or Misspelled URLs</h3>
            <p>Legit domains are rarely misspelled. Be cautious of URLs like paypaI.com or g00gle.net.</p>
          </div>
          <div className="card">
            <h3>Unfamiliar Domain Extensions</h3>
            <p>Be cautious with weird domain endings like .xyz, .top, or .click. They’re cheap and often used in phishing.</p>
          </div>
          <div className="card">
            <h3>No HTTPS? No Way!</h3>
            <p>Legit sites use HTTPS to protect your data. If you see only "http", don’t trust it.</p>
          </div>
          <div className="card">
            <h3>Links From Unknown Emails or Texts</h3>
            <p>If it comes out of nowhere and urges you to click fast, it’s probably a trap.</p>
          </div>
          <div className="card">
            <h3>Too Good to Be True Offers</h3>
            <p>"Win a free iPhone!" — classic bait. Don’t fall for it.</p>
          </div>
          <div className="card">
            <h3>Random Characters or Gibberish in the URL</h3>
            <p>If the link looks messy or doesn’t match the site it claims to be, it’s suspicious.</p>
          </div>
        </div>

        <Link to="/execute" className="custom-button">Start Scanning</Link>
      </section>
      <footer>© PhishScan2025</footer>
    
    </div>
    
  );
};

export default PhishScanInfo;

