require('dotenv').config();
const { connect } = require('./db');
const ProductService = require('./services/productService');
const ContainerService = require('./services/containerService');

async function run() {
  await connect();

  const product = await ProductService.createProduct({
    name: 'Tomato Sauce',
    upc: '012345678905',
    uuid: '550e8400-e29b-41d4-a716-446655440000',
    nutrition: {
      calories: 80,
      fat: 1,
      protein: 2,
      carbs: 15,
    },
  });

  await ContainerService.createContainer({
    product: product._id,
    quantity: 2,
    opened: false,
    remaining: 2,
  });

  console.log('Seed data inserted');
  process.exit();
}

run().catch(err => {
  console.error(err);
  process.exit(1);
});
