import { useState } from "react";
import API from "../services/api";

function UploadForm({ setResult }) {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [participantId, setParticipantId] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);

      const response = await API.post("/youtube", {
        url: youtubeUrl,
        participant_id: participantId,
      });

      setResult(response.data);

    } catch (err) {
      console.error(err);
      alert("Generation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "30px" }}>

      <input
        type="text"
        placeholder="Paste YouTube URL"
        value={youtubeUrl}
        onChange={(e) => setYoutubeUrl(e.target.value)}
        style={{
          width: "600px",
          padding: "14px",
          fontSize: "16px",
          marginRight: "10px",
        }}
      />

      <button
        onClick={handleSubmit}
        disabled={loading}
        style={{
          padding: "14px 24px",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        {loading ? "Generating..." : "Generate"}
      </button>

      {loading && (
        <div style={{ marginTop: "20px" }}>
          ⏳ Audio descriptions are being generated for your video...
        </div>
      )}
    </div>
  );
}

export default UploadForm;