import {
  Button,
  Flex,
  FormControl,
  FormErrorMessage,
  FormHelperText,
  FormLabel,
  Input,
} from "@chakra-ui/react";
import React, { useState } from "react";

export default function RequestNewEmailVerificationPage() {
  const [email, setEmail] = useState<string>();
  const [emailError, setEmailError] = useState(false);
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
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
            <FormErrorMessage>Email is required.</FormErrorMessage>
          )}
        </FormControl>
        <Button type="submit">Request New Verification Link</Button>
      </Flex>
    </Flex>
  );
}
