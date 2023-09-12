import { Flex, Heading } from "@chakra-ui/react";
import React from "react";
import RequiresValidToken from "../wrappers/RequiresValidToken";

export default function AddReceiptPage() {
  return (
    <RequiresValidToken>
      <Flex
        alignItems="center"
        justifyContent="center"
        m="0 auto"
        maxW={400}
        height="80vh"
      >
        <Heading>Add a receipt</Heading>
      </Flex>
    </RequiresValidToken>
  );
}
