import { Center, Flex, Heading } from "@chakra-ui/react";
import RegisterForm from "../../components/auth/RegisterForm";

export default function RegisterPage() {
  return (
    <>
      <Flex
        justifyContent="center"
        alignItems="center"
        flexDirection="column"
        gap={15}
      >
        <Heading size="xl">Register</Heading>
        <RegisterForm />
      </Flex>
    </>
  );
}
