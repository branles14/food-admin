const { Schema, model } = require('mongoose');

const NutritionSchema = new Schema(
  {
    calories: Number,
    fat: Number,
    protein: Number,
    carbs: Number,
  },
  { _id: false }
);

const ProductSchema = new Schema(
  {
    name: { type: String, required: true },
    upc: { type: String, required: true, unique: true },
    uuid: { type: String, required: true, unique: true },
    nutrition: NutritionSchema,
  },
  { timestamps: true }
);

module.exports = model('Product', ProductSchema);
