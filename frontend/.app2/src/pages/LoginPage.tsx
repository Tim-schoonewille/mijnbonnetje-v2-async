import React from "react";
import LoginForm from "../components/LoginForm";
import { Center, Container, Heading } from "@chakra-ui/react";


export default function LoginPage() {

  return (
      <Container maxW="md">
        <Center>
        <Heading mt={10} mb={10} size="2xl">Login</Heading>
      </Center>
      <LoginForm />
    </Container>
  );
}
