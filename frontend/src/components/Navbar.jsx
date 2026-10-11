import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar">
      <NavLink to="/" className="brand">Career Analyzer</NavLink>
      <div className="nav-links">
        <NavLink to="/upload">Upload</NavLink>
        <NavLink to="/results">Results</NavLink>
        <NavLink to="/roadmap">Roadmap</NavLink>
      </div>
    </nav>
  );
}