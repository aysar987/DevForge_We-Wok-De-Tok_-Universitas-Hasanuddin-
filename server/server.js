const express = require('express');
const app = express();
const cors = require('cors');

const scanRouter = require('./routes/scan');

app.use(cors());
app.use(express.json());
app.use('/api', scanRouter);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Node.js backend listening on http://localhost:${PORT}`);
});
