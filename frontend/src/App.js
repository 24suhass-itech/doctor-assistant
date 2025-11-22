import React, { useState } from "react";
import SpeechRecognition, { useSpeechRecognition } from "react-speech-recognition";

function App() {
  const [qr, setQr] = useState("");
  const [disease, setDisease] = useState("");
  const [cleaned, setCleaned] = useState([]);

  const { transcript, resetTranscript } = useSpeechRecognition();

  if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
    return <div>Your browser does not support Speech Recognition.</div>;
  }

  const handleDiagnose = async () => {
    const res = await fetch("http://localhost:5000/diagnose", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symptoms: transcript }),
    });

    const data = await res.json();
    setDisease(data.disease);
    setCleaned(data.cleaned);
    setQr("data:image/png;base64," + data.qr);
  };

  return (
    <div style={{ padding: 40, background: "#eef5ff", minHeight: "100vh", fontFamily: "Arial" }}>
      <h1 style={{ color: "#1a4ba3" }}>🩺 Doctor Assistant Panel</h1>

      <div
        style={{
          background: "white",
          padding: 20,
          borderRadius: 10,
          boxShadow: "0 3px 10px rgba(0,0,0,0.1)",
          maxWidth: 700,
        }}
      >
        <h3> Speak Patient Symptoms</h3>

        <div
          style={{
            background: "#f1f5ff",
            padding: 15,
            borderRadius: 8,
            minHeight: 70,
            fontSize: 18,
          }}
        >
          {transcript || "Start speaking..."}
        </div>

        <button
          onClick={SpeechRecognition.startListening}
          style={{
            marginTop: 20,
            padding: "10px 25px",
            fontSize: 18,
            background: "#1a73e8",
            color: "white",
            borderRadius: 8,
            border: "none",
            cursor: "pointer",
          }}
        >
          🎙 Start Listening
        </button>

        <button
          onClick={() => {
            resetTranscript();
            setDisease("");
            setCleaned([]);
            setQr("");
          }}
          style={{
            marginLeft: 10,
            marginTop: 20,
            padding: "10px 25px",
            fontSize: 18,
            background: "#888",
            color: "white",
            borderRadius: 8,
            border: "none",
            cursor: "pointer",
          }}
        >
           Clear
        </button>

        <button
          onClick={handleDiagnose}
          style={{
            marginLeft: 10,
            marginTop: 20,
            padding: "10px 25px",
            fontSize: 18,
            background: "#0a991a",
            color: "white",
            borderRadius: 8,
            border: "none",
            cursor: "pointer",
          }}
        >
          🔍 Diagnose
        </button>

        {cleaned.length > 0 && (
          <div style={{ marginTop: 30 }}>
            <h3>Corrected Symptoms</h3>
            <ul style={{ fontSize: 18 }}>
              {cleaned.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </div>
        )}

        {disease && (
          <div style={{ marginTop: 30 }}>
            <h3> Predicted Disease</h3>
            <div
              style={{
                fontSize: 24,
                background: "#e6ffe6",
                padding: 15,
                borderRadius: 10,
                border: "1px solid #55c755",
                color: "#0a540a",
              }}
            >
              {disease}
            </div>
          </div>
        )}

        {qr && (
          <div style={{ marginTop: 30 }}>
            <h3>📲 Scan QR for Report</h3>
            <img src={qr} alt="QR Code" style={{ width: 220 }} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
