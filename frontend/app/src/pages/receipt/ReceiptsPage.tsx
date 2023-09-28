import { Accordion, Box, Flex, Spinner } from "@chakra-ui/react";

import ReceiptFilterMenu from "../../components/receipt/ReceiptFilterMenu";
import ReceiptOrderByMenu from "../../components/receipt/ReceiptOrderByMenu";
import { useEffect, useRef, useState } from "react";

export default function ReceiptsPage() {
  const [isLoading, setIsLoading] = useState(true);

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
        {isLoading ? (
          <Spinner />
        ) : (
          <>
            <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            R Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            eceipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
            Receipt <br />
          </>
        )}
      </Flex>
    </>
  );
}
