import React from "react";
import PiiSentinelUI from "../components/PiiSentinelUI";
function Upload() {
  return (
    <div className="flex flex-col gap-4 items-center justify-center py-12">
      <h1 className="text-2xl font-bold">Upload</h1>
      <p className="text-sm text-gray-700">Please add your CSV file here.</p>
      <PiiSentinelUI />
    </div>
  );
}

export default Upload;
