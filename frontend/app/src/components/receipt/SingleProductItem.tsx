import { Flex, Text } from "@chakra-ui/react";
import React from "react";


export default function SingleProductItem() {
  return (
    <Flex alignItems="center" justifyContent="space-between">
      <Text as="i">1 x</Text>
      <Text as="i">KipdijenfiletKipdijenfilet</Text>
      <Text as="i"> € 3,20 </Text>
    </Flex>
  );
}
