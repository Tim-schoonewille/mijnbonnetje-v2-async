import {
  Flex,
  Heading,
  Text,
  Box,
  FormControl,
  FormLabel,
  Input,
  FormHelperText,
  Button,
  useStatStyles,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { AuthService } from "../client";
import RequiresValidToken from "../wrappers/RequiresValidToken";

export default function NewEmailVerificationPage() {
  const [email, setEmail] = useState("");
  const [message, setMesssage] = useState("");
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await AuthService.authRequestEmailVerificationCode();

      if (response.status === 200) {
        setMesssage("New email sent.");
      }
    } catch (e) {
      console.error(e);
    }
  };
  return (
    <Box maxWidth={400} m="20px auto">
      <Flex
        direction={"column"}
        mt={7}
        maxW="600px"
        rounded={"md"}
        boxShadow={"md"}
        justifyContent={"center"}
        alignItems={"center"}
        p="6"
      >
        <Text mb="10">New Email Verification</Text>
        <form onSubmit={handleSubmit}>
          <FormControl mb="6">
            <FormLabel>Email address</FormLabel>
            <Input
              variant="flushed"
              placeholder="user@testaco.com"
              type="email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <FormHelperText>We'll never share your email.</FormHelperText>
          </FormControl>
          <Button type="submit">Request New</Button>
        </form>
        {message && <Text color={"green.400"}>{message}</Text>}
      </Flex>
    </Box>
  );
}
