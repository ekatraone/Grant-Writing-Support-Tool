import React, { useState, useEffect } from "react";

function OutputDisplay() {
  const [aiOutput, setAiOutput] = useState(""); // Store AI-generated output

  useEffect(() => {
    // Open a WebSocket connection
    const ws = new WebSocket("ws://localhost:8080");

    // Listen for messages from the WebSocket
    ws.onmessage = (event) => {
      console.log("Received from WebSocket:", event.data); // Log WebSocket data
      setAiOutput((prev) => prev + event.data + "\n"); // Append received data to aiOutput
    };

    // Cleanup: close WebSocket connection on unmount
    return () => {
      ws.close();
    };
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">AI Output</h2>
      <div className="border p-4 bg-gray-100">
        {aiOutput ? (
          <pre>{aiOutput}</pre> // Display AI output
        ) : (
          <p>No output yet. Waiting for AI response...</p> // Placeholder text
        )}
      </div>
    </div>
  );
}

export default OutputDisplay;
