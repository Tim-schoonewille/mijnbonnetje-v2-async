import React, { FormEvent, useState } from "react";
import { AuthService, User } from "../client";
import { UserLogin } from "../client/models/UserLogin";
import axios from "axios";
import {Button, Container, Input, FormLabel } from "@chakra-ui/react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: FormEvent) => {
    console.log("Loggin in");
    e.preventDefault();
    const userLoginData: UserLogin = { email, password };
    try {
      const response = await AuthService.authLoginUser(userLoginData);
      console.log(response.body);
      if (response.status !== 200) {
        console.error("wassup");
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div>
      <h1>Login</h1>
      <Container maxW="md">
        <form onSubmit={handleSubmit}>
          <div>
            <FormLabel>Email address</FormLabel>
            <Input
              placeholder="E-mail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <FormLabel>Password </FormLabel>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div>
            <Button colorScheme='blue' variant='solid'>Login</Button>
          </div>
          {error && error}
        </form>
      </Container>
    </div>
  );
}
