require('dotenv').config();
const fs = require('fs');
const path = require('path');
const QRCode = require('qrcode');
const { connect } = require('../db');
const ContainerService = require('../services/containerService');

async function run() {
  await connect();
  const containers = await ContainerService.listContainers();
  const dir = path.join(__dirname, '..', 'qrcodes');
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir);
  }
  for (const c of containers) {
    const file = path.join(dir, `${c.uuid}.png`);
    await QRCode.toFile(file, c.uuid);
    console.log('Generated QR for', c.uuid);
  }
  process.exit();
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
