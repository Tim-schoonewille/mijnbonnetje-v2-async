import {
  Button,
  Flex,
  FormControl,
  FormErrorMessage,
  FormHelperText,
  FormLabel,
  Heading,
  Input,
  InputGroup,
  InputRightElement,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { useSearchParams } from "react-router-dom";

export default function VerifyNewPasswordPage() {
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [show, setShow] = useState(false);
  const [passwordError, setPasswordError] = useState(false);
  const [queryParams] = useSearchParams();
  const newPasswordVerificationToken =
    queryParams.get("token") ?? "invalid token";

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
  }
  return (
    <Flex
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
      gap={15}
    >
      <Heading size="xl">
        Verify new password: {newPasswordVerificationToken}
      </Heading>
      <Flex
        as="form"
        minW={["100%", "100%", "600px", "600px"]}
        p={5}
        flexDirection="column"
        gap={10}
        onSubmit={handleSubmit}
        noValidate
      >
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
        <Button type="submit">Change Password</Button>
      </Flex>
    </Flex>
  );
}
