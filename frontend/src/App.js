import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PiiSentinelUI from "./components/PiiSentinelUI";
import Register from "./components/RegisterForm";

// Ensure these components exist and are correctly exported from their respective files.

function App() {
  return (
    <Router>
      <main className="min-h-screen bg-white text-gray-900 p-6">
        <Routes>
          <Route path="/" element={<PiiSentinelUI />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
