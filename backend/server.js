const express = require('express');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();
const cors = require('cors');

const app = express();
const port = 5001;

app.use(express.json());
app.use(cors());

// Initialize Google Generative AI
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

// API route to handle grant submissions
app.post('/api/grant', async (req, res) => {
  const { grant_title, objective, audience, funding, details } = req.body;

  if (!grant_title || !objective || !audience || !funding || !details) {
    return res.status(400).json({ error: "All fields are required" });
  }

  try {
    // Create a structured prompt
    const prompt = `
      Grant Title: ${grant_title}
      Objective: ${objective}
      Target Audience: ${audience}
      Funding Request: ${funding}
      Project Description: ${details}
      
      Based on this information, write a brief grant proposal with the key objectives, target audience, and funding goals.
      
      Problem Statement: Clearly define the problem or issue your project addresses.
      leave empty line afer this
      Project Goals and Objectives: Outline the specific, measurable, achievable, relevant, and time-bound (SMART) goals and objectives of your project.
      Methodology: Describe the approach you will take to achieve your project goals, including specific activities, strategies, and interventions.
      Timeline: Provide a detailed timeline for the implementation of your project, including key milestones and deadlines.
      Evaluation Plan: Explain how you will measure the success of your project, including specific metrics, data collection methods, and reporting procedures.
      Budget: Present a detailed budget outlining the costs associated with your project, including personnel, materials, equipment, and other expenses.
      Sustainability Plan: Describe how you will ensure the long-term sustainability of your project beyond the initial funding period.

    `;

    const aiResponse = await model.generateContent(prompt);

    // Extract the text response correctly
    const responseText = aiResponse?.response?.candidates[0]?.content?.parts[0]?.text;

    if (!responseText) {
      throw new Error("Failed to extract AI response.");
    }

    res.status(200).json({ message: "AI response generated.", response: responseText });


  } catch (error) {
    console.error('Error in /api/grant:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
