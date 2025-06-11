const Container = require('../models/container');

async function createContainer(data) {
  const container = new Container(data);
  return container.save();
}

async function getContainerById(id) {
  return Container.findById(id).populate('product').exec();
}

async function listContainers() {
  return Container.find().populate('product').exec();
}

async function updateContainer(id, data) {
  return Container.findByIdAndUpdate(id, data, { new: true }).exec();
}

async function deleteContainer(id) {
  return Container.findByIdAndDelete(id).exec();
}

module.exports = {
  createContainer,
  getContainerById,
  listContainers,
  updateContainer,
  deleteContainer,
};
