require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const { connect } = require('./db');
const containerRoutes = require('./routes/containerRoutes');

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use('/containers', containerRoutes);


app.get('/health', async (req, res) => {
  const state = mongoose.connection.readyState;
  if (state === 1) {
    res.json({ status: 'ok' });
  } else {
    res.status(500).json({ status: 'error', message: 'DB not connected' });
  }
});

connect().then(() => {
  app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
});

