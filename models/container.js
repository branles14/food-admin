const { Schema, model, Types } = require('mongoose');

const ContainerSchema = new Schema(
  {
    product: { type: Types.ObjectId, ref: 'Product', required: true },
    quantity: { type: Number, required: true },
    opened: { type: Boolean, default: false },
    remaining: { type: Number },
  },
  { timestamps: true }
);

module.exports = model('Container', ContainerSchema);
