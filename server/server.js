const express = require('express');
const cors = require('cors');
const scanRoute = require('./routes/scan');

const app = express();
app.use(cors({
    origin: 
}));
app.use(express.json());

app.use('/api/scan-url', scanRoute);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

