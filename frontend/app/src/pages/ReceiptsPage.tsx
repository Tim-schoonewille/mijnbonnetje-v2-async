import { Center, Flex, Heading, Img, Text } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { AuthService, Receipt, ReceiptService } from "../client";
import RequiresValidToken from "../wrappers/RequiresValidToken";

export default function ReceiptsPage() {
  const [receipts, setReceipts] = useState<Receipt[]>([]);

  useEffect(() => {
    async function getReceipts() {
      try {
        const response = await ReceiptService.receiptReadMultipleReceipts();
        const receiptsFromApi = response.body;
        setReceipts(receiptsFromApi);
      } catch (e) {
        console.error(e);
      }
    }
    getReceipts();
  }, []);

  return (
    <RequiresValidToken>
      <Center>
        <Heading mt={5}>Your receipts</Heading>
      </Center>
      <Flex flexDir={"column"} m="0 auto" maxW={300}>
        {receipts.map((receipt) => {
          return (
            <>
              <Text> {receipt.purchaseDate}</Text>
              {receipt.receiptFiles.map((file) => {
                return <Img src={`http://backend.mijnbonnetje.lan:8000${file.filePath.slice(1)}`} />;
              })}
            </>
          );
        })}
      </Flex>
    </RequiresValidToken>
  );
}
