import { useState } from "react";
import UploadForm from "../components/UploadForm";
import ResultViewer from "../components/ResultViewer";

export default function HomePage() {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: 40 }}>
      <h1>AI Ad Generator</h1>

      <UploadForm onResult={setResult} />

      {result && <ResultViewer result={result} />}
    </div>
  );
}