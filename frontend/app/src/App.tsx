import { useEffect, useState } from "react";
import "./App.css";
import Login from "./components/Login";
import axios from "axios";
import Logout from "./components/Logout";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [tokenVerified, setTokenVerified] = useState(false);

useEffect(() => {
  async function verifyToken() {
    try {
      const response = await axios.get(
        'http://backend.mijnbonnetje.lan:8000/auth/verify-token',
        {
          withCredentials: true, // Include cookies
        }
      );

      if (response.status === 200) {
        setTokenVerified(true);
        setIsLoggedIn(true)
        console.log('Token is valid');
        console.log(response.data);
      } else {
        console.error('Token not verified');
        console.log(response.data);
        setTokenVerified(false);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  verifyToken();
}, [isLoggedIn]);

  return (
    <div className="App">
      <header className="App-header">
        <p>Token verified: {tokenVerified.toString()}</p>
        {isLoggedIn ? <Logout onLogout={setIsLoggedIn} /> : <Login onLogin={setIsLoggedIn} />}
      </header>
    </div>
  );
}

export default App;
