import React from "react";
import { Button } from "../components/button";

function LogoutButton() {
  const handleLogout = async () => {
    try {
      const response = await fetch("http://localhost:8000/auth/logout", {
        method: "POST",
        credentials: "include",
      });
      const data = await response.json();
      console.log(data.message);
      // Clear client-side tokens
      localStorage.removeItem("access_token");
      //redirect to /login
      window.location.href = "/login";
    } catch (err) {
      console.error("Logout failed: ", err);
    }
  };
  return (
    <Button
      onclick={handleLogout}
      className="text-sm text-red-600 hover:underline"
    >
      Logout
    </Button>
  );
}

export default LogoutButton;
