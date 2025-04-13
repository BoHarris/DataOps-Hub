// This code defines a Register component that provides a registration form for users to create an account. The form includes fields for email and password, and a button to submit the registration request. The component uses React hooks to manage state and handle user input.
// When the user clicks the "Register" button, an asynchronous function sends a POST request to the server with the email and password. The response message is displayed to the user. The component also handles loading state to disable the button while the request is in progress. The component is styled using Tailwind CSS classes for a clean and modern look.
import React, { useState } from "react";
import { Button } from "./button"; // Ensure this file exists and exports a Button component
import TextField from "./text_input"; // Ensure this file exists and exports a TextField component

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (Array.isArray(data.detail)) {
        const errors = data.detail.map((d) => d.msg).join(",");
        setMessage(errors);
      } else {
        setMessage(data.message || data.details || "Unknown Response");
      }
    } catch (err) {
      setMessage("Error registering user: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-4 items-center justify-center min-h-screen">
      <TextField
        id="email"
        label="Email"
        type="email"
        value={email}
        placeholder="you@example.com"
        onChange={(e) => setEmail(e.target.value)}
      />
      <TextField
        id="password"
        label="Password"
        type="password"
        value={password}
        placeholder="Enter your password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button onClick={handleRegister} disabled={loading}>
        {loading ? "Registering..." : "Register"}
      </Button>
      {message && <p className="text-sm text-gray-700">{message}</p>}
    </div>
  );
}
export default Register;
