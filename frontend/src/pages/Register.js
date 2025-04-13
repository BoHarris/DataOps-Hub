import React from "react";
import RegisterForm from "../components/RegisterForm"; // Ensure this file exists and exports a RegisterForm component
function Register() {
  return (
    <div className="flex flex-col gap-4 items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold">Register</h1>
      <p className="text-sm text-gray-700">
        Please fill in the form below to create an account.
      </p>
      <RegisterForm />
    </div>
  );
}

export default Register;
