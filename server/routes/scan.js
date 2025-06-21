const express = require('express');
const router = express.Router();
const axios = require('axios');

router.post('/scan', async (req, res) => {
  console.log("Menerima request ke /api/scan");
  const { url } = req.body;

  if (!url) return res.status(400).json({ error: 'URL is required' });

  try {
    const response = await axios.post('http://localhost:5001/predict', { url });
    res.json(response.data);
  } catch (error) {
    console.error('Gagal memanggil Flask:', error.message);
    res.status(500).json({ error: 'Flask service error', detail: error.message });
  }
});

module.exports = router;
