import {
  Button,
  Flex,
  FormControl,
  FormErrorMessage,
  FormHelperText,
  FormLabel,
  Input,
  Spinner,
  Text,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { AuthService } from "../../client";

export default function RequestNewEmailVerificationPage() {
  const [email, setEmail] = useState<string>();
  const [emailError, setEmailError] = useState(false);
  const [emailErrorMessage, setEmailErrorMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  async function handleNewEmailTokenRequest(emailAddress: string) {
    if (!emailAddress) return;
    try {
      setIsLoading(true);
      const response = await AuthService.authRequestEmailVerificationCode({
        email: emailAddress,
      });
      if (response.status === 200) {
        setEmailErrorMessage('')
        setEmailError(false)
        setSuccessMessage("Token has been sent to your inbox");
      } else {
        setEmailError(true)
        setSuccessMessage('')
        setEmailErrorMessage("Something went horribly wrong");
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  }
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return
    handleNewEmailTokenRequest(email)
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
        <Button type="submit">Request New Verification Link</Button>
        {isLoading && <Spinner />}
        {successMessage && <Text color="green.400">{successMessage}</Text>}
      </Flex>
    </Flex>
  );
}
