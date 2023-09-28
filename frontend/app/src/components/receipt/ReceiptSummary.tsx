import { CalendarIcon } from "@chakra-ui/icons";
import { Icon, SimpleGrid, Text } from "@chakra-ui/react";
import React from "react";
import { BiCategoryAlt } from "react-icons/bi";
import { BsShop } from "react-icons/bs";
import { RiMoneyDollarBoxLine } from "react-icons/ri";
import { Receipt } from "../../client";

type ReceiptSummaryProps = {
  receipt: Receipt | undefined;
};

export default function ReceiptSummary({ receipt }: ReceiptSummaryProps) {
  if (receipt === null || receipt === undefined)
    return <Text>Error fetching file</Text>;
  return (
    <>
      <SimpleGrid columns={2} spacing={10}>
        <Text as="b">
          <Icon as={BsShop} mr="12px" />
          Shop:
        </Text>
        <Text>{receipt.store?.name}</Text>
        <Text as="b">
          <Icon as={BiCategoryAlt} mr="12px" />
          Category:
        </Text>
        <Text>{receipt.category}</Text>
        <Text as="b">
          <Icon as={CalendarIcon} mr="12px" />
          Purchase date:
        </Text>
        <Text>{receipt.purchaseDate}</Text>
        <Text as="b">
          <Icon as={RiMoneyDollarBoxLine} mr="12px" />
          Total amount:
        </Text>
        <Text>€ { receipt.totalAmount ? receipt.totalAmount / 100 : ''}</Text>
      </SimpleGrid>
    </>
  );
}
