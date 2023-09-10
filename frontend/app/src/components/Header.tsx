import React from "react";
import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header>
      <div className="container">
        <h1><Link to="/">Mijn Bonnetje</Link></h1>
        <nav>
          <ul>
            <li>
              <Link to="/receipts">Receipts</Link>
            </li>
            <li>
              <Link to="/product-items">Product Items</Link>
            </li>
            <li>
              <Link to="/stores">Stores</Link>
            </li>
            <li>
              <Link to="/login">Login</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
