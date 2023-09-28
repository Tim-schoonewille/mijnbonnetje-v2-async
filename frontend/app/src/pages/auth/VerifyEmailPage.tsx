import { Flex, Text } from "@chakra-ui/react";
import React from "react";
import { useSearchParams } from "react-router-dom";

export default function VerifyEmailPage() {
  const [queryParams] = useSearchParams();
  const emailVerificationToken = queryParams.get("token") ?? "invalidtoken";
  return (
    <Flex
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
      gap={15}
    >
      <Text> {emailVerificationToken}</Text>
    </Flex>
  );
}
