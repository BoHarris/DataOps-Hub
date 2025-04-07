import React, { useState } from "react";
import { Card, CardContent } from "../components/card";
import { Button } from "../components/button";
import { Input } from "../components/input";

export default function PiiSentinelUI() {
  const [file, setFile] = useState(null);
  const [piiColumns, setPiiColumns] = useState([]);
  const [riskScore, setRiskScore] = useState(null);
  const [redactedFile, setRedactedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  // Reset state when a new file is selected
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setPiiColumns([]);
    setRiskScore(null);
    setRedactedFile(null);
    setError(null);
  };

  // Upload file and handle errors with proper feedback
  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    console.log("Uploading file:", file);

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.statusText}`);
      }

      const data = await res.json();
      console.log("Response data:", data);
      setPiiColumns(data.pii_columns);
      setRiskScore(data.risk_score);
      setRedactedFile(data.redacted_file);
    } catch (error) {
      console.error("Error uploading file:", error);
      setError(
        error.message.includes("Network")
          ? "Network error. Please check your connection."
          : "Failed to scan file. Please try again."
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-6 p-6">
      <h1 className="text-3xl font-bold">
        🔐 PII Sentinel – Privacy as a Service
      </h1>

      <Card className="w-full max-w-xl">
        <CardContent className="p-6 flex flex-col gap-4">
          <div className="flex flex-col items-center gap-4">
            {/* Accessibility improvement: meaningful label */}
            <label htmlFor="file-upload" className="font-medium">
              Upload CSV File
            </label>
            <Input
              id="file-upload"
              type="file"
              accept=".csv"
              required
              onChange={handleFileChange}
            />

            <Button onClick={handleUpload} disabled={!file || uploading}>
              {uploading ? "Scanning..." : "Scan File for PII"}
            </Button>

            {/* Improved loading feedback */}
            {uploading && (
              <p className="italic text-sm">Uploading and analyzing file...</p>
            )}

            {/* Error message now visible when NOT uploading */}
            {error && !uploading && (
              <p className="text-red-600 font-medium">{error}</p>
            )}

            {/* Optional message when no PII columns found */}
            {piiColumns.length === 0 && !uploading && !error && file && (
              <p className="text-green-600 font-medium">
                No PII columns detected.
              </p>
            )}
          </div>
        </CardContent>
      </Card>

      {piiColumns.length > 0 && (
        <Card className="w-full max-w-xl">
          <CardContent className="p-6">
            <h2 className="text-xl font-semibold mb-2">
              🔎 PII Columns Detected:
            </h2>
            <ul className="list-disc pl-6 text-red-600">
              {piiColumns.map((col) => (
                <li key={col}>{col}</li>
              ))}
            </ul>
            <p className="mt-4 font-medium">
              Risk Score:{" "}
              <span className="px-2 py-1 bg-yellow-100 rounded text-yellow-100">
                {" "}
                {riskScore}
              </span>
            </p>
            {redactedFile && (
              <a
                href={`http://localhost:8000/${redactedFile}`}
                download
                className="text-blue-600 underline mt-2 inline-block"
              >
                📥 Download Redacted CSV
              </a>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
