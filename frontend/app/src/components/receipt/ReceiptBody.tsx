import { Flex } from "@chakra-ui/react";
import React from "react";

type ReceiptBodyProps = {
  children: React.ReactNode;
};

export default function ReceiptBody({ children }: ReceiptBodyProps) {
  return (
    <Flex
      minW={["100%", "100%", "600px", "600px"]}
      p={5}
      flexDirection="column"
      gap="64px"
      boxShadow="base"
      rounded="base"
    >
      {children}
    </Flex>
  );
}
