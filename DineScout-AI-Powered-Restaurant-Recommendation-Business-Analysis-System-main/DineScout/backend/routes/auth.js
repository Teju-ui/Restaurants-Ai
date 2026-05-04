const express = require("express");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
require("dotenv").config();

const User = require("../models/User");

const router = express.Router();


// ================= REGISTER =================
router.post("/register", async (req, res) => {
  try {
    const { username, email, password, role } = req.body;

    // validate fields
    if (!username || !email || !password || !role) {
      return res.status(400).json({ message: "All fields required" });
    }

    // validate role
    if (!["user", "owner"].includes(role)) {
      return res.status(400).json({ message: "Invalid role" });
    }

    // check email exists
    const emailExist = await User.findOne({ email });
    if (emailExist) {
      return res.status(400).json({ message: "Email already exists" });
    }

    // check username exists (IMPORTANT FIX)
    const usernameExist = await User.findOne({ username });
    if (usernameExist) {
      return res.status(400).json({ message: "Username already exists" });
    }

    // hash password
    const hash = await bcrypt.hash(password, 10);

    // create user
    const user = new User({
      username,
      email,
      password: hash,
      role,
      verified: true
    });

    await user.save();

    return res.status(201).json({ message: "User registered successfully" });

  } catch (err) {
    console.log("Register Error:", err);
    return res.status(500).json({ message: err.message, stack: err.stack });
  }
});


// ================= LOGIN =================
// ALWAYS use email login (recommended)
router.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: "All fields required" });
    }

    const user = await User.findOne({ 
      $or: [{ email: email }, { username: email }] 
    });

    if (!user) {
      return res.status(400).json({ message: "User not found" });
    }

    const match = await bcrypt.compare(password, user.password);

    if (!match) {
      return res.status(400).json({ message: "Wrong password" });
    }

    const token = jwt.sign(
      { id: user._id, role: user.role },
      process.env.JWT_SECRET,
      { expiresIn: "1d" }
    );

    return res.json({
      token,
      role: user.role,
      username: user.username
    });

  } catch (err) {
    console.log("Login Error:", err);
    return res.status(500).json({ message: "Server error" });
  }
});

module.exports = router;