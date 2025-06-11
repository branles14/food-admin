const { MongoMemoryServer } = require('mongodb-memory-server');
(async () => {
  try {
    const mongod = await MongoMemoryServer.create();
    console.log(mongod.getUri());
    const cleanup = async () => {
      await mongod.stop();
      process.exit(0);
    };
    process.on('SIGINT', cleanup);
    process.on('SIGTERM', cleanup);
    // Keep process running
    await new Promise(() => {});
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
})();
