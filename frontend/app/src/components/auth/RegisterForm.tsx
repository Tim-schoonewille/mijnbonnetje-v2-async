import {
  Button,
  Flex,
  FormControl,
  FormErrorMessage,
  FormHelperText,
  FormLabel,
  Input,
  InputGroup,
  InputRightElement,
} from "@chakra-ui/react";
import React, { useState } from "react";

export default function RegisterForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [show, setShow] = useState(false);
  const [emailError, setEmailError] = useState(false);
  const [passwordError, setPasswordError] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    alert(email);
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
          <FormErrorMessage>Email is required.</FormErrorMessage>
        )}
      </FormControl>
      <Button type="submit">Register</Button>
    </Flex>
  );
}
