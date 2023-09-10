import React, { FormEvent, useState } from "react";

const ENDPOINT = "http://backend.mijnbonnetje.lan:8000/";

export default function Login({ onLogin }: { onLogin: (value: any) => void }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    console.log("Loggin in");
    e.preventDefault();
    const data = { email, password };
    console.log(data);
    try {
      const response = await fetch(ENDPOINT + `auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
        credentials: "include",
      });
      const responeData = await response.json();

      if (response.ok) {
        console.log("Logged in");
        console.log(response)
        console.log(responeData);
        onLogin(true)
      } else {
        console.error("login failed");
      }
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div>
          <button>Login</button>
        </div>
      </form>
    </div>
  );
}
