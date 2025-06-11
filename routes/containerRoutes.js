const express = require('express');
const QRCode = require('qrcode');
const ContainerService = require('../services/containerService');

const router = express.Router();

// List containers
router.get('/', async (req, res) => {
  const containers = await ContainerService.listContainers();
  res.json(containers);
});

// Create container
router.post('/', async (req, res) => {
  try {
    const container = await ContainerService.createContainer(req.body);
    res.status(201).json(container);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Update container quantity or other fields
router.patch('/:id', async (req, res) => {
  try {
    const container = await ContainerService.updateContainer(req.params.id, req.body);
    if (!container) return res.status(404).json({ error: 'Container not found' });
    res.json(container);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Delete container
router.delete('/:id', async (req, res) => {
  try {
    const container = await ContainerService.deleteContainer(req.params.id);
    if (!container) return res.status(404).json({ error: 'Container not found' });
    res.json({ message: 'Container deleted' });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// Serve QR code image for the container
router.get('/:id/qrcode', async (req, res) => {
  try {
    const container = await ContainerService.getContainerById(req.params.id);
    if (!container) return res.status(404).json({ error: 'Container not found' });
    res.type('png');
    await QRCode.toFileStream(res, container.uuid);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
