import { Accordion, Box, Flex, Spinner } from "@chakra-ui/react";

import ReceiptFilterMenu from "../../components/receipt/ReceiptFilterMenu";
import ReceiptOrderByMenu from "../../components/receipt/ReceiptOrderByMenu";
import { useEffect, useRef, useState } from "react";
import Receipts from "../../components/receipt/Receipts";
import { ReceiptEntry } from "../../client";

export default function ReceiptsPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [receipts, setReceipts] = useState<ReceiptEntry[] | null>(null);
  return (
    <>
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
        <Receipts receipts={receipts} />
        {isLoading && <Spinner />}
      </Flex>
    </>
  );
}
