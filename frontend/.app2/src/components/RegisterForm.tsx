import React, { useState } from "react";
import {
  Box,
  FormControl,
  FormLabel,
  Input,
  Button,
  Heading,
  Center,
} from "@chakra-ui/react";
import { AuthService } from "../client";

const RegisterForm: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordRetype, setPasswordRetype] = useState("");
  const [error, setError] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== passwordRetype) {
      setError("Passwords have to match!");
      return;
    }
    try {
      const response = await AuthService.authRegisterNewUser({
        email,
        password,
      });
      if (response.status === 201) {
        setError('')
        setSuccessMsg('Succesfully registerd, you can now login!')
      }
      if (response.status === 400) {
        setSuccessMsg('')
        setError('Email already registered!')
      }
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <Box maxW="md" mt={4} p={4} borderWidth={1} borderRadius="lg">
      <form onSubmit={handleSubmit}>
        <FormControl isRequired>
          <FormLabel>Email</FormLabel>
          <Input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </FormControl>
        <FormControl mt={4} isRequired>
          <FormLabel>Password</FormLabel>
          <Input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </FormControl>
        <FormControl mt={4} isRequired>
          <FormLabel>Retype Password</FormLabel>
          <Input
            type="password"
            placeholder="Retype your password"
            value={passwordRetype}
            onChange={(e) => setPasswordRetype(e.target.value)}
          />
        </FormControl>
        <Button type="submit" colorScheme="teal" mt={4}>
          Register
        </Button>
        {error && (
          <>
            <Center>
              <Heading mt={5} color="red.400" size="l">
                {error}
              </Heading>
            </Center>
          </>
        )}
        {successMsg && (
          <>
            <Center>
              <Heading mt={5} color="green.400" size="l">
                {successMsg}
              </Heading>
            </Center>
          </>
        )}
      </form>
    </Box>
  );
};

export default RegisterForm;
