const express = require('express');
const passport = require('passport');
const session = require('express-session');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const moment = require('moment');
const User = require('./models/User'); // Assuming you already have the User model
const CreditCard = require('./models/CreditCard'); // CreditCard model import
require('dotenv').config();

// Initialize Express App
const app = express();

// Set view engine to EJS
app.set('view engine', 'ejs');

// Serve static files from the public directory
app.use(express.static('public'));

// Express body parser to handle form submissions
app.use(express.urlencoded({ extended: true }));

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));

// Express session for authentication
app.use(session({
    secret: 'secret',
    resave: false,
    saveUninitialized: false
}));

// Passport middleware for authentication
app.use(passport.initialize());
app.use(passport.session());

// Passport config (Google OAuth setup)
require('./config/passport')(passport);

// Routes
app.use('/', require('./routes/auth')); // Authentication routes

// Dashboard Route (Shows credit cards, spending chart, and add card form)
app.get('/dashboard', async (req, res) => {
    if (!req.isAuthenticated()) {
        return res.redirect('/');
    }

    try {
        // Fetch the user's credit cards from MongoDB
        const cards = await CreditCard.find({ userId: req.user._id });

        // Dummy spending data for the chart (replace with real data if needed)
        const spendingData = {
            labels: ['Groceries', 'Utilities', 'Entertainment', 'Others'], // Categories
            data: [300, 150, 200, 100] // Example spending amounts
        };

        // Render the dashboard with user details, credit cards, and spending data
        res.render('dashboard', { user: req.user, cards, spendingData });
    } catch (error) {
        console.error('Error fetching credit cards:', error);
        res.redirect('/');
    }
});

// Add a New Credit Card Route (handles form submissions)
app.post('/cards/add', async (req, res) => {
    if (!req.isAuthenticated()) {
        return res.redirect('/');
    }

    try {
        const { cardType, balance, limit, dueDate } = req.body;

        // Create a new credit card and save to the database
        const newCard = new CreditCard({
            userId: req.user._id, // Associate the card with the logged-in user
            cardType,
            balance,
            limit,
            dueDate: new Date(dueDate) // Convert due date string to a Date object
        });

        await newCard.save(); // Save the card to the database

        // Redirect to the dashboard after adding the card
        res.redirect('/dashboard');
    } catch (error) {
        console.error('Error adding credit card:', error);
        res.redirect('/dashboard');
    }
});

// Logout route
app.get('/logout', (req, res) => {
    req.logout(() => {
        res.redirect('/');
    });
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
