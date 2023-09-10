import React, { FormEvent, useState } from "react";
import { AuthService } from "../client";
import { UserLogin } from '../client/models/UserLogin';

const ENDPOINT = "http://backend.mijnbonnetje.lan:8000";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    console.log("Loggin in");
    e.preventDefault();
    const userLoginData: UserLogin = {email, password}
    try {

      await AuthService.authLoginUser(userLoginData)


    } catch(error) {
      // console.error(error)
      console.log(error)
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
