// routes/creditCard.js
const express = require('express');
const CreditCard = require('../models/CreditCard');
const router = express.Router();

// Middleware to check if user is authenticated
function ensureAuthenticated(req, res, next) {
    if (req.isAuthenticated()) {
        return next();
    } else {
        res.redirect('/');
    }
}

// Add new credit card
router.post('/cards/add', ensureAuthenticated, (req, res) => {
    const { cardNumber, cardType, balance, dueDate, limit } = req.body;
    const newCard = new CreditCard({
        userId: req.user._id,
        cardNumber,
        cardType,
        balance,
        dueDate,
        limit
    });
    newCard.save().then(card => res.json(card));
});

// View all cards
router.get('/cards', ensureAuthenticated, (req, res) => {
    CreditCard.find({ userId: req.user._id })
        .then(cards => res.json(cards));
});

module.exports = router;
