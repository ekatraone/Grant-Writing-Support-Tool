import React from "react";
import ReactMarkdown from "react-markdown";

function OutputDisplay({ aiOutput, isLoading }) {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">AI Output</h2>
      <div
        className="border p-4 bg-gray-100 overflow-auto"
        style={{ maxHeight: "600px", wordBreak: "break-word" }}
      >
        {isLoading ? (
          <p>Loading... Please wait while the AI processes your request.</p>
        ) : aiOutput ? (
          <ReactMarkdown className="font-mono">{aiOutput}</ReactMarkdown> /* Render Markdown properly */
        ) : (
          <p>No output yet. Submit a grant to see the result.</p>
        )}
      </div>
    </div>
  );
}

export default OutputDisplay;
