import {
  Button,
  Center,
  Flex,
  FormControl,
  FormErrorMessage,
  FormHelperText,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
  Spinner,
  Text,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { AuthService } from "../../client";
import { useAuthContext } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [emailError, setEmailError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const { setIsLoggedIn } = useAuthContext();
  const navigate = useNavigate()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErrorMessage("");
    setSuccessMessage("");

    if (!email || !password) {
      setErrorMessage("Please fill in all the forms!");
      return;
    }

    try {
      setIsLoading(true);
      const response = await AuthService.authLoginUser({ email, password });

      if (response.status === 200) {
        setIsLoading(false);
        setIsLoggedIn(true);
        setSuccessMessage("Succesfull login!");
        setErrorMessage("");
        navigate('/receipts')
      } else {
        setSuccessMessage("");
        setErrorMessage("Invalid credentials");
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }
  return (
    <Flex
      as="form"
      minW={["100%", "100%", "600px", "600px"]}
      p={5}
      flexDirection="column"
      gap={10}
      onSubmit={handleSubmit}
      noValidate
    >
      <FormControl isInvalid={emailError}>
        <FormLabel>Email</FormLabel>
        <Input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        {!emailError ? (
          <FormHelperText>Your email address</FormHelperText>
        ) : (
          <FormErrorMessage>Email is required.</FormErrorMessage>
        )}
      </FormControl>

      <FormControl isInvalid={passwordError}>
        <FormLabel>Password</FormLabel>
        <InputGroup>
          <Input
            type={show ? "text" : "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <InputRightElement width="4.5rem">
            <Button h="1.75rem" size="sm" onClick={() => setShow(!show)}>
              {show ? "Hide" : "Show"}
            </Button>
          </InputRightElement>
        </InputGroup>
        {!passwordError ? (
          <FormHelperText>
            mijnbonnetje.nl will never ask for your passwod
          </FormHelperText>
        ) : (
          <FormErrorMessage>Email is required.</FormErrorMessage>
        )}
      </FormControl>
      <Button type="submit">Login</Button>
      <Center>
        {isLoading && <Spinner />}
        {successMessage && <Text color={"green.400"}>{successMessage}</Text>}
        {errorMessage && <Text color={"red.400"}>{errorMessage}</Text>}
      </Center>
    </Flex>
  );
}
