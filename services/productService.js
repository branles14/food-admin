const Product = require('../models/product');

async function createProduct(data) {
  const product = new Product(data);
  return product.save();
}

async function getProductById(id) {
  return Product.findById(id).exec();
}

async function listProducts() {
  return Product.find().exec();
}

async function updateProduct(id, data) {
  return Product.findByIdAndUpdate(id, data, { new: true }).exec();
}

async function deleteProduct(id) {
  return Product.findByIdAndDelete(id).exec();
}

module.exports = {
  createProduct,
  getProductById,
  listProducts,
  updateProduct,
  deleteProduct,
};
