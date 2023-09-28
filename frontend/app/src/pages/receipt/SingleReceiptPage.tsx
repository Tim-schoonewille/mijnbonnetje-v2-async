import { Flex } from "@chakra-ui/react";
import React from "react";
import { useParams } from "react-router-dom";
import ReceiptBody from "../../components/receipt/ReceiptBody";

export default function SingleReceiptPage() {
  const { id } = useParams();
  const receiptID = id || 0;
  return (
    <Flex
      justifyContent="center"
      alignItems="center"
      flexDirection="column"
      gap={15}
      mt="24px"
    >
      <ReceiptBody>{receiptID}</ReceiptBody>
    </Flex>
  );
}
