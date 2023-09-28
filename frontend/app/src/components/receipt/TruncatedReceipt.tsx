import { CalendarIcon } from "@chakra-ui/icons";
import { Flex, Icon, Spacer, Text } from "@chakra-ui/react";
import React from "react";
import { BiCategoryAlt } from "react-icons/bi";
import { BsShop } from "react-icons/bs";

export default function TruncatedReceipt() {
  return (
    <Flex
      justifyContent={"center"}
      flexDirection={"column"}
      minWidth="380px"
      p="12px"
      boxShadow="base"
      rounded="lg"
      gap={2}
      style={{ transition: "transform 0.3s ease" }}
      _hover={{
        transform: "translateY(-5px)",
      }}
    >
      <Flex alignItems={"center"}>
        <Icon as={BsShop} mr="12px" />
        <Text size={"lg"} as="b">
          LIDL
        </Text>
        <Spacer />
        <Text>€ 69.12</Text>
      </Flex>
      <Flex alignItems={"center"}>
        <Icon as={BiCategoryAlt} mr="12px" />
        <Text>Boodschappen</Text>
      </Flex>
      <Flex alignItems={"center"}>
        <Icon as={CalendarIcon} mr="12px" />
        <Text>9-9-2023</Text>
      </Flex>
    </Flex>
  );
}
