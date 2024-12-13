import React, { useState, useEffect } from "react";
import InputForm from "./InputForm";
import OutputDisplay from "./OutputDisplay";

function Body() {
  const [aiOutput, setAiOutput] = useState(""); // Store AI-generated output
  const [socket, setSocket] = useState(null);   // Store WebSocket instance

  useEffect(() => {
    // Open a WebSocket connection
    const ws = new WebSocket("ws://localhost:8080");
    setSocket(ws);

    // Listen for messages from the WebSocket
    ws.onmessage = (event) => {
      setAiOutput((prev) => prev + event.data); // Append received data to aiOutput
    };

    // Cleanup: close WebSocket connection on unmount
    return () => {
      ws.close();
    };
  }, []);

  const handleFormSubmit = async (data) => {
    try {
      // Prepare form data for submission
      const formData = new FormData();
      formData.append("grant_title", data.grant_title);
      formData.append("objective", data.objective);
      formData.append("audience", data.audience);
      formData.append("funding", data.funding);
      formData.append("details", data.details);
      if (data.file) {
        formData.append("file", data.file);
      }

      // Send data to the backend
      const response = await fetch("http://localhost:5001/api/grant", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to submit grant data");
      }

      console.log("Form submitted successfully");
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <section className="flex justify-center my-8">
      <div className="w-1/2 p-4">
        <InputForm onSubmit={handleFormSubmit} />
      </div>

      <div className="w-1/2 p-4">
        <OutputDisplay aiOutput={aiOutput} /> {/* Pass aiOutput as a prop */}
      </div>
    </section>
  );
}

export default Body;
