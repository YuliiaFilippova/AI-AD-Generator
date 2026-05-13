import { useState } from "react";
import API from "../services/api";

function ResultViewer({ result }) {
  const [scores, setScores] = useState({
    descriptiveness: 3,
    objectivity: 3,
    accuracy: 3,
    clarity: 3,
  });

  const [feedback, setFeedback] = useState("");

  const handleChange = (field, value) => {
    setScores({
      ...scores,
      [field]: value,
    });
  };

  const submitEvaluation = async () => {
    try {
      await API.post("/evaluate", {
        job_id: result.job_id,
        ...scores,
        feedback,
      });

      alert("Evaluation submitted!");
    } catch (err) {
      console.error(err);
      alert("Failed to submit evaluation");
    }
  };

  return (
    <div style={{ marginTop: "50px" }}>
      <h2>Generated Video with Audio Descriptions</h2>

      <video
        width="800"
        controls
        src={`http://127.0.0.1:8000${result.video_url}`}
        style={{
          borderRadius: "12px",
          marginTop: "20px",
        }}
      />

      <div style={{ marginTop: "20px" }}>
        <a
          href={`http://127.0.0.1:8000${result.video_url}`}
          target="_blank"
        >
          Download Video
        </a>
      </div>

      <div style={{ marginTop: "50px" }}>
        <h2>Evaluation Form</h2>

        <EvaluationSlider
          label="Descriptiveness"
          value={scores.descriptiveness}
          onChange={(v) => handleChange("descriptiveness", v)}
        />

        <EvaluationSlider
          label="Objectivity"
          value={scores.objectivity}
          onChange={(v) => handleChange("objectivity", v)}
        />

        <EvaluationSlider
          label="Accuracy"
          value={scores.accuracy}
          onChange={(v) => handleChange("accuracy", v)}
        />

        <EvaluationSlider
          label="Clarity"
          value={scores.clarity}
          onChange={(v) => handleChange("clarity", v)}
        />

        <div style={{ marginTop: "30px" }}>
          <textarea
            rows="6"
            placeholder="Optional qualitative feedback..."
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
            style={{
              width: "600px",
              padding: "12px",
              fontSize: "15px",
            }}
          />
        </div>

        <button
          onClick={submitEvaluation}
          style={{
            marginTop: "20px",
            padding: "14px 24px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Submit Evaluation
        </button>
      </div>
    </div>
  );
}

function EvaluationSlider({ label, value, onChange }) {
  return (
    <div style={{ marginTop: "25px" }}>
      <div style={{ marginBottom: "8px" }}>
        <strong>{label}</strong>: {value}
      </div>

      <input
        type="range"
        min="1"
        max="5"
        step="1"
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        style={{ width: "400px" }}
      />

      <div style={{ fontSize: "14px", color: "#666" }}>
        1 = Poor, 5 = Excellent
      </div>
    </div>
  );
}

export default ResultViewer;