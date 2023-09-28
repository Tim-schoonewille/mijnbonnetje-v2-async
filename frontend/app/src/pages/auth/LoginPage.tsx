import { Center, Flex, Heading, Link, Text } from "@chakra-ui/react";
import React from "react";
import LoginForm from "../../components/auth/LoginForm";
import { Link as NavLink } from "react-router-dom";

export default function LoginPage() {
  return (
    <>
      <Flex
        justifyContent="center"
        alignItems="center"
        flexDirection="column"
        gap={15}
      >
        <Heading size="xl">Login</Heading>
        <LoginForm />
        <Text>
          <Link as='span'>
            <NavLink to="/auth/request-new-password">
              Request new password
            </NavLink>
          </Link>
        </Text>
        <Text>
          <Link as='span'>
            <NavLink to="/auth/request-new-email-verification">
              Request new email verification link
            </NavLink>
          </Link>
        </Text>
      </Flex>
    </>
  );
}
