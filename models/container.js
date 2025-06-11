const { Schema, model, Types } = require('mongoose');
const { v4: uuidv4 } = require('uuid');

const ContainerSchema = new Schema(
  {
    product: { type: Types.ObjectId, ref: 'Product', required: true },
    uuid: { type: String, default: uuidv4, unique: true },
    quantity: { type: Number, required: true },
    opened: { type: Boolean, default: false },
    remaining: { type: Number },
  },
  { timestamps: true }
);

module.exports = model('Container', ContainerSchema);
