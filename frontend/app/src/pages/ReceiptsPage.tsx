import { Center, Heading, SimpleGrid, Text } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { Receipt, ReceiptService } from "../client";
import RequiresValidToken from "../wrappers/RequiresValidToken";
import { DeleteIcon } from "@chakra-ui/icons";
export default function ReceiptsPage() {
  const [receipts, setReceipts] = useState<Receipt[]>([]);
  const [changeDelete, setChangeDelete] = useState(false);

  const handleDeleteReceipt = async (id: number | string) => {
    console.log(`Deleting item: ${id}`);
    try {
      const response = await ReceiptService.receiptDeleteSpecificFullReceipt(
        id
      );

      if (response.status === 200) setChangeDelete((prev) => !prev);
    } catch (e) {
      console.error(e);
    }
  };
  useEffect(() => {
    async function getReceipts() {
      try {
        const response = await ReceiptService.receiptReadMultipleReceipts();
        const receiptsFromApi = response.body;
        setReceipts(receiptsFromApi.reverse());
      } catch (e) {
        console.error(e);
      }
    }
    getReceipts();
  }, [changeDelete]);

  return (
    <RequiresValidToken>
      <Center>
        <Heading mt={5}>Your receipts</Heading>
      </Center>
      <SimpleGrid columns={[1, 2, 4, 4]} spacing={10} m={"0 auto"} p={6}>
        {receipts.map((receipt, receiptIndex) => {
          return (
            <Text key={receiptIndex}>
              Created: {receipt.createdAt} <br />
              Receipt ID: {receipt.id} <br /> Store: {receipt.store?.name}{" "}
              <br />
              <DeleteIcon
                onClick={() => {
                  handleDeleteReceipt(receipt.id);
                }}
              />
            </Text>
          );
        })}
      </SimpleGrid>
    </RequiresValidToken>
  );
}
