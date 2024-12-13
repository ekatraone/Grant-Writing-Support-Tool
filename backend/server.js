// const express = require('express');
// const cors = require('cors');
// const bodyParser = require('body-parser');
// const { GoogleGenerativeAI } = require('@google/generative-ai');
// require('dotenv').config();

// const app = express();
// const port = 5001;

// // Middleware
// app.use(cors());
// app.use(bodyParser.json());

// // Initialize Google Generative AI
// const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);
// const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

// app.get('/', (req, res) => {
//     res.send('Hello, World!');
// });

// // POST route to handle grant proposal requests
// app.post('/api/grant', async (req, res) => {
//     const { grant_title, objective, audience, funding, details } = req.body;

//     // Construct the prompt
//     const prompt = `Write a compelling grant proposal for the **${grant_title}** project. 
//         The objective of this project is to **${objective}**. 
//         The target audience for this project is **${audience}**. 
//         The estimated funding amount required for this project is **${funding}**. 
//         **Project Details:** ${details}`;

//     try {
//         const response = await model.generateContent(prompt);
//         const aiContent = response.response.text();

//         res.json({
//             message: "Data received successfully",
//             aiContent: aiContent
//         });
//     } catch (error) {
//         console.error(error);
//         res.status(500).json({ error: 'Error generating AI content' });
//     }
// });

// app.listen(port, () => {
//     console.log(`Server running on http://localhost:${port}`);
// });









// const express = require('express');
// const EventSource = require('eventsource');
// const cors = require('cors');
// const bodyParser = require('body-parser');
// const { GoogleGenerativeAI } = require('@google/generative-ai');
// require('dotenv').config();

// const app = express();
// const port = 5001;

// // Middleware
// app.use(cors());
// app.use(bodyParser.json());

// // Initialize Google Generative AI
// const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);
// const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

// app.get('/', (req, res) => {
//   res.send('Hello, World!');
// });

// // POST route to handle grant proposal requests with SSE
// app.post('/api/grant', (req, res) => {
//   const { grant_title, objective, audience, funding, details } = req.body;

//   res.setHeader('Content-Type', 'text/event-stream');
//   res.setHeader('Cache-Control', 'no-cache');

// //   const eventSource = new EventSource();

//   const generateGrantStory = async () => {
//     const prompt = `Write a compelling grant proposal for the **${grant_title}** project. 
//       The objective of this project is to **${objective}**. 
//       The target audience for this project is **${audience}**. 
//       The estimated funding amount required for this project is **${funding}**. 
//       **Project Details:** ${details}`;

//     try {
//       for await (const chunk of model.generateContentStream(prompt)) {
//         eventSource.write(`data: ${chunk.text()}\n\n`);
//       }
//     } catch (error) {
//       console.error(error);
//       eventSource.write('data: Error generating story\n\n');
//     } finally {
//       eventSource.close();
//     }
//   };

//   generateGrantStory();

//   req.on('close', () => {
//     eventSource.close();
//   });
// });

// app.listen(port, () => {
//   console.log(`Server running on http://localhost:${port}`);
// });



const express = require('express');
const WebSocket = require('ws');
const multer = require('multer');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();
const cors = require('cors');

const app = express();
const port = 5001;
const wss = new WebSocket.Server({ port: 8080 });
const upload = multer(); // Middleware for handling file uploads

app.use(express.json());

app.use(cors({
    origin: 'http://localhost:3000' // Replace with your frontend's URL
  }));

// Enable CORS
app.use(cors());


// Initialize Google Generative AI
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_GENERATIVE_AI_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

// API route to handle grant submissions
app.post('/api/grant', upload.single('file'), async (req, res) => {
  const { grant_title, objective, audience, funding, details } = req.body;
  const file = req.file; // Uploaded file (optional)

  try {
    // Create a structured prompt
    const prompt = `
      Grant Title: ${grant_title}
      Objective: ${objective}
      Audience: ${audience}
      Funding: ${funding}
      Details: ${details}
      File: ${file ? file.originalname : 'No file uploaded'}
    `;

    // Broadcast the prompt to all WebSocket clients
    wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(prompt);
      }
    });

    res.status(200).json({ message: 'Prompt sent successfully.' });
  } catch (error) {
    console.error('Error in /api/grant:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// WebSocket connection handling
wss.on('connection', (ws) => {
    console.log('Client connected');
  
    ws.on('message', async (message) => {
      console.log('Received from client:', message);
      try {
        // Generate content with the AI model
        for await (const chunk of model.generateContentStream(message)) {
          ws.send(chunk.text); // Send AI-generated response in real-time
        }
      } catch (error) {
        console.error(error);
        ws.send(`Error: ${error.message}`); // Send error message to the client
      }
    });
  
    ws.on('close', () => {
      console.log('Client disconnected');
    });
  });
  

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});