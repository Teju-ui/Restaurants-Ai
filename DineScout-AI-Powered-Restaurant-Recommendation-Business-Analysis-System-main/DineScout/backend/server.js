const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
const axios = require("axios");
const path = require("path");
require("dotenv").config();

const authRoutes = require("./routes/auth");
const restaurantRoutes = require("./routes/restaurant");

const app = express();


// ================= MIDDLEWARE =================
app.use(express.json());

// FIX: allow frontend + local dev + deployment
app.use(cors({
  origin: "*"
}));


// ================= API ROUTES =================
app.use("/api/auth", authRoutes);
app.use("/api/restaurants", restaurantRoutes);


// ================= OWNER ROUTES =================
app.get("/api/owner/meta", async (req, res) => {
  try {
    const r = await axios.get("http://127.0.0.1:7000/meta");
    res.json(r.data);
  } catch (err) {
    console.log("META ERROR:", err.message);
    res.status(500).json({ error: "Meta error" });
  }
});

app.post("/api/owner/market-analysis", async (req, res) => {
  try {
    const r = await axios.post(
      "http://127.0.0.1:7000/market-analysis",
      req.body
    );
    res.json(r.data);
  } catch (err) {
    console.log("ANALYSIS ERROR:", err.message);
    res.status(500).json({ error: "Analysis error" });
  }
});


// ================= FRONTEND =================
app.use(express.static(path.join(__dirname, "../frontend")));


// ================= MONGODB =================
if (process.env.MONGO_URI) {
  mongoose.connect(process.env.MONGO_URI, {
    dbName: "dinescout"
  })
  .then(() => console.log("MongoDB Connected ✅"))
  .catch(err => {
    console.log("Mongo Error:", err);
  });
} else {
  console.log("MONGO_URI is missing from Environment Variables!");
}


// ================= SERVER =================
// Export the Express API for Vercel instead of listening on a port
module.exports = app;

if (require.main === module) {
  const PORT = process.env.PORT || 5000;
  app.listen(PORT, () => {
    console.log(`Server running on port ${PORT} 🚀`);
  });
}