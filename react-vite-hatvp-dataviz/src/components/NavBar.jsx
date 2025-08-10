import { Link } from 'react-router-dom';

function NavBar() {
  return (
    <nav className="bg-blue-600 text-white px-4 py-2">
      <ul className="flex gap-4">
        <li><Link to="/">Organizations</Link></li>
        <li><Link to="/age">Age</Link></li>
        <li><Link to="/pyramid">Age Pyramid</Link></li>
        <li><Link to="/gender">Gender</Link></li>
        <li><Link to="/delay">Delays</Link></li>
        <li className="ml-auto"><Link to="/about">About</Link></li>
      </ul>
    </nav>
  );
}

export default NavBar;
