
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './components/Landing-Page';
import PhishingInfoPage from './components/Info-page';
import ExecutePage from './components/execute-page';
import SafePage from './components/safe';
import UnsafePage from './components/unsafe';
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/info" element={<PhishingInfoPage />} />\
        <Route path="/execute" element={<ExecutePage />} />
        <Route path="/safe" element={<SafePage />} />
        <Route path="/unsafe" element={<UnsafePage />} />
      </Routes>
    </Router>
  );
}

export default App;

