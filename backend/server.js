import express from 'express';
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';
import cors from 'cors';
import multer from 'multer';

import fetch from 'node-fetch';

const app = express();
const port = process.env.PORT || 5001;

app.use(express.json());
app.use(cors());

dotenv.config() 

// Configure Multer for in-memory storage
const storage = multer.memoryStorage();
const upload = multer({ storage });


// Initialize Google Generative AI
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

// Route to handle voice file uploads
app.post("/api/voice", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file uploaded" });
    }

    const audioBuffer = req.file.buffer; // File data in memory

    // Send file to Hugging Face Whisper model
    const hfResponse = await fetch("https://api-inference.huggingface.co/models/openai/whisper-large", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.HUGGINGFACE_API_KEY}`,
        "Content-Type": "application/octet-stream",
      },
      body: audioBuffer, // Pass the buffer
    });

    if (!hfResponse.ok) {
      // console.log(hfResponse)
      throw new Error("Failed to process audio with Hugging Face API");
    }

    const transcription = await hfResponse.json();

    // Send the transcription result back to the frontend and console log it
    res.status(200).json({ transcription });

  } catch (error) {
    console.error("Error processing voice input:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});


// API route to handle grant submissions
app.post('/api/grant', async (req, res) => {
  const { grant_title, objective, audience, funding, details, transcription } = req.body;

  if (!grant_title || !objective || !audience || !funding || !details || transcription) {
    return res.status(400).json({ error: "All fields are required" });
  }

  console.log(transcription)
  try {
    // Create a structured prompt
    const prompt = `
      Grant Title: ${grant_title}
      Objective: ${objective}
      Target Audience: ${audience}
      Funding Request: ${funding}
      Project Description: ${details}
      
      Transcription from Voice Input: ${transcription}

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
