import UploadForm from "./components/UploadForm";
import ResultViewer from "./components/ResultViewer";
import { useState } from "react";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>AI AD Generator</h1>

      <UploadForm setResult={setResult} />

      {result && <ResultViewer result={result} />}
    </div>
  );
}

export default App;