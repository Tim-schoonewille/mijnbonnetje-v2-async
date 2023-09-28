import { CalendarIcon } from "@chakra-ui/icons";
import { Flex, Icon, Spacer, Text } from "@chakra-ui/react";
import React from "react";
import { BiCategoryAlt } from "react-icons/bi";
import { BsShop } from "react-icons/bs";
import { ReceiptEntry, Store } from "../../client";

type TruncatedReceiptProps = {
  receipt: ReceiptEntry;
  store: Store | undefined;
};

export default function TruncatedReceipt({ receipt, store }: TruncatedReceiptProps) {
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
          {store?.name}
        </Text>
        <Spacer />
        <Text>€ {receipt.totalAmount ? receipt.totalAmount / 100 : '?'}</Text>
      </Flex>
      <Flex alignItems={"center"}>
        <Icon as={BiCategoryAlt} mr="12px" />
        <Text>{receipt.category}</Text>
      </Flex>
      <Flex alignItems={"center"}>
        <Icon as={CalendarIcon} mr="12px" />
        <Text>{receipt.purchaseDate}</Text>
      </Flex>
    </Flex>
  );
}
