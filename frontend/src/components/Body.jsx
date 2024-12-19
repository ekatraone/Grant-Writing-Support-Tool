import React, { useState } from "react";
import InputForm from "./InputForm";
import OutputDisplay from "./OutputDisplay";

function Body() {
  const [aiOutput, setAiOutput] = useState(""); // Store AI-generated output
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const handleFormSubmit = async (data) => {
    setIsLoading(true); // Show loading indicator
    setAiOutput(""); // Clear previous AI output

    try {
      console.log("Submitting data to backend:", data);

      const response = await fetch("https://grant-writing-support-tool-1.onrender.comhttps://grant-writing-support-tool-1.onrender.com/api/grant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch AI response.");
      }

      const result = await response.json();
      console.log("Received AI response from backend:", result);
      setAiOutput(result.response); // Update with AI response
    } catch (error) {
      console.error("Error while fetching AI response:", error);
    } finally {
      setIsLoading(false); // Hide loading indicator
    }
  };

  return (
    <section className="flex justify-center my-8">
      <div className="w-3/12  p-4">
        <InputForm onSubmit={handleFormSubmit} />
      </div>

      <div className="w-7/12 p-4">
        <OutputDisplay aiOutput={aiOutput} isLoading={isLoading} />
      </div>
    </section>
  );
}

export default Body;
