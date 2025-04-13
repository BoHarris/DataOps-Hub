import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-gray-900 title-white px-4 py-4 py-3 shadow-ms flex justify-Center min-h-screen pt-24">
      <div className="text-xl font-bold tracking-wide">
        <Link to="/">
          ALEX<span className="text-blue-400">.ai</span>
        </Link>
      </div>
      <div className="space-x-4">
        <Link to="/" className="hover:text-blue-300">
          Home
        </Link>
        <Link to="/upload" className="hover:text-blue-300">
          Upload
        </Link>
        <Link to="/register" className="hover:text-blue-300">
          Register
        </Link>
        <Link to="/login" className="hover:text-blue-300">
          Login
        </Link>
        {/* Future links for other pages */}
        {/* <Link to="/about" className="hover:text-blue-300">About</Link> */}
        {/* <Link to="/contact" className="hover:text-blue-300">Contact</Link> */}
        {/* <Link to="/audit" className="hover:text-blue-300">Audit</Link> */}
        {/* <Link to="/settings" className="hover:text-blue-300">Settings</Link> */}
      </div>
    </nav>
  );
}
