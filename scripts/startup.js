require('dotenv').config();
const { spawn } = require('child_process');
const { MongoMemoryServer } = require('mongodb-memory-server');

async function start() {
  let mongod;
  if (!process.env.MONGODB_URI) {
    mongod = await MongoMemoryServer.create();
    process.env.MONGODB_URI = mongod.getUri();
    console.log(`Started in-memory MongoDB at ${process.env.MONGODB_URI}`);
  }

  const server = spawn('node', ['index.js'], {
    stdio: 'inherit',
    env: process.env,
  });

  server.on('exit', code => {
    if (mongod) mongod.stop();
    process.exit(code);
  });
}

start().catch(err => {
  console.error(err);
  process.exit(1);
});
