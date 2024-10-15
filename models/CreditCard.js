// models/CreditCard.js
const mongoose = require('mongoose');

const CreditCardSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' }, // Reference to the user who owns the card
    cardType: { type: String, required: true }, // Type of card (e.g., Visa, Mastercard)
    balance: { type: Number, required: true }, // Current balance on the card
    limit: { type: Number, required: true }, // Credit limit
    dueDate: { type: Date, required: true } // Due date for payments
});

module.exports = mongoose.model('CreditCard', CreditCardSchema);
