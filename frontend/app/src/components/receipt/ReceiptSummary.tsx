import { CalendarIcon } from "@chakra-ui/icons";
import {  Icon, SimpleGrid, Text } from "@chakra-ui/react";
import React from "react";
import { BiCategoryAlt } from "react-icons/bi";
import { BsShop } from "react-icons/bs";
import { RiMoneyDollarBoxLine } from "react-icons/ri";

export default function ReceiptSummary() {
  return (
    <SimpleGrid columns={2} spacing={10}>
      <Text as="b">
        <Icon as={BsShop} mr="12px" />
        Shop:
      </Text>
      <Text>Lidl</Text>
      <Text as="b">
        <Icon as={BiCategoryAlt} mr="12px" />
        Category:
      </Text>
      <Text>Boodschappen</Text>
      <Text as="b">
        <Icon as={CalendarIcon} mr="12px" />
        Purchase date:
      </Text>
      <Text>06-05-1991</Text>
      <Text as="b">
        <Icon as={RiMoneyDollarBoxLine} mr="12px" />
        Total amount:
      </Text>
      <Text>€ 69,69</Text>
    </SimpleGrid>
  );
}
