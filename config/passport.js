const GoogleStrategy = require('passport-google-oauth20').Strategy;
const User = require('../models/User'); // Assuming User model is already set up

module.exports = function(passport) {
    passport.use(new GoogleStrategy({
        clientID: process.env.GOOGLE_CLIENT_ID,
        clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        callbackURL: "/auth/google/callback"
    },
    async (accessToken, refreshToken, profile, done) => {
        // Find or create user in database
        const { id, displayName, emails } = profile;
        try {
            let user = await User.findOne({ googleId: id });
            if (!user) {
                user = new User({
                    googleId: id,
                    displayName: displayName,
                    email: emails[0].value
                });
                await user.save();
            }
            return done(null, user);
        } catch (err) {
            return done(err, false);
        }
    }));

    passport.serializeUser((user, done) => {
        done(null, user.id);
    });

    passport.deserializeUser((id, done) => {
        User.findById(id, (err, user) => {
            done(err, user);
        });
    });
};
