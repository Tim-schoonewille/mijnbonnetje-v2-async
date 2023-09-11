import React, { useState } from "react";
import { Box, FormControl, FormLabel, Input, Button } from "@chakra-ui/react";
import { AuthService } from "../client";
import { useAuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const LoginForm: React.FC = () => {
  const { isLoggedIn, setIsLoggedIn } = useAuthContext();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await AuthService.authLoginUser({ email, password });
      if (response.status === 200) {
        setIsLoggedIn(true)
        navigate('/')
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
        <Button type="submit" colorScheme="teal" mt={4}>
          Login
        </Button>
      </form>
    </Box>
  );
};

export default LoginForm;
