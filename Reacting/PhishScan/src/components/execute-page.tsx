import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './global.css';

const ExecutePage: React.FC = () => {

  const [url, setUrl] = useState('');
  const [result, setResult] = useState<any>(null);
  const navigate = useNavigate();

  const handleScan = async () => {
    if (!url) return alert('Harap masukkan URL!');
    try {
      const response = await fetch('http://localhost:3000/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await response.json();
      setResult(data);
      console.log('Hasil scan: ', data);

      if (data.isPhishing) {
        navigate('/unsafe', { state: { detail: data } });
      } else {
        navigate('/safe', { state: { detail: data } });
      }

    } catch (error) {
      console.error('Error scanning URL:', error);
    }
  };

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
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com..."
            className="container input"
          />
          </div>
          <button onClick={handleScan} className="custom-button">
            Scan
          </button>
        </div>
      </div>
      <footer>© PhishScan2025</footer>
    </div>
  );
};

export default ExecutePage;
