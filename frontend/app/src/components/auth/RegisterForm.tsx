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

export default function RegisterForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [show, setShow] = useState(false);
  const [emailError, setEmailError] = useState(false);
  const [emailErrorMessage, setEmailErrorMessage] = useState("");
  const [passwordError, setPasswordError] = useState(false);
  const [passwordErrorMessage, setPasswordErrorMessage] = useState("");
  const [success, setSuccess] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;

    if (!emailRegex.test(email) || !email) {
      setEmailError(true);
      setEmailErrorMessage("Invalid email!");
      return;
    }
    if (!password || !password2) {
      setPasswordError(true);
      setPasswordErrorMessage("Password required!");
      return;
    }
    if (password !== password2) {
      setPasswordError(true);
      setPasswordErrorMessage("Passwords must match!");
      return;
    }

    try {
      setIsLoading(true);
      const response = await AuthService.authRegisterNewUser({
        email,
        password,
      });
      if (response.status === 201) {
        setSuccess(
          "Succesfull registration, please verify your email address by clicking the link in your inbox"
        );
      }
      if (response.status === 400) {
        setEmailError(true)
        setEmailErrorMessage("E-mail already registerd!");
      }
    } catch (e) {
      console.error(e)

    } finally {
      setIsLoading(false)
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
          <FormErrorMessage>{emailErrorMessage}</FormErrorMessage>
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
          <FormErrorMessage>{passwordErrorMessage} </FormErrorMessage>
        )}
      </FormControl>
      <FormControl isInvalid={passwordError}>
        <FormLabel>Password</FormLabel>
        <InputGroup>
          <Input
            type={show ? "text" : "password"}
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
          />
          <InputRightElement width="4.5rem">
            <Button h="1.75rem" size="sm" onClick={() => setShow(!show)}>
              {show ? "Hide" : "Show"}
            </Button>
          </InputRightElement>
        </InputGroup>
        {!passwordError ? (
          <FormHelperText>Retype your password to verify</FormHelperText>
        ) : (
          <FormErrorMessage>{passwordErrorMessage}</FormErrorMessage>
        )}
      </FormControl>
      <Button type="submit">Register</Button>
      <Center>
        {isLoading && <Spinner />}

        {success && <Text>{success}</Text>}
      </Center>
    </Flex>
  );
}
