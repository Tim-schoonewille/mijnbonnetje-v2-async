import { Accordion, Box, Flex, Spinner } from "@chakra-ui/react";

import ReceiptFilterMenu from "../../components/receipt/ReceiptFilterMenu";
import ReceiptOrderByMenu from "../../components/receipt/ReceiptOrderByMenu";
import { useEffect, useRef, useState } from "react";
import Receipts from "../../components/receipt/Receipts";
import { ReceiptEntry, ReceiptEntryService, Store, StoreService } from "../../client";
import RequiresValidToken from "../../wrappers/RequiresValidToken";

export default function ReceiptsPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [receipts, setReceipts] = useState<ReceiptEntry[] | null>(null);
  const [stores, setStores] = useState<Store[] | null>(null)

  async function readReceipts() {
    const response = await ReceiptEntryService.receiptEntryReadMultipleReceiptEntries()
    setReceipts(response.body)
  }
  async function readStores() {
    try {
      setIsLoading(true)
      const response = await StoreService.storeReadUserStores()
      if (response.status === 200) {
        setStores(response.body)
      }
    } catch (e) {
      console.error(e)
    } finally {
      setIsLoading(false)
    }
  }
  useEffect(() => {
    readReceipts()
    readStores()
  }, [])

  console.log(stores)
  return (
    <RequiresValidToken>
      <Accordion allowToggle>
        <ReceiptFilterMenu />
        <ReceiptOrderByMenu />
      </Accordion>

      <Flex
        justifyContent="center"
        alignItems="center"
        flexDirection="column"
        gap={15}
        mt="24px"
      >
        <Receipts receipts={receipts} stores={stores}/>
        {isLoading && <Spinner />}
      </Flex>
    </RequiresValidToken>
  );
}
