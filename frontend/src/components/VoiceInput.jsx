import React, { useState } from "react";
import { ReactMic } from "react-mic";

function VoiceInput({ onTranscription }) {
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleStopRecording = async (recordedBlob) => {
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", recordedBlob.blob, "voice-note.wav");

      const response = await fetch("http://localhost:5001/api/voice", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to fetch transcription.");
      }

      const result = await response.json();
      console.log("Received transcription:", result);

      if (onTranscription) {
        onTranscription(result.transcription); // Pass the transcription to the parent component
      }
    } catch (error) {
      console.error("Error while processing voice note:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="voice-input bg-white p-6 rounded-lg shadow-lg border border-gray-200 mt-3">
      <h3 className="text-xl font-semibold mb-4 text-center">Record Voice Note</h3>
      
      <ReactMic
        record={isRecording}
        onStop={handleStopRecording}
        mimeType="audio/wav"
        strokeColor="#000000"
        // backgroundColor="#FF4081"
        className="w-full h-48 mb-4 rounded-lg"
      />
      
      <div className="flex justify-center gap-4 mt-4">
        <button
          className="px-6 py-3 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          onClick={() => setIsRecording(true)}
          disabled={isRecording}
        >
          Start Recording
        </button>
        
        <button
          className="px-6 py-3 bg-red-600 text-white rounded-lg shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500"
          onClick={() => setIsRecording(false)}
          disabled={!isRecording}
        >
          Stop Recording
        </button>
      </div>
      
      {isLoading && (
        <p className="text-gray-500 mt-4 text-center">Processing voice input...</p>
      )}
    </div>
  );
}

export default VoiceInput;