import React from "react";
import { Center, Container, Heading } from "@chakra-ui/react";
import RegisterForm from "../components/RegisterForm";

export default function RegisterPage() {
  return (
      <Container maxW="md">
        <Center>
        <Heading mt={10} mb={10} size="2xl">Register</Heading>
      </Center>
      <RegisterForm />
    </Container>
  );
}
