import {
  Button,
  Flex,
  FormControl,
  FormErrorMessage,
  FormHelperText,
  FormLabel,
  Input,
  Text,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { AuthService } from "../../client";

export default function RequestNewPasswordPage() {
  const [email, setEmail] = useState<string>();
  const [emailError, setEmailError] = useState(false);
  const [emailErrorMessage, setEmailErrorMessage] = useState("");
  const [success, setSuccess] = useState("");
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      setEmailError(true);
      setEmailErrorMessage("Requires a valid email address to proceed");
      return;
    }

    try {
      setEmailErrorMessage("");
      setEmailError(false);

      const response = await AuthService.authRequestNewPasswordToken({ email });

      if (response.status === 200) {
        setSuccess("Check inbox for link to generate new password");
      } else {
        setEmailError(true);
        setSuccess("");
        setEmailErrorMessage("Invalid email address, try again loser");
      }
    } catch (e) {
      console.error(e);
    }
  };
  return (
    <Flex
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
      gap={15}
    >
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
        <Button colorScheme="teal" type="submit">
          Request New Password
        </Button>
        {success && <Text color="green.400">{success}</Text>}
      </Flex>
    </Flex>
  );
}
